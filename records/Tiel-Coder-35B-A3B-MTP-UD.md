# Model Scorecard — Tiel-Coder-35B-A3B-MTP-UD (Q4_K_XL)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-08 |
| **Model** | Tiel-Coder-35B-A3B-MTP-UD (Ornith-1.5 base, Sharp template, MTP head) |
| **Source** | [peculiar-ragdoll/Tiel-Coder-35B-A3B-MTP-GGUF](https://huggingface.co/peculiar-ragdoll/Tiel-Coder-35B-A3B-MTP-GGUF) |
| **Quantization** | UD-Q4_K_XL (22.5 GiB) + BF16 mmproj |
| **Engine** | LM Studio (`tiel-coder-35b-a3b-mtp-ud`, qwen35moe) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 262K (capable; tested at 131K) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **19/20** | one problem failed |
| Tasks (5) | **4/5** | expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · adherence ✓ (grader fix) · reasoning ✗ |
| Agency (15) | **13/15** | `book_room_a`/`book_room_b` (availability check, no booking call) |
| Throughput | **57.4 tok/s** | 1,293 tok in 22.5s |
| Tool-call | **OK** | schema-compliant {'a': 37, 'b': 15} |

## Notes & quirks

- **MTP / speculative decoding** head included — the UD (unsloth-dynamic) Q4_K_XL
  variant loads with the draft model in LM Studio (`--speculative-draft-mtp` usable).
- **Agentic coding focus** (model card): SWE-bench-Live 12/25 = Opus 4.6 medium,
  best-in-class multi-turn Claw-Eval 67.2. Our HE 19/20 + Tool OK is consistent
  with a strong coder; Tasks 3/5 with verbose outputs (~120K chars on
  fake-desktop/kanban) shows the same verbosity pressure as other 35B-A3B family.
- **MCP + vision smoke-tested**: `hub_repo_search` via HuggingFace ephemeral MCP
  returned live trending data; native `/v1/responses` tool call emitted clean
  `get_current_weather` arguments; mmproj present (visual inputs accepted).
- **Verbosity**: kanban/fake-desktop tasks ran ~120-130K chars each — bounded
  output prompts or max_tokens caps recommended for build-tool use.
- Same `book_room` drop pattern as the rest of the 35B-A3B family (Ornith-1.5):
  read-only tools succeed, state-changing booking action dropped.

## Verdict

The "agentic coding" pick of the 35B-A3B family: HE 19/20, real MCP integration
verified, MTP spec-decode available, vision adapter included. Slightly below
CRACK/QAT 31B on our toy battery (19 vs 20/20; 13 vs 15/15 agency) — but the
SWE-bench-Live 12/25 claim targets actual repo fixes, a harder scale than HE.
If you want a fast local coder with MTP + tooling, this is the one.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/tiel-coder-35b-a3b-mtp-ud.json`, `results/tiel-coder-35b-a3b-mtp-ud-full.json`.