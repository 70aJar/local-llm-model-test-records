# flint-UD-Q4_K_XL — testing notes

- Source result: `flint-UD-Q4_K_XL.json`
- Timestamp: 2026-10-27 07:26:53
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`flint-UD-Q4_K_XL`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 324 | 36.8 |
| expense-tracker | answered | Y | 22282 | 259.0 |
| fake-desktop | truncated | Y | 119492 | 427.5 |
| kanban | answered | Y | 25949 | 431.6 |
| reasoning | answered | Y | 861 | 94.0 |

- Throughput: 4129 tokens / 51.7 s = 79.9 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.0}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
