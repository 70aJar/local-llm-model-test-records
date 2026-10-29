# Model Scorecard — bakeoff-gemma26b-MAGNITUDE

| Field | Value |
|---|---|
| **Date tested** | 2026-10-15 |
| **Model** | `gemma-4-26b-a4b-it-qat:gguf:q4` |
| **Label** | `bakeoff-gemma26b-MAGNITUDE` |
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
| Throughput | **123.5 tok/s** | 615 tokens in 5.0 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.2 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 362 | 1.1 |
| expense-tracker | ✓ | 18573 | 31.0 |
| fake-desktop | ✓ | 17404 | 32.7 |
| kanban | ✓ | 27706 | 47.5 |
| reasoning | ✓ | 2495 | 5.1 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 123.5 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/bakeoff-gemma26b-MAGNITUDE-testing-notes.md)
