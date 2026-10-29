# Model Scorecard — omlx_qwen38_awq50bpw

| Field | Value |
|---|---|
| **Date tested** | 2026-10-12 |
| **Model** | `Qwen3.8-27B-AWQ-5.0bpw` |
| **Label** | `omlx_qwen38_awq50bpw` |
| **Engine** | oMLX |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: book_room_b, book_room_a |
| Throughput | **24.3 tok/s** | 8000 tokens in 329.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 3.1 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 312 | 183.8 |
| expense-tracker | ✓ | 107567 | 1341.1 |
| fake-desktop | ✓ | 102420 | 1336.9 |
| kanban | ✓ | 114606 | 1344.8 |
| reasoning | ✓ | 943 | 282.8 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 13/15, 24.3 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/omlx_qwen38_awq50bpw-testing-notes.md)
