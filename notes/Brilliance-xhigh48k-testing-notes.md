# Brilliance-xhigh48k — testing notes

- Source result: `Brilliance-xhigh48k.json`
- Timestamp: 2026-10-24 09:32:36
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Brilliance-xhigh48k`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 369 | 169.8 |
| expense-tracker | answered | Y | 44809 | 2005.0 |
| fake-desktop | answered | Y | 43791 | 2119.0 |
| kanban | answered | Y | 12059 | 2570.3 |
| reasoning | answered | Y | 1113 | 281.9 |

- Throughput: 8000 tokens / 324.5 s = 24.7 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 4.3}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
