# Model Scorecard — magnitude_friday_12b

| Field | Value |
|---|---|
| **Date tested** | 2026-10-11 |
| **Model** | `gemma-4-12b-it-qat:gguf:q4` |
| **Label** | `magnitude_friday_12b` |
| **Engine** | Magnitude |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/10 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **50.6 tok/s** | 619 tokens in 12.2 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 431 | 4.1 |
| expense-tracker | ✓ | 17306 | 119.5 |
| fake-desktop | ✓ | 14825 | 93.9 |
| kanban | ✓ | 20630 | 127.0 |
| reasoning | ✓ | 2125 | 11.8 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 15/15, 50.6 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/magnitude_friday_12b-testing-notes.md)
