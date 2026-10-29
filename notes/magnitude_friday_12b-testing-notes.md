# magnitude_friday_12b — testing notes

- Source result: `magnitude_friday_12b.json`
- Timestamp: 2026-10-11 19:18:30
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`magnitude_friday_12b`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 431 | 4.1 |
| expense-tracker | answered | Y | 17306 | 119.5 |
| fake-desktop | answered | Y | 14825 | 93.9 |
| kanban | answered | Y | 20630 | 127.0 |
| reasoning | answered | Y | 2125 | 11.8 |

- Throughput: 619 tokens / 12.2 s = 50.6 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
