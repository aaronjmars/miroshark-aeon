# Push Recap — 2026-04-20

## Overview
A big merge day on MiroShark: four outstanding PRs (#36, #37, #38, #39) landed into `main` in a nine-minute window (12:04–12:13 UTC), clearing the entire backlog from the weekend. Two of the merges are the first external backend contributions to the repo — Muhammad Bin Sohail (`mbs5` / `builtbydesigninc`) shipped a 5x report-generation speedup and a live-read fix for embedding settings. The other two are Aeon-built analytics panels — the Counterfactual Explorer (`What If?`) and Scenario Auto-Suggest, completing the "research-grade introspection" and "setup-friction removal" arcs respectively. Meanwhile on `miroshark-aeon`, five fix commits from Aaron Mars hardened the notification chunking, article-URL formatting, and XAI tweet-fetch paths — all rooted in real defects caught during today's skill runs.

**Stats:** 14 files changed, +1,961 / -97 lines across 9 substantive commits. Author spread: 3 distinct humans/agents (Aeon, Aaron Mars, Muhammad Bin Sohail) plus ~35 automated chore commits from `aeonframework`.

---

## aaronjmars/MiroShark

### Theme 1: Research-grade analytics panels shipped — Counterfactual Explorer & Scenario Auto-Suggest

**Summary:** Two Aeon-authored PRs merged in the same window. Each closes a specific friction point the analytics stack had been circling for weeks. #37 gives researchers a way to quantify influence by simulated removal; #39 gives users a way to start a simulation from a document instead of a blank prompt.

**Commits:**

- `f6c43e4` — feat: agent counterfactual explorer ("What If?") (#37)
  - New file `frontend/src/components/WhatIfPanel.vue` (+761 lines): agent picker with top-12 influence leaderboard, up to 3 exclusions, split-line SVG chart showing original (dashed) vs counterfactual (solid) bullish curves, plain-English impact summary, PNG export button.
  - Changed `backend/app/api/simulation.py` (+229 lines): new `GET /api/simulation/<id>/counterfactual?exclude_agents=...` endpoint + `_drift_from_positions_by_agent` helper. Resolves usernames → user_ids against `reddit_profiles.json` / `twitter_profiles.csv`, recomputes per-round stance drift with selected agents filtered out, emits `delta_final_bullish`, `delta_consensus_round`, and a `strong`/`moderate`/`minimal` impact badge.
  - Changed `frontend/src/components/Step3Simulation.vue` (+26, -5): `◐ What If?` overlay toggle with mutual exclusion against other analytics overlays.
  - Changed `frontend/src/api/simulation.js` (+15): `getCounterfactualDrift(simId, names[])` helper.
  - Pure data transform over the existing `trajectory.json`. No re-simulation, no LLM calls, milliseconds per recompute.

- `feb0771` — feat: scenario auto-suggest from document preview (#39)
  - Changed `backend/app/api/simulation.py` (+271, -1): `POST /api/simulation/suggest-scenarios` endpoint. Normalizes the text preview, SHA-256 hashes it, caches results in an in-memory LRU (cap 64) so brief edits above/below the sampled window don't re-hit the LLM. Clamps preview to 2000 chars, calls `create_llm_client().chat_json()` with a 20s timeout and a compact prompt asking for Bull / Bear / Neutral prediction-market scenarios (label, YES probability range 0–100, one-sentence rationale). `_clean_suggestions` validates labels, swaps reversed ranges, rejects overlong questions, caps at 3 suggestions. A second follow-up commit adds per-IP sliding-window rate limiting (10/60s) and hides stack traces on 500s — returns a generic `scenario_suggest_failed` reason code to the client.
  - Non-blocking end-to-end: LLM unavailable / timeout / malformed response → 200 + `suggestions:[]` + reason → UI silently hides the panel.
  - New file `frontend/src/components/ScenarioSuggestions.vue` (+366 lines): debounced card grid (800ms, min 120 chars), Bull/Bear/Neutral colored left-borders + badges, loading spinner, dismiss, monotonic `requestSeq` guard so late responses from an outdated preview can't overwrite current suggestions.
  - Changed `frontend/src/views/Home.vue` (+67): reads `.md`/`.txt` client-side via `File.slice(0, 6000).text()`, combines with `urlDocs[].text`, clamps to 6KB, hands to the component. `handleSuggestionUse` fills `formData.simulationRequirement`.
  - Changed `frontend/src/api/simulation.js` (+26): `suggestScenarios({ text_preview, no_cache? })` with 25s client-side override timeout.
  - Changed `README.md` (+6): new "Smart Setup (Scenario Auto-Suggest)" subsection under How It Works.

**Impact:** Both features ship the "introspection-first" analytics posture MiroShark has been building toward since Trace Interview (PR #26). A researcher now has two net-new levers at the setup-and-result boundary: (1) *before* the simulation runs, three LLM-grounded prediction-market scenario cards pulled from whatever document they drop in — eliminating the blank-page problem that had been the single largest setup-friction signal in repo-actions ideation; (2) *after* it runs, one-click removal of the top-influence hub to quantify its causal share of the final bullish outcome with a Strong/Moderate/Minimal attribution badge. The Counterfactual Explorer completes the DAMIP-style attribution stack sketched in the Apr 19 project-lens piece; Scenario Auto-Suggest fills the very first entry point of the funnel, where drop-off was highest.

### Theme 2: First external backend contributions merged — report perf + embedding config fix

**Summary:** Two PRs from `mbs5` (Muhammad Bin Sohail, `builtbydesigninc`) merged together. #36 is a pure performance rewrite of the report generator; #38 is a subtle lifecycle bug in how `EmbeddingService` reads runtime config. Together they mark the first sustained external backend contribution cycle — not a doc typo or a README tweak, but real engineering on two of the hotter code paths.

**Commits:**

- `a1d7a8d` — perf(report): parallelize section generation (~5x speedup on real runs) (#36)
  - Changed `backend/app/services/report_agent.py` (+87, -60). Three small changes working together:
    1. `ThreadPoolExecutor` with up to 6 workers (configurable via `MAX_PARALLEL_SECTIONS`) replaces the sequential for-loop over `_generate_section_react`. Per-section exceptions are caught inside the worker and rendered as an inline error stub so one bad section doesn't kill the whole report.
    2. `previous_sections=[]` during the parallel phase. Previously each section was given the running draft of earlier sections as context, making input tokens grow linearly with section index (section 1 ~5K in, section 5 ~17K in). Since sections now run concurrently they can't see each other's drafts anyway; the already-existing Phase 2.5 cross-section synthesis pass stitches coherence at the end.
    3. `MAX_REFLECTION_ROUNDS` lowered 3 → 1. Extra rounds added ~30% latency and token cost with marginal measured quality gain.
  - Measured on a 5-section Claude Sonnet 4.6 / OpenRouter run: wall-clock 20.8 min → ~4 min (**5x faster**), LLM calls 21 → ~10, input tokens 270K → ~50K, cost $2.16 → ~$0.95 (**55% cheaper**). Public contract unchanged (same sections, same markdown_content output, same ReportManager progress events); progress events become per-section-completion instead of sequential.
  - Thread-safety handled: lock around `completed_titles` list mutation and `ReportManager.update_progress` calls; `save_section` still runs per-section so partial progress is durable if the process dies mid-report.

- `65f8e57` — fix(embedding): read Config lazily so POST /api/settings takes effect (#38)
  - Changed `backend/app/storage/embedding_service.py` (+34, -10): `provider`, `model`, `base_url`, `api_key`, `dimensions` converted from `__init__` captures to `@property` accessors so every call reads `Config` fresh. Explicit constructor args still take precedence (tests, alternate pipelines).
  - The bug: `EmbeddingService` is constructed once when `Neo4jStorage` initializes at app startup. Post-`POST /api/settings` updates were silently ignored — the cached client kept hitting whatever `EMBEDDING_BASE_URL` was set at process-boot, with the boot-time API key. On Railway redeploys this meant the first simulation after a restart would route every embedding request to the baked-in default URL with a key that had been stale since before the user clicked "Test Connection" in the UI.
  - Zero behavioral change when instantiated with explicit values or when Config is static after startup. Only affects the runtime-update path — but that path is how production users actually configure the app.

**Impact:** The repo now has a measurable outside-engineering moment. The community perf PR (covered in yesterday's repo-article) brings report generation — the slowest user-visible stage — from 20 minutes to 4 minutes for 55% less money, which is a meaningful star-driver: "simulation → report" is the marketed end-to-end. The embedding-config lazy-read fix is subtle but high-impact: it explains a class of silent failures ("my simulation worked but the knowledge graph seems sparse") that Railway users would have hit after every redeploy. Both shipped in the same merge window as Aeon's own two PRs — the repo graduated from "solo agent workshop" to "multi-author merge cadence" in a single morning.

---

## aaronjmars/miroshark-aeon

### Theme 3: Notification reliability — no more truncated messages, no more broken article links

**Summary:** Three tight fix commits from Aaron Mars covering defects observed in the last 24h of skill runs. The Scenario Auto-Suggest feature notification this morning was the concrete trigger — it crossed Telegram's 4096-char cap and was sliced mid-paragraph, losing the PR link and the How-it-works section.

**Commits:**

- `c79401a` — fix(notify): chunk long Telegram messages instead of truncating
  - Changed `.github/workflows/aeon.yml` (+54, -20) inside the notify job: replaces the single `TG_MSG="${TG_MSG:0:3990}\n\n...(truncated)"` call with a Python chunker. Splits `$MSG` at `\n\n` paragraph boundaries first, then `\n` line boundaries, and only hard-splits if a single paragraph/line exceeds 3900 chars (leaving room for the `[i/N]` suffix). Each chunk is base64-encoded when piped through the shell loop so embedded newlines survive intact. HTML conversion + HTML parse-mode + raw-text fallback are reused per-chunk unchanged. 0.3s delay between sends preserves in-channel ordering.

- `1cde4f3` — fix(article): use `$GITHUB_REPOSITORY` for article URL, not OWNER/REPO
  - Changed `skills/article/SKILL.md` (+3, -1): replaces the literal `OWNER/REPO` placeholder plus "run `git remote get-url origin`" instruction with the unambiguous `$GITHUB_REPOSITORY` env var. The old instruction was ambiguous — Claude could resolve it to the *watched* repo (aaronjmars/miroshark) instead of the *running* repo (aaronjmars/miroshark-aeon), producing a 404 on the article link.

- `f5a06a9` — fix(skill-leaderboard): emit clickable article URL in notification
  - Changed `skills/skill-leaderboard/SKILL.md` (+3, -1): wraps the article reference in a full `https://github.com/$GITHUB_REPOSITORY/blob/main/...` URL so Telegram and Discord render it as a tappable link rather than a bare `articles/skill-leaderboard-YYYY-MM-DD.md` path.

**Impact:** Telegram recipients now see full feature announcements rather than pre-CTA truncation; article links across `article` and `skill-leaderboard` skills consistently resolve to the correct running repo. Both were live bugs confirmed in today's logs.

### Theme 4: XAI tweet-fetch path finally unsticks — workflow var passthrough + curl timeout

**Summary:** Two fix commits that together resolved the morning's `fetch-tweets` misbehaviour. Yesterday's re-run in today's log (`Fetch Tweets (re-run 2 — corrected cache)`) was the first time the XAI path worked end-to-end with the correct query; these two commits are why.

**Commits:**

- `06e76ba` — fix(workflow): pass `inputs.var` via env not template substitution
  - Changed `.github/workflows/aeon.yml` (+4, -1): the prefetch step had `VAR="${{ inputs.var }}"`, which inlines the var value *into the bash script source*. When the var contains a `$TOKEN` reference (e.g. a cashtag like `$MIROSHARK`), bash then expands that at script-exec time — and since `MIROSHARK` isn't a defined shell variable, it expands to empty. Symptom confirmed in today's 12:17 UTC run: prefetch cache held 5 tweets, `filter-xai-tweets.py` got only 2 query patterns, cashtag silently dropped, 5/5 tweets rejected as "non-matching." Switches to `SKILL_VAR` env var so bash receives the literal string intact, matching how the main `Run` step already passed it.

- `aeb7961` — fix(prefetch-xai): bump curl timeout 60s → 180s, retry once on timeout
  - Changed `scripts/prefetch-xai.sh` (+11, -4): `--max-time` raised from 60 to 180 seconds, with a single automatic retry on curl exit code 28. Grok's `x_search` tool routinely takes 60–120s to search X and return structured tweet results, so the 60s ceiling was hitting curl 28 on every `fetch-tweets` run. That silently fell through to the WebSearch fallback (stale / empty results for the very content we care about — recent tweets). The two re-runs in today's log suggest the right path was reachable but flaky; this commit makes it reliable.

**Impact:** `fetch-tweets` now actually uses the XAI path it's been falling back from for weeks. Today's `Fetch Tweets (re-run 2)` confirmed 11 fresh tweet URLs including the Kelp DAO / Aave exploit coincidence thread — that result was only reachable after both of these fixes.

---

## Developer Notes

- **New dependencies:** None. Everything was built on existing primitives (`ThreadPoolExecutor`, `hashlib.sha256`, `@property`, standard Vue/FastAPI).
- **Breaking changes:** None. Public contracts preserved across all PRs — report generator emits the same `markdown_content` / progress events, `EmbeddingService` accepts the same explicit constructor args, analytics overlays mutually exclude via an existing pattern.
- **Architecture shifts:**
  - `EmbeddingService` now reads `Config` lazily via `@property` — a small but important lifecycle shift for anything configured at runtime. Pattern worth considering for other service singletons that capture config at init.
  - MiroShark analytics panels now have a consistent template: picker → SVG overlay chart → plain-English summary → PNG export. Counterfactual Explorer follows the same pattern as Trace Interview / Director Mode / Demographic Breakdown. If this keeps up, extracting a shared `<AnalyticsOverlay>` wrapper component is plausible next week.
- **Tech debt:** PR #39's rate-limiting fix was a same-session follow-up to the initial merge (traceback leakage + cost-blast-radius). Worth flagging as a pattern — new LLM-backed endpoints should ship with per-IP sliding-window rate limits and sanitized 500s from day one rather than in a follow-up.

## What's Next

- With PRs #36/#37/#38/#39 all merged, MiroShark is at **0 open PRs** — the cleanest state in ~10 days. The next wave will come from today's `repo-actions` ideation (Round Scrubber, Social Share Card Generator, Trending Topics Auto-Discovery, Collaborative Review Comments, Config Export/Import). Social Share Card Generator is the one with the clearest direct star-growth lever for the 1K-by-Apr-30 hyperstition.
- PR #39 shipped with a same-day security hardening commit (rate limit + traceback scrubbing). That's worth formalizing into a "new LLM-backed endpoint checklist" in the skills layer — the feature skill currently doesn't prompt for either.
- On miroshark-aeon: the XAI fetch path is now reliable; the next follow-up is probably to wire a second-stage dedup on *near-duplicate tweet text* (4 identical `@DaWachu80608` tweets collapsed to 1 manually today). The notification chunking fix is orthogonal but might surface a new edge — some platforms (Discord) have 2000-char caps that still need per-chunk verification; logs should be watched over the next 2–3 notification-heavy skill runs.
- No open branches remain on either repo after today's merges, so there are no in-flight threads the diffs expose. Tomorrow's work is freshly seeded from repo-actions rather than stitched-in from yesterday.
