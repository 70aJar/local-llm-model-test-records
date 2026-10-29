# Model Scorecard — magnitude_qwen38-27b-q6-v2

| Field | Value |
|---|---|
| **Date tested** | 2026-10-12 |
| **Model** | `qwen3.8-27b:gguf:q6` |
| **Label** | `magnitude_qwen38-27b-q6-v2` |
| **Engine** | Magnitude |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **44.6 tok/s** | 8000 tokens in 179.3 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 367 | 104.5 |
| expense-tracker | ✓ | 102703 | 845.2 |
| fake-desktop | ✓ | 101651 | 931.1 |
| kanban | ✓ | 109940 | 1055.9 |
| reasoning | ✓ | 1089 | 230.2 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 44.6 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/magnitude_qwen38-27b-q6-v2-testing-notes.md)
