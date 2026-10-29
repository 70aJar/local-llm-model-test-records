# Model Scorecard — gemma-4-31B-it-uncensored-heretic-4bit

| Field | Value |
|---|---|
| **Date tested** | 2026-10-07 |
| **Model** | `gemma-4-31B-it-uncensored-heretic-4bit` |
| **Label** | `gemma-4-31B-it-uncensored-heretic-4bit` |
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
| Throughput | **17.3 tok/s** | 1214 tokens in 70.1 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 4.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 369 | 331.8 |
| expense-tracker | ✓ | 20948 | 351.0 |
| fake-desktop | ✓ | 19400 | 445.2 |
| kanban | ✓ | 26795 | 517.6 |
| reasoning | ✓ | 2286 | 103.9 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 15/15, 17.3 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/gemma-4-31B-it-uncensored-heretic-4bit-testing-notes.md)
