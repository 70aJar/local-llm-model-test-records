# qwen38-flash-next-Q2-lmstudio — testing notes

- Source result: `qwen38-flash-next-Q2-lmstudio.json`
- Timestamp: 2026-10-17 05:40:35
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`qwen38-flash-next-Q2-lmstudio`)

## Raw observations

- HumanEval: 20/20
- Agency: 15/15

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 340 | 61.4 |
| expense-tracker | truncated | Y | 138147 | 725.5 |
| fake-desktop | truncated | Y | 130420 | 791.6 |
| kanban | answered | Y | 10753 | 815.6 |
| reasoning | answered | Y | 1735 | 145.9 |

- Throughput: 2172 tokens / 56.9 s = 38.2 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 2.5}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
