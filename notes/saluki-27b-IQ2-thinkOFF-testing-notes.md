# saluki-27b-IQ2-thinkOFF — testing notes

- Source result: `saluki-27b-IQ2-thinkOFF.json`
- Timestamp: 2026-10-25 23:03:15
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`saluki-27b-IQ2-thinkOFF`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/5
- Agency: 14/15
- Agency failures: ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 364 | 4.6 |
| expense-tracker | answered | N | 332 | 5.2 |
| fake-desktop | answered | N | 321 | 6.2 |
| kanban | answered | N | 214 | 4.2 |
| reasoning | answered | Y | 3014 | 34.4 |

- Throughput: 645 tokens / 24.7 s = 26.1 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.7}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
