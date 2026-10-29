# minicpmv47-35b-a3b-mlxvlm — testing notes

- Source result: `minicpmv47-35b-a3b-mlxvlm.json`
- Timestamp: 2026-10-17 17:45:58
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`minicpmv47-35b-a3b-mlxvlm`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 429 | 13.6 |
| expense-tracker | answered | Y | 22187 | 605.6 |
| fake-desktop | answered | Y | 27149 | 633.4 |
| kanban | answered | Y | 36046 | 769.3 |
| reasoning | answered | Y | 5012 | 128.1 |

- Throughput: 637 tokens / 55.5 s = 11.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 3.7}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
