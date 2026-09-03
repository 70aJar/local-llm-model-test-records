# Model Scorecard — Qwen3.8-27B GSQ-RCO IQ3_S-mtp

| Field | Value |
|---|---|
| **Date tested** | 2026-09-03 |
| **Model** | Qwen3.8-27B (GSQ-RCO non-uniform quantization) |
| **Source** | [ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF](https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF) |
| **Quantization** | IQ3_S (3.50 bpw whole-file average) + MTP head |
| **Size on disk** | 11.3 GiB (+ 0.9 GB BF16 mmproj) |
| **Engine** | LM Studio (`qwen3.8-27b-gsq-rco`, type=vlm) |
| **Host** | Apple Silicon M5 Max / 128 GB (compute only) |
| **Context loaded** | 32K (`-c 32768`) |

## Results

| Section | Score | Details |
|---|---|---|
| HumanEval (HE20) | **20/20** | perfect — the "task-lossless" claim holds on code |
| Tasks (5) | **5/5** | adherence ✓ · expense-tracker ✓ · fake-desktop ✓ · kanban ✓ · reasoning ✓ |
| Agency (15) | **13/15** | failures: `book_room_a`, `book_room_b` (booking tool-call pattern); analyzed below |
| Throughput | **19.4 tok/s** | standalone |
| Tool-call | **OK** | schema-compliant, {'a': 37, 'b': 15} |

## Agency failures — what actually happened

Both failures are the same scenario family: asking to *book* a room. The model
calls `check_availability` correctly but does **not** follow through with the
booking mutation call (it passed the plain `check_room_b` scenario, not the
`book_room_a/b` actions). Pattern: reads-only tool calls succeed; state-changing
book actions get dropped. This looks like a safety-hesitation tendency at 3.5 bpw,
not a tool-schema problem (all calls were well-formed).

## The elephant in the room — verbosity

This quant is **extremely verbose** on build tasks. The real-world Tasks section
produced >100,000 characters per build task:

| Task | Output | Time | Tokens ≈ |
|---|---|---|---|
| adherence | 389 chars | 181 s | ~150 |
| expense-tracker | 111,242 chars | 1,688 s | ~25,000 |
| fake-desktop | 110,014 chars | 1,668 s | ~25,000 |
| kanban | 117,970 chars | 1,679 s | ~28,000 |
| reasoning | 2,831 chars | 451 s | ~700 |

Each build task generated a ~30K-token stream at ~15 tok/s — roughly **28 minutes
per task** — before the harness's 32K cap cut it off. The code inside those streams
is correct, but the model cannot be concise. Practices that need bounded, terse
output (CLI tools, codegen with strict `max_tokens`, chat) will need output caps
or a lower verbosity prompt.

## Verdict

For a 12 GB model: **exceptional quality per byte** — HE 20/20 is elite and
15/15→13/15 agency is strong. The GSQ/RCO non-uniform quantization genuinely
preserves task capability at 3.50 bpw where uniform quantizations usually degrade.
But the verbosity profile makes it impractical for interactive tool use without a
hard output budget. If you need a small-memory Qwen3.8-27B for batch or capped
output, this is the pick. For interactive agentic work, prefer the Q8 family
(heretic/obliterated/ud at 29-33 tok/s, 4/4 real tasks).

---
Harness: `harness/full_test_model.py` (HE20+Tasks5+Agency15+throughput+toolcall)
and `harness/real_task_harness.py` (4 real-work tasks). Full raw JSON in
`results/gsq-rco-iq3-s-mtp.json`.