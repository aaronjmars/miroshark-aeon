# Push Recap — 2026-04-22

## Overview

Twenty-four substantive commits from two authors (Aaron Mars, Aeon), spanning a day that read less like a single feature drop and more like a project-grade tightening pass: the Social Share Card landed in production, the settings/onboarding surface was rebuilt from the model list down to the README hero, the simulation runner got the four reliability fixes that have been outstanding since pause/resume shipped, and the eight-branch cleanup sweep finally merged into `main`. Aeon shipped one infra fix on miroshark-aeon — PR #22 closes a three-day silent-fail in the daily token report's social-pulse step. Most of the visible-to-users work happened in a tight 21:07–22:52 UTC window on 2026-04-21 as the model-routing surface and README were refactored together.

**Stats:** ~150 files changed, +8,645/-3,726 lines across 24 substantive commits (plus ~28 auto-chore commits on miroshark-aeon).

---

## aaronjmars/MiroShark

### Theme 1: Social Share Card Lands (PR #42)

**Summary:** A 1200×630 PNG generator that auto-unfurls a simulation's scenario, status, quality, and bullish/neutral/bearish split when the share link is pasted into Twitter/X, Discord, Slack, LinkedIn, or any Open-Graph-aware client. Closes the gap between MiroShark's existing share permalinks (which produced a generic preview) and what a researcher actually wants to drop into a post.

**Commits:**
- `9d71291` — feat: social share card (Open Graph image + landing page) (#42)
  - New `backend/app/services/share_card.py` (+501 lines): Pillow renderer for the 1200×630 PNG. Deterministic, takes the embed-summary dict, renders dark header band + scenario headline (3-line wrap with auto-shrink + ellipsis), status/quality/resolution/consensus pills, three-column metric row (Agents / Rounds / Net Bull-Bear), stacked bullish/neutral/bearish bar with legend, dark footer with repo URL + creation date. Falls back through DejaVu/Helvetica/Arial/PIL bitmap default — never 500s on missing font. Pillow already pinned ≥12.0 via `tool.uv.override-dependencies` so **zero new dependencies**.
  - New `backend/app/api/share.py` (+181 lines) + `share_bp` blueprint: `GET /share/<id>` server-rendered HTML carrying `og:image` / `og:title` / `twitter:card=summary_large_image` / `twitter:image` meta tags. Inline JS `window.location.replace()` redirect for browsers + `<meta http-equiv="refresh">` fallback. Honors `X-Forwarded-Proto`/`X-Forwarded-Host`. Private sims render the page but omit scenario from meta tags. Mounted at root (no `/api/` prefix) so the URL stays clean.
  - Refactor in `backend/app/api/simulation.py` (+199/-136): extracted `_build_embed_summary_payload()` so embed-summary endpoint and share-card endpoint share one source of truth.
  - New `GET /api/simulation/<id>/share-card.png` endpoint with same `is_public` gate as embed-summary; on-disk cache at `<sim_dir>/share-cards/<sha256-16>.png` keyed by render-affecting fields; `Cache-Control: public, max-age=3600`; `Content-Disposition: inline; filename=miroshark-<sim_id[:12]>.png`.
  - `frontend/src/api/simulation.js` (+37): `getShareCardUrl()` + `getShareLandingUrl()` helpers.
  - `frontend/src/components/EmbedDialog.vue` (+202/-1): "Social card" section — preview `<img>` (cache-busted on public toggle flip + dialog reopen), copyable share-link snippet, copyable card-image-URL snippet, "Download PNG" button. Disabled state when sim is private.
  - New `backend/tests/test_unit_share_card.py` (+252): 11 unit tests — PNG signature + IHDR size, cache-key stable across calls + sensitive to render-affecting fields + insensitive to peripheral fields, edge cases (empty, 600-char, single-word, failed status, minimal payload), OG meta-tag rendering with quote escaping, private-sim leak check.
  - Docs: README features table row + new "Social Share Card" section in `docs/FEATURES.md`.
  - CI: pillow added to `.github/workflows/tests.yml` for the share-card unit tests.

**Impact:** Single most aligned shipped feature with the 1K-stars-by-Apr-30 target. Every share link from this point forward becomes a marketing surface; the EmbedDialog upgrade puts that surface in the user's hands during the sim's existing share flow rather than asking them to discover a new path.

---

### Theme 2: Onboarding Rebuilt — Settings Presets, Cheap Preset, LLM URL Fetcher

**Summary:** Two paired commits at 22:05 and 22:52 UTC rewired both *what* models the project recommends and *how* users select them. The Cheap preset moved off vintage Llama/Mistral defaults to Qwen3.5-flash / DeepSeek-v3.2 / Grok-4.1-fast (with `:online` for web search) and disabled CoT by default for ~3× lower latency on the chat-routed models. The Settings modal got a Current Setup readout, a preset dropdown (Cheap/Best/Local), and advanced per-slot overrides — surfacing every model slot the backend already had (LLM, Smart, NER, Wonderwall, Embedding, Web Search) and applying presets server-side instead of forcing users to hand-edit `.env`. The brittle HTML parser in url-import was replaced with an LLM-based fetcher routed through the Web Search slot.

**Commits:**

- `db6af41` — feat: new Cheap preset (Qwen/DeepSeek/Grok) + disable CoT by default
  - `backend/app/utils/llm_client.py` (+6): LLMClient injects `reasoning:{enabled:false}` into OpenRouter `extra_body`; gated by new `LLM_DISABLE_REASONING` config (default true). Benchmarked ~3× lower latency on qwen3.5-flash and grok-4.1-fast.
  - `backend/app/config.py` (+15/-7), `.env.example` (+10/-9), `backend/app/api/settings.py` (+7/-7), `docs/INSTALL.md` (+14/-12), `docs/MODELS.md` (+18/-14), `docs/CONFIGURATION.md` (+17/-8), `README.md` (+1/-1): Cheap preset rewritten to qwen/qwen3.5-flash-02-23 (default+wonderwall), deepseek/deepseek-v3.2 (smart), x-ai/grok-4.1-fast (ner), x-ai/grok-4.1-fast:online (web search), openai/text-embedding-3-large @ 768 dims.
  - `backend/app/utils/run_summary.py` (+6/-1): pricing table extended with real OpenRouter rates for the new models so future run summaries compute cost correctly.
  - `backend/app/utils/url_fetcher.py` (+6/-4): docstring updated; `WEB_SEARCH_MODEL` now requires an `:online`-capable variant since non-browsing models reject URLs past training cutoff.
  - `frontend/src/components/ScenarioSuggestions.vue` (+8/-1): set `loading=true` the moment a fetch is queued (was deferred until after the debounce window) so the spinner tracks user intent; race-guard preserved.
  - `frontend/src/views/Home.vue` (+12/-4): hard-cap displayed doc title at 70 chars and URL at 72 chars so long titles/paths can't widen the doc-list row.
  - `docs/MODELS.md`: recorded real observed latency + cost numbers from a 359-call end-to-end run (~$0.50 total with web enrichment).

- `13dbce2` — feat: settings presets, richer Just Ask briefings, LLM URL fetcher, landing refresh
  - `frontend/src/components/SettingsPanel.vue` (+343/-42): Current Setup readout, preset dropdown (Cheap/Best/Local), advanced per-slot overrides for every model slot.
  - `backend/app/api/settings.py` (+190/-53): GET/POST now surfaces every model slot (LLM, Smart, NER, Wonderwall, Embedding, Web Search) and applies presets server-side.
  - `backend/app/utils/url_fetcher.py` (+88/-142): brittle HTML parser replaced with LLM-based fetcher routed through `WEB_SEARCH_MODEL` (Gemini `:online` via OpenRouter). SSRF host/IP validation preserved. Cap extracted title at 120 chars so long bylines don't bleed into the UI.
  - `backend/app/api/simulation.py` (+59/-17): inject today's date into the user prompt for `/suggest-scenarios` so deadlines anchor on now instead of model training cutoff; thread the user's simulation prompt through to `/suggest-scenarios`. Rewrote the Ask system prompt to require 15-25 specifically named actors (executives, VCs, journalists, analysts, regulators, critics) across stances and geographies so personas seed a richer simulation.
  - `frontend/src/views/Home.vue` (+186/-25): clicking an uploaded/fetched/generated doc opens a preview modal with the full extracted text. Ask-generated briefings render under Just Ask; URL-fetched docs render under URL Import. Hero tag/title/description and left-panel workflow now mirror the README wording and cost framing.
  - `frontend/src/api/settings.js` (+16/-4), `frontend/src/components/ScenarioSuggestions.vue` (+5/-1): wiring + loading-state tweak.

- `cf60136` — feat: route prediction-market title generation to the Smart slot
  - `backend/app/services/simulation_config_generator.py` (+7/-2): tiny but load-bearing change — `_generate_prediction_markets` now goes through `create_smart_llm_client()` so `SMART_MODEL_NAME` (Claude Sonnet in the Best preset) produces sharp, time-bound, resolvable questions instead of generic ones from the cheaper Default model. Falls back to the default client transparently when `SMART_MODEL_NAME` is unset. Market titles frame the whole simulation, so the routing matters.

**Impact:** Removes the "fork-the-.env" friction that's been the project's longest-standing first-run barrier. The Cheap preset's CoT-off + new model lineup is now consistent with the public "$1 & under 10 min" tagline (see Theme 4). The LLM-based URL fetcher means dropping in a paywalled or JS-heavy article URL works where the regex parser silently failed.

---

### Theme 3: Simulation Runner Hardening + What If? Bug Fixes

**Summary:** Targets the symptoms flagged in the session kickoff (sims stop too early, pause loses state, branches don't work, UI round counter is wrong, What If? returns empty for most agents). One commit hardens the runner end-to-end; a sibling commit fixes a Python falsy-zero trap + namespace mismatch that made the Recompute button silently yield `counterfactual=null` for most agent selections. Together they close the reliability gap between the simulator and the analytics overlays it feeds.

**Commits:**

- `2fd2532` — fix: harden simulation runner, wire counterfactual branches, preserve belief state across pause/resume
  - `backend/scripts/run_parallel_simulation.py` (+199/-27): counterfactual injection now actually called — `counterfactual_loader` has existed since forever but was never imported anywhere, so branch sims silently ran as plain forks. Wired into all four loops (Twitter, Reddit, Polymarket, synchronized multi-platform); fires exactly once at `round == trigger_round` via the existing director-event injector. Per-round error isolation: `asyncio.wait_for` + try/except wrap `env.step`, `fetch_actions`, and `belief_tracker.after_round` so a single bad round no longer escalates to an unhandled exception → subprocess exit ≠ 0 → the sim being marked FAILED halfway through. New `MIROSHARK_ROUND_TIMEOUT` env var (default 600s) bounds round duration so a hung LLM call can't freeze the run indefinitely.
  - `backend/scripts/belief_integration.py` (+171/-4): `BeliefTracker` persists per-agent `BeliefState` to `belief_states_<platform>.json` after each `after_round()` call and reloads them on `__init__`. Resumed sims keep their accumulated stance instead of snapping back to profile defaults.
  - `backend/scripts/agent_guidelines.py` (+61, new): `inject_posting_rules_into_graph()` follows the same marker-replace idiom as `inject_director_event_context` — injected once at each simulation setup point, idempotent, coexists with per-round injections. First rule wired in: never use hashtags.
  - `backend/app/services/simulation_runner.py` (+16/-2): UI round counter keeps up with the subprocess by handling `round_start` events from `actions.jsonl`, so the counter advances when a round begins rather than waiting until it completes.

- `2f08f76` — fix: What If? counterfactual returning empty when agent_id is 0 or display name ≠ handle
  - `backend/app/api/simulation.py` (+385/-44): two compounding bugs in `/counterfactual` and `/demographics`. (1) Classic Python falsy-zero trap: `uid = p.get('user_id') or p.get('agent_id') or p.get('id')` — when `user_id` is `0` (legitimate id, but falsy), `or` short-circuits to `None` and agent 0 is silently dropped from the name → id map. (2) Namespace mismatch: the influence leaderboard surfaces the profile's display `name` field ("Mallku"), while the counterfactual endpoint built its lookup keyed by `user_name` / `username` first (the handle, "mallku_519"). Incoming display names never resolved, `excluded_ids` stayed empty, counterfactual came back null. Fix: index every profile under all three name fields via `setdefault` (display wins) and replace the `or` chain with an explicit-`None` check via `next(...)`. Same fix applied to `/demographics` where the identical pattern was silently misattributing influence scores and platform affiliations. Live-tested on an existing sim.

**Impact:** Counterfactual Explorer (PR #37, shipped Apr 19) and Director Mode branches (PR #31, Apr 16) both go from "works in demo, fails in production" to "works." Pause/resume becomes the legitimate workflow it was advertised as. The runner now isolates failures rather than escalating them — the difference between "round 7 had a bad LLM response" and "the whole sim died at round 7."

---

### Theme 4: README & Docs Rewrite — Slim Landing + `docs/` Reference

**Summary:** A 12-commit cluster (21:07–21:32 UTC) that turned the monolithic 698-line README into a 243-line landing page with a 5-line OpenRouter + `./miroshark` quick start, then split everything else into nine separate docs. The hero now leads with cost framing ("$1 & under 10 min"), branches install into A.1 OpenRouter / A.2 OpenAI / A.3 Anthropic so users with existing keys skip OpenRouter entirely, swaps Docker-for-Neo4j recommendation for native install, and adds Windows path and named use cases (market reaction, advertisement, life decision, what-if history). A separate commit (`32f95d5`) added the README pass over previously undocumented features (director mode, preset templates, article generation, interaction network, demographics, quality diagnostics, history database, trace interview, PWA push) plus a grouped HTTP API reference for the ~65 live endpoints.

**Commits:**

- `cbbf155` — docs: compact README + lead with OpenRouter + ./miroshark easy start (`README.md` +243/-698): replaces the long-form README with the compact version. Promotes OpenRouter + `./miroshark` to prominent default. Four alternative runtimes (Cloud deploy, Docker+Ollama, Manual+Ollama, Claude Code) sit in collapsed `<details>` blocks.
- `ea1e799` — docs: split README into slim landing page + full docs/ reference
  - 9 new docs: `docs/INSTALL.md` (+256), `docs/CONFIGURATION.md` (+162), `docs/ARCHITECTURE.md` (+125), `docs/API.md` (+120), `docs/FEATURES.md` (+117), `docs/MODELS.md` (+77), `docs/OBSERVABILITY.md` (+57), `docs/MCP.md` (+54), `docs/CLI.md` (+31).
  - `CONTRIBUTING.md` (+28) at repo root.
  - `README.md` (+71/-443): becomes the landing surface only.
- `32f95d5` — docs: document director mode, templates, analytics, push, and full API (`README.md` +198/-12): pass over `backend/app/api` and `frontend/src` to surface shipped-but-undocumented features; grouped HTTP API reference for ~65 endpoints; fixes Ollama model tags that didn't exist in the registry (qwen3.5:27b → qwen2.5:32b / qwen3:30b-a3b).
- `b7256fb` — docs: add OpenAI and Anthropic direct-API install paths + side-by-side diagrams (+99/-20): Option A branches into A.1 OpenRouter / A.2 OpenAI / A.3 Anthropic. Anthropic path flags the embeddings caveat (no native embeddings → Ollama or OpenAI key) and notes prompt caching pays off on the ReACT loop. Two architecture diagrams shrink into a side-by-side 2-column table under Screenshots.
- `a02e04f` — docs: swap Docker-for-Neo4j recommendation for native install, add use cases (+34/-18): native install (brew/apt) leads, Aura mentioned for zero-install cloud option, Docker preserved only for Option B. New use cases: market reaction, advertisement, life decision, what-if history.
- `53e497f` — docs: tighten quick-start claims, drop free-credit mention, add Windows Neo4j path: removes "no GPU, no Ollama, no model downloads" filler; first-sim estimate 15-25 min → ~10 min (matches Cheap preset); drops "free" before OpenRouter (paid-per-use); Windows: Neo4j Desktop (native) or WSL2 (recommended).
- `d65fbac` — docs: update tagline to "$1 & under 10 min" value prop.
- Cosmetic README pass (8 small commits, 21:23–21:25 UTC): `4d64801` bullet points for "What it does", `2d17b3d` move overview image above Features, `3e89bfc` move architecture diagrams from hero into Screenshots, `b7d46da` narrative rewrite of "What it does", `bec3dc4` sharper hero description, `3753770` restore overview + architecture images lost in slim swap, `32bca58` drop Credits and How-it-works sections, `a02e04f` use cases.

**Impact:** First-run friction collapses. A new contributor lands on the README, sees `OPENROUTER_API_KEY=...` + `./miroshark`, and is in a sim. The deeper material is one click away in `docs/` for the people who need it. The "$1 & under 10 min" frame is the project's first concrete cost claim and ties cleanly to the new Cheap preset's measured ~$0.50/run baseline.

---

### Theme 5: OASIS → Wonderwall Rename + CI Unblock

**Summary:** The project's social-platform fork has been internally called "Wonderwall" in commits and in the env file, but the import paths and logger names still said `oasis`. This rename closes that. CI was simultaneously failing on test collection because two modules transitively import `app.storage.neo4j_storage` and `neo4j` wasn't in the test workflow's deps — fixed in the same commit.

**Commits:**

- `d3cfff7` — refactor: rename OASIS → Wonderwall and unblock CI
  - 35 files touched, +149/-148 (mostly identifier swaps): `backend/wonderwall/` (renamed dir, was `backend/oasis/`), `backend/app/services/wonderwall_profile_generator.py` (renamed file), env vars, logger names, README prose. Preserves upstream attribution in README and historical `camel-oasis` pip package references in dependency comments.
  - `.github/workflows/tests.yml` (+2/-1): adds `neo4j` to the CI test deps so collection no longer fails on `app.storage.neo4j_storage` transitive imports.
  - OpenRouter category header expanded from `roleplay` to `roleplay,personal-agent`.

**Impact:** First standing CI test suite (62 unit tests, shipped via PR #41 yesterday) actually runs green on a fresh checkout. The fork now has a consistent name across the whole codebase rather than the half-renamed state it had been in for two weeks.

---

### Theme 6: Cleanup-Branch Merge Wave + Artifact Cleanup

**Summary:** Eight cleanup branches were prepared in the 17-commit sweep referenced in yesterday's recap (15:26–15:44 UTC). Today seven of them merged into `main` in a 13-second window (15:38:16–15:38:55 UTC), followed by `32e3537` deleting the 8 `CLEANUP_ASSESSMENT_*.md` working artifacts (-911 lines) and fixing one EmbedDialog Vite import (the project has no `@/` alias configured; switched `@/api/simulation` to relative `../api/simulation`).

**Commits:**

- `4441b04` — Merge type-definition consolidation (+103/-4, 2 files)
- `3faf945` — Merge weak-type strengthening (+127/-3, 2 files)
- `1d7fea9` — Merge defensive error-swallowing cleanup (+220/-120, 7 files)
- `ef78c64` — Merge DRY consolidation pass (+107/-230, 5 files)
- `14b181b` — Merge legacy/deprecated/fallback removal (+135/-96, 8 files)
- `6a4ca76` — Merge AI slop and stale-comment cleanup (+135/-96, 8 files)
- `8e8477a` — Merge unused-code removal (+169/-83, 38 files; merged with conflict resolution in `simulation_runner.py`)
- `32e3537` — fix: EmbedDialog Vite import and drop cleanup assessments (+1/-911, 9 files): deletes CLEANUP_ASSESSMENT_{CYCLES,DEFENSIVE,DRY,LEGACY,SLOP,TYPES,UNUSED,WEAK_TYPES}.md; one-line EmbedDialog import path fix.

**Impact:** The cleanup work that's been on a side branch for a week becomes part of the codebase the new docs describe. Net reduction is real (the cleanup pass deletes more than it adds, not counting `32e3537`'s artifact removal). The conflict in `simulation_runner.py` was resolved cleanly — the runner-hardening commit and the unused-code cleanup both touched it on the same day.

---

### Theme 7: Simulation Page UI/UX Overhaul (`6fb30bd`)

**Summary:** A standalone polish pass that pulls the simulation page's overlays into a single design language and adds chart-export to all four chart panels. The Markets panel stops being a full-screen modal and becomes an inline overlay matching `InfluenceLeaderboard`. WhatIf and Branch panels swap their off-palette teal for the design-system orange/green bicolor. Every chart panel (Drift, Network, What If?, Markets) gets Copy + Download buttons that produce a HiDPI PNG with a `SIMULATED BY MIROSHARK` footer. Markets multi-config goes from 1 fixed market to 1–5 user-configurable.

**Commits:**

- `6fb30bd` — feat: align overlays to design system, add chart copy/download, multi-market settings
  - `frontend/src/components/PolymarketChart.vue` (+985, new): renders inline inside `.influence-overlay` like every other panel, with subtle 1px borders matching `InfluenceLeaderboard` instead of the prior Neubrutalist 2px-black-border + 8px offset shadow.
  - `frontend/src/components/Step3Simulation.vue` (+221/-61): reworked `.action-btn` to follow the Hyperstitions filter-button pattern (transparent base + 2px border + uppercase Space Mono); orange when toggled, solid black for primary CTA, solid red for Pause. One `toggleOverlay(key)` dispatcher replaces N-squared inline flag flips so every button mutexes every overlay via a single table.
  - `frontend/src/components/WhatIfPanel.vue` (+254/-134): all off-palette teal (`rgba(20,184,166,*)`) swapped for design-system orange/green bicolor. Recompute becomes a black-filled primary CTA. Chart strokes: dashed gray original, solid orange counterfactual. Impact badges use orange/amber/neutral palette.
  - `frontend/src/components/CounterfactualBranchPanel.vue` (+98/-72): JetBrains Mono and Apple-system fonts replaced with Space Mono; matches the filter-button CTA language.
  - `frontend/src/components/InteractionNetwork.vue` (+289/-35), `frontend/src/components/BeliefDriftChart.vue` (+102/-30): Copy + Download buttons added to header; design-system color alignment.
  - `frontend/src/utils/chartExport.js` (+280, new): `renderSvgToCanvas` (SVG → HiDPI canvas), `downloadCanvas`, `copyCanvasToClipboard`, `canCopyImageToClipboard`, plus `wrapText` and `buildTitledHeader` helpers. Every exported PNG carries a MiroShark footer (logo + "SIMULATED BY MIROSHARK" wordmark at 24px, sim id + date on the right). Markets exports get a full poster-style header (Young Serif title, big orange price, delta pill, stats row); other charts use the lighter `buildTitledHeader` (title + one-line context). Pre-loads Young Serif + Space Mono via `document.fonts.load()` so the very first export after page load doesn't silently fall back to system fonts.
  - `backend/app/services/simulation_config_generator.py` (+38/-10), `backend/app/services/simulation_manager.py` (+11/-1), `frontend/src/components/Step1GraphBuild.vue` (+65/-1), `frontend/src/api/simulation.js` (+17): `polymarket_market_count` threads through `SimulationState` → `generate_config` → Step1 UI (1–5 select). Default bumped to 3. Config prompt adapts (singular vs plural axes).
  - `.gitignore` (+4): exclude `design-system/` (reference-only clone of Hyperstitions system, not part of project).

**Impact:** Every chart panel becomes a shareable artifact in one click — pairs naturally with the Social Share Card landing today (Theme 1) to make the sim's output visually portable end-to-end. The multi-market setting unlocks scenario-comparison flows that were previously impossible without re-running the sim.

---

## aaronjmars/miroshark-aeon

### Theme 8: Token-Report XAI Prefetch Migration (PR #22)

**Summary:** The Social Pulse step in the daily token-report skill has shown "XAI_API_KEY not set — social data unavailable" for three days running (Apr 20/21/22) despite the secret being correctly configured (the fetch-tweets prefetch consumes it daily). Root cause: the inline `curl -H "Authorization: Bearer $XAI_API_KEY"` call inside the skill runs in Claude Code's sandbox, which blocks env var expansion in shell-launched commands; the curl fails silently and the skill falls through to the wrong "not set" branch. Fix migrates to the same prefetch + sidecar-validation pattern that was applied to fetch-tweets in PRs #19/#20.

**Commits:**

- `696efdc` — improve(token-report): migrate Social Pulse to XAI prefetch pattern (#22)
  - `scripts/prefetch-xai.sh` (+38): new `token-report)` case. Parses the tracked token symbol from `memory/MEMORY.md`'s `## Tracked Token` table via a small Python regex (captures the first data-row cell under the markdown header+separator), `rm -f`s any stale cache + sidecar, calls `xai_search` with a `$SYMBOL` cashtag query, and writes the symbol verbatim to `.xai-cache/token-report-social.symbol` on success.
  - `skills/token-report/SKILL.md` (+6/-13): step 5 replaced inline curl with Path A (cache hit + sidecar match → parse `output_text`, cite handles/permalinks) / Path B (cache missing, symbol mismatch, or empty → one-line "X/Grok data unavailable this run" note, NOT a false "XAI_API_KEY not set" claim). Social Pulse template language updated to match.

**Impact:** Restores real Social Pulse content to the daily token report. Same self-heal property as fetch-tweets' PR #19 sidecar — changing the tracked token in `MEMORY.md` invalidates the old cache on the next prefetch automatically. Zero new dependencies. Closes the "separate scope" callout flagged in PR #21's body. Will visibly land in tomorrow morning's (2026-04-23) token report.

---

## Developer Notes

- **New dependencies:** None. PR #42's Pillow renderer reuses the Pillow ≥12.0 pin already in `tool.uv.override-dependencies`; the OASIS→Wonderwall commit only adds `neo4j` to the CI test workflow's deps (already in main app deps).
- **Breaking changes:** OASIS → Wonderwall rename touches env var names (e.g. `OASIS_*` → `WONDERWALL_*`) and import paths. Anyone running off a fork or local `.env` predating today will need to update env keys. The `simulation_runner.py` merge conflict in `8e8477a` was resolved with hardening winning over the cleanup-branch state.
- **Architecture shifts:** (1) Documentation now lives in `docs/` as nine standalone reference docs rather than a monolithic README — meaningful for new-contributor onboarding. (2) Settings backend now exposes every model slot via `GET/POST /settings`, so per-slot model overrides are now a first-class concept rather than an `.env` artifact. (3) `_build_embed_summary_payload()` extracted as the shared source of truth between the embed-summary endpoint and the new share-card endpoint — first explicit "embed payload schema" in the codebase.
- **Tech debt:** The 8 `CLEANUP_ASSESSMENT_*.md` working artifacts have been merged + deleted; the 7 cleanup branches are now in `main`. `MIROSHARK_ROUND_TIMEOUT` env var is undocumented in `.env.example` (only set in Python; consider documenting). Counterfactual injection wiring (`2fd2532`) was previously dead code — worth confirming no other "imported but unused" loaders exist.
- **CI:** test workflow now installs `neo4j` and `pillow`; tests collect cleanly post-rename.

## What's Next

- **PR #42 is the only PR open** at the moment of the recap window close (it merged at 13:33 UTC; nothing new opened). The repo is back to a clean slate.
- The settings preset rework + URL fetcher refactor likely needs a follow-up to surface the LLM-fetcher's failure mode in the UI (current behavior: falls through silently to the legacy parser if `WEB_SEARCH_MODEL` lacks `:online`).
- Counterfactual branching is now wired end-to-end for the first time — expect a follow-up commit or two as users hit edge cases the live test ("Mallku" with `user_id=0`) didn't surface.
- The `articles/repo-actions-2026-04-22.md` ideas list (generated this morning by Aeon) leads with **Public Simulation Gallery** and **Simulation Clone / One-Click Fork** as next-feature candidates that compose with today's share-card work.
- For miroshark-aeon: PR #22 should land its first real Social Pulse content in tomorrow's 06:30 UTC token-report run; worth grepping the next day's article to verify Path A activated.
