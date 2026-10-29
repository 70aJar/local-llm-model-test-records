# Model Scorecard — iris_qwen3-vl-8b

| Field | Value |
|---|---|
| **Date tested** | 2026-10-11 |
| **Model** | `qwen/qwen3-vl-8b` |
| **Label** | `iris_qwen3-vl-8b` |
| **Engine** | LM Studio (Iris) |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | failed: HumanEval/1 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **13/15** | failed: dept_lookup, ticket_platform |
| Throughput | **16.0 tok/s** | 682 tokens in 42.6 s (standalone) |
| Tool-call | **pass** | emitted args {"a": 37, "b": 15} in 2.0 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 427 | 9.5 |
| expense-tracker | ✓ | 12716 | 230.2 |
| fake-desktop | ✓ | 10367 | 195.7 |
| kanban | ✓ | 11734 | 215.4 |
| reasoning | ✓ | 3254 | 59.4 |

## Verdict

Measured profile: HE 19/20, Tasks 5/5, Agency 13/15, 16.0 tok/s, tool-call pass. Strength: code, build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/iris_qwen3-vl-8b-testing-notes.md)
