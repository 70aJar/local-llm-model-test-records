# lms_aescode-8b — testing notes

- Source result: `lms_aescode-8b.json`
- Timestamp: 2026-10-11 20:25:39
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`lms_aescode-8b`)

## Raw observations

- HumanEval: 17/20
- HumanEval failures: HumanEval/1, HumanEval/10, HumanEval/11
- Agency: 14/15
- Agency failures: ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 479 | 1.7 |
| expense-tracker | answered | Y | 17531 | 75.3 |
| fake-desktop | answered | Y | 24110 | 117.5 |
| kanban | answered | Y | 2511 | 10.3 |
| reasoning | answered | Y | 8298 | 33.0 |

- Throughput: 658 tokens / 11.7 s = 56.3 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
