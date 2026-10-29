# nanbeige4.3-33b-Q4_K_M-thinkOFF — testing notes

- Source result: `nanbeige4.3-33b-Q4_K_M-thinkOFF.json`
- Timestamp: 2026-10-27 08:59:26
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`nanbeige4.3-33b-Q4_K_M-thinkOFF`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 539 | 10.1 |
| expense-tracker | answered | Y | 45821 | 788.3 |
| fake-desktop | answered | Y | 33246 | 606.7 |
| kanban | answered | Y | 4079 | 69.9 |
| reasoning | answered | Y | 2270 | 34.8 |

- Throughput: 938 tokens / 48.1 s = 19.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.3}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
