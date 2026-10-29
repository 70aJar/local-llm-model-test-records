# Model Scorecard — Ornith-1.5-122B-MLX-4bit

| Field | Value |
|---|---|
| **Date tested** | 2026-10-24 |
| **Model** | `Ornith-1.5-122B-MLX-4bit` |
| **Label** | `Ornith-1.5-122B-MLX-4bit` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/10 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **58.3 tok/s** | 1441 tokens in 24.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.6 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 404 | 11.5 |
| expense-tracker | ✓ | 37910 | 176.5 |
| fake-desktop | ✓ | 35668 | 250.8 |
| kanban | ✓ | 71005 | 340.0 |
| reasoning | ✓ | 1357 | 83.4 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 13/15, 58.3 tok/s, tool-call pass. Strength: code, build tasks, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Ornith-1.5-122B-MLX-4bit-testing-notes.md)
