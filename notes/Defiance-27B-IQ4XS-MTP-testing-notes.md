# Defiance-27B-IQ4XS-MTP — testing notes

- Source result: `Defiance-27B-IQ4XS-MTP.json`
- Timestamp: 2026-10-24 14:35:20
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`Defiance-27B-IQ4XS-MTP`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 437 | 148.7 |
| expense-tracker | truncated | Y | 47366 | 495.8 |
| fake-desktop | truncated | Y | 47237 | 599.1 |
| kanban | truncated | Y | 52282 | 573.9 |
| reasoning | answered | Y | 972 | 175.9 |

- Throughput: 8000 tokens / 299.4 s = 26.7 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 3.4}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
