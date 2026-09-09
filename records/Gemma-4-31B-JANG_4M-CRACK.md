# Model Scorecard — Gemma-4-31B JANG_4M-CRACK (GGUF quant matrix)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-07 |
| **Model** | Gemma-4-31B (JANG v2 mixed-precision → dequantized → GGUF) + CRACK abliteration |
| **Source** | [douyamv/Gemma-4-31B-JANG_4M-CRACK-GGUF](https://huggingface.co/douyamv/Gemma-4-31B-JANG_4M-CRACK-GGUF) |
| **Quantizations** | Q8_0 (30.4 GB), Q5_K_M (20.4 GB, in-house from Q8), Q4_K_M (17.4 GB) |
| **Engine** | LM Studio (`gemma-4-31b-jang_4m-crack@q8_0` / `@q5_k_m` / `@q4_k_m`) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 128K (`-c 131072`) |

## Results

| Section | Q8_0 | Q5_K_M | Q4_K_M |
|---|---|---|---|
| HumanEval (HE20) | **20/20** | **20/20** | **20/20** |
| Agency (15) | **15/15** | **15/15** | **15/15** |
| Throughput | — | — | — (reasoning-on runs dominate) |
| Tool-call | **OK** (8.8s) | **OK** (10.4s) | **OK** (3.3s) |

## Notes & quirks

- **Thinking is baked in.** Gemma-4 architecture + this conversion has reasoning
  effectively always-on; LM Studio's `enable_thinking` knob is ignored. Runs used
  temp 0.5 (card warns temp=0 with thinking ON increases loop risk).
- **GGUF conversion strips two capability markers:** `vision: False` (no mmproj
  ships with this repo) and "reasoning" not advertised — yet `reasoning_content`
  IS emitted at inference and all three quants score identically perfect on HE.
  Behavior, not cosmetics, is what counts.
- **Q4_K_M = value pick:** identical 15/15 + 20/20 at 57% of Q8's size (17.4 vs
  30.4 GB). Q5_K_M was quantized locally from Q8 (`llama-quantize
  --allow-requantize`) because no mirror existed; it needed an LM Studio full
  restart + settle to index.
- **Vision graft (later work):** copying a gemma-4-31b-it mmproj into the folder
  + clearing `model-index-cache.json` + restart made LM Studio register vision;
  the same graft worked for the QAT (see QAT scorecard / CRACK vision note).
- Despite "CRACK" being an abliteration, all three quants are **fully functional
  on code + tool loops** — no refusal-mode artifacts on the battery.

## Verdict

A perfect-sweep 31B dense: 20/20 HE and 15/15 agency at every quantization level
we tested. The uncensored ("CRACK") variant is the default daily-driver for the
fleet's Hermes agent, beating the safe QAT only on refusal behavior — capability
is identical. Take Q4_K_M for memory-constrained use; Q8_0 only if you want
near-lossless and have the RAM.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/gemma4-31b-jang-crack-q4-agency.json`, `-q4-humaneval.json`,
`-q5-agency.json`, `-q5-humaneval.json`.