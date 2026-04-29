# Push Recap — 2026-04-29

## Overview
Seven substantive commits by aaronjmars (squash-author on every PR; aeonframework + Claude Opus 4.7 (1M context) co-authors on three of them) across both watched repos. The dominant thrust was finishing the work yesterday's PRs #50/#51/#52 started: Langfuse metadata that PR #51 added was being silently dropped at OpenRouter's broadcast boundary (PR #54), the cross-round token bloat that PR #52 partly addressed got compressed -57% on the wire (PR #55), and the agent-env compaction tests broke CI on collection until the helpers were moved out of the camel/numpy import chain entirely (PR #58, three iterations). On top of that: PR #57 shipped the third quote-friendly share format (Markdown + JSON transcript export) alongside share-card.png and replay.gif; PR #56 hardened observability pagination against bad query strings; PR #53 (already merged before yesterday's recap window closed but re-pushed at 16:32 UTC) added five NoneType guards, Polymarket on four more templates, clickable history files, and capped default rounds to [30,40]. On the aeon side, PR #26 fixed skill-leaderboard so it scans every entry in `memory/watched-repos.md` instead of only the first.

**Stats:** 32 files changed, +2,419 / −258 across 7 substantive commits. (~28 chore auto-commits from the aeonframework cron loop excluded from the count and themes below.)

---

## aaronjmars/MiroShark

### Cost-compression continuation: trace fields that actually arrive + agent-env wire-format compaction

**Summary:** Yesterday's PR #51 shipped Langfuse metadata on every OpenRouter call so per-phase cost questions could become Langfuse filters. Today's PR #54 found out it wasn't working: OpenRouter's Langfuse Broadcast forwards exactly three top-level keys from the request body (`user`, `session_id`, `trace`) and strips everything else at the broadcast boundary. The previous code put `metadata`, `tags`, and `name` directly on `extra_body` — none spec'd. Verified against a 1,783-event Langfuse export from a recent run pair: 0/1783 events had tags, sessionId, or a custom name; metadata only contained OpenRouter's own `openrouter.*` keys. Every observability field the code intended to set was being dropped. PR #55 then ports the compact-env wire format from miroshark-api PR #30 — same change, same rationale, validated end-to-end on the API run before landing here. Two earlier attempts at this exact problem on the API side (PR #24 `clear_memory`, PR #27 delta env dump) regressed simulate stability; this one is purely cosmetic on the wire so it sidesteps those failure modes.

**Commits:**
- `b1240b4` — `fix: switch OpenRouter→Langfuse pass-through to spec-compliant trace field (#54)` (+40/−42 in `backend/app/utils/llm_client.py`)
  - Moves all per-call context (`run_id`, `simulation_id`, `caller`, `prompt_type`, `sim_phase`, `agent_name`, `agent_id`, `round`, `source`) into a `trace` block with the documented Langfuse keys (`trace_id`, `trace_name`, `span_name`, `generation_name`, `environment`) plus free-form keys that Langfuse exposes as filterable trace metadata.
  - Adds `session_id` (was missing entirely) so calls from one sim group into a Langfuse session.
  - `trace_id = run_id` collapses every LLM call in a run into one Langfuse trace — the grouping the dashboard renders best.

- `bcd269f` — `perf: compact agent env wire format to cut cross-round token bloat (#55)` (+270/−2 across 2 files: `backend/wonderwall/social_agent/agent_environment.py` +115/−2, `backend/tests/test_unit_agent_env_compaction.py` +155 new)
  - In `agent_environment.get_posts_env` only: compact `json.dumps` (no `indent=4`) — pretty-printing the env dump adds whitespace bytes that get re-shipped on every round as CAMEL accumulates user-msg env dumps in agent memory.
  - `created_at` → relative offset against the most recent post (e.g. `"5m"`), since absolute timestamps in a synthetic-time sandbox carry no signal.
  - Comments capped at top-K (3) by score; total preserved as a hint (`"comments_total": 12`) so the agent still knows engagement is deep.
  - Drops `num_shares` / `num_reports` / `num_likes` / `num_dislikes` when 0, drops empty comments arrays, drops `score: 0` — absence is the signal.
  - API validation results (run_12597043a6a4 vs run_f912c2d45627): avg input tokens / sim call **14,527 → 6,241 (−57%)**; per-agent simulate cost **$0.045 → $0.020 (−55%)**; simulate stage cost **$0.898 → $0.652 (−27%)**; simulate wall time **1072s → 818s (−24%)**; rounds completed 10/10 → 10/10 (no hang); actions/agent/round 5.33 → 4.28 (−20%, healthy range); report quality preserved (4 sections vs 3, no errors).

**Impact:** Langfuse rows now actually carry the metadata the dashboard filters on (sessionId / tags / per-call name), and the dominant cost line item — input tokens on the simulate stage — is roughly halved by a wire-format change that doesn't touch agent loop, memory accumulation, or tool surface. Combined with yesterday's PR #53 default-round drop (128 → 30–40), the per-default-run cost compression for the week is multiplicative.

### Three quote-friendly share formats now complete: Simulation Transcript Export

**Summary:** Until today, the only way to quote a simulation in prose was a screenshot. PR #57 closes that gap with `transcript.md` + `transcript.json` downloads — the third quote-friendly share format alongside share-card.png (preview, PR #42) and replay.gif (motion, PR #50). Same publish gate as the share card. PR #52's `prune_tool_calls_from_memory=True` from yesterday cleaned the agent conversation history so the transcript is now readable rather than a wall of tool-call boilerplate; without that prerequisite the transcript wouldn't have been worth shipping.

**Commits:**
- `48b38f9` — `feat: simulation transcript export (Markdown + JSON) (#57)` (+1,538/−0 across 8 files)
  - New `backend/app/services/transcript.py` (+615): pure-stdlib renderer (`json` + `io`) reading `trajectory.json` + `reddit_profiles.json` + `polymarket_profiles.json` + `quality.json` + `resolution.json` + `outcome.json`.
  - ±0.2 stance threshold matches every other surface (gallery, share card, replay GIF, webhook) — a "bullish" agent in the transcript is the same agent's tag on /explore.
  - Defense-in-depth strip on `outcome_url` so a corrupt `javascript:` URL never lands on the transcript.
  - 400-char per-post excerpt with word-boundary trim. 80-round Markdown cap with first-20 + last-20 preservation + "skipped N rounds" annotation pointing at the JSON form for the full series; JSON keeps every round.
  - Markdown form opens with a YAML front-matter block (`sim_id`, `scenario`, `agent_count`, `total_rounds`, `consensus_label`, `quality_health`, `outcome_label`) so Notion / Obsidian / Bear / Substack pick it up as page metadata.
  - `backend/app/api/simulation.py` (+86): `GET /api/simulation/<id>/transcript.md` + `transcript.json` — share publish gate, 60s `Cache-Control`, on-disk data assembly only (no LLM calls, no DB joins). Inline `Content-Disposition` so a click renders in-tab; the frontend uses an explicit `download` attribute when it wants save-as.
  - `backend/openapi.yaml` (+143): both routes under Publish & Embed + new `SimulationTranscript` schema with the full per-round shape — drift-detection test passes.
  - `frontend/src/components/EmbedDialog.vue` (+156): "Export transcript" section beneath the replay-GIF row with Download .md / Download .json buttons, copyable Markdown URL, publish-gated empty state.
  - `frontend/src/api/simulation.js` (+33): `getTranscriptMarkdownUrl()` + `getTranscriptJsonUrl()` helpers.
  - `backend/tests/test_unit_transcript.py` (+493 new, 18 offline tests): ±0.2 stance threshold parity, profile-name resolution across reddit + polymarket, corrupt-artifact graceful degradation, long-post excerpting at the configured cap, YAML front-matter integrity (quote + newline escaping), per-round section emission, oversized-trajectory Markdown truncation with head + tail preservation, JSON pretty-print round trip, route-decorator presence guard.
  - `docs/FEATURES.md` (+11) + `README.md` (+1): feature row + section under Sharing.

**Impact:** Substack / Notion / Bear / Obsidian publishers can now drop a transcript URL into a post and get rendered page metadata. SDK and LLM-as-judge eval pipelines can pull `transcript.json` for the full per-round shape. Combined with PR #50 (GIF) and PR #42 (share card), every published sim now ships three quote-friendly export formats from one EmbedDialog. Sim_dir is still the schema — the new endpoints just project from existing on-disk artifacts.

### Hardening pre-existing code: NoneType guards, observability pagination, default-round cap, history UX

**Summary:** Two PRs that aren't building new surfaces — they're cleaning up rough edges in code that's been shipping for a while. PR #53 (merged 16:32 UTC yesterday but re-pushed inside this window) bundles five NoneType guards on post-action handlers, Polymarket on four more templates, a TemplateGallery + TrendingTopics retry loop for cold launcher starts, clickable history file rows with a new path-traversal-guarded download endpoint, History modal overflow fixes, and a default-round cap [30,40]. PR #56 fixes the observability pagination handlers — `int(request.args.get(...))` raised `ValueError` on non-numeric query strings (e.g. `?from_line=abc`, `?limit=null`) and propagated as a 500.

**Commits:**
- `555c6bd` — `Templates UX, clickable history files, capped default rounds, NoneType guards (#53)` (+309/−90 across 14 files)
  - `backend/wonderwall/social_platform/platform.py` (+10): five Reddit/Twitter handlers (`like_post`, `unlike_post`, `dislike_post`, `undo_dislike_post`, `create_comment`) called `_get_post_type(post_id)` and immediately subscripted the result with `['type']` without nil-checking. When an agent invented a `post_id` that didn't exist, `_get_post_type` returned None, surfacing to the LLM as `'NoneType' object is not subscriptable` — a tool error the ReAct loop would retry up to 4 times before giving up. Added the same `if not post_type_result: return …` guard the existing handlers (`repost`, `quote_post`, `report_post`) already use.
  - `backend/wonderwall/social_agent/agent.py` + `backend/app/utils/llm_client.py` (+10 + +9): one-shot `[langfuse-debug]` log line at both OpenRouter `extra_body` call sites so we can confirm the metadata dict is actually on the wire — log fires once per process per site, then the `_extra_body_logged` class flag silences it. (Companion instrumentation that surfaced the bug PR #54 fixed.)
  - 4× `backend/app/preset_templates/*.json` (+13/−4 each): added `polymarket` to `platforms[]` and `enable_polymarket: true` on `corporate_crisis`, `political_debate`, `product_announcement`, `historical_whatif`. Skipped `campus_controversy` — university policy doesn't have a meaningful real-world prediction-market angle. Crypto Token Launch was already covered, so 5/6 templates now ship a Polymarket platform.
  - `frontend/src/components/TemplateGallery.vue` + `TrendingTopics.vue` (+31/−8 + +24/−13): both panels fetched their data in a single `onMounted` attempt with no retry. On a cold launcher start Vite serves the page before Flask is fully warm — the first GET would return empty/error and the panels would stay blank until the user manually refreshed. Both now retry with 0/750/1500/3000ms backoff on initial mount; the manual refresh button still does a single attempt so explicit refreshes don't double-trip. Also `white-space: nowrap` on `.platform-badge` and `flex-wrap: wrap; row-gap: 6px` on `.card-platforms` so the now-crowded Crypto card's 5-chip strip wraps cleanly to a second line instead of breaking a single chip in half.
  - `backend/app/api/simulation.py` (+46/−1): new `GET /api/simulation/project/<project_id>/files/<saved_filename>/download` endpoint — streams the original file with the human filename as `download_name`. Path-traversal guarded (rejects `..` / `/` / `\`, resolves the path and confirms it's still inside the project's files dir). `backend/app/api/graph.py` (+1) persists `saved_filename` on `project.files` at upload time so the new endpoint has something to resolve against.
  - `frontend/src/components/HistoryDatabase.vue` (+99/−31): associated-files rows are now clickable. URL-imported docs link to their original `url`; uploaded files resolve through the new download endpoint. `.modal-content` had `overflow-y: auto` but no `overflow-x` rule, so browsers defaulted it to auto and a long filename made the whole modal scroll sideways — set `overflow-x: hidden` on the modal and `min-width: 0` on the file row + name span so `text-overflow: ellipsis` finally engages. "Get Embed Code" now closes the project modal first instead of stacking on top of it. Prediction Outcome and Embed sections share a style now: same centered flex-column intro, same monospace 11px description, same ⌘-prefixed peach button. Quality block wrapped in a soft white card; `STANCE DIVERSITY` no longer wraps to two lines (label width 100→130, letter-spacing 2px→0.5px).
  - `frontend/src/components/Step2EnvSetup.vue` (+26/−21): cap auto-recommended round count to `[30, 40]`. The Smart-model config generator was picking 96h × 45min = 128 rounds, an ~17 min first run on the Cheap preset. New `naturalMaxRounds` computed preserves the original ceiling for the slider so power users in Custom mode can still dial up beyond 40.
  - `backend/tests/test_unit_openapi.py` (+1): allowlist new project-file download route in the OpenAPI drift test — same internal-SPA-flow nature as existing config/download and script/download routes.

- `02ff29a` — `fix(observability): coerce pagination ints via Flask type= so bad input doesn't 500 (#56)` (+124/−8 across 2 files)
  - `backend/app/api/observability.py` (+10/−8): `/events` and `/llm-calls` handlers wrapped `request.args.get(...)` in `int()`, which raises `ValueError` on non-numeric query strings (e.g. `?from_line=abc`, `?limit=null`, `?agent_id=foo`) and propagates as a 500. The `/llm-calls` endpoint already used Flask's `type=float` for `min_latency` correctly — the int casts on either side of it were the inconsistency. Switch to `request.args.get(name, default=N, type=int)` which silently falls back to the default on parse failure, matching the pattern in the same function and behaving the way OpenAPI advertises the params.
  - `backend/tests/test_unit_observability_routes.py` (+114 new): pure offline, mounts the blueprint on a stub Flask app and pins the no-500 contract for malformed query strings on both endpoints.

**Impact:** PR #53's NoneType guards close a tool-retry-loop cost leak that complemented yesterday's PR #52 fixes (idempotent action returns, max_iteration bound). Polymarket spread to 4 more templates means 5/6 default templates now have prediction-market integration on the new-sim form. Default-round cap means the Cheap preset finally actually behaves like "$1 & under 10 min" out of the box without the user knowing to dial down. PR #56 closes a small but real liveness hole — a single fuzzed query string against `/events` could trigger a 500 in the dashboard.

### CI repair: split env_compact into a stdlib-only module (three iterations)

**Summary:** PR #55's new `test_unit_agent_env_compaction.py` imported `wonderwall.social_agent.agent_environment`, which transitively pulled `camel.toolkits → numpy → torch`. The CI workflow installs only the thin offline-test dep set, so collection has been failing on main since #55 landed (ModuleNotFoundError on numpy then torch). PR #58 fixed it on the third try.

**Commits:**
- `cee23c7` — `fix(ci): split agent-env compaction helpers into stdlib-only module (#58)` (+129/−110 across 4 files)
  - **Iteration 1:** Add numpy to backend unit-test deps. CI still failed (transitive torch import).
  - **Iteration 2:** Move helpers (`_parse_ts` / `_comment_score` / `_compact_post_for_agent` / `_compact_comment` / `_compact_posts_for_agent` and `_MAX_COMMENTS_PER_POST`) into `wonderwall/social_agent/_env_compact.py` — pure stdlib (`json`, `datetime`). `agent_environment.py` re-exports them so its own callers are unchanged. Tests still failed with `ModuleNotFoundError: numpy` because Python's package-init mechanism still triggers `wonderwall/__init__.py` on any submodule import — and that init eagerly imports the camel/numpy chain.
  - **Iteration 3 (landed):** Move the helpers to `backend/lib/env_compact.py` (sibling of `wonderwall/`), which sits on the existing test sys.path. Both `agent_environment.py` and the test now import from `lib.env_compact`, bypassing wonderwall's init entirely. New `backend/lib/__init__.py` (empty), new `backend/lib/env_compact.py` (+120), `agent_environment.py` shrinks by 109 lines (helpers removed, single import added), test import update.

**Impact:** Main is green again. The takeaway is documented in the iterations themselves — re-exporting from a submodule isn't sufficient to dodge a heavy package init; the helpers have to live outside the package import path entirely.

---

## aaronjmars/miroshark-aeon

### Skill self-improvement: skill-leaderboard scans every watched repo

**Summary:** Apr 26 (Sunday weekly schedule) `skill-leaderboard` logged `SKILL_LEADERBOARD_INSUFFICIENT_DATA` because step 1 used only the FIRST entry in `memory/watched-repos.md` — `aaronjmars/MiroShark`, an application repo with 107 active forks but 0 carrying `aeon.yml`. The actual aeon-instance repo (`aaronjmars/miroshark-aeon`) sat at position 2 and never got scanned. Reordering `memory/watched-repos.md` would have cascaded to 17 other skills that read it as primary repo selector — fix lives in the skill, not the shared list. PR was opened yesterday (Apr 28); merged today.

**Commits:**
- `b910088` — `improve: skill-leaderboard scans all watched repos (#26)` (substantive: +9/−6 in `skills/skill-leaderboard/SKILL.md`; balance is auto-commits the bot rolled into the PR)
  - Step 1 now reads **every** entry in `memory/watched-repos.md` into a `TARGET_REPOS` array.
  - Step 2 iterates the array, fetches active forks for each, and unions the results deduped by `full_name`. Application repos (no aeon-shaped forks) contribute zero data and fall out naturally — no hard-coded ordering required.
  - Article footer + log entry both record the full list of source repos scanned.
  - Notification threshold (≥2 forks with readable `aeon.yml`) and `SKILL_LEADERBOARD_NO_FORKS` early-exit unchanged.

**Impact:** Next Sunday (May 3) the skill should now find both `AITOBIAS04/miroshark-aeon` and any future aeon fork; the threshold becomes meetable as soon as a second aeon fork lands instead of waiting for an aeon fork of the application repo (which by definition can't happen). Future-proof for additional aeon-instance entries.

---

## Developer Notes
- **New dependencies:** None across all 7 commits. PR #57 reuses Pillow / pyyaml / Flask already in pyproject; PR #55 is pure stdlib (json + datetime); PR #58 is pure stdlib (json + datetime); PR #54 is config-only on existing OpenRouter+Langfuse path.
- **Breaking changes:** None. All endpoints additive. PR #54 changes the on-the-wire shape of the `extra_body` Langfuse pass-through but the previous shape was being silently dropped; consumers (Langfuse dashboards) get strictly more fields, not different ones.
- **Architecture shifts:** `backend/lib/` introduced as a new top-level location for stdlib-only helpers that need to be importable without triggering the `wonderwall/__init__.py` heavy-import chain. Expect more code to move there over time as the camel/numpy import surface keeps surfacing in CI.
- **Tech debt:** PR #53's `[langfuse-debug]` one-shot log line at both `extra_body` call sites is debugging instrumentation — fine to leave for now (silenced after first fire) but worth removing once Langfuse trace metadata is confirmed flowing for a few days post-PR #54.
- **Sim_dir IS the schema (continued):** PR #57's transcript renderer reads `trajectory.json` + `reddit_profiles.json` + `polymarket_profiles.json` + `quality.json` + `resolution.json` + `outcome.json` from the same on-disk layout `_build_gallery_card_payload` and `_build_embed_summary_payload` already use. New view, no schema, no DB join.

## What's Next
- The Langfuse trace metadata (PR #54) needs a verification pass — the next run pair after this lands should be checked against a fresh Langfuse export to confirm the `trace` block + `session_id` are now actually arriving on every event (the same check that caught the bug originally: 0/N events with tags would be the failure mode). Once verified, the `[langfuse-debug]` log lines from PR #53 can come out.
- The agent-env compaction (PR #55) was validated on miroshark-api before landing here. Next default-config simulate run on this codebase should be checked for the −57% input-token / −55% per-agent cost expected from the API run — any drift would suggest something env-specific in CAMEL accumulation differs between the two repos.
- Repo-actions Apr 28 idea #2 (Transcript Export) shipped as PR #57. Open from that batch: #1 Langfuse Cost Breakdown Panel (now feasible since PR #54 makes the per-phase metadata actually arrive), #3 RSS Feed for Public Gallery, #4 Scenario Template Library, #5 Comparative Run View. Earlier batches still open: Apr 26 #3 Thread Formatter / #4 Python SDK / #5 Director Overlay; Apr 24 #1 SSE / #2 Leaderboard / #4 Discord-Slack share button (largely subsumed by PR #46 webhook).
- 1K-stars-by-Apr-30 sprint: 860 stars as of today's repo-pulse (+6 net since yesterday's recap). Need ~70/day for the next 1.5 days to clear the bar.
