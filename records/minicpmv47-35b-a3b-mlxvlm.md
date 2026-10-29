# Model Scorecard — minicpmv47-35b-a3b-mlxvlm

| Field | Value |
|---|---|
| **Date tested** | 2026-10-17 |
| **Model** | `/Volumes/AIPortable/AI Shared Models/OMLX/models/mlx-community/MiniCPM-V-4.7-35B-A3B-mxfp8` |
| **Label** | `minicpmv47-35b-a3b-mlxvlm` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **11.5 tok/s** | 637 tokens in 55.5 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 3.7 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 429 | 13.6 |
| expense-tracker | ✓ | 22187 | 605.6 |
| fake-desktop | ✓ | 27149 | 633.4 |
| kanban | ✓ | 36046 | 769.3 |
| reasoning | ✓ | 5012 | 128.1 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 11.5 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/minicpmv47-35b-a3b-mlxvlm-testing-notes.md)
