# Testing notes — LFM2.5-2.6B Turbo-Brilliance Power X12 NEO MAX

Companion to `records/LFM2.5-2.6B-Turbo-Brilliance.md`. This file records the **harness setup,
raw observations, and harness-level findings** from the six runs — the detail that makes the
scorecard reproducible and auditable. Everything here is quoted from the run JSONs in `../results/`.

---

## 1. Harness configuration (identical for all six runs)

| Setting | Value |
|---|---|
| Harness | `harness/full_test_model.py` |
| Engine | LM Studio `:1234` (llama.cpp backend), OpenAI-compatible `/v1/chat/completions` |
| Model id sent | `lfm2.5-2.6b-qwen3.8-turbo-brilliance-power-x12-neo-max` |
| Quant | **Q8_0** (~3.12 GB) |
| Context loaded | **131,072** — verified via `/api/v0/models` → `loaded_context_length` |
| Residency | sole resident; no other engine loaded (one-model-at-a-time rule) |
| Host | Apple Silicon M5 Max / 128 GB |
| HumanEval set | `openai/human-eval` canonical `HumanEval.jsonl.gz`, first 20 (`HE_N=20`) |
| Task set | 5 build prompts from `youtube-main/prompts/` |
| Agency set | 15 scenarios, 8 MiniCorp tools incl. the `wiki_search` decoy |
| `REQUEST_TIMEOUT` | 1800 s |
| `HE_MAX_TOKENS` | 16000 (default) |
| `TASK_MAX_TOKENS` | 32000 (default) |

### The six configurations

| Run | `REASON_MODE` | `TEMP` / samplers | Notes |
|---|---|---|---|
| baseline | *(unset)* → model default `high` | 0.2, no top_k/min_p/top_p | **original harness, no unwrapper** |
| default + unwrap | *(unset)* → model default `high` | 0.2 | parser fixed, mode unchanged |
| off | `off` | 0.2 | |
| low | `low` | 0.2 | |
| medium | `medium` | 0.2 | |
| medium + samplers | `medium` | `TEMP=1 TASK_TEMP=1 AGENCY_TEMP=1 TOP_K=64 MIN_P=0.05 TOP_P=0.95` | card's tester set |

### Reproduction

```bash
export HE_PATH=/path/to/HumanEval.jsonl.gz
export TASK_DIR=/path/to/prompts/
export OUT_DIR=./results

# published configuration
MODEL="<engine-model-id>" LOAD_KEY="<engine-model-id>" REASON_MODE=off \
  python3 harness/full_test_model.py "<engine-model-id>" "lfm2.5-off"

# the card's tester samplers, for comparison
MODEL="<engine-model-id>" REASON_MODE=medium TEMP=1 TASK_TEMP=1 AGENCY_TEMP=1 \
  TOP_K=64 MIN_P=0.05 TOP_P=0.95 \
  python3 harness/full_test_model.py "<engine-model-id>" "lfm2.5-medium-samplers"
```

---

## 2. Observation — the output-format trap (root cause of the baseline 0/20)

`HumanEval/0` (`has_close_elements`), raw response, **default mode**:

```
<|tool_call_start|>[stateful_python_code_exec(code='from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    ...
    if len(numbers) < 2:
        return False
    sorted_numbers = sorted(numbers)
    for i in range(len(sorted_numbers) - 1):
        if abs(sorted_numbers[i+1] - sorted_numbers[i]) < threshold:
            return True
    return False')]<|tool_call_end|>
```

Same problem, **`{REASON:off}`**:

````
```python
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    ...
```
````

**The algorithm is correct in both.** Only the wrapper differs. The model is returning a *tool call*
because it was RL-trained inside real agent harnesses — "complete this function" reads to it as an
action to perform, not text to print.

Observed wrapper variants across the matrix:

| Wrapper | Carries usable code? | Unwrapped by the fix? |
|---|---|---|
| `stateful_python_code_exec(code='…')` | ✅ yes | ✅ yes |
| `stateful_python_exec(code='…')` | ✅ yes | ✅ yes |
| `edit(path='…', old_text='…', new_text='…')` | ❌ no — a real edit action | ❌ **deliberately not** |
| bare ```` ```python ```` block | ✅ yes | n/a (normal path) |

Only `code=`-style calls are unwrapped. `edit()` calls are genuine agent actions, not answers, and
must still score FAIL — otherwise the fix becomes a score-inflation bug. A negative-control unit test
covers this.

---

## 3. Observation — HumanEval timings and failure sets

| Run | HE | per-problem secs (min / mean / max) | total | failed items |
|---|---|---|---|---|
| baseline | **0/20** | 5.5 / 15.4 / 36.0 | 309 s | all 20 |
| default + unwrap | **11/20** | 6.1 / 14.6 / 33.9 | 292 s | 1,3,4,5,8,10,11,12,13 |
| **off** | **19/20** | 3.0 / 18.5 / **111.9** | 371 s | 14 |
| low | 15/20 | 2.8 / 8.7 / 49.4 | **175 s** | 0,3,4,5,9 |
| medium | 15/20 | 3.7 / 13.8 / 95.3 | 276 s | 4,7,10,13,15 |
| medium + samplers | 13/20 | 3.4 / 13.7 / 76.0 | 275 s | 0,7,10,12,14,16,19 |

**Failure sets differ between modes** — item 4 fails under four different configurations, but item 0
fails under some and passes under others. The residual misses behave like **sampling variance**, not a
stable capability boundary. Anyone quoting a single-run HumanEval figure for this model should treat
±2 items as noise.

`low` is the fastest configuration (8.7 s mean, 175 s total) *and* still scores 15/20 — the modes
trade wall-clock for no accuracy gain here.

---

## 4. Observation — Agency call sequences (the most stable signal)

| Scenario | baseline | dflt+unwrap | off | low | medium | +samplers |
|---|---|---|---|---|---|---|
| dept_lookup | P | P | P | P | P | P |
| list_active_eng | P | P | P | P | P | P |
| count_eng | P | P | P | P | P | P |
| list_support_platform | P | P | P | P | P | P |
| **book_room_b** | F check_avail | F check_avail | F check_avail | F check_avail | F check_avail | **P book_room** |
| **book_room_a** | F check_avail | F check_avail | **P book_room** | **P book_room** | F check_avail | F check_avail |
| check_room_b | P | P | P | P | P | P |
| ticket_manager | P | P | P | P | P | P |
| **ticket_support_lead** | F | F | F | F | F | F |
| **ticket_platform** | P | P | **F lookup_employee** | **F lookup_employee** | P | P |
| convert_eur_usd | P convert_currency | P | P | P get_exchange_rate | P get_exchange_rate | P get_exchange_rate |
| convert_usd_jpy | P convert_currency | P | P | P get_exchange_rate | P convert_currency | P get_exchange_rate |
| restraint_thanks | P | P | P | P | P | P |
| **restraint_weather** | P | P | P | **F wiki_search** | P | **F wiki_search** |
| focus_team | P | P | P | P | P | P |

Three distinct behaviours worth recording:

1. **`ticket_support_lead` fails in all six runs** — it emits `lookup_employee` where the scenario
   wants `search_directory` → `create_ticket`. This is a *stable* model limitation, not configuration
   noise, and it is the one miss that no setting fixes.
2. **`book_room` is the classic family trait** — the model calls `check_availability` and then stops,
   never issuing the booking mutation. The same failure appears across the 35B-A3B family
   (Ornith / Tiel both 13/15 for this reason). Which of the two booking scenarios it solves flips with
   the mode; it never solves both.
3. **`wiki_search` over-calling is introduced by configuration, not present by default.** The
   `restraint_weather` scenario ("what's the weather forecast for London tomorrow?") has **no valid
   tool** — the correct behaviour is to make **no call**. Runs `low` and `medium + samplers` call the
   decoy `wiki_search`; the `off` / `medium` / default runs correctly abstain. The tester sampler set
   therefore *costs* one agency point rather than buying any.

### Reading the agency total correctly

Agency is **12/15** under `off`, `medium` and the model default — i.e. it is **configuration-invariant**.
Only `low` drops to 11/15, and only via the `wiki_search` over-call above. For a 2.6B model this is a
notably robust tool-loop score.

---

## 5. Observation — Tasks and throughput

| Task | baseline | off | low | medium | +samplers |
|---|---|---|---|---|---|
| adherence | ✓ 479 ch / 19 s | ✓ 418 / 17 | ✓ 558 / 11 | ✓ 478 / 14 | ✓ 524 / 15 |
| expense-tracker | ✗ 3781 / 25 | ✗ 4974 / 19 | ✗ 3244 / 17 | ✗ 4773 / 20 | ✓ 5019 / 27 |
| fake-desktop | ✗ 1043 / 26 | ✓ 23259 / 88 | ✗ 2482 / 34 | ✗ 1155 / 17 | ✗ 999 / 22 |
| kanban | ✓ 37801 / 216 | ✓ 28880 / 111 | ✗ 1715 / 38 | ✗ 5528 / 32 | ✗ 1375 / 43 |
| reasoning | ✓ 7306 / 117 | ✓ 4448 / 79 | ✓ 819 / 52 | ✓ 2882 / 49 | ✓ 6335 / 87 |

- The **task passes are not monotonic in output length** — `kanban` passes at 37,801 chars (baseline)
  *and* at 28,880 (off) but fails at 1,715 (low). Short answers are not the failure mode here.
- `{REASON:off}` produces the **longest and most complete** build outputs (23–29K chars), which is why
  its throughput figure is the lowest while its task score is the highest.

| Run | completion tokens | prompt tokens | secs | tok/s |
|---|---|---|---|---|
| baseline | 1923 | 203 | 18.9 | **101.9** |
| default + unwrap | — | — | — | 97.5 |
| off | 1265 | — | 15.3 | 82.5 |
| low | 923 | — | 11.1 | 83.0 |
| medium | 495 | — | 4.7 | **104.3** |
| medium + samplers | 1441 | — | 14.6 | 98.8 |

⚠️ **Throughput is measured on a fixed prompt and is confounded by answer length**, not engine speed.
The card quotes **220 tok/s on M5 Max** for the *stock LiquidAI* model; this is a re-tune under
LM Studio with thinking always on. Treat ~83–104 tok/s as a floor.

---

## 6. Harness findings (changes made to `harness/full_test_model.py`)

1. **Added `code=` tool-call unwrapping in `extract_code()`** — see §2. Guarded so `edit()`/`write()`
   style calls are *not* unwrapped.
2. **Added `REASON_MODE`** — prepends `{REASON:<mode>}` to the last user message. Necessary because a
   DavidAU Turbo-Brilliance model **defaults to `high` reasoning / `medium` instruct**, so an untagged
   request is not a neutral baseline.
3. **Added `TEMP`** — applies to sections that pass no explicit temperature (HumanEval, throughput,
   tool-call). Default 0.2 preserves comparability with older records.
4. **Added `TOP_K` / `MIN_P` / `TOP_P` / `REP_PEN`** — the card's tester set had no way to be expressed.
5. **Sanitized path defaults** — `HE_PATH`, `TASK_DIR`, `OUT_DIR`, `LMS_BIN` no longer carry
   machine-specific absolute defaults; they resolve to relative paths / `PATH` and are overridden by
   env vars as before.

All additions are **env-gated with unchanged defaults**, so previously recorded results stay comparable.

---

## 7. Caveats — what would change these numbers

- **Throughput is length-confounded** (§5) — do not read it as engine speed or compare across modes.
- **The model always thinks.** The card states LFM2.5 is "a pure reasoning model that always thinks
  before it answers — it adds a `<think>` tag directly in the chat template." `enable_thinking:false`
  and `reasoning_effort:low` are ignored **by design**; any harness expecting a thinking-off mode will
  silently get reasoning tokens (~85–92% of completion in default mode).
- **Tool-call protocol differs from OpenAI JSON.** LFM2.5 emits Pythonic calls by default; JSON only
  when the system prompt asks for it. LM Studio translated here, so `tool_calls` parsed cleanly — but a
  JSON-only harness should not be trusted to judge this family unaided.
- **Single-run residuals are noisy.** ±2 HumanEval items between runs of the same configuration is
  within observed variance (§3).
- **One sample size per cell.** Each configuration was run once. The agency column is stable enough to
  trust at 12/15; the HumanEval column is not stable enough to split hairs over 13 vs 15.
- **Do not generalise the mode finding.** At 2.6B the Turbo-Brilliance modes cost accuracy
  (`off 19 > low 15 = medium 15 > high 11`), but the author's card states the system scales with
  parameter count ("9B, 27B => will be a LOT stronger"). This file says nothing about the method at
  larger sizes.
