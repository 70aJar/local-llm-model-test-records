# Swift-1.5-5bit-MLX-omlx — testing notes

- Source result: `Swift-1.5-5bit-MLX-omlx.json`
- Timestamp: 2026-10-17 19:46:26
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Swift-1.5-5bit-MLX-omlx`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: book_room_b

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 365 | 430.1 |
| expense-tracker | answered | Y | 36018 | 3996.9 |
| fake-desktop | answered | Y | 102350 | 1686.6 |
| kanban | answered | Y | 5304 | 2187.7 |
| reasoning | answered | Y | 1553 | 341.5 |

- Throughput: 2074 tokens / 253.4 s = 8.2 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 8.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
