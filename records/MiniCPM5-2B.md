# Model Scorecard — MiniCPM5-2B (CORRECTED — XML tool protocol, FULL QUANT MATRIX)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-10 |
| **Model** | MiniCPM5-2B (OpenBMB, 2026-09-07) — 2,516,756,480 params, 42 layers, 131K ctx |
| **Key protocol fact** | MiniCPM5 emits **XML-style tool calls** (`harness/minicpm5_toolcheck.py`), NOT OpenAI-JSON `tool_calls`. Generic JSON-only harnesses UNDER-REPORT this family. |

## ⚠️ IMPORTANT CORRECTION (2026-09-10)
Initial verdict "Agency 2/15, NO tool call at every precision" was **WRONG — a testing fault**.
The generic harness parses only OpenAI-JSON `tool_calls`; MiniCPM5 answers with XML
`<function name="..."><param ...>...</function>` (per its chat_template.jinja), so the
generic parser reported nothing. XML-aware checkers in harness/ (`minicpm5_toolcheck.py`,
`minicpm5_agency_check.py`) prove the model calls tools correctly.

## Full quant matrix (XML-aware methods)

| Quant | HE20 | Tasks5 | Agency15 (XML) | Tool-call (XML) | tok/s |
|---|---|---|---|---|---|
| **BF16 original** (openbmb 5.03GB) | **19/20** | 3/5 | **13/15** | **5/5** | 84.6 |
| **MLX 8-bit** (abenzerps 2.5GB) | 18/20 | 4/5 | **12/15** | **5/5** | 164.5 |
| **MLX 4-bit** (openbmb 1.3GB) | 15/20 | 3/5 | **12/15** | **5/5** | 243.6 |

- **Tool-calling = perfect at every quantization (5/5)**: add/weather/convert/book/lookup
  all emitted as correct XML calls.
- **Agency = 12-13/15 with XML-aware parsing** (was 2/15 with JSON-blind harness). Real
  misses are model judgment: "book room" scenarios sometimes choose check_availability;
  one assign-ticket scenario chose lookup_employee first.
- HE scales with precision (15→19/20); agency/tool are quant-stable.

## Verdict
- MiniCPM5-2B is a genuinely capable agent for a 2.5B — tool-calling flawless, agency
  strong — but you MUST understand its XML protocol (SGLang `--tool-call-parser minicpm5`
  official, or the harness scripts here) before judging it.
- 5/5 XML tool calls at every quant: 4-bit (1.3GB @ 243.6 t/s) is the pragmatic pick for
  edge/agent work.
- SGLang parser needed for full OpenAI-JSON integration (merged May 2026; source build
  until v0.5.13).

---
Generic battery: `harness/full_test_model.py` · XML tool: `harness/minicpm5_toolcheck.py` ·
XML agency: `harness/minicpm5_agency_check.py`
Data: `results/minicpm5-2b-{bf16,8bit,4bit}-{agency,toolcheck}-xml.json` + `*-full.json`
