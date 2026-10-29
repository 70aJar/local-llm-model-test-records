# magnitude_qwen38-27b-q6-v2 — testing notes

- Source result: `magnitude_qwen38-27b-q6-v2.json`
- Timestamp: 2026-10-12 00:58:49
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`magnitude_qwen38-27b-q6-v2`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 367 | 104.5 |
| expense-tracker | truncated | Y | 102703 | 845.2 |
| fake-desktop | truncated | Y | 101651 | 931.1 |
| kanban | truncated | Y | 109940 | 1055.9 |
| reasoning | answered | Y | 1089 | 230.2 |

- Throughput: 8000 tokens / 179.3 s = 44.6 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
