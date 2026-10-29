# jarvis_production — testing notes

- Source result: `jarvis_production/jarvis_production.json`
- Timestamp: 2026-10-08 15:50:16
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`jarvis_production`)

## Raw observations

- HumanEval: 17/20
- HumanEval failures: HumanEval/5, HumanEval/10, HumanEval/17
- Agency: 2/15
- Agency failures: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 651 | 6.3 |
| expense-tracker | answered | Y | 10833 | 74.9 |
| fake-desktop | answered | Y | 13269 | 96.2 |
| kanban | answered | Y | 9363 | 63.7 |
| reasoning | answered | Y | 1088 | 9.5 |

- Throughput: 687 tokens / 21.2 s = 32.4 tok/s
- Tool-call: {"emitted": false, "args": null, "secs": 2.4}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
