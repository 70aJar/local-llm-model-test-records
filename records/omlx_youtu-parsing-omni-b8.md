# Model Scorecard — omlx_youtu-parsing-omni-b8

| Field | Value |
|---|---|
| **Date tested** | 2026-10-11 |
| **Model** | `Youtu-Parsing-Omni-mlx-8bit` |
| **Label** | `omlx_youtu-parsing-omni-b8` |
| **Engine** | oMLX |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **10/20** | failed: HumanEval/0, HumanEval/1, HumanEval/8, HumanEval/9, HumanEval/10, HumanEval/11, HumanEval/12, HumanEval/13, HumanEval/17, HumanEval/19 |
| Tasks (5) | **1/5** | passed: reasoning · failed: adherence, expense-tracker, fake-desktop, kanban |
| Agency (15) | **2/15** | failed: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team |
| Throughput | **0.0 tok/s** | 0 tokens in 0.1 s (standalone) |
| Tool-call | **fail** | no tool call emitted in 0.1 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✗ | 44611 | 156.4 |
| expense-tracker | ✗ | 153 | 1.2 |
| fake-desktop | ✗ | 211 | 1.0 |
| kanban | ✗ | 59 | 0.5 |
| reasoning | ✓ | 3093 | 11.0 |

## Verdict

Measured profile: HE 10/20, Tasks 1/5, Agency 2/15, 0.0 tok/s, tool-call fail. Weakness: failed adherence, expense-tracker, fake-desktop, kanban. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/omlx_youtu-parsing-omni-b8-testing-notes.md)
