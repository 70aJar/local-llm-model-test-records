# lms-qwen38-27b-ridge-37bpw-h164 — testing notes

- Source result: `lms-qwen38-27b-ridge-37bpw-h164.json`
- Timestamp: 2026-10-17 18:29:41
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`lms-qwen38-27b-ridge-37bpw-h164`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: book_room_b

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 361 | 504.4 |
| expense-tracker | truncated | Y | 114306 | 1733.3 |
| fake-desktop | truncated | Y | 109376 | 1771.6 |
| kanban | truncated | Y | 120160 | 1591.2 |
| reasoning | answered | Y | 1183 | 358.9 |

- Throughput: 3317 tokens / 154.4 s = 21.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 3.8}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
