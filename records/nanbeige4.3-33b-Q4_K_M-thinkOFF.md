# Model Scorecard — nanbeige4.3-33b-Q4_K_M-thinkOFF

| Field | Value |
|---|---|
| **Date tested** | 2026-10-27 |
| **Model** | `nanbeige4.3-33b-q4km` |
| **Label** | `nanbeige4.3-33b-Q4_K_M-thinkOFF` |
| **Engine** | as recorded |
| **Thinking** | off |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **19.5 tok/s** | 938 tokens in 48.1 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.3 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 539 | 10.1 |
| expense-tracker | ✓ | 45821 | 788.3 |
| fake-desktop | ✓ | 33246 | 606.7 |
| kanban | ✓ | 4079 | 69.9 |
| reasoning | ✓ | 2270 | 34.8 |

## Verdict

Measured profile: HE 20/20, Tasks 5/5, Agency 15/15, 19.5 tok/s, tool-call pass. Strength: code, build tasks, agent/tool use. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/nanbeige4.3-33b-Q4_K_M-thinkOFF-testing-notes.md)
