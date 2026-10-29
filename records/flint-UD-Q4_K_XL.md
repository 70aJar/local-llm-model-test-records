# Model Scorecard — flint-UD-Q4_K_XL

| Field | Value |
|---|---|
| **Date tested** | 2026-10-27 |
| **Model** | `flint-UD-Q4_K_XL` |
| **Label** | `flint-UD-Q4_K_XL` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: book_room_a |
| Throughput | **79.9 tok/s** | 4129 tokens in 51.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.0 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 324 | 36.8 |
| expense-tracker | ✓ | 22282 | 259.0 |
| fake-desktop | ✓ | 119492 | 427.5 |
| kanban | ✓ | 25949 | 431.6 |
| reasoning | ✓ | 861 | 94.0 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 14/15, 79.9 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/flint-UD-Q4_K_XL-testing-notes.md)
