# Model Scorecard — lithos-Qwen3.8-27B-NVFP4-clean

| Field | Value |
|---|---|
| **Date tested** | 2026-10-19 |
| **Model** | `nvidia/Qwen3.8-27B-NVFP4` |
| **Label** | `lithos-Qwen3.8-27B-NVFP4-clean` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **2/5** | passed: adherence, reasoning · failed: expense-tracker, fake-desktop, kanban |
| Agency (15) | **13/15** | failed: list_active_eng, ticket_platform |
| Throughput | **12.9 tok/s** | 719 tokens in 55.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.0 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 355 | 4.6 |
| expense-tracker | ✗ | 401 | 3.7 |
| fake-desktop | ✗ | 344 | 5.0 |
| kanban | ✗ | 668 | 6.0 |
| reasoning | ✓ | 8686 | 46.5 |

## Verdict

Measured profile: HE 20/20, Tasks 2/5, Agency 13/15, 12.9 tok/s, tool-call pass. Strength: code. Weakness: failed expense-tracker, fake-desktop, kanban. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/lithos-Qwen3.8-27B-NVFP4-clean-testing-notes.md)
