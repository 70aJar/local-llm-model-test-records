# groot-19b-a3b-q4km-llamacpp-thinkOFF — testing notes

- Source result: `groot-19b-a3b-q4km-llamacpp-thinkOFF.json`
- Timestamp: 2026-10-29 22:16:28
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`groot-19b-a3b-q4km-llamacpp-thinkOFF`)

## Raw observations

- HumanEval: 18/20
- HumanEval failures: HumanEval/11, HumanEval/15
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 483 | 1.2 |
| expense-tracker | answered | Y | 27382 | 73.9 |
| fake-desktop | answered | Y | 73832 | 325.2 |
| kanban | answered | Y | 63495 | 198.2 |
| reasoning | answered | Y | 11252 | 31.6 |

- Throughput: 768 tokens / 7.4 s = 103.4 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.4}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
