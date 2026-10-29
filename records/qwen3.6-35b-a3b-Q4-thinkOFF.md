# Model Scorecard — qwen3.6-35b-a3b-Q4-thinkOFF

| Field | Value |
|---|---|
| **Date tested** | 2026-10-28 |
| **Model** | `qwen3.6-35b-a3b:gguf:q4` |
| **Label** | `qwen3.6-35b-a3b-Q4-thinkOFF` |
| **Engine** | as recorded |
| **Thinking** | off |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **16/20** | failed: HumanEval/4, HumanEval/5, HumanEval/10, HumanEval/13 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: ticket_support_lead, ticket_platform |
| Throughput | **124.6 tok/s** | 701 tokens in 5.6 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 0.5 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 342 | 1.0 |
| expense-tracker | ✓ | 19641 | 26.3 |
| fake-desktop | ✓ | 26350 | 39.6 |
| kanban | ✓ | 31223 | 58.3 |
| reasoning | ✓ | 5113 | 20.3 |

## Verdict

Measured profile: HE 16/20, Tasks 5/5, Agency 13/15, 124.6 tok/s, tool-call pass. Strength: build tasks, throughput. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/qwen3.6-35b-a3b-Q4-thinkOFF-testing-notes.md)
