# Gemma-4-31B-it-QAT-Uncensored-Heretic-MLX-LM-4Bit (ailexleon)

| Field | Result |
|---|---|
| HE (20) | **20/20** |
| Tasks (5) | **5/5** (adherence ✓, expense-tracker ✓ 19.9KB, fake-desktop ✓ 19.2KB, kanban ✓ 25.7KB, reasoning ✓) |
| Agency (15) | **15/15** (all pass incl restraint + room-booking pair) |
| Throughput | 17.1 tok/s (battery) / 22.4-22.8 tok/s (live short-gen) |
| Tool-call | ✅ OK {"a": 37, "b": 15} |
| Engine | oMLX :8002 (MLX 4-bit) |
| Size | 17.3GB (4 shards) resident ~16.4-16.9GB |
| Date | 2026-09-11 |

## Notes
- MLX 4-bit beats the GGUF QAT 31B baseline (17.6-18.8 tok/s) on speed (~22.5 t/s short-gen).
- Same HE 20/20 + Agency 15/15 as google/gemma-4-31b-qat GGUF.
- Uncensored Heretic lineage (JANG tweaks applied by ailexleon).
- Tasks all code=Y at default 32K budget; reasoning 2,079 chars (succinct).
- Set as default local agentic model for Hermes local profile (oMLX served).
