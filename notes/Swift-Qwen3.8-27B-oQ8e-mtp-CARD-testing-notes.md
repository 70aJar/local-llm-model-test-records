# Swift-Qwen3.8-27B-oQ8e-mtp-CARD — testing notes

- Source result: `Swift-Qwen3.8-27B-oQ8e-mtp-CARD.json`
- Timestamp: 2026-09-29 23:41:05
- Sections completed: 
- Incomplete: None
- Thinking: as recorded in the label (`Swift-Qwen3.8-27B-oQ8e-mtp-CARD`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 322 | 117.5 |
| expense-tracker | answered | Y | 16644 | 1805.1 |
| fake-desktop | answered | Y | 106111 | 1814.2 |
| kanban | answered | Y | 114432 | 1805.3 |
| reasoning | answered | Y | 846 | 338.1 |

- Throughput: 6144 tokens / 332.8 s = 18.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 4.2}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
