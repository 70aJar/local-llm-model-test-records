# Model Scorecard — groot-19b-a3b-q4km-llamacpp-thinkOFF

| Field | Value |
|---|---|
| **Date tested** | 2026-10-29 |
| **Model** | `groot-19b-a3b` |
| **Label** | `groot-19b-a3b-q4km-llamacpp-thinkOFF` |
| **Engine** | as recorded |
| **Thinking** | off |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **18/20** | failed: HumanEval/11, HumanEval/15 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **15/15** | all 15 passed |
| Throughput | **103.4 tok/s** | 768 tokens in 7.4 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.4 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 483 | 1.2 |
| expense-tracker | ✓ | 27382 | 73.9 |
| fake-desktop | ✓ | 73832 | 325.2 |
| kanban | ✓ | 63495 | 198.2 |
| reasoning | ✓ | 11252 | 31.6 |

## Verdict

Measured profile: HE 18/20, Tasks 5/5, Agency 15/15, 103.4 tok/s, tool-call pass. Strength: build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/groot-19b-a3b-q4km-llamacpp-thinkOFF-testing-notes.md)
