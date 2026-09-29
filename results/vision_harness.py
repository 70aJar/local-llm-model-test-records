#!/usr/bin/env python3
"""Vision benchmark harness for fleet VLMs.

Sends an image + question to any OpenAI-compatible vision endpoint (LM Studio
`:1234`), grades the answer, and writes per-benchmark + per-capability results.

Grading is capability-aware, because "correct" means different things:
  · MCQ (A/B/C/D)      -> the model must emit the letter
  · yes/no             -> normalised boolean match (hallucination tests)
  · numeric            -> numeric equality with tolerance (charts)
  · short text / OCR   -> normalised string match (case/punct/space insensitive)

Deliberately strict on extraction: the model must actually answer. A model that
refuses or emits nothing counts as WRONG, not as "skipped" — otherwise a model
that cannot see scores the same as one that can.

Usage:
  python3 vision_harness.py <lmstudio-model-key> <label> [bench1,bench2,...]
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request

API = "http://127.0.0.1:1234/v1/chat/completions"
ROOT = "/Volumes/AIPortable/AI Server/Vision Benchmarks"
RESULTS = os.path.expanduser("~/Projects/AlitaAICore/benchmarks/results")
SUITE = ["mmstar", "realworldqa", "ocrbench", "ai2d", "chartqa", "pope"]

MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif"}


# ─────────────────────────── grading ───────────────────────────

def norm(s):
    """Aggressive normalisation for short free-text comparison."""
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s.]", "", s)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(".")


def first_letter(txt, valid="ABCDEFGH"):
    """Pull an MCQ letter. Accepts 'B', 'B)', '(B)', 'answer is B', 'B. foo'."""
    if not txt:
        return None
    t = txt.strip()
    m = re.search(r"\banswer\s*(?:is|:)?\s*[\(\[]?\s*([A-H])\b", t, re.I)
    if m:
        return m.group(1).upper()
    m = re.match(r"^\s*[\(\[]?\s*([A-H])\s*[\)\].:,\-]", t)
    if m:
        return m.group(1).upper()
    m = re.match(r"^\s*[\(\[]?\s*([A-H])\s*$", t, re.I)
    if m:
        return m.group(1).upper()
    m = re.search(r"\b([A-H])[\)\].:,]", t)
    if m and m.group(1).upper() in valid:
        return m.group(1).upper()
    return None


def to_num(s):
    try:
        return float(str(s).replace(",", "").replace("$", "").strip())
    except Exception:  # noqa: BLE001
        return None


def strip_think(txt):
    """Remove <think>...</think> reasoning that some models emit INSIDE content.

    ★ Found by smoke test: MiMo-VL puts its chain-of-thought in `content` wrapped
    in <think> tags rather than in a separate reasoning_content field. Left in, the
    grader scans the reasoning and can extract a letter that was never an answer
    (e.g. reading 'A' out of prose) — scoring noise as signal. Also handles the
    unclosed form, which appears when generation is cut off mid-thought.
    """
    if not txt:
        return ""
    # closed blocks first
    txt = re.sub(r"<think>.*?</think>", " ", txt, flags=re.S | re.I)
    # an unclosed <think> means the answer never arrived — drop everything after it
    m = re.search(r"<think>", txt, re.I)
    if m:
        txt = txt[:m.start()]
    return txt.strip()


def last_boxed(txt):
    """Return the content of the LAST \\boxed{...}, else None.

    Models routinely mark their final answer in LaTeX: \\boxed{yes}, \\boxed{8440}.
    ★ Found by smoke test: this scored 'yesno-missing' because the yes/no branch
    needs an exact match and never saw past the wrapper, so a model answering
    correctly would have scored ~0 on POPE. Taking the LAST box is deliberate:
    models often box intermediate values and box the final answer last.
    """
    if not txt:
        return None
    hits = re.findall(r"\\boxed\s*\{([^{}]*)\}", txt, flags=re.I)
    for h in reversed(hits):
        h = h.strip()
        if 0 < len(h) <= 40:          # skip boxed equations/output blocks
            return h
    return None


def grade(item, pred):
    """Return (correct: bool, how: str)."""
    gold = str(item.get("answer", "")).strip()
    p = strip_think(pred)
    boxed = last_boxed(p)
    cap = item.get("capability", "")

    # Recovery: some models box the answer INSIDE the <think> block and emit
    # nothing after it, so stripping leaves content empty. A \boxed{} is an
    # explicit answer marker rather than free reasoning, so recover it — but only
    # in this case, and tag the verdict so it stays auditable. (Grading reasoning
    # prose in general is NOT done; see the reasoning_content note in ask().)
    if not p:
        raw_box = last_boxed(pred)
        if raw_box:
            p = raw_box
            boxed = raw_box
            cap = cap + " (boxed-in-think)"

    if not p:
        return False, "empty"

    # yes/no (POPE, some RealWorldQA)
    if norm(gold) in ("yes", "no"):
        pn = norm(boxed or p)
        # take the first yes/no token present
        m = re.search(r"\b(yes|no)\b", pn)
        if m:
            return (m.group(1) == norm(gold)), ("yesno" if m.group(1) == norm(gold) else "yesno-wrong")
        return False, "yesno-missing"

    # MCQ: gold is a single letter, or question has options
    opts = item.get("options")
    if re.fullmatch(r"[A-H]", gold.upper()) and (opts or "option" in item.get("question", "").lower()
                                                 or cap in ("vision-centric MCQ",)):
        pl = (first_letter(boxed) if boxed else None) or first_letter(p)
        if pl is None:
            return False, "no-letter"
        return (pl == gold.upper()), ("letter" if pl == gold.upper() else f"letter-wrong({pl}!={gold.upper()})")

    # numeric
    gn = to_num(gold)
    src = boxed or p
    mm = re.search(r"-?\d[\d,]*\.?\d*", src)
    pn_ = to_num(mm.group(0)) if mm else None
    if gn is not None and pn_ is not None:
        if gn == 0:
            return (abs(pn_) < 1e-6), "num"
        return (abs(pn_ - gn) / max(abs(gn), 1e-9) <= 0.02), "num"

    # AI2D: options list, answer is a 0-BASED index into it
    # ★ Corrected Sep 29: this branch used to assume 1-based (`int(gold)-1`) and
    # required `1 <= gold <= len(opts)`. AI2D's answer field is 0-based — proven by
    # the presence of gold='0' (27/100 items), which a 1-based field cannot express.
    # Every 1..N item therefore mapped to the WRONG option, and every gold=0 item
    # fell through to text matching. AI2D scored 8% — below the 25% guessing floor —
    # which is what exposed it.
    if opts and re.fullmatch(r"\d+", str(gold)) and int(gold) < len(opts):
        idx = int(gold)                      # 0-BASED
        gold_value = str(opts[idx]).strip()
        # (a) the model named the option's value — unambiguous, always accept
        if norm(gold_value) and norm(gold_value) in norm(p):
            return True, "opt-value"
        # (b) the model answered by POSITION (A/B/C/D). Only meaningful when the
        # option is not itself a bare letter — otherwise "B" is ambiguous between
        # "the option at index 1" and "the label B", and crediting both would
        # inflate the score on a coin-flip.
        option_is_letter = bool(re.fullmatch(r"[A-Za-z]", gold_value))
        if not option_is_letter:
            pl = first_letter(boxed) if boxed else None
            pl = pl or first_letter(p)
            if pl and ord(pl) - 65 == idx:
                return True, "opt-position"
        return False, "opt-miss"

    # short text / OCR
    g, pp = norm(gold), norm(src)
    if g and g == pp:
        return True, "exact"
    if g and g in pp:
        return True, "contains"
    if g and pp and pp in g and len(pp) >= max(3, len(g) * 0.6):
        return True, "contained"
    return False, "text-miss"


# ─────────────────────────── model call ───────────────────────────

def b64_image(path):
    ext = os.path.splitext(path)[1].lower()
    with open(path, "rb") as fh:
        data = base64.b64encode(fh.read()).decode()
    return f"data:{MIME.get(ext, 'image/png')};base64,{data}"


def build_prompt(item):
    q = item["question"]
    if item.get("options"):
        letters = "ABCDEFGH"
        lines = [f"{letters[i]}. {o}" for i, o in enumerate(item["options"])]
        return (q + "\n" + "\n".join(lines) +
                "\nAnswer with the option letter only."), True
    low = q.lower()
    if "option" in low and re.search(r"\bA[\.\)]", q):
        return q + "\nAnswer with the option letter only.", True
    if item.get("capability", "").startswith("object hallucination"):
        return q + "\nAnswer yes or no only.", False
    return q + "\nAnswer concisely.", False


def ask(model, item, img_path, max_tokens=None, retries=3):
    # ★ Budget must be per-model. Findable by probe, not assumed: a heavy-reasoning
    # VLM can spend the whole budget on <think> and return EMPTY content with
    # finish_reason='length' — which looks exactly like "cannot see". A1 spends
    # ~5,000 chars reasoning per question and needs >=3072 to emit its answer;
    # MiMo-VL answers within 1536. Running A1 at the 1536 default would have scored
    # it ~0% on every benchmark and produced a false "A1 cannot see" verdict.
    if max_tokens is None:
        max_tokens = int(os.environ.get("VISION_MAX_TOKENS", "1536"))
    prompt, _ = build_prompt(item)
    uri = b64_image(img_path)
    body = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": uri}},
        ]}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
    }
    last = ""
    for a in range(retries):
        try:
            req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as fh:
                d = json.load(fh)
            m = d["choices"][0]["message"]
            # Content ONLY. Do NOT fall back to reasoning_content: chain-of-thought
            # is not an answer, and grading it lets a model that never answered score
            # on its own working. An empty content is a real failure (counted wrong
            # by grade()); the smoke test showed MiMo-VL emits <think> inside
            # content, which grade() now strips before any letter is extracted.
            txt = m.get("content") or ""
            return txt
        except Exception as exc:  # noqa: BLE001
            last = f"{type(exc).__name__}: {str(exc)[:80]}"
            time.sleep(1.5 * (a + 1))
    return f"__ERROR__ {last}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    model = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else model
    benches = sys.argv[3].split(",") if len(sys.argv) > 3 else SUITE

    os.makedirs(RESULTS, exist_ok=True)
    out = {"label": label, "model": model, "started": time.strftime("%Y-%m-%d %H:%M:%S"),
           "benchmarks": {}, "items": []}

    t_all = time.time()
    for bench in benches:
        d = os.path.join(ROOT, bench)
        f = os.path.join(d, "items.jsonl")
        if not os.path.exists(f):
            print(f"  ⚠️  {bench}: no items.jsonl — skipped")
            continue
        items = [json.loads(l) for l in open(f) if l.strip()]
        print(f"\n{'='*70}\n{bench}  ({len(items)} items)")
        per = {"total": 0, "correct": 0, "by_capability": {}, "by_category": {},
               "failures": [], "secs": 0.0}
        t0 = time.time()
        for i, it in enumerate(items, 1):
            img = os.path.join(ROOT, it["image"])
            if not os.path.exists(img):
                continue
            pred = ask(model, it, img)
            ok, how = grade(it, pred)
            per["total"] += 1
            per["correct"] += int(ok)
            cap = it.get("capability", "?")
            c = per["by_capability"].setdefault(cap, {"n": 0, "ok": 0})
            c["n"] += 1
            c["ok"] += int(ok)
            for k in ("category", "question_type", "type"):
                if k in it:
                    b = per["by_category"].setdefault(f"{k}={it[k]}", {"n": 0, "ok": 0})
                    b["n"] += 1
                    b["ok"] += int(ok)
                    break
            rec = dict(bench=bench, id=it["id"], ok=ok, how=how,
                       gold=it["answer"],
                       # ★ store what was actually GRADED (think-stripped), not just a
                       # prefix of the raw text. Previously only pred[:300] was kept and
                       # the AI2D answers sat AFTER long <think> blocks, so the graded
                       # answer was truncated away and results could NOT be re-graded
                       # after a grader fix — it forced a full re-run.
                       answer=(strip_think(pred) or "")[:400],
                       pred=(pred or "")[:1200])
            out["items"].append(rec)
            if not ok and len(per["failures"]) < 15:
                per["failures"].append(rec)
            if i % 10 == 0 or i == len(items):
                el = time.time() - t0
                print(f"    {i:>4}/{len(items)}  acc={per['correct']/per['total']:.1%}"
                      f"  {el:.0f}s  ({el/max(per['total'],1):.1f}s/item)")
        per["secs"] = round(time.time() - t0, 1)
        per["accuracy"] = round(per["correct"] / per["total"], 4) if per["total"] else None
        out["benchmarks"][bench] = per
        print(f"  → {bench}: {per['correct']}/{per['total']} = {per['accuracy']}"
              f"  ({per['secs']:.0f}s)")

    out["total_secs"] = round(time.time() - t_all, 1)
    tot = sum(b["total"] for b in out["benchmarks"].values())
    ok = sum(b["correct"] for b in out["benchmarks"].values())
    out["overall"] = {"correct": ok, "total": tot,
                      "accuracy": round(ok / tot, 4) if tot else None}
    path = os.path.join(RESULTS, f"vision-{label}.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print(f"\n{'='*70}\nVISION SUMMARY — {label}")
    print(f"  {'benchmark':<14} {'acc':>7}  {'n':>5}  secs")
    for b, s in out["benchmarks"].items():
        print(f"  {b:<14} {s['accuracy']:>7.1%}  {s['total']:>5}  {s['secs']:.0f}")
    print(f"  {'OVERALL':<14} {out['overall']['accuracy']:>7.1%}  {tot:>5}")
    print(f"\n  saved → {path}")


if __name__ == "__main__":
    main()
