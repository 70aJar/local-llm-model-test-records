# Nemotron-Bolt-E4B-Q4KM — testing notes

- Source result: `Nemotron-Bolt-E4B-Q4KM.json`
- Timestamp: 2026-10-24 15:54:14
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Nemotron-Bolt-E4B-Q4KM`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/17
- Agency: 12/15
- Agency failures: book_room_b, ticket_support_lead, ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 449 | 60.4 |
| expense-tracker | answered | Y | 22227 | 483.6 |
| fake-desktop | answered | Y | 24826 | 425.9 |
| kanban | answered | Y | 29980 | 451.7 |
| reasoning | answered | Y | 1058 | 92.6 |

- Throughput: 651 tokens / 26.5 s = 24.6 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 3.1}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
