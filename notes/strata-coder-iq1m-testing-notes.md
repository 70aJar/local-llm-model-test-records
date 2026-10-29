# strata-coder-iq1m — testing notes

- Source result: `strata-coder-iq1m.json`
- Timestamp: 2026-10-12 21:39:37
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`strata-coder-iq1m`)

## Raw observations

- HumanEval: 20/20
- Agency: 13/15
- Agency failures: book_room_a, focus_team

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 326 | 536.2 |
| expense-tracker | truncated | Y | 144466 | 435.3 |
| fake-desktop | truncated | Y | 75360 | 3018.9 |
| kanban | truncated | Y | 115633 | 511.5 |
| reasoning | answered | Y | 2187 | 898.2 |

- Throughput: 3649 tokens / 67.0 s = 54.5 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.2}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
