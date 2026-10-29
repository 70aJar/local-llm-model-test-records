# Model Scorecard — Swift-Qwen3.8-27B-oQ8e-mtp-CARD

| Field | Value |
|---|---|
| **Date tested** | 2026-09-29 |
| **Model** | `Swift-Qwen3.8-27B-oQ8e-mtp` |
| **Label** | `Swift-Qwen3.8-27B-oQ8e-mtp-CARD` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **18.5 tok/s** | 6144 tokens in 332.8 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 4.2 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 322 | 117.5 |
| expense-tracker | ✓ | 16644 | 1805.1 |
| fake-desktop | ✓ | 106111 | 1814.2 |
| kanban | ✓ | 114432 | 1805.3 |
| reasoning | ✓ | 846 | 338.1 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 18.5 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Swift-Qwen3.8-27B-oQ8e-mtp-CARD-testing-notes.md)
