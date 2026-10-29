# Model Scorecard — bakeoff-gemma26b-OMLX

| Field | Value |
|---|---|
| **Date tested** | 2026-10-15 |
| **Model** | `gemma-4-26B-A4B-it-QAT-MLX-4bit` |
| **Label** | `bakeoff-gemma26b-OMLX` |
| **Engine** | three-engine bake-off |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **105.7 tok/s** | 631 tokens in 6.0 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.3 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 351 | 1.5 |
| expense-tracker | ✓ | 20866 | 54.6 |
| fake-desktop | ✓ | 16318 | 54.3 |
| kanban | ✓ | 28463 | 87.1 |
| reasoning | ✓ | 2299 | 6.7 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 105.7 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/bakeoff-gemma26b-OMLX-testing-notes.md)
