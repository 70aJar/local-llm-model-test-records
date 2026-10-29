# Model Scorecard — strata-coder-iq1m

| Field | Value |
|---|---|
| **Date tested** | 2026-10-12 |
| **Model** | `qwen3.8-flash-next-coder-iq1_m` |
| **Label** | `strata-coder-iq1m` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_a, focus_team |
| Throughput | **54.5 tok/s** | 3649 tokens in 67.0 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.2 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 326 | 536.2 |
| expense-tracker | ✓ | 144466 | 435.3 |
| fake-desktop | ✓ | 75360 | 3018.9 |
| kanban | ✓ | 115633 | 511.5 |
| reasoning | ✓ | 2187 | 898.2 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 54.5 tok/s, tool-call pass. Strength: code, build tasks, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/strata-coder-iq1m-testing-notes.md)
