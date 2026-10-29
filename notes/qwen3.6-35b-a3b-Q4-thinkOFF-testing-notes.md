# qwen3.6-35b-a3b-Q4-thinkOFF — testing notes

- Source result: `qwen3.6-35b-a3b-Q4-thinkOFF.json`
- Timestamp: 2026-10-28 02:26:01
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`qwen3.6-35b-a3b-Q4-thinkOFF`)

## Raw observations

- HumanEval: 16/20
- HumanEval failures: HumanEval/4, HumanEval/5, HumanEval/10, HumanEval/13
- Agency: 13/15
- Agency failures: ticket_support_lead, ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 342 | 1.0 |
| expense-tracker | answered | Y | 19641 | 26.3 |
| fake-desktop | answered | Y | 26350 | 39.6 |
| kanban | answered | Y | 31223 | 58.3 |
| reasoning | answered | Y | 5113 | 20.3 |

- Throughput: 701 tokens / 5.6 s = 124.6 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 0.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
