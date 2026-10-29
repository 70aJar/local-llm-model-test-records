# Model Scorecard — lms_thinkingcap-q4km

| Field | Value |
|---|---|
| **Date tested** | 2026-10-14 |
| **Model** | `thinkingcap-qwen3.8-27b` |
| **Label** | `lms_thinkingcap-q4km` |
| **Engine** | LM Studio |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **31.7 tok/s** | 3717 tokens in 117.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.8 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 387 | 136.2 |
| expense-tracker | ✓ | 28281 | 1136.5 |
| fake-desktop | ✓ | 108681 | 1263.0 |
| kanban | ✓ | 118422 | 1325.2 |
| reasoning | ✓ | 276 | 78.0 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 31.7 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/lms_thinkingcap-q4km-testing-notes.md)
