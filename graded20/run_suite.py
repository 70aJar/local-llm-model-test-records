#!/usr/bin/env python3
"""Run GRADED-20 against any OpenAI-compatible endpoint.

Design choices that keep the score honest:
  * one attempt per question, temperature 0 by default — no retries, no self-repair loop;
  * the model gets ONLY the prompt; tests are never shown to it;
  * every question is scored independently in a fresh temp dir, so a crash cannot poison the next;
  * the result JSON carries the suite's sha256 and the per-question matrix, so a published score
    can be tied to an exact question set and audited question by question.

Usage:
  run_suite.py --endpoint http://localhost:8080/v1/chat/completions --model my-model-id \
               --label my-model-20260101 --out results/graded20
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
SYSTEM = ("You are solving a Python programming task. Reply with the complete solution in a single "
          "```python code block. No explanations, no tests, no example usage.")


def load_questions():
    spec = importlib.util.spec_from_file_location("q", HERE / "questions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS


def suite_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(endpoint, model, prompt, temperature, max_tokens, timeout=900):
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"content": "", "error": f"HTTP {e.code}: {e.read()[:200].decode('utf-8', 'ignore')}",
                "secs": time.time() - t0}
    except Exception as e:
        return {"content": "", "error": f"{type(e).__name__}: {e}", "secs": time.time() - t0}
    choice = (data.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    # Reasoning models occasionally spend the whole budget thinking and return empty content.
    # That is "no answer", not "wrong answer" — keep the distinction or the score misleads.
    return {
        "content": msg.get("content") or "",
        "reasoning": msg.get("reasoning_content") or msg.get("reasoning") or "",
        "finish_reason": choice.get("finish_reason"),
        "secs": time.time() - t0,
    }


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)?\s*(.*?)```", text, re.S)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()


def run_tests(code, tests, timeout=180):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "submission.py").write_text(code)
        (td / "tests.py").write_text(tests)
        try:
            p = subprocess.run([sys.executable, "tests.py"], cwd=td, capture_output=True,
                               text=True, timeout=timeout)
            ok = p.returncode == 0
            err = ""
            if not ok:
                err = (p.stderr or p.stdout or "").strip().splitlines()
                err = err[-1][:200] if err else "failed"
            return ok, err
        except subprocess.TimeoutExpired:
            return False, "TIMEOUT"
        except Exception as e:
            return False, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", default=str(HERE.parent / "results/graded20"))
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--only", default="", help="comma separated ids, e.g. E1,H1")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    qs = load_questions()
    if args.only:
        want = {x.strip() for x in args.only.split(",")}
        qs = [q for q in qs if q["id"] in want]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "label": args.label,
        "model": args.model,
        "endpoint": args.endpoint,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "started": datetime.datetime.now().isoformat(timespec="seconds"),
        "suite_sha256": suite_hash(HERE / "questions.py"),
        "questions": [],
    }

    tiers = {}
    outcomes = {}
    for q in qs:
        resp = call(args.endpoint, args.model, q["prompt"], args.temperature,
                    args.max_tokens, args.timeout)
        content = resp["content"]
        err = resp.get("error")
        row = {"id": q["id"], "tier": q["tier"], "title": q["title"],
               "seconds": round(resp["secs"], 1)}
        if err:
            row.update(passed=False, outcome="transport_error", error=err)
        else:
            code = extract_code(content)
            if not code.strip():
                row.update(passed=False, outcome="no_answer", chars=0,
                           reasoning_chars=len(resp.get("reasoning") or ""),
                           finish_reason=resp.get("finish_reason"),
                           error="empty content — the model spent its budget without answering")
            else:
                ok, terr = run_tests(code, q["tests"])
                row.update(passed=ok, outcome="pass" if ok else "wrong", error=terr,
                           chars=len(code), finish_reason=resp.get("finish_reason"),
                           answer=content[:4000])
        result["questions"].append(row)
        outcomes[row["outcome"]] = outcomes.get(row["outcome"], 0) + 1
        t = tiers.setdefault(q["tier"], {"passed": 0, "total": 0})
        t["total"] += 1
        t["passed"] += 1 if row["passed"] else 0
        mark = "PASS" if row["passed"] else row["outcome"].upper()[:4]
        print(f"  {mark:5s} {q['id']:3s} [{q['tier']:6s}] {row['seconds']:>6}s  {q['title'][:40]:42s} {row.get('error','')[:60]}",
              flush=True)

    result["tiers"] = tiers
    result["outcomes"] = outcomes
    result["total_passed"] = sum(t["passed"] for t in tiers.values())
    result["total"] = sum(t["total"] for t in tiers.values())
    result["finished"] = datetime.datetime.now().isoformat(timespec="seconds")
    path = out_dir / f"{args.label}.json"
    path.write_text(json.dumps(result, indent=1))

    print(f"\n{args.label}: {result['total_passed']}/{result['total']}  " +
          "  ".join(f"{k} {v['passed']}/{v['total']}" for k, v in tiers.items()))
    print(f"results -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
