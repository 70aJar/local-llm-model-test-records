# Model Scorecard — MiniCPM5-2B (CORRECTED — XML tool protocol)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 |
| **Model** | MiniCPM5-2B (OpenBMB, 2026-09-07) — 2,516,756,480 params, 42 layers, 131K ctx |
| **Key protocol fact** | MiniCPM5 emits **XML-style tool calls** (`harness/minicpm5_toolcheck.py`), NOT OpenAI-JSON `tool_calls` |

## ⚠️ IMPORTANT CORRECTION
An initial verdict of "Agency 2/15, NO tool call at every precision" was WRONG.
Cause: the generic harness (OpenAI-JSON tool_calls parser) is **incompatible with
MiniCPM5's XML tool protocol**. The model answers tool calls as XML
`<function name="..."><param name="...">value</param></function>` (as its chat
template hardwires), which generic JSON parsing never sees.

With the XML-aware checker (`minicpm5_toolcheck.py`): **5/5 tool scenarios matched**
(add 37+15, weather Lahore, convert 100 USD→EUR, book Room B May 12, lookup Jane Smith).
OpenAI tool_calls field = 0 on every one — the model is correct; the parser was blind.

## Results (all three precisions — full battery each)
| Section | BF16 original (5.03GB) | MLX 8-bit (oMLX) | MLX 4-bit (LM Studio) |
|---|---|---|---|
| HumanEval (HE20) | **19/20** | 18/20 | 15/20 |
| Tasks (5) | 3/5 | 4/5 | 3/5 |
| Agency (15) | 2/15 ⚠️ (XML-incompatible harness) | 2/15 ⚠️ | 2/15 ⚠️ |
| Throughput | 84.6 tok/s | 164.5 tok/s | 243.6 tok/s |
| Tool-call (generic) | NO ⚠️ | NO ⚠️ | NO ⚠️ |
| **Tool-call (XML-aware)** | **5/5 MATCH** | — | — |

## Verdict (corrected)
- **MiniCPM5-2B CAN call tools correctly** — 5/5 in its native XML protocol.
- The generic `full_test_model.py` Agency/Tool-call sections are NOT meaningful for
  this model family; use `minicpm5_toolcheck.py` (in harness/) instead.
- SGLang with `--tool-call-parser minicpm5` is the official way to get OpenAI-JSON
  tool_calls from this model (parser merged May 2026; needs SGLang from source until v0.5.13).
- Deployment: works as an edge coder (19/20 HE @ 84.6 t/s BF16); add an XML→JSON
  layer (SGLang parser or local patch) to use it as an agent.

---
Generic battery: `harness/full_test_model.py` · XML checker: `harness/minicpm5_toolcheck.py`
Data: `results/minicpm5-2b-bf16-original-full.json`, `results/minicpm5-2b-toolcheck-xml.json`
