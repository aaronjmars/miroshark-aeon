# Push Recap — 2026-04-30

## Overview

Three substantive commits across both repos in the 2026-04-29 15:17 UTC → 2026-04-30 15:16 UTC window. MiroShark closed the four-format share-anywhere arc with **PR #60 RSS / Atom feeds** (the fourth orthogonal projection of the same on-disk sim folder), and shipped **PR #59 Wonderwall per-slot endpoint override + Cloud preset refresh** late yesterday — operators can now point the simulation loop at any OpenAI-compatible endpoint (self-hosted vLLM / Modal / Ollama) without touching the Default/Smart/NER slots, and the previous Best (Claude-tier) preset was dropped because the new Mimo V2 Flash + Grok-4.1 Fast Cloud lineup hits the same ~$1/run budget. miroshark-aeon merged **PR #27**, an explicit `date -u +%A/%u/%d` Step 0 in the heartbeat skill so the daily report stops hallucinating the weekday from `${today}`.

**Stats:** 35 substantive files changed, +2,001 / −276 lines across 3 substantive commits (excluding ~30 cron / per-skill auto-commits on miroshark-aeon).

---

## aaronjmars/MiroShark

### Theme 1: Discovery loop closes — RSS / Atom feeds (PR #60)

**Summary:** Atom 1.0 + RSS 2.0 syndication of the public simulation gallery, served as a fourth share/discovery surface alongside the existing share card (PR #42, Apr 22), replay GIF (PR #50, Apr 28), and Markdown/JSON transcript (PR #57, Apr 29) — same on-disk sim folder, four orthogonal projections of `_build_gallery_card_payload`. Pure stdlib (`xml.etree.ElementTree` + `html`); zero new dependencies, zero new infrastructure, zero ongoing maintenance.

**Commits:**

- `91e22e4` — feat: RSS / Atom feeds for the public simulation gallery (#60) (merged 2026-04-30 13:12 UTC by @aaronjmars; co-authored by aeonframework). +1,604 / −1, 13 files.
  - **NEW** `backend/app/services/feed.py` (+584): Atom 1.0 + RSS 2.0 renderer + `select_public_cards()` selection helper. Per-entry payload — scenario as title (100-char `…` truncation), bullish / neutral / bearish consensus split as plain summary, share-card PNG as `<media:thumbnail>` + `<media:content>`, replay GIF as second `<media:content>` (motion-capable surfaces auto-play), `verified-{label}` + `quality-{label}` as `<category>` so subscribers can filter on outcome and quality. RSS variant adds `<enclosure type="image/png">` for podcatcher-style readers and `<guid isPermaLink="false">` for stable identification across deployments. Same ±0.2 stance threshold as gallery / share card / replay GIF / transcript / webhook — five surfaces, one threshold, one folder.
  - **NEW** `backend/app/api/feed.py` (+144): `feed_bp` blueprint mounted at `/api`. `_resolve_base_url()` honors `Config.PUBLIC_BASE_URL` first (the same operator-supplied canonical URL the webhook + share-card use), falls back to `request.host_url` with `X-Forwarded-Proto` / `X-Forwarded-Host` for reverse-proxy deployments. `_serve_feed()` shared body for both routes — local-imports `_build_gallery_card_payload` + `_read_outcome_file` from `simulation.py` so the selection stays single-sourced with `GET /api/simulation/public`. Fail-soft against `SimulationManager` errors → empty feed. `Cache-Control: public, max-age=300` (5-minute CDN-friendly).
  - **NEW** `backend/tests/test_unit_feed.py` (+566): 17 offline tests covering Atom + RSS validity, share-link + media enclosures (PNG + GIF), summary stance-split + quality + agents, 100-char title truncation with `…`, outcome + quality categorisation, empty-feed handling, missing-optional-fields → "(untitled scenario)", self-link query string preservation (`?verified=1` round-trips), skips entries with empty `simulation_id`, RSS guid stability, RSS PNG enclosure, dispatcher MIME (`render_feed("atom"|"rss")` returns correct content type, falls back to Atom on garbage input), verified-only branch flips title + alternate link to `/verified`, selection helper filter+sort+limit+graceful-degradation, source-side route-presence guard alongside the openapi drift test.
  - `backend/openapi.yaml` (+64): both endpoints under Publish & Embed tag with `application/atom+xml` and `application/rss+xml` response schemas + `verified` query param.
  - `backend/tests/test_unit_openapi.py` (+1): `feed_bp: /api` added to `_BLUEPRINT_PREFIXES` so the drift-detection test passes on first run — the contract enforces itself, same beat as PR #45 OpenAPI and PR #44 MCP.
  - `backend/app/__init__.py` (+6 / −1) + `backend/app/api/__init__.py` (+2): blueprint registration boilerplate.
  - `frontend/index.html` (+5): `<link rel="alternate" type="application/atom+xml">` + RSS variant for browser auto-discovery (the address-bar globe icon).
  - `frontend/src/api/simulation.js` (+25): `getFeedUrl({ format='atom', verified=false, origin })` helper.
  - `frontend/src/views/ExploreView.vue` (+37): "📡 Subscribe via RSS" chip in the stats row that mirrors the active filter (verified-only when on); muted-text styling so it reads as a passive subscription action, not a content filter.
  - `frontend/src/components/EmbedDialog.vue` (+150): "Follow the gallery via RSS" callout below the gallery callout, with three one-click subscribe buttons (Atom feed filled, RSS 2.0 outline, Verified-only outline).
  - `README.md` (+1) + `docs/FEATURES.md` (+19): feature row + Public Gallery Feeds section.

**Impact:** Converts the pull surface (a researcher / DeFi analyst manually checking `/explore`) into a push channel — every newly published simulation lands in subscribers' Feedly / Readwise / Inoreader / NetNewsWire / Obsidian RSS the same way an AI newsletter or Substack post does. The four-format share-anywhere arc is now complete: preview PNG (Twitter / X / Discord / Slack / LinkedIn unfurls) + animated GIF (Discord / Slack auto-play) + Markdown / JSON (Notion / Obsidian / Substack / SDK pipelines) + Atom / RSS (research RSS readers). Repo-actions Apr 28 idea **#3**, picked because all data sat on disk, zero external API dependency, zero ongoing maintenance, and it compounds with every newly published sim without any operator curation.

---

### Theme 2: Cost line item gets an operator escape valve — Wonderwall per-slot endpoint override + Cloud preset refresh (PR #59)

**Summary:** Wonderwall is the simulation loop's #1 cost driver (850+ LLM calls per run). PR #59 adds two new env vars — `WONDERWALL_BASE_URL` and `WONDERWALL_API_KEY` — so the simulation loop can target any OpenAI-compatible endpoint (self-hosted vLLM, Modal, fine-tunes, Ollama on a different host) without affecting the Default / Smart / NER slots. Both fields fall back to `LLM_*` when blank, so existing setups keep working without any change. Same PR refreshes the cloud preset and **drops the Best (Claude-tier) preset entirely** because the new Mimo V2 Flash + Grok-4.1 Fast Cloud lineup hits the same ~$1/run budget.

**Commits:**

- `2e782e0` — feat(wonderwall): per-slot endpoint override + cloud preset refresh (#59) (merged 2026-04-29 20:27 UTC by @aaronjmars; co-authored by Claude Opus 4.7 1M context). +267 / −266, 16 files.
  - `backend/app/config.py` (+11 / −7): new `WONDERWALL_API_KEY` + `WONDERWALL_BASE_URL` `os.environ.get` reads next to the existing `WONDERWALL_MODEL_NAME`. Comment notes "Wonderwall is the #1 cost driver — 850+ calls per run. Keep it cheap." `LLM_MODEL_NAME` default flips from `qwen/qwen3.5-flash-02-23` to `xiaomi/mimo-v2-flash`. Cheap-preset / Best-preset reference comments rewritten to single Cloud-preset commentary.
  - `backend/scripts/run_parallel_simulation.py` + `run_reddit_simulation.py` + `run_twitter_simulation.py` (+26 / −18 across 3 files): each subprocess startup now reads `os.environ.get("WONDERWALL_API_KEY", "") or os.environ.get("LLM_API_KEY", "")` (same pattern for `BASE_URL` / `MODEL_NAME`) so all three simulator entry points respect the per-slot override.
  - `backend/app/services/simulation_runner.py` (+10): the Flask process side. After Settings UI mutates `Config.WONDERWALL_*`, those values aren't in `os.environ` — so this PR forwards each non-empty `Config.WONDERWALL_*` into the subprocess `env` dict at `start_simulation()` spawn time. Settings UI updates apply on the next run without a Flask restart.
  - `backend/app/api/settings.py` (+14 / −27): preset blueprints rewritten. The **`best`** preset (Claude Haiku personas + Claude Sonnet reports + Gemini NER, ~$3.50/run) is **deleted entirely**. The `cheap` preset is renamed Cloud (`Cloud — ~$1/run (Mimo V2 Flash + Grok-4.1 Fast)`) — Default + Wonderwall now both pin to `xiaomi/mimo-v2-flash`, Smart pins to `x-ai/grok-4.1-fast`, NER stays on `x-ai/grok-4.1-fast`. New body fields: `wonderwall: { base_url, model_name, api_key }` (was just `model_name`); `_current_snapshot()` exposes Wonderwall `base_url` + masked `api_key_masked` + boolean `has_api_key`. Update body fields downgrade `preset: "cheap" | "best" | "local"` to `preset: "cheap" | "local"`.
  - `frontend/src/components/SettingsPanel.vue` (+31 / −7) + `frontend/src/api/settings.js` (+2 / −2): new base_url + api_key inputs alongside Model in the Wonderwall section, with the existing key-masking convention applied (saved key shown as placeholder).
  - `frontend/src/views/Home.vue` (+1 / −1): drop the "Best preset" mention from any chip / hover text.
  - `.env.example` (+91 / −136): the dominant churn — the previous Cheap / Best / Local three-block layout collapses to Cloud / Local. New defaults active in the file (operator-friendly: drop into a fresh `.env` and you're on the new Cloud preset out of the box).
  - `docs/INSTALL.md` (+20 / −33), `docs/MODELS.md` (+23 / −24), `docs/CONFIGURATION.md` (+9 / −5), `docs/FEATURES.md` (+19), `README.md` (+6 / −3): cloud-as-default phrasing throughout, new "Custom endpoint" subsection in MODELS.md documenting the per-slot fallback, slot-fallback note + commented example block in CONFIGURATION.md, FEATURES.md gets a new section, README adds a feature row + quick-start update.
  - `backend/app/utils/run_summary.py` (+4 / −3): minor drift — likely just preset-label text or a list of recognised presets dropping `best`.

**Impact:** Two complementary wins. (1) The model menu collapses from three presets to two — the Best preset existed for users who wanted Claude reports but spent ~$3.50/run; with the new Cloud lineup at the same ~$1/run budget the Claude tier was redundant for most users. The default landing experience now starts at the cost the GitHub tagline promises ($1 & under 10 min). (2) The Wonderwall slot becomes operator-controlled: anyone with a self-hosted vLLM, Modal, fine-tune, or remote Ollama can point the simulation loop at it without disturbing the Default / Smart / NER slots — useful for research operators with their own models, cost-sensitive operators with cached / volume-discounted endpoints, and anyone testing a fine-tuned persona model in-loop. Mirrors the existing webhook + share-card pattern: `Config.PUBLIC_BASE_URL` + per-slot `*_BASE_URL` fields are the sanctioned operator-supplied URL fields.

---

## aaronjmars/miroshark-aeon

### Theme 3: Heartbeat day-of-week accuracy (PR #27)

**Summary:** The Apr 29 heartbeat report opened with `Date: Tuesday Apr 29, 2026` when Apr 29 was actually **Wednesday**. The LLM hallucinated the weekday from the YYYY-MM-DD `${today}` value, then listed `memory-flush (Sun+Wed)` under "Not scheduled today (Tuesday)" and re-classified its on-schedule 18:25 UTC run as "ran off-schedule on-demand". Apr 25 / 26 / 27 / 28 reports all had the right weekday, so this is intermittent — but the failure mode is hallucination from a YYYY-MM-DD string, which means it can recur on any day, and would silently mask a real "memory-flush failed to fire on Wed" outage if one ever happened.

**Commits:**

- `f5ff617` — improve(heartbeat): compute day-of-week from shell, not inference (#27) (merged 2026-04-30 14:47 UTC; co-authored by aeonframework + Claude Opus 4.7). +130 / −9, 6 files (+20 substantive on `skills/heartbeat/SKILL.md`; rest is a self-improve auto-commit + log entry + memory pointer + token-usage CSV row + dashboard JSON).
  - `skills/heartbeat/SKILL.md` (+20): adds an explicit **Step 0** before any schedule check that runs `date -u +%A`, `+%u`, `+%d` and uses those shell-computed values as the source of truth in every "is this skill scheduled today?" comparison. Anchors the report header on the shell output (`Date: <%A> <Mon DD>, <YYYY> — <HH:MM> UTC`). Adds an explicit cron-translation note: cron weekday `0=Sun` while `+%u` returns `7=Sun` — silently off-by-one. Adds ground-truth guidance for every-other-day cron expressions: when in doubt, check the last 7 days of `cron-state.json` `last_dispatch` history rather than guessing odd/even-day parity.
  - `dashboard/outputs/self-improve-2026-04-30T13-42-01Z.json` (+91): the json-render dashboard payload for the self-improve run.
  - `memory/logs/2026-04-30.md` + `.outputs/self-improve.md` + `memory/MEMORY.md` + `memory/token-usage.csv`: routine self-improve bookkeeping.

**Impact:** Closes a subtle hallucination class — the model was reasoning about the calendar from a date string rather than asking the shell. The fix is small (≤20 lines on a single skill file) but covers a failure mode that would have silently masked a real missed run. Surfaces a useful pattern for any other skill that does day-of-week scheduling in plain English: shell out for the canonical answer rather than letting the LLM compute it.

---

## Developer Notes

- **No new dependencies.** PR #60 is pure stdlib (`xml.etree.ElementTree` + `html`); PR #59 only adds two `os.environ.get` calls and a settings-route field; PR #27 only edits a SKILL.md.
- **Breaking change in PR #59:** the `best` preset is removed from the public preset list. Any external script POSTing `{"preset": "best"}` to `/api/settings` will get a `400` after this PR. The migration path is `cheap` (now relabeled Cloud, ~$1/run); operators wanting the Claude tier set the slots manually. Default `LLM_MODEL_NAME` env-var value flipped from `qwen/qwen3.5-flash-02-23` to `xiaomi/mimo-v2-flash` for fresh installs — existing `.env` files with an explicit `LLM_MODEL_NAME` are unaffected.
- **Architecture shift in PR #59:** `simulation_runner.py:start_simulation()` now reads `Config.WONDERWALL_*` and forwards non-empty values into the subprocess `env`. The pattern is general — any future per-slot override that the Settings UI mutates at runtime should follow this same `for _attr in (...)` loop in `simulation_runner.py` so it doesn't require a Flask restart.
- **Tech debt:** none introduced. The PR #60 selection helper (`select_public_cards`) was extracted explicitly *to* be unit-testable without booting Flask — a small refactor that paid for itself in 17 tests.

## What's Next

- **From repo-actions Apr 28 (still unbuilt):** Langfuse Cost Breakdown Panel (#1), Scenario Template Library (#4), Comparative Run View (#5). Apr 28 idea #2 (transcript) shipped Apr 29 (PR #57); idea #3 (RSS feed) shipped today (PR #60). Two of five built; three remain.
- **From repo-actions Apr 30 (filed today, unbuilt):** Historical Simulation Mode (Feature, Small) — date-anchor + historical templates capitalising on the Apr 29 WWII talkie demo viral moment; LLM-as-Judge Audit Panel (Feature, Small); Batch Rerun / Reproducibility Badge (Feature, Medium); Belief Trajectory CSV / JSONL Export (Integration, Small) — fifth export surface; Spectator Watch Page (Growth, Small) — `/watch/:id` minimal live viewer.
- **Operational thread:** PR #59's per-slot endpoint override is the unannounced enabler for any fine-tuned-persona experiments. If the simulation loop is ever pointed at a custom Mimo / Qwen / Llama fine-tune, this is the configuration surface that makes it possible.
- **No open PRs on either repo at the time of this recap.**
