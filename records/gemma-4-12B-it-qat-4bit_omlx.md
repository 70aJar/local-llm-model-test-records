# Model Scorecard — gemma-4-12B-it-qat-4bit_omlx

| Field | Value |
|---|---|
| **Date tested** | 2026-10-08 |
| **Model** | `gemma-4-12B-it-qat-4bit` |
| **Label** | `gemma-4-12B-it-qat-4bit_omlx` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/10 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **39.3 tok/s** | 620 tokens in 15.8 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.7 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 410 | 3.6 |
| expense-tracker | ✓ | 17411 | 127.8 |
| fake-desktop | ✓ | 18012 | 147.7 |
| kanban | ✓ | 16539 | 130.6 |
| reasoning | ✓ | 1655 | 13.2 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 15/15, 39.3 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/gemma-4-12B-it-qat-4bit_omlx-testing-notes.md)
