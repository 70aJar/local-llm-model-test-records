# Gemma-4-12B-AEON-Abliterated_omlx — testing notes

- Source result: `Gemma-4-12B-AEON-Abliterated_omlx.json`
- Timestamp: 2026-10-08 14:27:21
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Gemma-4-12B-AEON-Abliterated_omlx`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 389 | 4.4 |
| expense-tracker | answered | Y | 16680 | 147.6 |
| fake-desktop | answered | Y | 16171 | 165.7 |
| kanban | answered | Y | 20309 | 180.1 |
| reasoning | answered | Y | 2104 | 17.4 |

- Throughput: 625 tokens / 18.5 s = 33.8 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.8}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
