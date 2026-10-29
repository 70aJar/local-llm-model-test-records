# bakeoff-gemma26b-OMLX — testing notes

- Source result: `bakeoff-gemma26b-OMLX.json`
- Timestamp: 2026-10-15 11:32:59
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`bakeoff-gemma26b-OMLX`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 351 | 1.5 |
| expense-tracker | answered | Y | 20866 | 54.6 |
| fake-desktop | answered | Y | 16318 | 54.3 |
| kanban | answered | Y | 28463 | 87.1 |
| reasoning | answered | Y | 2299 | 6.7 |

- Throughput: 631 tokens / 6.0 s = 105.7 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.3}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
