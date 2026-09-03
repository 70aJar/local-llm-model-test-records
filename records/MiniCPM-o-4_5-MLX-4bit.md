# Model Scorecard — MiniCPM-o-4.5 (MLX 4-bit)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-03 |
| **Model** | MiniCPM-o-4.5 (omni-modal: text + vision + audio) |
| **Source** | mlx-community MLX 4-bit (`MiniCPM-o-4_5-4bit`) |
| **Quantization** | 4-bit MLX |
| **Size on disk** | 6.0 GB (2 safetensors shards) |
| **Engine** | oMLX (:8002) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 40,960 (oMLX default) |

> Note: the sibling `andrevp/MiniCPM-o-4_5-MLX-4bit` conversion **fails to load** on
> oMLX (`'NoneType' object is not iterable` VLM error — omni-architecture custom
> code not supported by the standard MLX-VLM runtime; oMLX also refuses to execute
> the repo's custom Python for safety). The mlx-community build tested here loads
> clean.

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **15/20** | good but not elite for a coding agent |
| Tasks (5) | **5/5** | adherence ✓ · expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✓ |
| Agency (15) | **6/15** | most failures = tool-name mismatch (below) |
| Throughput | **95.4 tok/s** | standalone — very fast |
| Tool-call | **OK** | schema-compliant, {'a': 37, 'b': 15} |

## Agency — the tool-name mismatch story

The model understands tool *intent* but not the harness's exact schema names.
Every "failed" scenario produced a well-formed tool call with a near-synonym name:

| Expected | MiniCPM called |
|---|---|
| `lookup_employee` | `employee_lookup` |
| `book_room` | `book_meeting_room` (or `book_room`) |
| `convert_currency` | `currency_conversion` |
| `get_tickets` | `support_tickets` |
| `create_ticket` | `create_ticket` ✅ (this one it got) |

Pattern: it reliably calls the correct tool for intent, but freely renames the
function. Scenarios where the expected name matched its convention (`search_directory`,
`create_ticket`) passed cleanly. This is a schema-adherence limitation, not an
agent-loop failure — and it would likely score 13-15/15 with an alias-tolerant
harness or a model-config tool-name map.

## Verbosity — the good news

MiniCPM is the **opposite of the GSQ-Qwen** record: concise by default.

| Task | Output | Time |
|---|---|---|
| adherence | 394 chars | 7 s |
| expense-tracker | 17,751 chars | 64 s |
| fake-desktop | 26,356 chars | 234 s |
| kanban | 33,371 chars | 139 s |
| reasoning | 1,202 chars | 37 s |

Compare: the same 5 tasks on Qwen3.8-27B GSQ took 100K+ chars and 28 min each.
MiniCPM completes all 5 in **8 minutes total** with outputs that are still
functionally complete.

## Verdict

The fastest capable small-local agent we've tested (**95 tok/s**), all 5 build
tasks pass, and it needs tiny memory (6 GB). The trade-offs: HE 15/20 (mid-tier
for a coding agent) and tool-name freedom (alias-tolerant systems will love it,
strict-schema systems will need a name map). For quick, budget agentic work where
verbosity control matters, this is a genuinely useful pick.

---
Harness: `harness/full_test_model.py` · raw JSON in `results/minicpm-o-4_5-4bit.json`.
Compare: [Qwen3.8-27B GSQ-RCO IQ3_S](Qwen3.8-27B-GSQ-RCO-IQ3_S-mtp.md) — the
anti-profile (elite HE, terrible verbosity).