# Model Scorecard — saluki-27b-IQ2-thinkOFF

| Field | Value |
|---|---|
| **Date tested** | 2026-10-25 |
| **Model** | `saluki-27b` |
| **Label** | `saluki-27b-IQ2-thinkOFF` |
| **Engine** | as recorded |
| **Thinking** | off |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/5 |
| Tasks (5) | **2/5** | passed: adherence, reasoning · failed: expense-tracker, fake-desktop, kanban |
| Agency (15) | **14/15** | failed: ticket_platform |
| Throughput | **26.1 tok/s** | 645 tokens in 24.7 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 1.7 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 364 | 4.6 |
| expense-tracker | ✗ | 332 | 5.2 |
| fake-desktop | ✗ | 321 | 6.2 |
| kanban | ✗ | 214 | 4.2 |
| reasoning | ✓ | 3014 | 34.4 |

## Verdict

Measured profile: HE 19/20, Tasks 2/5, Agency 14/15, 26.1 tok/s, tool-call pass. Strength: code, agent/tool use. Weakness: failed expense-tracker, fake-desktop, kanban. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/saluki-27b-IQ2-thinkOFF-testing-notes.md)
