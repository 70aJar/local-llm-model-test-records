# bakeoff-gemma26b-LMSTUDIO — testing notes

- Source result: `bakeoff-gemma26b-LMSTUDIO.json`
- Timestamp: 2026-10-15 11:18:57
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`bakeoff-gemma26b-LMSTUDIO`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 356 | 77.9 |
| expense-tracker | answered | Y | 21477 | 75.8 |
| fake-desktop | answered | Y | 19879 | 85.7 |
| kanban | answered | Y | 31072 | 113.5 |
| reasoning | answered | Y | 1771 | 53.2 |

- Throughput: 1652 tokens / 17.8 s = 93.0 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.8}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
