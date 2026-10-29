# omlx_youtu-parsing-omni-b8 — testing notes

- Source result: `omlx_youtu-parsing-omni-b8.json`
- Timestamp: 2026-10-11 20:19:05
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`omlx_youtu-parsing-omni-b8`)

## Raw observations

- HumanEval: 10/20
- HumanEval failures: HumanEval/0, HumanEval/1, HumanEval/8, HumanEval/9, HumanEval/10, HumanEval/11, HumanEval/12, HumanEval/13, HumanEval/17, HumanEval/19
- Agency: 2/15
- Agency failures: dept_lookup, list_active_eng, count_eng, list_support_platform, book_room_b, book_room_a, check_room_b, ticket_manager, ticket_support_lead, ticket_platform, convert_eur_usd, convert_usd_jpy, focus_team

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | N | 44611 | 156.4 |
| expense-tracker | answered | N | 153 | 1.2 |
| fake-desktop | answered | N | 211 | 1.0 |
| kanban | answered | N | 59 | 0.5 |
| reasoning | answered | Y | 3093 | 11.0 |

- Throughput: 0 tokens / 0.1 s = 0.0 tok/s
- Tool-call: {"emitted": false, "args": null, "secs": 0.1}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
