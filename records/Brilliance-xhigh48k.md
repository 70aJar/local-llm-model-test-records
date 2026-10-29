# Model Scorecard — Brilliance-xhigh48k

| Field | Value |
|---|---|
| **Date tested** | 2026-10-24 |
| **Model** | `qwen3.8-27b-turbo-brilliance-50x-reasoning-instruct-neo-max-mtp` |
| **Label** | `Brilliance-xhigh48k` |
| **Engine** | as recorded |
| **Thinking** | on |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **24.7 tok/s** | 8000 tokens in 324.5 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 4.3 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 369 | 169.8 |
| expense-tracker | ✓ | 44809 | 2005.0 |
| fake-desktop | ✓ | 43791 | 2119.0 |
| kanban | ✓ | 12059 | 2570.3 |
| reasoning | ✓ | 1113 | 281.9 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 24.7 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Brilliance-xhigh48k-testing-notes.md)
