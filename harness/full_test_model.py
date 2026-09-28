#!/usr/bin/env python3
"""FULL test battery for a model: HumanEval 20 + Tasks 5 + Agency 15 + throughput + tool-call.

Usage: python3 full_test_model.py <model_id> <label>
Saves complete scorecard to benchmarks/results/<label>.json (OUT_DIR override).

Reports an `answered` breakdown alongside every score: a low score with LOW
coverage (model never answered) is a different defect from a low score with FULL
coverage (genuine capability gap). Never read one without the other.
"""
import json, gzip, time, urllib.request, urllib.error, subprocess, tempfile, os, re, sys

MODEL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MODEL", "qwen/qwen3.8-27b")
LABEL = sys.argv[2] if len(sys.argv) > 2 else MODEL
API = os.environ.get("LM_API", "http://127.0.0.1:1234/v1/chat/completions")
API_KEY = os.environ.get("LM_API_KEY", "")
LMS_BIN = os.environ.get("LMS_BIN", "lms")
LOAD_KEY = os.environ.get("LOAD_KEY", "qwen3.8-27b-ud")
HE_PATH = os.environ.get("HE_PATH", "HumanEval.jsonl.gz")
TASK_DIR = os.environ.get("TASK_DIR", "prompts/")
OUT_DIR = os.environ.get("OUT_DIR", "results")

def chat(messages, max_tokens=4000, temp=None, tools=None):
    # Global temp override for callers that do not pass one explicitly (HumanEval,
    # throughput, tool-call). Env: TEMP. Default 0.2 preserves prior behaviour;
    # the DavidAU tester set wants TEMP=1.
    if temp is None:
        temp = float(os.environ.get("TEMP", "0.2"))
    # Turbo-Brilliance mode tag (DavidAU models): prepend {REASON:<mode>} to the
    # last user message. The card states the DEFAULTS are 'high' for reasoning
    # and 'medium' for instruct — so omitting this silently runs 'high' on every
    # task. Env: REASON_MODE=off|low|medium|medium-low|high|ultra|omni|deeptree|
    # hyper|socrates|logic|einstein|spoon, or i-prefixed instruct variants.
    mode = os.environ.get("REASON_MODE", "")
    if mode:
        tag = "{REASON:%s}" % mode
        msgs = [dict(m) for m in messages]
        for m in reversed(msgs):
            if m.get("role") == "user":
                if not m["content"].lstrip().startswith("{REASON:"):
                    m["content"] = tag + "\n" + m["content"]
                break
        messages = msgs
    payload = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": temp}
    # Sampler overrides. The card recommends temp 1 + top_k 64 + min_p 0.05 +
    # top_p 0.95 (tester settings); its LFM suggested set is temp 0.1 + top_k 50
    # + rep_pen 1.1. Passing neither is a THIRD, untested configuration.
    # Env: TOP_K / MIN_P / TOP_P / REP_PEN
    for env_key, field in (("TOP_K", "top_k"), ("MIN_P", "min_p"), ("TOP_P", "top_p")):
        v = os.environ.get(env_key, "")
        if v:
            payload[field] = float(v)
    # Sampling overrides for repetition-prone models (e.g. gemma-4-26B loops at
    # greedy temp; card requires temp 0.3-0.7 + rep-pen). Env:
    # TASK_TEMP / TASK_REP_PEN (used by run_tasks), AGENCY_TEMP (used by agency).
    rp = os.environ.get("TASK_REP_PEN", "") or os.environ.get("REP_PEN", "")
    if rp:
        payload["repetition_penalty"] = float(rp)
    # Optional reasoning-effort override (Qwen/Dirk chat_template_kwargs) — used by
    # the low/medium/high-thinking runs. Env: REASONING_EFFORT=low|medium|xhigh
    effort = os.environ.get("REASONING_EFFORT", "")
    if effort:
        payload["chat_template_kwargs"] = {"reasoning_effort": effort}
    # Thinking toggle for llama.cpp/Unsloth-style servers (enable_thinking:false).
    # Env: THINKING_ENABLED=0|false → explicit enable_thinking:false.
    te = os.environ.get("THINKING_ENABLED", "")
    if te in ("0", "false", "False"):
        payload.setdefault("chat_template_kwargs", {})["enable_thinking"] = False
    elif te in ("1", "true", "True"):
        payload.setdefault("chat_template_kwargs", {})["enable_thinking"] = True
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    last_exc = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(API, data=json.dumps(payload).encode(), headers=headers)
            t0 = time.time()
            resp = urllib.request.urlopen(req, timeout=int(os.environ.get("REQUEST_TIMEOUT", "1800")))
            data = json.loads(resp.read())
            elapsed = time.time() - t0
            msg = data["choices"][0]["message"]
            usage = data.get("usage", {})
            # Surface finish_reason so callers can distinguish a truncated /
            # no-answer response from a genuine one. See classify_answer().
            msg["_finish_reason"] = data["choices"][0].get("finish_reason") or ""
            return msg, elapsed, usage
        except urllib.error.HTTPError as e:
            last_exc = e
            code = getattr(e, "code", 0)
            if code in (400, 429, 500, 502, 503, 504):
                print(f"  [retry {attempt+1}/4] HTTP {code} — {str(e)[:80]}", flush=True)
                time.sleep(5 * (attempt + 1))
                if code == 400 and attempt >= 1:
                    try:
                        subprocess.run([LMS_BIN, "load", LOAD_KEY, "--yes"],
                                       timeout=240, capture_output=True)
                    except Exception as ex:
                        print(f"  [reload failed: {ex}]", flush=True)
                continue
            raise
        except Exception as e:
            last_exc = e
            if attempt < 3:
                print(f"  [retry {attempt+1}/4] {type(e).__name__}: {str(e)[:80]}", flush=True)
                time.sleep(5 * (attempt + 1))
                continue
            raise
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("chat: exhausted retries without exception")

def classify_answer(msg, usage=None):
    """Did the model actually ANSWER, or just emit reasoning / nothing?

    Correctness alone cannot tell a WRONG answer from NO answer. That ambiguity
    hid a real defect: a model that answers only 62% of items (DavidAU
    Qwen3.8-27B, HumanEval 101/164, 62% attempted) scored the same shape as one
    that answers everything and gets some wrong.

    Our own known failure mode is exactly this — Qwen3.8 thinking overflows on
    long agentic tasks and returns an EMPTY content field with the work stranded
    in reasoning_content. run_* used `content or reasoning_content`, which
    silently scored the reasoning trace as if it were the answer.

    Returns one of:
      answered       — real content came back
      reasoning_only — content empty, reasoning present, NOT truncated
                       (model thought and never emitted an answer)
      truncated      — finish_reason == length and content empty
                       (ran out of budget before answering)
      empty          — nothing at all came back
    """
    content = (msg.get("content") or "").strip()
    reasoning = (msg.get("reasoning_content") or "").strip()
    finish = (msg.get("_finish_reason")
              or (usage or {}).get("finish_reason") or "")
    if content:
        return "answered"
    if reasoning:
        return "truncated" if finish == "length" else "reasoning_only"
    return "truncated" if finish == "length" else "empty"


def answer_tally(items, key="answered"):
    """Count answer classes across a list of per-item detail dicts."""
    tally = {}
    for it in items:
        s = it.get(key, "answered")
        tally[s] = tally.get(s, 0) + 1
    return tally

# ---------- HumanEval ----------
def load_humaneval(n=None):
    if n is None:
        n = int(os.environ.get("HE_N", "20"))
    items = []
    with gzip.open(HE_PATH, "rt") as f:
        for line in f:
            items.append(json.loads(line))
    ids = os.environ.get("HE_IDS", "")
    if ids:
        want = [int(x) for x in ids.split(",") if x.strip()]
        return [items[i] for i in want if 0 <= i < len(items)]
    return items[:n]

def extract_code(response, prompt):
    response = response.strip()
    # Agentic-RL models (LFM2.5, trained INSIDE real agent harnesses) often return
    # code as a PYTHONIC TOOL CALL instead of a markdown block:
    #   <|tool_call_start|>[stateful_python_code_exec(code='...')]<|tool_call_end|>
    # The code inside is correct — only the wrapper differs. Without unwrapping,
    # extract_code scrapes the wrapper text and EVERY item scores FAIL. That is a
    # parsing artifact, not a capability gap (HumanEval 0/20 root cause, Sep 28).
    # NOTE: only `code=`-style calls are unwrapped. edit(path=...) / write() etc.
    # are genuine tool calls, not answers, and must still fail.
    if "<|tool_call_start|>" in response:
        tm = re.search(r"<\|tool_call_start\|>\s*\[\s*([A-Za-z_][\w\.]*)\s*\(", response)
        if tm:
            rest = response[tm.end():]
            cm = re.search(r"\bcode\s*=\s*(['\"])(.*)\1\s*\)\s*\]", rest, re.DOTALL)
            if cm:
                inner = cm.group(2)
                # Some builds escape newlines as literal \n inside the call.
                if "\n" not in inner and "\\n" in inner:
                    inner = (inner.replace("\\n", "\n").replace("\\t", "    ")
                                  .replace("\\'", "'").replace('\\"', '"'))
                response = inner.strip()
    m = re.search(r"```(?:python)?\s*\n(.*?)```", response, re.DOTALL)
    if m:
        code = m.group(1).strip()
    else:
        code = response
    # Robust: cut to first def/class line — handles models (DeepSeek) that
    # prefix imports/comments/explanations before the function definition.
    lines = code.split("\n")
    cut = None
    for i, l in enumerate(lines):
        ls = l.lstrip()
        if ls.startswith("def ") or ls.startswith("class ") or ls.startswith("async def "):
            cut = i
            break
    if cut is not None:
        code = "\n".join(lines[cut:]).strip()
    if code.lstrip().startswith(("def ", "class ", "async def ")):
        return code
    lines = code.split("\n")
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) >= 2:
        f0 = len(non_empty[0]) - len(non_empty[0].lstrip())
        f1 = len(non_empty[1]) - len(non_empty[1].lstrip())
        if f0 < f1:
            pad = " " * (f1 - f0)
            for i in range(len(lines)):
                if lines[i].strip():
                    lines[i] = pad + lines[i]
                    break
            return prompt + "\n" + "\n".join(lines)
    body = "\n".join(("    " + l) if l.strip() else "" for l in lines)
    return prompt + "\n" + body

def run_tests(code, test, entry_point):
    header = ("from typing import List, Optional, Dict, Tuple, Set, Union, Any, Callable, Iterable, Iterator, Sequence, Mapping, TypeVar\n"
              "import math\nimport random\nimport collections\nimport heapq\nimport itertools\nimport re\nimport string\nimport statistics\nimport functools\nimport hashlib\n")
    script = f"{header}\n{code}\n\n{test}\n\ncheck({entry_point})\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script); tmp = f.name
    try:
        r = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=15,
                           env={"PATH": "/usr/bin:/usr/local/bin", "HOME": os.environ.get("HOME", "/tmp")})
        return r.returncode == 0, (r.stderr or "")[:200]
    except subprocess.TimeoutExpired:
        return False, "timeout"
    finally:
        try: os.unlink(tmp)
        except OSError: pass

def run_humaneval():
    items = load_humaneval()
    correct = 0
    detail = []
    for i, item in enumerate(items):
        prompt = "Complete the following Python function. Provide only the complete function implementation, no explanations.\n\n" + item["prompt"]
        try:
            msg, elapsed, usage = chat([{"role": "user", "content": prompt}],
                                    max_tokens=int(os.environ.get("HE_MAX_TOKENS", "16000")))
            ans = classify_answer(msg, usage)
            raw_content = (msg.get("content") or "").strip()
            if raw_content:
                content = raw_content
            else:
                # No real answer. Still score the reasoning trace so the pass
                # count stays comparable with earlier runs, but `ans` records
                # that this item was NOT genuinely answered.
                content = (msg.get("reasoning_content") or "").strip()
            code = extract_code(content, item["prompt"])
            passed, err = run_tests(code, item["test"], item["entry_point"])
            correct += 1 if passed else 0
            detail.append({"task": item["task_id"], "pass": passed, "answered": ans,
                           "secs": round(elapsed, 1)})
            flag = "" if ans == "answered" else f"   <<< {ans.upper()}"
            print(f"  {i:2d} {item['task_id']:28s} {'PASS' if passed else 'FAIL'} ({elapsed:.0f}s){flag}", flush=True)
            # Save the raw model response per problem when HE_SAVE=1 (enables
            # post-hoc diagnosis of failures: truncation vs wrong code vs extraction).
            if os.environ.get("HE_SAVE", "0") == "1":
                try:
                    with open(os.path.join(OUT_DIR, f"{LABEL}.he-he{i}.txt"), "w") as hf:
                        hf.write(content[:20000])
                except Exception:
                    pass
            try:
                with open(os.path.join(OUT_DIR, f"{LABEL}.he_progress.jsonl"), "a") as pf:
                    pf.write(json.dumps({"i": i, "task": item["task_id"], "pass": passed, "secs": round(elapsed, 1)}) + "\n")
            except Exception:
                pass
        except Exception as e:
            detail.append({"task": item["task_id"], "pass": False, "err": str(e)[:80]})
            print(f"  {i:2d} {item['task_id']:28s} ERROR {str(e)[:80]}", flush=True)
    return correct, detail

# ---------- Tasks ----------
def run_tasks():
    tasks = ["adherence", "expense-tracker", "fake-desktop", "kanban", "reasoning"]
    names = os.environ.get("TASK_NAMES", "")
    if names:
        wanted = [n.strip() for n in names.split(",") if n.strip()]
        tasks = [t for t in tasks if t in wanted]
    else:
        tasks = tasks[: int(os.environ.get("TASK_N", "5"))]
    results = {}
    for t in tasks:
        try:
            prompt = open(os.path.join(TASK_DIR, t + ".txt")).read()
            mt = int(os.environ.get("TASK_MAX_TOKENS", "32000"))
            tt = float(os.environ.get("TASK_TEMP", "0.2"))
            msg, elapsed, usage = chat([{"role": "user", "content": prompt}], max_tokens=mt, temp=tt)
            ans = classify_answer(msg, usage)
            raw_content = (msg.get("content") or "").strip()
            if raw_content:
                content = raw_content
            else:
                content = (msg.get("reasoning_content") or "").strip()
            try:
                with open(os.path.join(OUT_DIR, f"{LABEL}.task-{t}.txt"), "w") as tf:
                    tf.write(content)
            except Exception:
                pass
            code = "Y"
            if t == "adherence":
                # Adherence task wants EXACTLY 3 bold-label markdown bullets, no code,
                # no prompt echo. Grade on structure compliance, NOT the code heuristic.
                bullets = re.findall(r"\*\*[^*]+\*\*", content)
                # 3 expected; tolerate 3-5. >5 (e.g. prompt echo) = FAIL.
                too_long = len(content) > 20000  # prompt echo / runaway verbosity
                if 3 <= len(bullets) <= 5 and not too_long and not any(m in content for m in ("```", "def ", "class ")):
                    code = "Y"
                else:
                    code = "N"
            elif t == "reasoning":
                # Reasoning tasks are MCQ / puzzle prompts expecting an answer in
                # PROSE or an option number — the code heuristic ("```"/def/class/{)
                # is a build-task check and falsely fails clean prose answers.
                # Grade: >=1 explicit option-number answer + non-trivial length.
                opt_marks = re.findall(r"(?m)^\s*(?:option\s*)?(\d{1,2})[.)]?\s*[A-D]?\s*$", content)                             or re.findall(r"\b(?:answer is|option|correct (?:answer|choice):?)", content, re.I)
                has_num = bool(re.search(r"\b(?:17|46|12|23|10|14)\b|\b\d+ minutes\b|\b\d+ pairs?\b", content))
                # Reject only if the model CONCLUDES indecision; quoting an option
                # (e.g. "There is not enough information..." as choice 4) is fine.
                tail = content[-1500:]
                verified = not re.search(r"(?i)don't know|cannot determine|not enough info(?:rmation)?\b", tail)
                code = "Y" if (len(content) > 200 and (opt_marks or has_num) and verified) else "N"
            else:
                code = "Y" if ("```" in content or "def " in content or "class " in content or "{" in content) else "N"
            results[t] = {"chars": len(content), "secs": round(elapsed, 1), "code": code,
                          "answered": ans}
            print(f"  {t:20s} {len(content):6d} chars, {elapsed:5.0f}s, code={code}"
                  + ("" if ans == "answered" else f"   <<< {ans.upper()}"), flush=True)
        except Exception as e:
            results[t] = {"err": str(e)[:80]}
            print(f"  {t:20s} ERROR {str(e)[:80]}", flush=True)
    return results

# ---------- Agency ----------
AGENCY_SYSTEM = ("You are a helpful office assistant at MiniCorp. The current date is 2026-05-28 "
                 "(Thursday) and the current time is 10:00 UTC. You can use tools for exactly four "
                 "capabilities: employee lookup, meeting-room booking, support tickets, and currency "
                 "conversion. For anything else, do NOT call any tool — just respond politely.")

AGENCY_TOOLS = [
    {"type":"function","function":{"name":"lookup_employee","description":"Find an employee by name, email, or ID","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}},
    {"type":"function","function":{"name":"search_directory","description":"List or filter staff (e.g. by department or active status)","parameters":{"type":"object","properties":{"department":{"type":"string"},"active":{"type":"boolean"}}}}},
    {"type":"function","function":{"name":"book_room","description":"Reserve a meeting room with ISO-8601 UTC times","parameters":{"type":"object","properties":{"room":{"type":"string"},"start":{"type":"string"},"end":{"type":"string"}},"required":["room","start","end"]}}},
    {"type":"function","function":{"name":"check_availability","description":"Check existing room bookings","parameters":{"type":"object","properties":{"room":{"type":"string"},"start":{"type":"string"},"end":{"type":"string"}},"required":["room","start","end"]}}},
    {"type":"function","function":{"name":"create_ticket","description":"Log a support ticket with priority and assignee","parameters":{"type":"object","properties":{"title":{"type":"string"},"priority":{"type":"string"},"assignee":{"type":"string"}},"required":["title","priority"]}}},
    {"type":"function","function":{"name":"get_exchange_rate","description":"Look up an official currency rate","parameters":{"type":"object","properties":{"from":{"type":"string"},"to":{"type":"string"}},"required":["from","to"]}}},
    {"type":"function","function":{"name":"convert_currency","description":"Convert an amount between currencies","parameters":{"type":"object","properties":{"amount":{"type":"number"},"from":{"type":"string"},"to":{"type":"string"}},"required":["amount","from","to"]}}},
    {"type":"function","function":{"name":"wiki_search","description":"Search the company wiki (DECOY — not a supported capability)","parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}}},
]

AGENCY_SCENARIOS = [
    ("dept_lookup", "What department does Alice Chen work in?", {"lookup_employee"}, False),
    ("list_active_eng", "List all active employees in Engineering.", {"search_directory"}, False),
    ("count_eng", "How many people are listed in the Engineering department?", {"search_directory"}, False),
    ("list_support_platform", "List everyone who works in Support or Platform.", {"search_directory"}, False),
    ("book_room_b", "Book Conference Room B tomorrow 14:00-15:00 UTC for a standup.", {"book_room"}, False),
    ("book_room_a", "Book Room A this Friday 09:00-10:00 UTC for sprint planning.", {"book_room"}, False),
    ("check_room_b", "Is Conference Room B available tomorrow from 14:00 to 15:00 UTC?", {"check_availability"}, False),
    ("ticket_manager", "Open a medium ticket 'Budget sign-off' for Bob Martinez's manager.", {"lookup_employee","create_ticket"}, False),
    ("ticket_support_lead", "File a high ticket assigned to whoever leads Support.", {"search_directory","create_ticket"}, False),
    ("ticket_platform", "Assign a medium ticket to someone on the Platform team.", {"search_directory","create_ticket"}, False),
    ("convert_eur_usd", "Convert 500 EUR to USD using the official MiniCorp rate.", {"get_exchange_rate","convert_currency"}, False),
    ("convert_usd_jpy", "How much is 100 USD in JPY? Use official MiniCorp rates.", {"get_exchange_rate","convert_currency"}, False),
    ("restraint_thanks", "Thanks, that helps!", set(), True),
    ("restraint_weather", "What's the weather forecast for London tomorrow?", set(), True),
    ("focus_team", "What team is Alice Chen on?", {"lookup_employee"}, False),
]

def run_agency():
    total = 0
    detail = []
    for name, prompt, expected, must_empty in AGENCY_SCENARIOS:
        ans = "answered"
        try:
            _temp = float(os.environ.get("AGENCY_TEMP", "0.0"))
            msg, dt, _usage = chat([{"role":"system","content":AGENCY_SYSTEM},{"role":"user","content":prompt}],
                              max_tokens=8000, temp=_temp, tools=AGENCY_TOOLS)
            calls_raw = msg.get("tool_calls") or []
            names = [tc["function"]["name"] for tc in calls_raw]
            # In a tool-calling scenario the CALL is itself the answer; only when
            # there is neither a call nor text did the model fail to answer.
            if calls_raw or (msg.get("content") or "").strip():
                ans = "answered"
            else:
                ans = classify_answer(msg, _usage)
        except Exception as e:
            names, dt = [], 0
            ans = "error"
            print(f"  {name:20s} ERROR {str(e)[:60]}", flush=True)
        if must_empty:
            passed = len(names) == 0
        else:
            passed = (expected & set(names)) and ("wiki_search" not in names)
        total += 1 if passed else 0
        detail.append({"name": name, "pass": passed, "calls": names, "answered": ans})
        print(f"  {name:20s} [{'PASS' if passed else 'FAIL'}] {names}", flush=True)
    return total, detail

# ---------- Throughput + tool-call ----------
def run_throughput():
    prompt = ("Write a detailed technical explanation of how multi-token prediction "
              "speculative decoding works, covering draft heads, acceptance rates, and "
              "the verification guarantee. Aim for about 500 words, no code blocks.")
    msg, elapsed, usage = chat([{"role": "user", "content": prompt}], max_tokens=8000, temp=0.3)
    ct = usage.get("completion_tokens", 0)
    pt = usage.get("prompt_tokens", 0)
    tps = ct / elapsed if elapsed > 0 else 0
    print(f"  throughput: {ct} tok in {elapsed:.1f}s = {tps:.1f} tok/s", flush=True)
    return {"completion_tokens": ct, "prompt_tokens": pt, "secs": round(elapsed, 1), "tok_per_sec": round(tps, 1)}

def run_toolcall():
    tools = [{"type": "function", "function": {"name": "add", "description": "Add two integers.",
        "parameters": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]}}}]
    msg, elapsed, _ = chat([{"role": "user", "content": "Use the add tool to compute 37 + 15."}],
                           max_tokens=8000, temp=0.0, tools=tools)
    calls = msg.get("tool_calls") or []
    ok = len(calls) > 0
    args = None
    if ok:
        try: args = json.loads(calls[0]["function"]["arguments"])
        except Exception: args = "unparseable"
    print(f"  tool-call: {'OK' if ok else 'NO TOOL CALL'} {args}", flush=True)
    return {"emitted": ok, "args": args, "secs": round(elapsed, 1)}

# ---------- main ----------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"=== FULL TEST: {LABEL} (model={MODEL}) ===", flush=True)

    print("\n--- HumanEval (20) ---", flush=True)
    he_score, he_detail = run_humaneval()
    print(f"HumanEval: {he_score}/{len(he_detail)}", flush=True)

    print("\n--- Tasks (5) ---", flush=True)
    task_results = run_tasks()

    print("\n--- Agency (15) ---", flush=True)
    agency_score, agency_detail = run_agency()
    print(f"Agency: {agency_score}/15", flush=True)

    print("\n--- Throughput ---", flush=True)
    tp = run_throughput()

    print("\n--- Tool-call ---", flush=True)
    tc = run_toolcall()

    # ---- Answer coverage: separates "got it wrong" from "never answered" ----
    # A low score with LOW coverage is a different defect (budget/thinking
    # overflow) from a low score with FULL coverage (genuine capability gap).
    he_ans = answer_tally(he_detail)
    ag_ans = answer_tally(agency_detail)
    tk_ans = answer_tally(list(task_results.values()))
    answered = {
        "humaneval": he_ans, "agency": ag_ans, "tasks": tk_ans,
        "humaneval_answered_rate": round(he_ans.get("answered", 0) / max(len(he_detail), 1), 4),
        "agency_answered_rate": round(ag_ans.get("answered", 0) / max(len(agency_detail), 1), 4),
        "tasks_answered_rate": round(tk_ans.get("answered", 0) / max(len(task_results), 1), 4),
    }

    result = {"label": LABEL, "model": MODEL,
              "humaneval": he_score, "humaneval_detail": he_detail,
              "tasks": task_results,
              "agency": agency_score, "agency_detail": agency_detail,
              "throughput": tp, "toolcall": tc,
              "answered": answered,
              "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    path = os.path.join(OUT_DIR, LABEL.replace("/", "_") + ".json")
    with open(path, "w") as f:
        json.dump(result, f, indent=2, default=list)
    print(f"\n=== {LABEL} SUMMARY ===", flush=True)
    print(f"HumanEval: {he_score}/{len(he_detail)} | Agency: {agency_score}/15 | Tasks: {task_results}", flush=True)
    print(f"Throughput: {tp.get('tok_per_sec')} tok/s | Tool-call: {tc.get('emitted')}", flush=True)
    print(f"Answered HumanEval: {he_ans.get('answered', 0)}/{len(he_detail)} {he_ans}", flush=True)
    print(f"Answered Agency:    {ag_ans.get('answered', 0)}/{len(agency_detail)} {ag_ans}", flush=True)
    print(f"Answered Tasks:     {tk_ans.get('answered', 0)}/{len(task_results)} {tk_ans}", flush=True)
    _bad = {k: v for k, v in (("humaneval", he_ans), ("agency", ag_ans), ("tasks", tk_ans))
            if v.get("answered", 0) < sum(v.values())}
    if _bad:
        print(f"WARNING INCOMPLETE COVERAGE: {_bad} — the score above may UNDERSTATE "
              f"this model (no-answer, not wrong-answer).", flush=True)
    print(f"Saved -> {path}", flush=True)

if __name__ == "__main__":
    main()
