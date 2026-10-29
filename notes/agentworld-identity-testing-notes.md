# agentworld-identity — testing notes

- Source result: `agentworld-identity/agentworld-identity.json`
- Timestamp: 2026-10-08 16:03:41
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`agentworld-identity`)

## Raw observations

- HumanEval: 20/20
- Agency: 2/15
- Agency failures: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 405 | 0.9 |
| expense-tracker | answered | Y | 12169 | 28.4 |
| fake-desktop | answered | Y | 17851 | 51.6 |
| kanban | answered | Y | 31549 | 67.3 |
| reasoning | answered | N | 41 | 0.4 |

- Throughput: 552 tokens / 4.8 s = 114.0 tok/s
- Tool-call: {"emitted": false, "args": null, "secs": 0.3}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
