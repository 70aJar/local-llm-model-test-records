# lms_swift15-iq3s-mtp — testing notes

- Source result: `lms_swift15-iq3s-mtp.json`
- Timestamp: 2026-10-14 18:14:50
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`lms_swift15-iq3s-mtp`)

## Raw observations

- HumanEval: 20/20
- Agency: 14/15
- Agency failures: ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 308 | 75.2 |
| expense-tracker | answered | Y | 12621 | 835.9 |
| fake-desktop | None | None | None | None |
| kanban | None | None | None | None |
| reasoning | None | None | None | None |

- Throughput: 4638 tokens / 122.6 s = 37.8 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.9}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
