# A3b-MiMo-VL-7B-RL-2508-Q8_0 — testing notes

- Source result: `A3b-MiMo-VL-7B-RL-2508-Q8_0.json`
- Timestamp: 2026-09-29 05:03:23
- Sections completed: 
- Incomplete: None
- Thinking: as recorded in the label (`A3b-MiMo-VL-7B-RL-2508-Q8_0`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | N | 2107 | 11.1 |
| expense-tracker | answered | Y | 43723 | 246.2 |
| fake-desktop | answered | Y | 42385 | 351.1 |
| kanban | answered | Y | 74193 | 662.9 |
| reasoning | answered | Y | 25640 | 351.9 |

- Throughput: 4366 tokens / 262.2 s = 16.7 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 5.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
