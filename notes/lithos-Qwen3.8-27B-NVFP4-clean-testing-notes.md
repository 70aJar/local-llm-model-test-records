# lithos-Qwen3.8-27B-NVFP4-clean — testing notes

- Source result: `lithos-Qwen3.8-27B-NVFP4-clean.json`
- Timestamp: 2026-10-19 15:35:46
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`lithos-Qwen3.8-27B-NVFP4-clean`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: list_active_eng, ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 355 | 4.6 |
| expense-tracker | answered | N | 401 | 3.7 |
| fake-desktop | answered | N | 344 | 5.0 |
| kanban | answered | N | 668 | 6.0 |
| reasoning | answered | Y | 8686 | 46.5 |

- Throughput: 719 tokens / 55.7 s = 12.9 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.0}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
