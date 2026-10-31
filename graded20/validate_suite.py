#!/usr/bin/env python3
"""Prove the GRADED-20 suite is correct BEFORE any model is scored against it.

Every question ships a reference solution; if a reference solution cannot pass its own tests, the
test is wrong and the suite must not be published. This is the check that keeps a benchmark from
quietly measuring nothing.
"""
import importlib.util
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).parent


def load_questions():
    spec = importlib.util.spec_from_file_location("q", HERE / "questions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.QUESTIONS


def run_one(q, timeout=120):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "submission.py").write_text(q["solution"])
        (td / "tests.py").write_text(q["tests"])
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, "tests.py"], cwd=td, capture_output=True,
                               text=True, timeout=timeout)
            ok = p.returncode == 0
            err = (p.stderr or "").strip().splitlines()[-1] if not ok and p.stderr else ""
        except subprocess.TimeoutExpired:
            ok, err = False, "TIMEOUT"
        return ok, round(time.time() - t0, 2), err


def main():
    qs = load_questions()
    print(f"validating {len(qs)} questions against their reference solutions\n")
    fails = []
    for q in qs:
        ok, secs, err = run_one(q)
        mark = "PASS" if ok else "FAIL"
        print(f"  {mark}  {q['id']:3s} [{q['tier']:6s}] {q['title'][:44]:46s} {secs:>5}s  {err[:70]}")
        if not ok:
            fails.append(q["id"])
    print()
    if fails:
        print(f"SUITE INVALID — {len(fails)} reference solution(s) do not pass: {', '.join(fails)}")
        return 1
    print("SUITE VALID — every reference solution passes its own tests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
