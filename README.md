# Local LLM Model Test Records

A living, reproducible record of local LLM tests. Every model we evaluate gets a
scorecard in `records/`, produced by the same battery and harness, so results are
comparable across models and over time. Add a model any time — no personal
information, no synthetic benchmarks, just real work.

## The battery (same for every model)

| Section | What it measures | Scale |
|---|---|---|
| **HumanEval** | Python code correctness (20 canonical problems) | 0-20 |
| **Tasks** | Real build tasks (adherence, expense-tracker, fake-desktop, kanban, reasoning) | 0-5 |
| **Agency** | Tool-calling scenarios — does the model follow the system/agent loop? | 0-15 |
| **Throughput** | Answer tokens/sec (standalone) | tok/s |
| **Tool-call** | Native tool-call/schema compliance | pass/fail |

Every model runs: **one engine at a time, standalone**, prompt-compatible harness
from `harness/`, thinking on/off per model card. Host: Apple Silicon M5 Max / 128 GB.

## Layout

```
├── README.md                → this file (methodology + index)
├── MODEL_SCORECARD.md.template
├── harness/
│   ├── full_test_model.py   → HE20 + Tasks5 + Agency15 + throughput + toolcall
│   ├── real_task_harness.py → 4 real-work tasks (invoice, grounded QA, summary, email)
│   └── requirements.txt
└── records/
    ├── Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md
    └── ...                   → one scorecard per tested model
```

## Datasets (all public)

| Dataset | Where | Used by |
|---|---|---|
| HumanEval (canonical gzip) | `openai/human-eval` on GitHub/HF | `full_test_model.py` → `HE_PATH` |
| 5 build-task prompts | `youtube-main/prompts/` (public repo) | `full_test_model.py` → `TASK_DIR` |

Point the harness at them with env vars, e.g.:
```bash
HE_PATH="/path/to/HumanEval.jsonl.gz" TASK_DIR="/path/to/prompts/" \
python3 harness/full_test_model.py "<engine-model-id>" "<label>"
```

## How to add a model

1. Load the model in the engine you're testing (LM Studio / oMLX / Ollama).
2. Run the battery:
   ```bash
   LM_API="http://127.0.0.1:1234/v1/chat/completions" \
   HE_N=20 python3 harness/full_test_model.py "<engine-model-id>" "<label>"
   ```
3. Copy `MODEL_SCORECARD.md.template` → `records/<label>.md`, fill from the
   printed scorecard, add the results JSON from `benchmarks/results/`.
4. Add a row to the index table and open a PR.

## Index

| Date | Model | Engine | HE | Tasks | Agency | tok/s | Tool-call | Record |
|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | Qwen3.8-27B GSQ-RCO IQ3_S-mtp (3.50 bpw) | LM Studio | 20/20 | 5/5 | 13/15 | 19.4 | ✅ | [records/Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md](records/Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md) |

---
*Every result is measured, wire-collected, and reproducible. If a row looks wrong,
open an issue — the harness is in this repo.*