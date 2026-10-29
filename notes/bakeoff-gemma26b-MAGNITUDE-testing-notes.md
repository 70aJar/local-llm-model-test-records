# bakeoff-gemma26b-MAGNITUDE — testing notes

- Source result: `bakeoff-gemma26b-MAGNITUDE.json`
- Timestamp: 2026-10-15 11:36:22
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`bakeoff-gemma26b-MAGNITUDE`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 362 | 1.1 |
| expense-tracker | answered | Y | 18573 | 31.0 |
| fake-desktop | answered | Y | 17404 | 32.7 |
| kanban | answered | Y | 27706 | 47.5 |
| reasoning | answered | Y | 2495 | 5.1 |

- Throughput: 615 tokens / 5.0 s = 123.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.2}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
