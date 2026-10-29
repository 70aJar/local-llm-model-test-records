# gemma-4-31B-it-uncensored-heretic-4bit — testing notes

- Source result: `gemma-4-31B-it-uncensored-heretic-4bit.json`
- Timestamp: 2026-10-07 17:47:39
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`gemma-4-31B-it-uncensored-heretic-4bit`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 369 | 331.8 |
| expense-tracker | answered | Y | 20948 | 351.0 |
| fake-desktop | answered | Y | 19400 | 445.2 |
| kanban | answered | Y | 26795 | 517.6 |
| reasoning | answered | Y | 2286 | 103.9 |

- Throughput: 1214 tokens / 70.1 s = 17.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 4.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
