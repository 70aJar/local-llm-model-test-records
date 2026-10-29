# Model Scorecard — Gemma-4-12B-AEON-Abliterated_omlx

| Field | Value |
|---|---|
| **Date tested** | 2026-10-08 |
| **Model** | `Gemma-4-12B-it-AEON-Abliterated-MLX-8bit` |
| **Label** | `Gemma-4-12B-AEON-Abliterated_omlx` |
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
| Throughput | **33.8 tok/s** | 625 tokens in 18.5 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.8 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 389 | 4.4 |
| expense-tracker | ✓ | 16680 | 147.6 |
| fake-desktop | ✓ | 16171 | 165.7 |
| kanban | ✓ | 20309 | 180.1 |
| reasoning | ✓ | 2104 | 17.4 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 15/15, 33.8 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/Gemma-4-12B-AEON-Abliterated_omlx-testing-notes.md)
