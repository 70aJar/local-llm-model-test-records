# Lightning-30B-A3B-Q4_0 — testing notes

- Source result: `Lightning-30B-A3B-Q4_0.json`
- Timestamp: 2026-10-24 17:23:03
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Lightning-30B-A3B-Q4_0`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, ticket_support_lead

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 417 | 65.8 |
| expense-tracker | truncated | Y | 50504 | 144.7 |
| fake-desktop | truncated | Y | 47889 | 151.3 |
| kanban | answered | Y | 18697 | 153.4 |
| reasoning | answered | N | 9 | 80.3 |

- Throughput: 2324 tokens / 29.8 s = 77.9 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
