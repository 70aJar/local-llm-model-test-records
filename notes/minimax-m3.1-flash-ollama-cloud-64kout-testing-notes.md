# minimax-m3.1-flash-ollama-cloud-64kout — testing notes

- Source result: `minimax-m3.1-flash-ollama-cloud-64kout.json`
- Timestamp: 2026-10-29 12:45:47
- Sections completed: HumanEval (20), Tasks (5), Agency (15), Throughput, Tool-call
- Incomplete: False
- Thinking: as recorded in the label (`minimax-m3.1-flash-ollama-cloud-64kout`)

## Raw observations

- HumanEval: 19/20
- HumanEval failures: HumanEval/10
- Agency: 13/15
- Agency failures: book_room_b, book_room_a

| Task | answered | code | chars | secs |
|---|---|---|---|---|
| adherence | answered | Y | 429 | 22.5 |
| expense-tracker | answered | Y | 51143 | 254.0 |
| fake-desktop | truncated | N | 0 | 419.9 |
| kanban | answered | Y | 98130 | 580.6 |
| reasoning | answered | Y | 812 | 43.0 |

- Throughput: 4313 tokens / 59.7 s = 72.2 tok/s
- Tool-call: {"emitted": true, "args": {"a": 37, "b": 15}, "secs": 1.1}

## Caveats

- Single run per section; the battery is not repeated, so per-item noise is not averaged out.
- Throughput is one standalone measurement, not a distribution.
- Tasks are scored on emitted code/answer, not on subjective quality.
