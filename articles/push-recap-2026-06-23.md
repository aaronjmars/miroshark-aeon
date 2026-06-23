# Push Recap — 2026-06-23

## Verdict
> SHIPPING — `cost` CLI lands; deprecated mimo-v2-flash default swapped to mimo-v2.5

**Shape:** 3 user-visible commits · 1 internal · 0 infra · 0 bot-filtered (strict 24h window; 4 dependabot PRs merged ~27h ago, outside window)
**Volume:** 55 files changed, +620/−1219 lines across 4 signal commits by 1 author
**Merged PRs:** 4 (#205 code-quality cleanup; #206 branding/tagline; #207 model default swap; #208 cost CLI)

---

## Top impact today
1. `6cf32a8` — code-quality cleanup across backend and frontend. 680 lines of dead code and duplicated per-channel notification scaffolding removed; two new leaf modules (`simulation_run_state.py`, `_notify_base.py`) replace inline type definitions and copy-pasted dedup logic scattered across 5 notify services. (36 files, +484/−1164)
2. `cef787b` — add `cost` CLI subcommand surfacing per-run USD estimate. New `cmd_cost()` in `cli.py` calls `/api/simulation/<id>/cost.json` and formats `~$X.XXXX (tokens, LLM calls)` with a per-phase breakdown; `~` prefix mirrors the EmbedView pill to signal lower-bound. (4 files, +81/−1)
3. `ec707cd` — switch default model from mimo-v2-flash to mimo-v2.5. `config.py` default and the Cloud preset in `settings.py` updated; `run_summary.py` pricing table corrected to mimo-v2.5 rates ($0.14/$0.28 per M). (18 files, +37/−36)

---

## aaronjmars/MiroShark

### The "$1 claim" is now scriptable

**What this is:** MiroShark's cost transparency stack — the `/cost.json` endpoint (#179) and EmbedView pill (#190) — now has a CLI entry point. Any automation pipeline or integrator can verify the "$1 to simulate anything" claim without opening a browser.

**Shipped to users**
- `cef787b` — feat(cli): add cost subcommand surfacing per-run USD estimate
  - `backend/cli.py`: +34 new `cmd_cost()` function calls the existing `/api/simulation/<id>/cost.json` endpoint. Exits with code 2 when cost isn't available yet (run still in progress), code 1 on auth/server errors. `--json` flag emits the raw payload for scripting. A `~` prefix on the printed figure matches the EmbedView pill and signals the lower-bound nature of the estimate (models absent from the price table count as $0).
  - `docs/CLI.md`: +20 adds the command to the reference table and a `Cost` section with a full example showing per-phase breakdown (`graph_build`, `simulation`, `report`).
  - `docs/CLI.zh-CN.md`: +18 Chinese mirror of the same docs.

### First-run model fix and brand refresh

**What this is:** Two connected changes landed together. The `xiaomi/mimo-v2-flash` slug OpenRouter deprecated (full delisting June 30) is replaced everywhere; separately, the "Universal Swarm Intelligence Engine" label is retired in favor of the shorter, speed-led tagline already used in READMEs.

**Shipped to users**
- `ec707cd` — chore(models): switch default model from mimo-v2-flash to mimo-v2.5
  - `backend/app/config.py`: `LLM_MODEL_NAME` default changed from `xiaomi/mimo-v2-flash` to `xiaomi/mimo-v2.5`. Also updates the `WONDERWALL_MODEL_NAME` cloud preset comment.
  - `backend/app/api/settings.py`: the in-app Cloud preset's `LLM_MODEL_NAME` and `WONDERWALL_MODEL_NAME` fields updated so the Settings UI one-click preset also stops 404ing.
  - `backend/app/utils/run_summary.py`: pricing table row corrected — mimo-v2.5 costs $0.14/$0.28 per M tokens (was $0.10/$0.40 for mimo-v2-flash), so the cost.json estimates now reflect real OpenRouter pricing.
  - `.env.example`, `railway.env.example`, `cloudrun.env.yaml.example`, and the 4 README variants: updated to mimo-v2.5 for consistent clean-install experience.

- `fc69fb4` — chore(branding): adopt new tagline and point OpenRouter attribution at miroshark.xyz
  - `frontend/src/views/Home.vue`: hero chip changed from "Universal Swarm Intelligence Engine" to "Your first result in under 10 minutes" — replaces the category descriptor with a speed promise.
  - `backend/app/utils/llm_client.py` and `embedding_service.py`: `HTTP-Referer` header updated from `github.com/aaronjmars/MiroShark` to `https://www.miroshark.xyz/`; `X-OpenRouter-Title` now reads "Simulate anything, for $1 & less than 10 min." — OpenRouter attribution now routes to the product domain instead of the repo.
  - `backend/openapi.yaml`: API summary line updated to match new tagline.

### Internal: backend consolidation

**What this is:** 8-agent audit drove a structural cleanup: dead code removed, notification services DRYed, type annotations fixed. No behavior change.

**Under the hood**
- `6cf32a8` — refactor: code-quality cleanup across backend and frontend. Key reductions: `simulation_ipc.py` −106 lines (SimulationIPCServer removed, confirmed zero callers); `graph_builder.py` −165 lines (build_graph_async and _build_graph_worker removed, async build path was dead); `simulation_runner.py` −359 lines (fan-out notification dispatch collapsed into `_fan_out_notifications`, IPC scaffolding removed). New `_notify_base.py` (+82) provides shared Dedup + `post_json` used by all 4 notification channels — previously each channel duplicated identical dedup logic. New `simulation_run_state.py` (+184) extracts `RunnerStatus`, `AgentAction`, `RoundSummary`, `SimulationRunState` from scattered TYPE_CHECKING imports. Frontend: 6 unused axios wrappers in `api/simulation.js` removed (−61), `toggleLocale` removed (−9), orphaned entity-card CSS removed (−41).

---

## aaronjmars/miroshark-aeon

All 16 commits in window are scheduler/cron state bookkeeping (`chore(cron)`, `chore(scheduler)`) — automated agent telemetry, no signal.

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** Default model slug changed (`xiaomi/mimo-v2-flash` → `xiaomi/mimo-v2.5`). Self-hosters with no explicit `LLM_MODEL_NAME` in `.env` automatically switch to mimo-v2.5 after pulling main. Pricing changes slightly ($0.10 input → $0.14; $0.40 output → $0.28 per M tokens).
- **New public surface:** `python backend/cli.py cost <sim_id>` — new CLI subcommand. Exit codes: 0 ok, 1 error, 2 cost not yet available. `--json` flag for machine-readable output.
- **Tech debt added:** none (PR #205 explicitly left two pre-existing bugs for maintainer decision: `Project.chunk_size` 3-way default mismatch, `repro_export` director-events filename)

## Open threads
- tomer-liran's PR #204 (migrate deprecated mimo-v2-flash → mimo-v2.5, 18 files, opened Jun 22) — now superseded by #207 which landed the same fix. PR #204 is still open/unmerged; likely to be closed as redundant.
- PR #203 (thinking-token budget) was closed unmerged — engine-frozen streak on `simulation_runner`/`simulation_manager` continues; the #205 refactor touched `simulation_runner.py` for cleanup but added no simulation logic.

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (automation chore only)
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 4 (dependabot PRs #199/#200/#201/#202, merged ~27h before window)
- diff-truncated: 0
