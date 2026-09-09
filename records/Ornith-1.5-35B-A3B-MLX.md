# Model Scorecard — Ornith-1.5-35B-A3B-MLX (fp16)

| Field | Value |
|---|---|
| **Date tested** | 2026-09-08 |
| **Model** | Ornith-1.5-35B-A3B (official MLX, fp16) |
| **Source** | [ornith-ai/Ornith-1.5-35B-A3B-MLX](https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B-MLX) |
| **Quantization** | bf16/fp16 (14 shards, ~65 GB) |
| **Engine** | oMLX (`Ornith-1.5-35B-A3B-MLX`, engine=batched) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | default (262K capable) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | perfect — real run, wire-confirmed model |
| Agency (15) | **13/15** | `book_room_a`/`book_room_b` only (availability check, no booking call) |
| Throughput | **56-59 tg tok/s** | ~2,300-2,800 pp tok/s (oMLX single-request bench) |
| Tool-call | **OK** | tool loops emitted (Agency scenarios) |

## Agency failures — what actually happened

Same family as other 35B-A3B models: `book_room` scenarios call
`check_availability` but never follow through with the booking mutation.
Read-only tool calls succeed; state-changing booking action gets dropped —
looks like action-hesitation, not schema issues (the plain `check_room_b`
scenario passed).

## Notes & quirks

- **MoE speed at 35B size:** 56-59 tok/s generation with only 3B active params —
  fp16 density is fine on the M5 Max (65-66 GB peak) because only experts run.
  This is what makes a full-precision 35B practical as a daily coding model.
- **Official SWE-bench lineage** (from the model card): SWE-bench Verified 79,
  Pro 59.6, TermBench 67.8 — the strongest coding-family claim of any model on
  this roster; our HE 20/20 is consistent with that.
- **Harness lesson:** the model id must be explicit — an early run fell back to a
  different resident oMLX model because the harness defaulted the id; oMLX logs
  (`Chat completion: model=...`) were used to verify the real target. Fixed and
  documented in the harness (MODEL env now honored).
- A3B MoE reasoning + tools + vision-capable (mmproj available separately).

## Verdict

The strongest coding-family model we've tested: MoE speed, fp16 fidelity,
20/20 HE. The 13/15 agency (no booking follow-through) is the same minor
pattern across the family. If you want a big-model coding lane that stays fast
and precise, this is the pick — and the 4-bit oQ4e MTP sibling (22 GB) is the
memory-lean alternative.

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
Data: `results/ornith-1.5-mlx-fp16.json`, `results/ornith-1.5-mlx-fp16-he.json`.