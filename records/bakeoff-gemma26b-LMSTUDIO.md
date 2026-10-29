# Model Scorecard — bakeoff-gemma26b-LMSTUDIO

| Field | Value |
|---|---|
| **Date tested** | 2026-10-15 |
| **Model** | `google/gemma-4-26b-a4b-qat` |
| **Label** | `bakeoff-gemma26b-LMSTUDIO` |
| **Engine** | three-engine bake-off |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **93.0 tok/s** | 1652 tokens in 17.8 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.8 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 356 | 77.9 |
| expense-tracker | ✓ | 21477 | 75.8 |
| fake-desktop | ✓ | 19879 | 85.7 |
| kanban | ✓ | 31072 | 113.5 |
| reasoning | ✓ | 1771 | 53.2 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 93.0 tok/s, tool-call pass. Strength: code, build tasks, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/bakeoff-gemma26b-LMSTUDIO-testing-notes.md)
