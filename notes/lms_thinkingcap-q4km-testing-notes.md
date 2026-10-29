# lms_thinkingcap-q4km — testing notes

- Source result: `lms_thinkingcap-q4km.json`
- Timestamp: 2026-10-14 17:40:51
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`lms_thinkingcap-q4km`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 387 | 136.2 |
| expense-tracker | answered | Y | 28281 | 1136.5 |
| fake-desktop | truncated | Y | 108681 | 1263.0 |
| kanban | truncated | Y | 118422 | 1325.2 |
| reasoning | answered | Y | 276 | 78.0 |

- Throughput: 3717 tokens / 117.4 s = 31.7 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.8}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
