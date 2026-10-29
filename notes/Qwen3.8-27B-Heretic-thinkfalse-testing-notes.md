# Qwen3.8-27B-Heretic-thinkfalse — testing notes

- Source result: `Qwen3.8-27B-Heretic-thinkfalse.json`
- Timestamp: 2026-10-04 08:16:53
- Sections completed: 
- Incomplete: None
- Thinking: as recorded in the label (`Qwen3.8-27B-Heretic-thinkfalse`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 341 | 5.9 |
| expense-tracker | answered | N | 89 | 6.0 |
| fake-desktop | answered | N | 81 | 7.5 |
| kanban | answered | N | 91 | 10.3 |
| reasoning | answered | Y | 5437 | 91.0 |

- Throughput: 766 tokens / 46.9 s = 16.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
