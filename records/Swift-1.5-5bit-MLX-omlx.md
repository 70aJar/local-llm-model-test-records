# Model Scorecard — Swift-1.5-5bit-MLX-omlx

| Field | Value |
|---|---|
| **Date tested** | 2026-10-17 |
| **Model** | `Swift-1.5-5bit-MLX-omlx` |
| **Label** | `Swift-1.5-5bit-MLX-omlx` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: book_room_b |
| Throughput | **8.2 tok/s** | 2074 tokens in 253.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 8.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 365 | 430.1 |
| expense-tracker | ✓ | 36018 | 3996.9 |
| fake-desktop | ✓ | 102350 | 1686.6 |
| kanban | ✓ | 5304 | 2187.7 |
| reasoning | ✓ | 1553 | 341.5 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 14/15, 8.2 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Swift-1.5-5bit-MLX-omlx-testing-notes.md)
