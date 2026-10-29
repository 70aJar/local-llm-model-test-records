# Model Scorecard — jarvis_production

| Field | Value |
|---|---|
| **Date tested** | 2026-10-08 |
| **Model** | `/Volumes/2TBXPG/PROJECTSJARVIS/model/jarvis_production` |
| **Label** | `jarvis_production` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **17/20** | failed: HumanEval/5, HumanEval/10, HumanEval/17 |
| Tasks (5) | **5/5** | passed: adherence, expense-tracker, fake-desktop, kanban, reasoning |
| Agency (15) | **2/15** | failed: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team |
| Throughput | **32.4 tok/s** | 687 tokens in 21.2 s (standalone) |
| Tool-call | **fail** | no tool call emitted in 2.4 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 651 | 6.3 |
| expense-tracker | ✓ | 10833 | 74.9 |
| fake-desktop | ✓ | 13269 | 96.2 |
| kanban | ✓ | 9363 | 63.7 |
| reasoning | ✓ | 1088 | 9.5 |

## Verdict

Measured profile: HE 17/20, Tasks 5/5, Agency 2/15, 32.4 tok/s, tool-call fail. Strength: build tasks. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/jarvis_production-testing-notes.md)
