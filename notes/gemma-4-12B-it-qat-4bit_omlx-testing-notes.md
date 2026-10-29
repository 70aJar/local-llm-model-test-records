# gemma-4-12B-it-qat-4bit_omlx — testing notes

- Source result: `gemma-4-12B-it-qat-4bit_omlx.json`
- Timestamp: 2026-10-08 14:02:23
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`gemma-4-12B-it-qat-4bit_omlx`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 410 | 3.6 |
| expense-tracker | answered | Y | 17411 | 127.8 |
| fake-desktop | answered | Y | 18012 | 147.7 |
| kanban | answered | Y | 16539 | 130.6 |
| reasoning | answered | Y | 1655 | 13.2 |

- Throughput: 620 tokens / 15.8 s = 39.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.7}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
