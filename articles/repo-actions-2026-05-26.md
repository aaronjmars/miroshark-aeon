# Repo Action Ideas — 2026-05-26

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,201 stars · 251 forks · 2 open issues (#95 French locale) · 1 open PR (#106 Railway deployment, external/DYAI2025)
**Recent activity:** PR #109 (ECOSYSTEM.md — 10 integrators: AntFleet, Blue Agent, Crucible Sim, Echo, Monitor, Nookplot, RootAI, Signa, Supercompact, Xerg) + PR #108 (Peak-Round Analytics, 22nd surface key) + PR #107 (oEmbed, 21st surface key) all merged. New post-Nemotron zero-deps streak: 5 PRs. Token $0.00001244 (-71.5% from ATH $0.0000436 May 18); 30d +267%.

## Ecosystem Context

PR #109 landing today signals a shift: MiroShark is no longer describing what it does in isolation — it's describing who is building with it. Ten integrators are publicly identified. AntFleet, Signa, and the rest aren't passive forks; they're products. This is the first time the project has formally named its downstream community in a structured format.

That creates three new gaps visible from this baseline:

**The machine-readable integrator gap.** ECOSYSTEM.md is HTML-Markdown — readable by humans, opaque to scripts. The same data served as `GET /api/ecosystem.json` lets Aeon track integrators programmatically, lets directories ingest the list automatically, and lets bots watch for new additions without scraping. One JSON file + one route. Net-new.

**The webhook noise gap.** Ten integrators means ten different use cases — not all of which care about every sim completion. A Polymarket bot wants only Bullish + high-confidence signals. A research pipeline wants only excellent-quality outcomes. `WEBHOOK_EVENTS` env var (comma-separated tokens: `bullish`, `bearish`, `neutral`, `high_confidence`, `good_quality`, etc.) filters dispatch at the source. Zero new endpoints; backward-compatible. Net-new.

**The international discovery gap.** @btcbabycow's CN tweet "米罗莎要来了" (May 16) and @m000_crypto's JP coverage (May 17) confirm organic CN/JP developer interest. A bilingual README converts that interest into a path in. The CN-locale contributor hyperstition deadline is 2026-06-15 — 20 days away. The pattern exists (PR #65 Chinese locale). Re-eligible from May-18 (unbuilt).

Two additional ideas from the May-18 batch are now re-eligible at 8 days:

**The agent visualization gap.** The EmbedDialog shows aggregate belief curves. No per-agent dimension exists in any visual surface. Per-Agent Stance Sparklines adds 40×15px SVG sparklines per agent — each agent's belief trajectory colored by final stance. Researchers studying swarm convergence patterns (do financial-analyst agents align faster?) get the data they need without parsing transcript.md.

**The iteration friction gap.** Operators running variant sims — same scenario, different agent count, neutral phrasing — currently copy-paste and reset manually. A Clone button pre-fills the new-sim form with the source scenario's parameters. One-click variant analysis.

Previously suggested ideas excluded from this batch (7-day window May 19–25): Belief Volatility Score (May-20 #3, unbuilt); Webhook Test Ping (May-20 #4, unbuilt); Gallery Public JSON (May-20 #5, unbuilt); Private Share Link (May-22 #1, unbuilt); French Locale (May-22 #2, unbuilt); Operator Profile (May-24 #3, unbuilt); Agent Persona Export JSON (May-24 #4, unbuilt); Simulation Search JSON API (May-24 #5, unbuilt). All 5 ideas below are net-new or re-eligible.

---

### 1. Per-Agent Stance Sparklines

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** The EmbedDialog shows aggregate belief curves via chart.svg — what the swarm concluded. Sparklines add the per-agent layer: for each agent, a 40×15px SVG sparkline of their bullish_pct across all rounds, colored by final stance (green/gray/red). Researchers studying convergence patterns — do financial-analyst agents align faster than retail traders? which agent anchored the consensus? — get a visual answer without downloading or parsing transcript.md. Every published sim with per-agent trajectory data becomes a miniature swarm analysis dashboard. Re-eligible from May-18 (unbuilt).

**How:**
1. Add `backend/app/services/agent_sparklines_service.py` (~120 LoC, stdlib `json` + `os`). `load_agent_trajectories(sim_dir) -> list[dict] | None`: reads `simulation_state.json`; returns `[{agent_id, name, role, final_stance, trajectory: [{round, bullish_pct}]}]` if agents array includes per-round data; returns the list with empty `trajectory: []` if agents only have final state. Returns `None` if no agents. Add `GET /api/simulation/<id>/agents/sparklines` (publish-gated; `Content-Type: application/json`; `Cache-Control: public, max-age=300`). Response: `{sim_id, agent_count, has_per_agent_data: bool, agents: [{agent_id, name, role, final_stance, color: "#22c55e" | "#6b7280" | "#ef4444", trajectory: [{round, pct}]}]}`. 403 unpublished; 404 no agent data. Extend `SURFACE_KEYS` + `surface_stats` with `agent_sparklines`. Add 10 offline unit tests in `test_unit_agent_sparklines.py`: per-agent trajectory present → returned correctly; `color` maps to stance for all three; unpublished → 403; no agents → 404; `has_per_agent_data: true` when trajectory non-empty; `agent_count` matches list length; `final_stance` one of Bullish/Neutral/Bearish; `sim_id` in response matches param; fallback returns `has_per_agent_data: false` with empty trajectories; surface_stats increment called.
2. Add `getAgentSparklines(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "🤖 Agent Trajectories" section (publish-gated). If `has_per_agent_data: true`: for each agent, render a compact row — name chip (20-char truncated) + role tag (12-char max) + 40×15px inline SVG sparkline computed client-side from `trajectory` data (round → x, pct → y scaled 0–100 to 0–15px, `<polyline>` stroke in `color`). If `has_per_agent_data: false`: single line "Agent-level trajectory data not available for this simulation." "Copy sparklines URL" button below the section.
3. Add `GET /api/simulation/<id>/agents/sparklines` to `openapi.yaml` under Publish & Embed with `AgentSparklineResponse` + `AgentTrajectoryPoint` schemas. Add to `docs/API.md` under Publish & Embed. Add "Agent Stance Sparklines" to `docs/FEATURES.md`. Zero new deps.

---

### 2. CN+JP README

**Type:** Community
**Effort:** Small (hours)
**Impact:** @btcbabycow's "米罗莎要来了" (CN, May 16) and @m000_crypto's coverage (JP, May 17) confirm organic interest in the CN/JP developer communities — neither was prompted. A bilingual README converts that interest into a path in: developers who arrive from those communities via X or GitHub's Explore page see documentation in their language immediately. Direct support for the CN-locale contributor hyperstition (deadline 2026-06-15, 20 days out). PR #65 established the pattern; the content is already written in English. Re-eligible from May-18 (unbuilt).

**How:**
1. Add `README.zh.md` in the repo root — full Chinese translation of README.md. Lead with the headline in Chinese: "通用群智能引擎，1美元起，不到10分钟完成模拟". Key sections to translate: what MiroShark is, features list, quick start, API overview, $MIROSHARK token context, contribution guide. Technical terms: 模拟 (simulation), 群智能 (swarm intelligence), 智能体 (agent), 信念分布 (belief distribution), 共识方向 (consensus direction), 发布门控接口 (publish-gated surface). Keep all code blocks, CLI commands, and API routes in English — don't translate code. Add disclaimer at top: "此文档是英文 README 的翻译版本。如有差异，以英文原版为准。" Add `[中文](README.zh.md)` link at the top of README.md language row.
2. Add `README.ja.md` in the repo root — full Japanese translation. Headline: "汎用スウォームインテリジェンスエンジン — $1以下、10分未満". Technical terms: シミュレーション (simulation), スウォームインテリジェンス (swarm intelligence), エージェント (agent), 信念分布 (belief distribution), コンセンサス方向 (consensus direction). Same structure as the Chinese README. Disclaimer at top: "このドキュメントは英語版 README の翻訳です。相違がある場合は英語版を参照してください。" Add `[日本語](README.ja.md)` to README.md language row.
3. In `README.md`, add a language-switcher row between the badges and the main heading: `**[中文](README.zh.md) | [日本語](README.ja.md) | English**`. This change to README.md is the only modification outside the two new files. Zero new deps.

---

### 3. Scenario Clone Button

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Operators running variant analysis — same scenario, 5 more agents; same topic, neutral phrasing; same setup, different mode — currently copy-paste the scenario title, reset agent count, and manually re-configure each field. A "Clone" button on any completed or published sim fetches the source parameters and redirects to the new-sim form pre-filled. One-click to explore a variant. Directly reduces the per-iteration friction for the repeat-operator cohort that makes up MiroShark's most active users. Re-eligible from May-18 (unbuilt).

**How:**
1. Add `GET /api/simulation/<id>/clone-config` (~50 LoC inline in `simulation.py` or a new `clone.py`). No auth required; works on any completed sim (not publish-gated — you can clone your own private sim's config without exposing results). Response: `{scenario_title: str, scenario_context: str | null, agent_count: int, mode: str | null, locale: str | null}`. Reads these fields from `simulation_state.json`. Returns 404 for unknown sim_id. Response explicitly excludes all belief/result/trajectory data. Add 6 offline unit tests: known sim → config dict returned; `scenario_title` present; `agent_count` is integer; unknown sim → 404; `locale` defaults to `"en"` when absent from state; response contains no direction/belief fields.
2. Add `getCloneConfig(simId)` to `frontend/src/api/simulation.js`. In the simulation detail view and gallery card (wherever "Share" / "Embed" actions appear), add a "🔁 Clone" button. On click: fetch `/api/simulation/<id>/clone-config`; redirect to `/new?topic={encodeURIComponent(title)}&agent_count={n}&mode={mode}&locale={locale}`. In `NewSimView.vue`, read these query params on mount and pre-fill the corresponding form fields. Show a subtle `"Cloned from #{simId.slice(0,8)}"` banner (dismissible) above the pre-filled form.
3. Add `GET /api/simulation/<id>/clone-config` to `docs/API.md` under Simulation Management with a `CloneConfigResponse` schema. Add to `openapi.yaml`. Add "Scenario Clone" to `docs/FEATURES.md` under Simulation Management. Zero new deps.

---

### 4. Webhook Event Filtering

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Ten integrators are now named in ECOSYSTEM.md, and more are running quietly. Not all of them want a webhook fire for every sim completion — a Polymarket bot wants only Bullish + high-confidence signals; a research pipeline wants only excellent-quality outcomes; an alert system wants anything Bearish. `WEBHOOK_EVENTS` env var (comma-separated) filters dispatch at the source: `bullish`, `bearish`, `neutral`, `high_confidence` (≥75%), `medium_confidence` (50–74%), `good_quality`, `excellent_quality`. AND logic within the set. Blank = fire on all (existing behavior, backward-compatible). Zero new endpoints; ~40 LoC total change. Net-new.

**How:**
1. In the webhook dispatch logic (wherever the HTTP POST to `WEBHOOK_URL` is executed), add filter evaluation before dispatch. Parse `WEBHOOK_EVENTS = os.environ.get("WEBHOOK_EVENTS", "").lower()` into a set of tokens by splitting on commas and stripping whitespace. Define filter predicates: `"bullish"` → `sim_state["final_beliefs"]["direction"] == "Bullish"`; `"neutral"` → `direction == "Neutral"`; `"bearish"` → `direction == "Bearish"`; `"high_confidence"` → `confidence_pct >= 75`; `"medium_confidence"` → `50 <= confidence_pct < 75`; `"good_quality"` → `quality_health in ("good", "excellent")`; `"excellent_quality"` → `quality_health == "excellent"`. Logic: if event_tokens is empty → dispatch (existing path). Otherwise: evaluate all tokens; unrecognized tokens are skipped (future-proof). If all recognized tokens pass → dispatch; else → skip and log `{"webhook_filtered": true, "events_configured": [...], "sim_direction": ..., "confidence_pct": ..., "quality_health": ...}`. Add 8 unit tests: blank WEBHOOK_EVENTS → always dispatches; `"bullish"` → dispatches on Bullish, skips on Bearish; `"bullish,high_confidence"` → dispatches only when both pass; `"excellent_quality"` → dispatches on excellent, skips on good; unknown token alone → dispatches (no recognized tokens, treated as passthrough); multiple direction tokens → OR-like (dispatches if any direction matches); case-insensitive parsing; suppressed dispatch logs correctly.
2. Add `WEBHOOK_EVENTS=` to `.env.example` with a comment block: `# Comma-separated filter tokens for webhook delivery.\n# Leave blank to fire on all events.\n# Tokens: bullish, bearish, neutral, high_confidence, medium_confidence, good_quality, excellent_quality\n# Example: WEBHOOK_EVENTS=bullish,high_confidence`. Add a "Filtering Events" subsection to `docs/NOTIFICATIONS.md` under Webhook with the full token reference table (token, meaning, example use case). Zero new deps.
3. No openapi changes needed (this is a server-side config behavior, not an API contract). Add a note to `docs/API.md` Configuration section referencing `WEBHOOK_EVENTS` alongside `WEBHOOK_URL` and `WEBHOOK_SECRET`.

---

### 5. Ecosystem JSON Registry API

**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** ECOSYSTEM.md lists 10 integrators — it's the first formal inventory of who is building with MiroShark. Machine-readable, it becomes a live registry: Aeon can track integrator count programmatically; third-party directories can ingest the list; bots can watch for new additions without scraping Markdown. `GET /api/ecosystem.json` returns `{count, updated_at, integrators: [{name, x_handle, github_url, website_url}]}`. One JSON file maintained alongside ECOSYSTEM.md, one route that serves it. A `<link rel="alternate">` on the main page makes it auto-discoverable. The platform-level registry endpoint to complement the sim-level and operator-level surfaces. Net-new.

**How:**
1. Add `ecosystem.json` to the repo root, pre-populated with the 10 integrators from ECOSYSTEM.md. Structure: `{"count": 10, "updated_at": "2026-05-26", "integrators": [{"name": "AntFleet", "x_handle": "AntFleetDev", "github_url": "https://github.com/AntFleet/miroshark-bench", "website_url": null}, {"name": "Blue Agent", "x_handle": "blueagent_", "github_url": "https://github.com/madebyshun/blue-agent", "website_url": null}, ...]}` — alphabetical order, all 10 entries. Add to ECOSYSTEM.md contributing guidelines: "Also update `ecosystem.json` in the same PR, incrementing `count` and setting `updated_at`." Add a comment line to ECOSYSTEM.md: `<!-- Sync ecosystem.json when updating this table -->`.
2. Add `GET /api/ecosystem.json` route (~25 LoC in a new `ecosystem.py` blueprint or inline in a top-level routes file). Reads `ecosystem.json` from the repo root (resolved relative to the app root). Returns `Content-Type: application/json`; `Cache-Control: public, max-age=300`; `ETag: sha256(content)[:16]`; returns 304 on `If-None-Match` match. On missing file: 503 `{"error": "ecosystem registry not found"}`. Add 4 offline unit tests: returns valid JSON; `count` matches `integrators` list length; `ETag` header present; `updated_at` is a date string.
3. In the main app `<head>` (or the `/` root route), add `<link rel="alternate" type="application/json" href="/api/ecosystem.json" title="MiroShark Ecosystem Registry">` for auto-discoverability. Add `GET /api/ecosystem.json` to `openapi.yaml` under Community with an `EcosystemRegistry` + `IntegratorEntry` schema. Add to `docs/API.md` under Community. Add "Ecosystem Registry" to `docs/FEATURES.md`. Zero new deps.

---

## Selection Rationale

Today's batch spans the layer shift that ECOSYSTEM.md signals: the project now has an ecosystem, not just a codebase. The ideas respond to what that unlocks.

- **Per-Agent Stance Sparklines** (#1) — Re-eligible from May-18. The last visualization gap at the agent level. Aggregate curves exist; individual agent trajectories don't. Researchers studying swarm dynamics have been waiting for this since the surface layer was built. Per-agent data is in simulation_state.json; the rendering is client-side SVG. No external deps.
- **CN+JP README** (#2) — Re-eligible from May-18. Organic CN/JP coverage already exists. A bilingual README converts interest to contribution. The CN-locale contributor hyperstition (2026-06-15) is 20 days out; this is the most direct lever available. Pure content, zero backend work.
- **Scenario Clone Button** (#3) — Re-eligible from May-18. The repeat-operator cohort is the platform's most active user segment. Reducing variant-analysis friction from "re-enter everything" to one click compounds every research workflow that runs multiple sim iterations.
- **Webhook Event Filtering** (#4) — Net-new. Ten named integrators means ten different filtering needs. A `WEBHOOK_EVENTS` config env var respects them all without requiring downstream filtering logic in each integrator. 40 LoC, backward-compatible, no new endpoints.
- **Ecosystem JSON Registry** (#5) — Net-new. ECOSYSTEM.md is a human-readable list; `ecosystem.json` is its machine-readable twin. The smallest idea in the batch, and the one that most directly supports Aeon's own integrator-tracking and the hyperstition of ≥3 external integrators by 2026-07-31 (currently at 10+ named).
