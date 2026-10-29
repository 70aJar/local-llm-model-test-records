# omlx_qwen38_awq50bpw — testing notes

- Source result: `omlx_qwen38_awq50bpw.json`
- Timestamp: 2026-10-12 03:49:21
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`omlx_qwen38_awq50bpw`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 312 | 183.8 |
| expense-tracker | answered | Y | 107567 | 1341.1 |
| fake-desktop | answered | Y | 102420 | 1336.9 |
| kanban | answered | Y | 114606 | 1344.8 |
| reasoning | answered | Y | 943 | 282.8 |

- Throughput: 8000 tokens / 329.4 s = 24.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 3.1}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
