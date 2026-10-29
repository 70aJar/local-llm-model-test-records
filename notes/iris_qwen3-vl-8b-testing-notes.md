# iris_qwen3-vl-8b — testing notes

- Source result: `iris_qwen3-vl-8b.json`
- Timestamp: 2026-10-11 20:07:11
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`iris_qwen3-vl-8b`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/1
- Agency: 13/15
- Agency failures: dept_lookup, ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 427 | 9.5 |
| expense-tracker | answered | Y | 12716 | 230.2 |
| fake-desktop | answered | Y | 10367 | 195.7 |
| kanban | answered | Y | 11734 | 215.4 |
| reasoning | answered | Y | 3254 | 59.4 |

- Throughput: 682 tokens / 42.6 s = 16.0 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.0}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
