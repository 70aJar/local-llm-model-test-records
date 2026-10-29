# omlx_qwen38_obliterated8bit — testing notes

- Source result: `omlx_qwen38_obliterated8bit.json`
- Timestamp: 2026-10-12 02:21:37
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`omlx_qwen38_obliterated8bit`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: book_room_b

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 342 | 356.7 |
| expense-tracker | answered | Y | 111136 | 1974.5 |
| fake-desktop | answered | Y | 94956 | 1991.7 |
| kanban | answered | Y | 108375 | 1982.7 |
| reasoning | answered | Y | 823 | 473.6 |

- Throughput: 6271 tokens / 351.2 s = 17.9 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 4.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
