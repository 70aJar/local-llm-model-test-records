# Model Scorecard — gemma4-coding-agent (S4MPL3BI4S E4B Instruct, Q4_K_M)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-08 |
| **Model** | Gemma 4 E4B Instruct (7.5B, gemma4 arch) |
| **Source** | S4MPL3BI4S/gemma4-coding-agent (`gemma-4-E4B-it.Q4_K_M.gguf`) |
| **Quantization** | Q4_K_M (5.34 GiB) |
| **Engine** | LM Studio on Desktop (UBHOME-PC, RTX 5060) via LM Link |
| **Host** | Desktop i9 + RTX 5060 Ti 16GB (compute only) |
| **Context loaded** | 131K (`-c 131072`) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | one problem failed |
| Tasks (5) | **4/5** | expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✓ · adherence ✗ |
| Agency (15) | **15/15 PERFECT** | no tool-loop drops — best small-model agency score on the roster |
| Throughput | **77.8 tok/s** | on RTX 5060 GPU |
| Tool-call | **OK** | schema-compliant {'a': 37, 'b': 15} |

## Notes & quirks

- **Agency 15/15 at 7.5B** — beats the 35B-A3B family (Ornith/Tiel 13/15) and ties the
  31B CRACK/QAT on tool discipline. Strongest value-per-byte tool-loop model tested.
- **MCP + tooling smoke-tested**: `hub_repo_search` via HuggingFace ephemeral MCP
  returned live trending data (Spark-X2.5-4B top); `/v1/responses` emitted clean
  `get_current_weather` args. No reasoning field emitted (lean E4B, fast answers).
- Runs on the **Desktop GPU node** shared via LM Link — 5.3GB means it loads in
  seconds and leaves the rest of VRAM free.
- Tasks outputs were concise (not verbose like the 35B family): max 44K chars kanban.

## Verdict

The surprise of the batch: a 7.5B E4B that's **perfect on agentic tool loops**
(15/15) at 5.3GB and 77.8 tok/s on the Desktop's RTX 5060. For lightweight
agentic/tool work where speed and discipline matter more than raw knowledge, it
outperforms models 4-5× its size. Keep it as the fleet's fast agentic worker.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/gemma4-coding-agent-full.json`.