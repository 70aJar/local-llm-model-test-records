# Ornith-1.5-122B-MLX-4bit — testing notes

- Source result: `Ornith-1.5-122B-MLX-4bit.json`
- Timestamp: 2026-10-24 21:03:46
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Ornith-1.5-122B-MLX-4bit`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 404 | 11.5 |
| expense-tracker | answered | Y | 37910 | 176.5 |
| fake-desktop | answered | Y | 35668 | 250.8 |
| kanban | answered | Y | 71005 | 340.0 |
| reasoning | answered | Y | 1357 | 83.4 |

- Throughput: 1441 tokens / 24.7 s = 58.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.6}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
