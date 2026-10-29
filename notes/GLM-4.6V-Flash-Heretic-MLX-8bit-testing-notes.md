# GLM-4.6V-Flash-Heretic-MLX-8bit — testing notes

- Source result: `GLM-4.6V-Flash-Heretic-MLX-8bit.json`
- Timestamp: 2026-10-07 16:16:55
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`GLM-4.6V-Flash-Heretic-MLX-8bit`)

## Raw observations

- HumanEval: 14/20
- HumanEval failures: HumanEval/0, HumanEval/1, HumanEval/4, HumanEval/6, HumanEval/10, HumanEval/15
- Agency: 12/15
- Agency failures: list_support_platform, ticket_support_lead, ticket_platform

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 402 | 24.6 |
| expense-tracker | answered | Y | 3635 | 307.2 |
| fake-desktop | truncated | Y | 76848 | 962.4 |
| kanban | answered | Y | 78420 | 912.0 |
| reasoning | truncated | Y | 54890 | 927.0 |

- Throughput: 886 tokens / 20.5 s = 43.2 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.0}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
