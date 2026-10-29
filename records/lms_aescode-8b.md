# Model Scorecard — lms_aescode-8b

| Field | Value |
|---|---|
| **Date tested** | 2026-10-11 |
| **Model** | `aescode-8b` |
| **Label** | `lms_aescode-8b` |
| **Engine** | LM Studio |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **17/20** | failed: HumanEval/1, HumanEval/10, HumanEval/11 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **14/15** | failed: ticket_platform |
| Throughput | **56.3 tok/s** | 658 tokens in 11.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 479 | 1.7 |
| expense-tracker | ✓ | 17531 | 75.3 |
| fake-desktop | ✓ | 24110 | 117.5 |
| kanban | ✓ | 2511 | 10.3 |
| reasoning | ✓ | 8298 | 33.0 |

## Verdict

Measured profile: HE 17/20, Tasks 5/5, Agency 14/15, 56.3 tok/s, tool-call pass. Strength: build tasks, agent/tool use, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/lms_aescode-8b-testing-notes.md)
