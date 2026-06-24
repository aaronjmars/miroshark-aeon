# Push Recap — 2026-06-24

## Verdict
> SHIPPING — wait subcommand and thinking-model robustness ship; automation pipeline complete

**Shape:** 5 user-visible commits · 2 internal · 0 infra · ~40 bot-filtered (aeon scheduler/cron auto-commits)
**Volume:** 19 files changed, +308/−25 lines across 5 product commits by 2 authors (aaronjmars, dan-and) on aaronjmars/MiroShark
**Merged PRs:** 7 (#208 cost CLI, #209 thinking-model robustness, #210 blank-model fallback, #211 graph fan-out fix, #215 wait CLI — MiroShark; #74 XAI prefetch fix, #75 xai=skip observability — miroshark-aeon)

---

## Top impact today

1. `7a9dffa` — fix(llm): thinking model robustness — budget, JSON repair, None guards (#209). Nine-file hardening pass across the full inference pipeline: `llm_client.py` now pads `max_tokens` by `THINKING_BUDGET_TOKENS` so `<think>` blocks don't eat the response budget, strips unclosed `<think>` blocks, and returns `None` on empty content so callers' retry logic fires instead of crashing on `json.loads("")`; `json_repair.py` strips invalid backslash escapes (Windows paths, LaTeX) that break JSON parsing after think-block stripping; six call sites get `repair_truncated=True`; `run_parallel_simulation.py` passes the combined token budget to CAMEL's `ModelFactory`. (+97/−21, 9 files)
2. `959aef8` — feat(cli): add wait subcommand to block until a simulation finishes (#215). `cmd_wait` polls `/api/simulation/<id>/run-status` on a monotonic deadline, exits 0 on `completed`, 1 on `failed`/`stopped`, 2 on timeout; progress prints to stderr so stdout stays clean for `--json` piping; transient poll errors warn and keep going rather than treating a 5xx as a failed sim. Kills integrators' hand-rolled `while not done: sleep` loops — `python cli.py wait "$SIM" && python cli.py report "$SIM"` now works. (+69/−0 cli.py, 4 files total)
3. `cef787b` — feat(cli): add cost subcommand surfacing per-run USD estimate (#208). Surfaces `/api/simulation/<id>/cost.json` at the CLI so the "$1 to simulate anything" claim is checkable from a script, not only the EmbedView pill — closes the automation gap between "sim finished" and "how much did it cost". (+34/−0 cli.py, 4 files)

---

## aaronjmars/MiroShark

### CLI automation pipeline — cost + wait complete the loop

**What this is:** Two new `cli.py` subcommands shipped in the same 24h window that together make `list → wait → report`/`cost` a fully scriptable, one-liner pipeline. Before: `cost` existed in the API and embed widget but not the terminal; `wait` didn't exist at all, so any script that needed to act after a run finished had to hand-roll its own poll loop.

**Shipped to users**
- `cef787b` — feat(cli): add cost subcommand surfacing per-run USD estimate (#208)
  - `backend/cli.py`: `cmd_cost` calls `/api/simulation/<id>/cost.json` via `_api`, prints estimate with `~$` prefix when `is_estimate=true` (mirrors the embed pill's caveat), exits 2 when no cost is recorded yet (+34/−0)
  - `docs/CLI.md` / `docs/CLI.zh-CN.md`: new `cost` row in command table + usage section (+38/−0)
  - `backend/tests/test_unit_cli.py`: registry assertion + `test_cost_parses_positional` (+9/−1)
- `959aef8` — feat(cli): add wait subcommand to block until a simulation finishes (#215)
  - `backend/cli.py`: `cmd_wait` with `--interval` (default 5s) + `--timeout` (default 600s), monotonic deadline, transient-error retry, clean exit codes 0/1/2 (+69/−0)
  - `docs/CLI.md`: new `wait` table entry + full "Wait" section with bash pipeline example (+19/−0)
  - `docs/CLI.zh-CN.md`: bilingual equivalent (+18/−0)
  - `backend/tests/test_unit_cli.py`: `test_wait_defaults_and_overrides` covering default floats + override parse (+15/−1)

### Thinking-model compatibility — full-pipeline hardening

**What this is:** External contributor dan-and (Daniel Andersen) threaded `THINKING_BUDGET_TOKENS` support and `<think>`-block safety through nine files in a single PR, making the engine functional with reasoning models like DeepSeek, Qwen3, and MiniMax M2.5 that previously could silently produce empty responses or truncated JSON when their thinking budget overflowed the `max_tokens` ceiling.

**Shipped to users**
- `7a9dffa` — fix(llm): thinking model robustness — budget, JSON repair, None guards (#209)
  - `backend/app/utils/llm_client.py`: adds `_thinking_budget` from `THINKING_BUDGET_TOKENS`; every `chat()` call uses `effective_max_tokens = max_tokens + _thinking_budget`; strips unclosed `<think>` blocks via `re.sub(r'<think>[\s\S]*$', '', content)`; returns `None` on empty post-strip content (+18/−2)
  - `backend/app/config.py`: new `THINKING_BUDGET_TOKENS` env var (int, default 0, no-op for non-thinking models); `validate()` emits a warning when `THINKING_BUDGET_TOKENS > 0` and `LLM_DISABLE_REASONING=true` conflict (+16/−0)
  - `backend/app/utils/json_repair.py`: `re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)` fixes invalid escape sequences (Windows paths like `C:\Users`, LaTeX `\f`) that broke parsing after think-block stripping (+6/−0)
  - `backend/app/services/graph_tools.py`: `repair_truncated=True` on `_generate_sub_queries` + new plain-text fallback (numbered/bulleted list → regex extraction) when JSON parse fails; `repair_truncated=True` on `_generate_interview_questions` (+33/−17)
  - `backend/app/services/simulation_config_generator.py` + `wonderwall_profile_generator.py`: guard `if content is None: continue` before `json.loads()` so thinking-model empty responses retry instead of crash (+5/−0 each)
  - `backend/app/storage/contradiction_detector.py` + `ner_extractor.py`: `repair_truncated=True` on `chat_json()` calls (+1/−0 each)
  - `backend/scripts/run_parallel_simulation.py`: passes `max_tokens = 4096 + thinking_budget` to CAMEL `ModelFactory.create()` via `model_config_dict` so the CAMEL agent also gets enough headroom (+12/−2)
- `9097055` — fix(graph): restore semantic default fan-out in sub-query fallback (#211)
  - `backend/app/services/graph_tools.py`: #209's total-failure fallback returned `[query]` — a single item, collapsing the panorama search fan-out that previously explored four semantic facets (participants, causes, development process). This restores the richer 4-way default when even the plain-text fallback fails, so PanoramaSearch still explores multiple facets under LLM outage (+8/−1)

**Under the hood**
- `35206d5` — fix(config): fall back to default when LLM_MODEL_NAME is blank (#210): `config.py` `LLM_MODEL_NAME` uses `or` so a present-but-empty env var (`LLM_MODEL_NAME=`) resolves to `xiaomi/mimo-v2.5` instead of sending an empty model name that 400s. Spotted by tomer-liran (#204).

---

## aaronjmars/miroshark-aeon

### Internal: Agent observability — XAI prefetch and skip/quiet split

**What this is:** Two self-improve PRs closed a monitoring blind spot in the token-report skill: the `xai=skip` footer flag was overloaded to mean both "prefetch ran fine, token is just quiet" and "prefetch never ran / key unset," making it impossible to tell whether a fix (#74) had taken effect after merge.

**Under the hood**
- `b74f038` — fix(token-report): prefetch X sentiment so Social Pulse stops silently skipping (#74): adds a `token-report)` case to `scripts/prefetch-xai.sh` that derives the tracked token from `memory/MEMORY.md` and writes `.xai-cache/token-report-social.json` before Claude starts (outside the sandbox, full env). Mirrors the tweet-digest prefetch pattern (#67). (+21/−0 prefetch-xai.sh, +15/−2 SKILL.md)
- `df3bb56` — fix(token-report): split xai=skip into quiet vs skip (#75): `skills/token-report/SKILL.md` distinguishes `xai=quiet` (cache present, <2 qualifying tweets — token is genuinely quiet) from `xai=skip` (cache missing / key unset — prefetch broken). Evidence: 5 consecutive `xai=skip` days (06-20→06-24) with no way to tell success from failure after #74 merged. (+24/−7 SKILL.md)

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none — `THINKING_BUDGET_TOKENS` defaults to 0 (no behavior change for existing installs); `wait`/`cost` are additive CLI subcommands
- **New public surface:** `wait <sim_id> [--interval N] [--timeout N]` CLI subcommand (exit codes 0/1/2); `cost <sim_id>` CLI subcommand (added yesterday, docs now bilingual); `THINKING_BUDGET_TOKENS` env var in config
- **Tech debt added:** none — #211 actually closed a regression introduced by #209's total-failure fallback

## Open threads
- aaronjmars/MiroShark: PRs #212, #213, #214 (all dan-and, opened 2026-06-23) open as of last heartbeat — likely more robustness/LLM-compatibility work in the same vein as #209
- tomer-liran's PR #204 (rename mimo-v2-flash → mimo-v2.5 across 18 files/37 occurrences) still unmerged; the blank-env fallback (#210) is a partial fix that doesn't close the slug rename PR

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (automation chore auto-commits bot-filtered)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: ~40 (aeonframework chore/scheduler/cron auto-commits)
- diff-truncated: 0
