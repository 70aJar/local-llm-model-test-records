# Model Scorecard — agentworld-identity

| Field | Value |
|---|---|
| **Date tested** | 2026-10-08 |
| **Model** | `agentworld-identity-v3-fused` |
| **Label** | `agentworld-identity` |
| **Engine** | as recorded |
| **Thinking** | as recorded |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Harness** | `harness/full_test_model.py` (HE20 + Tasks5 + Agency15 + throughput + tool-call) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | all 20 passed |
| Tasks (5) | **4/5** | passed: adherence, expense-tracker, fake-desktop, kanban · failed: reasoning |
| Agency (15) | **2/15** | failed: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team |
| Throughput | **114.0 tok/s** | 552 tokens in 4.8 s (standalone) |
| Tool-call | **fail** | no tool call emitted in 0.3 s |

## Per-task timings

| Task | OK | Chars | Seconds |
|---|---|---|---|
| adherence | ✓ | 405 | 0.9 |
| expense-tracker | ✓ | 12169 | 28.4 |
| fake-desktop | ✓ | 17851 | 51.6 |
| kanban | ✓ | 31549 | 67.3 |
| reasoning | ✗ | 41 | 0.4 |

## Verdict

Measured profile: HE 20/20, Tasks 4/5, Agency 2/15, 114.0 tok/s, tool-call fail. Strength: code, throughput. Weakness: failed reasoning. Numbers only — read the companion testing notes for caveats.

[Testing notes](../notes/agentworld-identity-testing-notes.md)
