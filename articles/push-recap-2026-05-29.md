# Push Recap — 2026-05-29

## Overview
Three PRs landed on `aaronjmars/MiroShark` in the last 24h, all merged within a 2-minute window (14:36–14:38 UTC). Aeon shipped the 25th platform surface (Belief Volatility Score); aaronjmars shipped a top-to-bottom frontend visual identity flip from light "Hyperstitions" to dark "deep-space-violet"; and the locale-negotiation protocol that already existed in code finally got documented on the API surface. The watched `aaronjmars/miroshark-aeon` repo had only scheduler/cron auto-commits in the window — no substantive code changes.

**Stats:** 48 files changed, +4,782 / −3,452 lines across 3 PRs (2 authors)

---

## aaronjmars/MiroShark

### Theme 1: Belief Volatility Score — the third leg of the analytical quadrant
**Summary:** Closes the analytical triangle that `signal.json` (where the swarm landed) and `peak-round` (when each stance peaked) opened. The new `/volatility` surface describes the *distribution* of round-over-round belief swings: mean, population std dev, max, a normalized 0–100 volatility index, and a `stable` / `converging` / `contested` trend label. Position-sizing models can now tell a high-volatility Bullish result (agents swung repeatedly before aligning) from a low-volatility one (consensus formed in round three and held) — the same final direction means very different things to a downstream consumer.

**Commits:**
- `822c3db` — `feat: belief-volatility analytics surface (/volatility) (#124)`
  - New file `backend/app/services/volatility_service.py` (+206 lines) — `compute_volatility(rounds)` + `compute_volatility_for_sim(sim_dir)`. Pure stdlib (`json` + `os` + `math`). Reuses `peak_round.load_trajectory_rounds` so the per-round bullish/neutral/bearish percentages come from the exact same `compute_stance_split` (±0.2 threshold) that `trajectory.csv`, `chart.svg`, `signal.json`, and `peak-round` use. By construction `max_delta_round` here equals `most_volatile_round` from peak-round on identical input — the new value is the *distribution* of deltas rather than just the max.
  - `backend/app/api/simulation.py` (+84 lines) — `GET /<simulation_id>/volatility` route. Publish-gated (403 when `is_public=false`), reuses `_build_embed_summary_payload`. 404 when fewer than two rounds (no deltas to compute) — lets consumers distinguish "not ready" (404) from "private" (403). Pretty-printed JSON + 5-minute cache + `Content-Disposition` matching the peak-round / chart.svg / signal.json posture. Increments `volatility` surface stat.
  - `backend/app/services/surface_stats.py` (+1 line) — registers `"volatility"` in `SURFACE_KEYS` (25th surface key).
  - `backend/openapi.yaml` (+143 lines) — `/api/simulation/{id}/volatility` path + `VolatilityResponse` schema.
  - `backend/tests/test_unit_volatility.py` (new, +285 lines, 18 offline tests) — boundary cases (empty/single-round → None, two-round well-defined), arithmetic (mean / max / population std dev / `max_delta_round` matches peak-round's `most_volatile_round`), index normalization (flat → 0, clamped at 100), trend buckets (stable / converging / contested), route + surface-stats + OpenAPI wiring guards.
  - `backend/tests/test_unit_surface_stats.py` (+1 line) — adds `volatility` to the SURFACE_KEYS invariant set (the missing entry that failed CI on the first push; second commit fixed it).
  - `frontend/src/api/simulation.js` (+49 lines) — `getVolatilityUrl`, `getVolatility` (same 403/404 → null contract as `getPeakRound`).
  - `frontend/src/components/EmbedDialog.vue` (+219 lines) — 📈 "Belief volatility (JSON)" section after peak-round. Index with gradient bar (green ≤33 / amber 34–66 / red ≥67), max swing + round, mean swing, std dev, trend chip, copyable URL + curl. Loads on dialog open and on publish-gate flip, matching peak-round's lifecycle.
  - `docs/API.md` (+1 line) — `/volatility` row under Analytics with curl example.
  - `docs/FEATURES.md` (+35 lines) — Belief Volatility Score section between Peak-Round Analytics and Per-Agent Belief Sparklines.

**Volatility index formula:** `min(std_dev_delta_pct × 5, 100)`. Flat trajectory → 0, typical mild oscillation lands 20–40, a single dramatic swing drives the index above 80. The 5× multiplier is a calibration knob, documented so external integrators can rescale.

**Trend classifier:** `stable` when std dev < 3.0 pp; `converging` when the second half of the trajectory's deltas has strictly lower std dev than the first half (swarm calmed down); `contested` otherwise. <4 deltas falls back to stable/contested on std dev alone.

**Impact:** AntFleet's benchmark, the Polymarket prediction-JSON consumer, and any future quant integrator now have a single number for "how confident is this signal" that isn't confidence itself. Zero new deps (33rd straight PR since Nemotron). Same publish gate + late-bound env + pretty-JSON contract as every other share surface.

### Theme 2: Frontend visual identity flip — light Hyperstitions → dark deep-space-violet
**Summary:** Replaces the previous Evangelion-orange/green/cream "Hyperstitions" theme across the entire SPA with a deep-space-violet system that matches miroshark.xyz. The PR landed in eight commits stacked on the same branch — each one a follow-up fix after the previous broke into white-on-light, dark-on-dark, or invisible-text states. Read as one operation: a token-level palette remap in `App.vue` cascaded through 27 component files, with targeted upgrades to the shells that the cascade broke.

**Commits:** all under `5535432` (squash-merge of `frontend: rewrite Home view in real MiroShark visual language (#122)`)
  - `frontend/src/App.vue` (+28, −18) — palette remap at the `:root` token level. Legacy token NAMES kept (`--color-orange`, `--color-green`, `--color-white`, `--color-black`, `--color-gray`, `--color-red`) so every scoped `<style>` inherits the new palette automatically; VALUES remapped: orange → bright violet `#a78bfa`, green → soft violet `#c4b5fd`, white → deep glossy-panel base `#110a26`, black → light foreground text `#f4f1ff`, red → soft fuchsia `#f0abfc`. `--background` flipped to deep-space `#05030a`. Light-on-dark text opacity helpers (`.text-primary-100`/70/50/40/35) inverted.
  - `frontend/src/views/Home.vue` (+996, −1237) — full rewrite. Deep-space radial-gradient body + twinkling stars, chrome-shimmer "Simulate anything for $1" headline (comma dropped) next to a floating shark webp, glossy violet console with file / Just Ask / URL / Trending / Scenario / Launch pipeline. Geist + Geist Mono fonts added alongside Young Serif + Space Mono so other views still see their original fonts and Home gets the new system.
  - `frontend/src/views/MainView.vue`, `ReportView.vue`, `SimulationView.vue`, `SimulationRunView.vue`, `InteractionView.vue`, `ReplayView.vue`, `ComparisonView.vue`, `ExploreView.vue` — deep-space radial bg + glossy glassmorphic header + chrome-text MIROSHARK brand + nav-pill switch buttons. Hard-coded `rgba(10,10,10,X)` text colours flipped to `rgba(244, 241, 255, X)` so text reads on dark cards. `.chip-active` and `.filter-chip-active` rebuilt as glossy violet pills instead of black-bg active states.
  - `frontend/src/components/Step1GraphBuild.vue` (+74, −73), `Step2EnvSetup.vue` (+142, −138), `Step3Simulation.vue` (+317, −235), `Step4Report.vue` (+310, −307), `Step5Interaction.vue` (+185, −182) — step-cards reskinned as glossy violet panels with left accent rail. Step3 (the running-sim surface the user flagged as ugly) got the heaviest pass: toolbar buttons in glossy violet nav-pill family, platform tabs (X / Reddit / Polymarket) with per-platform left accent rails, timeline cards as glossy panels with inset highlight + outer shadow, system-logs glassmorphic with violet-tinted scrollbar.
  - `frontend/src/components/SettingsPanel.vue` (+134, −107), `LocaleToggle.vue` (+31, −19), `ZhWarningBanner.vue` (+101, −65) — overlay flipped from 60% light wash to 70% deep-space wash with backdrop-blur. Modal rebuilt on glossy violet panel base. EN/中 toggle and Chinese-mode warning reskinned to match nav-pill / glossy modal family.
  - `frontend/src/components/TemplateGallery.vue` (+133, −76), `HistoryDatabase.vue` (+152, −156), `TrendingTopics.vue` (+90, −47), `ScenarioSuggestions.vue` (+128, −71) — reskinned and reinstated on Home. Difficulty colors remapped (easy=violet / medium=amber / hard=fuchsia). Scenario cards keep semantic Bull/Bear/Neutral cues but remapped: bullish stays violet, bearish moves to soft fuchsia, neutral stays amber against the dark surface.
  - `frontend/src/components/EmbedDialog.vue` (+130, −116), `NetworkPanel.vue` (+40, −52), `GraphPanel.vue` (+84, −99), `InteractionNetwork.vue`, `BeliefDriftChart.vue`, `DebugPanel.vue`, `DemographicBreakdown.vue`, `InfluenceLeaderboard.vue`, `PolymarketChart.vue`, `WhatIfPanel.vue`, `CounterfactualBranchPanel.vue` — embed overlay and visualization canvases flipped to deep-space radial + glossy violet panels.
  - `frontend/src/views/EmbedView.vue` — link color flipped to violet.
  - The final commit (`Fix dark-on-dark text by flipping legacy #0A0A0A literal`) systematically flipped the literal `#0A0A0A` to `#f4f1ff` across 13 files where it had been used as the "dark ink" pair — backgrounds (dark CTA pills) and text (text on light cards). After the page got darker, any `#0A0A0A` bg + `#110a26` text became near-black on near-black; any `#0A0A0A` text became invisible on the dark surface. The flip restores readable primary CTAs (light pill bg + dark text), readable text on dark pages, and visible borders on dark surfaces.
  - `frontend/index.html` (+1, −1) — added Geist font family.
  - `frontend/public/shark.webp` (new binary) — the floating shark mascot for the Home hero.

**Impact:** SPA now matches miroshark.xyz visually. Every page renders dark; orange/green theme is gone. Script logic on Home is 1:1 with the previous version (refs, computed, handlers, lifecycle, imports unchanged — only template + style touched), which kept the cascade safe. The heavy `+3,716 / −3,452` line count is almost entirely CSS/template churn; the diff is overwhelmingly token swaps + scoped style rewrites, not behavior changes.

### Theme 3: Localization protocol documentation
**Summary:** The locale-negotiation protocol already existed in code — every endpoint resolves an active locale per request via `?lang=` → `X-MiroShark-Locale` → `Accept-Language` → `en` (see `backend/app/utils/i18n.py::get_locale`), the bundled SPA sends the header on every call, and `apply_i18n` / `_t()` localize error messages, template metadata, feed copy, and the report agent's narration. None of that was discoverable from `docs/API.md`. PR #123 surfaces it.

**Commits:**
- `3ce49e9` — `docs: document the locale-negotiation protocol on the HTTP API surface (#123)`
  - `docs/API.md` (+21 lines) — new "Localization" section near the top, right after the Interactive docs note and before the endpoint tables. Documents the precedence order, the supported locales (`en`, `zh-CN`), the "unknown tags fall back to en silently" rule (so `?lang=fr` on the current build returns English, not 400), what gets localized (error messages, template metadata, RSS/Atom feed copy, report narration), and what doesn't (raw simulation data, posts, trades, agent stances). Two curl examples: SPA-style header-driven and share-surface-style query-pinned for stable canonical URLs.
  - `docs/API.zh-CN.md` (+21 lines) — mirrors the section verbatim into the Chinese API reference.

**Impact:** SDK authors running `openapi-generator` against the spec, third-party integrators pulling templates or RSS, and anyone investigating issue #95 (French locale interest) can now find the protocol in the place they'd look first. Docs-only; no spec or code touched. Co-authored by aeonframework, externally landed.

---

## aaronjmars/miroshark-aeon

No substantive commits in the window. ~29 auto-commits from the scheduler (cron state updates and per-skill `chore(skill): auto-commit YYYY-MM-DD` markers from `feature`, `token-report`, `repo-pulse`, `star-momentum-alert`, `star-milestone`, `repo-article`, `project-lens`, `push-recap`, `thread-formatter`, `heartbeat`) — operational telemetry, excluded from this recap.

---

## Developer Notes
- **New dependencies:** zero. PR #124 holds the 33-PR zero-deps streak since Nemotron.
- **Breaking changes:** none. The visual identity flip kept legacy CSS token names so scoped styles inherit automatically; no API contracts changed.
- **Architecture shifts:** the analytics surface family now has three orthogonal axes (`signal.json` = direction, `peak-round` = when, `volatility` = how contested). Each is derived from the same `compute_stance_split(±0.2)` so cross-surface comparisons stay byte-consistent.
- **Tech debt:** PR #122's eight stacked commits show the dark-theme cascade was a "fix the next thing the user can see" loop rather than a planned rollout. The pattern (token remap → cascade breaks → targeted fix → next view) worked, but a handful of components still inherit the new palette indirectly through `--color-orange` / `--color-green` rather than via explicit new tokens — a follow-up pass to rename those to `--color-accent-violet` / `--color-accent-soft-violet` would make the codebase honest about what's now there.
- **Required CI fix mid-PR:** PR #124's first push failed because `test_surface_keys_includes_every_serve_handler` had a hard-coded expected set that didn't include `volatility`. Second commit (`test(surface-stats): add volatility to SURFACE_KEYS invariant set`) fixed it. Worth remembering: any new surface needs three updates (route, `SURFACE_KEYS`, the invariant test's expected set), not two.

## What's Next
- **Webhook Test Ping** (May-20 batch #4, re-eligible) and **Surface Catalog API** (`GET /api/surfaces.json`) were the two net-new ideas from yesterday's `repo-actions-2026-05-28.md` that weren't picked today — likely candidates for the next `feature` skill run.
- **Frontend reskin follow-up:** the PR #122 commit-by-commit notes flag a few remaining gaps — TrendingTopics / ScenarioSuggestions render silently when the API has no items so they weren't visible during testing, and a few components were upgraded reactively rather than proactively. A "find every remaining `#0A0A0A` / `var(--color-orange)` literal that's now wrong on dark" sweep would close the loop.
- **PR #106** (Railway deployment, external/Devin) remains the only open PR on MiroShark — stalled ~3.2 days as of yesterday's heartbeat.
