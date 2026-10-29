# Model Scorecard — Qwen3.8-27B-Heretic-thinkfalse

| Field | Value |
|---|---|
| **Date tested** | 2026-10-04 |
| **Model** | `Qwen3.8-27B-Heretic-Abliterated-MLX-8bit` |
| **Label** | `Qwen3.8-27B-Heretic-thinkfalse` |
| **Engine** | as recorded |
| **Thinking** | off |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/10 |
| Tasks (5) | **2/5** | passed: adherence, reasoning · failed: expense-tracker, fake-desktop, kanban |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **16.3 tok/s** | 766 tokens in 46.9 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.9 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 341 | 5.9 |
| expense-tracker | ✗ | 89 | 6.0 |
| fake-desktop | ✗ | 81 | 7.5 |
| kanban | ✗ | 91 | 10.3 |
| reasoning | ✓ | 5437 | 91.0 |

## Verdict

Measured profile: HE 19/20, Tasks 2/5, Agency 13/15, 16.3 tok/s, tool-call pass. Strength: code. Weakness: failed expense-tracker, fake-desktop, kanban. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Qwen3.8-27B-Heretic-thinkfalse-testing-notes.md)
