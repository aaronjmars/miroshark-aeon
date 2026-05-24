# Repo Action Ideas — 2026-05-24

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,194 stars · 247 forks · 4 open issues (#95 French locale, #101 .env wildcard) · 2 open PRs (#104 gitignore, #105 Platform Stats API + Badge)
**Recent activity:** PR #103 (Nemotron demographic grounding — duckdb + huggingface_hub, breaks 31-PR zero-deps streak) merged 2026-05-23. PR #99 (Polymarket-ready prediction JSON, 15th surface) merged. PR #97 (WaybackClaw IPFS + Nostr, 16th surface) merged. Token: $0.0000175 (+25.3% 24h); ATH $0.0000436 (May 18); -59.9% from ATH; FDV $1.75M; buy/sell 2.63×. 1,194 stars, 247 forks.

## Ecosystem Context

Sixteen publish-gated surfaces now ship from a single sim. The platform-level API (PR #105, pending) closes the gap between "what individual sims say" and "what the platform as a whole says." Three new external contributors in 10 days (teifurin, antfleet-ops, voidfreud) signal that the architecture is stable enough for third-party work. AntFleet is running MiroShark as a benchmark target for a two-model consensus review pipeline.

With the surface count maturing and external contributors arriving, three gaps become visible at this baseline:

**The unfurl gap.** The share card (Open Graph) covers social platforms; Discord and Slack get rich embeds; Farcaster has Frame tags. But writing platforms — Notion, Ghost, Substack, WordPress — show bare links. All four implement the oEmbed spec. One `GET /oembed?url=` endpoint + a `<link rel="alternate">` discovery tag turns every paste of a `/share/<id>` URL into an auto-unfurled sim card — no user action required. Re-eligible from May 16 (unbuilt).

**The trajectory insight gap.** `trajectory.csv` gives raw per-round data; `chart.svg` shows the visual. Neither answers "when did bullish peak?" or "which round had the biggest swing?" without parsing. `GET /api/simulation/<id>/peak-round` returns machine-readable inflection points in one O(n) pass — the analytical summary quant tools need alongside signal.json. Re-eligible from May 16 (unbuilt).

**The identity gap.** 1,194 stars and growing, but operators who have run 30+ published sims have no shareable "all my work" link. `/profile/<operator_name>` is a per-operator gallery with a summary card. Every share page becomes a backlink; researchers can follow a specific operator's body of work. Re-eligible from May 16 (unbuilt, Medium effort).

Two net-new ideas round out the batch:

**The per-agent data gap.** Transcript.md is the only place agent-level data lives — name, role, initial belief, final stance, per-round contributions — but it's Markdown, requiring parsing. `GET /<id>/agents.json` is a machine-readable export of all agent personas. The 17th publish-gated surface; opens agent-level cross-sim analysis (do financial-analyst agents converge faster than retail traders?) without requiring transcript parsing.

**The programmatic search gap.** The gallery HTML has filters; `GET /api/gallery.json` (May-20 idea, not yet built) would be a full index. Neither serves the query pattern an LLM agent or research script actually needs: "give me all Bullish sims with confidence > 75% about crypto topics." `GET /api/search.json?q=&consensus=&min_confidence=` is the filtered, query-driven JSON endpoint — distinct from the unfiltered full-index of gallery.json.

Previously suggested ideas excluded from this batch (7-day window May 17–23): Private Share Link (May-22 #1, unbuilt); French Locale (May-22 #2, unbuilt); Polymarket-Ready Prediction JSON (May-22 #3, built as PR #99); Platform Aggregate Statistics API (May-22 #4, built as PR #105); Platform Stats Badge SVG (May-22 #5, built as PR #105); Belief Volatility Score (May-20 #3, unbuilt); Webhook Test Ping (May-20 #4, unbuilt); Gallery Public JSON (May-20 #5, unbuilt); Per-Agent Stance Sparklines (May-18 #3, unbuilt); Scenario Clone Button (May-18 #4, unbuilt); CN+JP README (May-18 #5, unbuilt). All 5 ideas below are net-new or re-eligible.

---

### 1. oEmbed Endpoint

**Type:** Integration
**Effort:** Small (hours)
**Impact:** Notion, Ghost, Substack, and WordPress all implement the oEmbed spec. A single `GET /oembed?url=` route + a `<link rel="alternate" type="application/json+oembed">` discovery tag in the share page `<head>` auto-unfurls every paste of a MiroShark share URL in any of these platforms into a sim card — scenario title, share-card thumbnail, and iframe embed — without any user action. Currently analysts citing MiroShark sims in Notion notes or Substack articles see a bare link. With this endpoint live, every organic reference becomes a rich preview. Re-eligible from May 16 (unbuilt).

**How:**
1. Add `backend/app/services/oembed_service.py` (~80 LoC, pure stdlib `re` + `urllib.parse`). `parse_sim_id_from_url(url: str) -> str | None`: regex `r'/share/([a-zA-Z0-9_-]{4,64})'` against the URL; rejects non-MiroShark domains (must match `BASE_URL` domain). `build_oembed_response(sim_state, sim_id, base_url) -> dict`: type `"rich"`, `provider_name: "MiroShark"`, `title: sim_state["scenario_title"][:100]`, `thumbnail_url: f"{base_url}/api/simulation/{sim_id}/share-card.png"`, `thumbnail_width: 1200`, `thumbnail_height: 630`, `width: 800`, `height: 500`, `html: f'<iframe src="{base_url}/embed/{sim_id}" width="800" height="500" frameborder="0" allowfullscreen></iframe>'`. Add `GET /oembed` route (no auth): validates `url` query param domain against `BASE_URL` (foreign domains → 404), parses `sim_id`, publish-gates (404 for unpublished), returns `Content-Type: application/json+oembed`. Add 8 offline unit tests in `test_unit_oembed.py`: valid share URL extracts sim_id, foreign domain → 404, unpublished → 404, response type `"rich"`, html contains `<iframe>`, thumbnail_url ends with `share-card.png`, title capped at 100 chars, `provider_name: "MiroShark"`. Extend `SURFACE_KEYS` + `surface_stats` with `oembed`.
2. In the share page `<head>` (same injection pattern as the existing `<meta property="og:*">` tags), add `<link rel="alternate" type="application/json+oembed" href="{base_url}/oembed?url={url_encoded_share_url}" title="{scenario_title[:60]}">`. Also add the XML variant `type="text/xml+oembed"` pointing to the same URL (Notion checks for the XML link — returning JSON is spec-compliant). Inject only for published sims, consistent with OG tag gating. Add `getOEmbedUrl(simId, baseUrl)` helper to `frontend/src/api/simulation.js`.
3. Add `GET /oembed` to `openapi.yaml` under Publish & Embed with an `OEmbedResponse` schema. Add "oEmbed Endpoint" to `docs/FEATURES.md` with a one-line compatibility note: "Auto-unfurl in Notion, Ghost, Substack, WordPress." Add to `docs/API.md` with a curl example. Zero new deps.

---

### 2. Peak-Round Belief Analytics

**Type:** Feature
**Effort:** Small (hours)
**Impact:** `trajectory.csv` has the raw data; `chart.svg` has the visual. Neither answers "which round did bullish peak?" or "which round had the biggest total swing?" without parsing. `GET /api/simulation/<id>/peak-round` returns `{bullish: {round, pct}, neutral: {round, pct}, bearish: {round, pct}, most_volatile_round: int, max_swing_pct: float, total_rounds: int}` in one O(n) pass over the trajectory. The machine-readable inflection-point summary quant tools and researchers need alongside signal.json. Re-eligible from May 16 (unbuilt).

**How:**
1. Add `backend/app/services/peak_round.py` (~120 LoC, pure stdlib `json` + `os`). `load_trajectory_rounds(sim_dir) -> list[dict]`: reads `trajectory.json`, returns per-round `{round: int, bullish_pct: float, neutral_pct: float, bearish_pct: float}` dicts; returns `[]` on missing or corrupt file. `compute_peak_rounds(rounds) -> dict | None`: returns `None` for empty input. Single O(n) pass: tracks per-stance `(max_pct, round_num)` and per-round `total_delta = |Δbullish| + |Δneutral| + |Δbearish|` (comparing to previous round; round 0 has delta 0). Returns `{bullish: {round: int, pct: float}, neutral: ..., bearish: ..., most_volatile_round: int, max_swing_pct: float, total_rounds: int}` — all pct values rounded to 2 dp. Add `GET /api/simulation/<id>/peak-round` (publish-gated; 404 `{"error": "no trajectory data yet"}` when None). Extend `SURFACE_KEYS` + `surface_stats` with `peak_round`. Add 10 offline unit tests in `test_unit_peak_round.py`: single-round trajectory → all peaks at round 1, multi-round → bullish peak at correct round, empty trajectory → None, `most_volatile_round` correct on known delta sequence, `max_swing_pct` rounds to 2 dp, published → 200, unpublished → 403, empty trajectory → 404, `total_rounds` matches input, surface_stats increment called.
2. Add `getPeakRound(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "📊 Peak Beliefs" section (publish-gated; gated on trajectory data — show only when endpoint returns 200). Layout: compact four-field grid — `Bullish peak: {pct}% at round {n}`, `Bearish peak: {pct}% at round {n}`, `Most volatile: round {n} (±{max}% swing)`, `Total rounds: {n}`. "Copy peak-round JSON URL" button.
3. Add `GET /api/simulation/<id>/peak-round` to `docs/API.md` under Analytics with a definition of `most_volatile_round`. Add `PeakRoundResponse` schema to `openapi.yaml`. Add "Peak-Round Analytics" to `docs/FEATURES.md` under Data Export & Analysis. Zero new deps.

---

### 3. Operator Profile Page

**Type:** Community
**Effort:** Medium (1-2 days)
**Impact:** 1,194 stars, multiple external contributors, and operators running dozens of published sims — but no per-operator view. `/profile/<operator_name>` is a per-operator gallery page: all their published sims, summary card (total sims, consensus distribution, average quality, total views). `GET /api/operator/<name>/profile` backs it. Every `/share/<id>` page becomes a backlink to the operator's profile, creating organic discovery loops. Researchers can follow a specific operator's body of work. Makes MiroShark a community platform, not just a tool. Re-eligible from May 16 (unbuilt).

**How:**
1. Add `backend/app/services/operator_service.py` (~160 LoC, pure stdlib `json` + `os`). `get_operator_sims(operator_name, sim_root) -> list[dict]`: scan all `sim_dir/` directories; filter `is_public=True` AND `operator.lower() == operator_name.lower()` (case-insensitive). Sort by `created_at` descending; cap at 100. Per sim: `{sim_id, scenario_title: str[:80], created_at, consensus: {direction, bullish_pct, neutral_pct, bearish_pct}, quality_health, total_rounds, surface_views: int}`. `build_operator_profile(operator_name, sims) -> dict`: `{operator, total_sims, consensus_distribution: {bullish_count, neutral_count, bearish_count}, avg_quality_tier: str (mode of quality_health), total_surface_views, sims}`. Unknown operators return `total_sims: 0` with empty sims list (no 404). Add `GET /api/operator/<name>/profile` (no auth; public). Sanitize `operator_name`: `[a-zA-Z0-9_.-]` max 80 chars, 400 on invalid. Add `ProfileResponse` + `OperatorSimSummary` schemas to `openapi.yaml`. Add 10 offline unit tests: unknown operator → `total_sims: 0`, 3 sims → `total_sims: 3`, unpublished excluded, `consensus_distribution` counts correct, `surface_views` sum correct, 100-sim cap respected, case-insensitive name match, `avg_quality_tier` non-empty, valid name → 200, special chars → 400.
2. Add `OperatorProfileView.vue` in `frontend/src/views/`. Route `/profile/:operatorName` (add to router). On mount: validate `operatorName`; redirect to `/explore` with error toast if invalid. Fetch `GET /api/operator/<operatorName>/profile`. Layout: header card with operator name + stats row (total sims, consensus mini-bar in belief colors, avg quality, total views). Below: sim grid using the existing `SimCard` component. Empty state for unknown or zero-sim operators. "Share this profile" button copies `/profile/<name>` URL. Add `getOperatorProfile(operatorName)` to `frontend/src/api/simulation.js`.
3. In the share page (`/share/<id>`), add "by [operator_name]" attribution text linking to `/profile/<operator_name>` — visible only when the `operator` field is non-empty. This propagates organic backlinks from every published share. Add `GET /api/operator/<name>/profile` to `docs/API.md`. Add "Operator Profile" to `docs/FEATURES.md` under Gallery & Discovery. Zero new deps.

---

### 4. Agent Persona Export JSON

**Type:** Feature
**Effort:** Small (hours)
**Impact:** Agent-level data — name, role, initial belief, final stance, rounds participated, per-round belief — exists only in `transcript.md` (Markdown text requiring parsing). `GET /<id>/agents.json` exports a structured JSON array of all agent personas, making the 17th publish-gated surface and the first per-agent data surface. Researchers studying swarm dynamics (do financial-analyst agents align faster than retail traders?) currently need to parse Markdown; this reduces it to a single API call. Cross-sim agent analysis — running the same scenario with different persona mixes and comparing convergence — becomes trivial.

**How:**
1. Add `backend/app/services/agent_export.py` (~150 LoC, pure stdlib `json` + `os`). `extract_agents(sim_state) -> list[dict]`: reads the agents array from `simulation_state.json` (the same structure the simulation runner populates per round). Per agent: `{agent_id: str, name: str, role: str, initial_belief: {bullish_pct, neutral_pct, bearish_pct}, final_stance: str, rounds_participated: int, final_confidence: float}`. If per-round trajectory exists, include `trajectory: [{round: int, stance: str, pct: float}]` for each agent. `build_agents_payload(sim_state, sim_id) -> dict`: wrapper with `{sim_id, scenario_title, total_agents: int, completed_at: str, agents: list[dict]}`. `Content-Type: application/json`; `Cache-Control: public, max-age=300`. Add `GET /api/simulation/<id>/agents.json` (publish-gated; 404 `{"error": "no agent data"}` when empty). Extend `SURFACE_KEYS` + `surface_stats` with `agents_json`. Add 10 offline unit tests in `test_unit_agent_export.py`: published sim → list of dicts, each dict has required fields, unpublished → 403, empty agents → 404, `total_agents` matches list length, `final_stance` is one of Bullish/Neutral/Bearish, `rounds_participated` is int ≥ 0, `sim_id` in payload matches route param, `completed_at` is ISO-8601, `surface_stats` increment called.
2. Add `getAgentsJsonUrl(simId)` + `getAgentsJson(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "🤖 Agent Data" section (publish-gated). Layout: agent count badge + "Download agents.json" anchor + "Copy agents.json URL" button. Below: collapsible agent roster table showing name, role, final stance (colored chip), confidence. Add "Agent Persona Export" to `docs/API.md` under Data Export & Analysis with a curl example + cross-sim analysis pattern (pipe to `jq '[.agents[] | select(.final_stance == "Bullish")]'`).
3. Add `AgentsPayload` + `AgentSummary` schemas to `openapi.yaml` under Data Export. Add `GET /api/simulation/<id>/agents.json` to `docs/FEATURES.md` under Data Export & Analysis. Add to the EmbedDialog surface count ("17th publish-gated surface"). Zero new deps.

---

### 5. Simulation Search JSON API

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The gallery HTML at `/explore` has interactive filters; a planned `GET /api/gallery.json` would return all public sims as a full index. Neither serves the query-driven pattern an LLM agent, research script, or integration actually needs: "show me Bullish sims with confidence > 75% about crypto topics, sorted by most recent." `GET /api/search.json?q=&consensus=&min_confidence=&sort=` is the filtered, query-driven JSON endpoint — distinct from a full-index dump. Downstream: an Aeon `feature-discovery` skill can query for the strongest signals before deciding what to build next; AntFleet's benchmark pipeline can find the highest-confidence sims automatically; external dashboard builders get a single curl command.

**How:**
1. Add `backend/app/api/search.py` (new blueprint, ~130 LoC, pure stdlib `json` + `os` + `re`). `GET /api/search.json` — accepted query params: `q` (full-text match against `scenario_title` + `scenario_context`, case-insensitive substring), `consensus` (`bullish`/`neutral`/`bearish`, filters by `final_beliefs.direction`), `min_confidence` (float, filters sims where `signal_service.compute_signal` confidence_pct ≥ value), `max_confidence` (float), `sort` (`recent` default / `confidence_desc` / `views_desc`), `limit` (int, 1–100, default 20). Reads from the same sim_root scan as the gallery service. Filters applied in order: is_public + status=completed → q → consensus → confidence range → sort → limit. Response: `{results: list[{sim_id, title, created_at, direction, confidence_pct, quality_health, total_rounds, surface_views}], total_matching: int, query: {q, consensus, min_confidence, max_confidence, sort, limit}}`. `Cache-Control: public, max-age=30` (shorter than gallery — search results are query-specific). No ETag (queries vary). Add 10 offline unit tests in `test_unit_search.py`: empty query returns all public completed sims (up to limit), `q=bitcoin` matches title substring, `consensus=bullish` filters correctly, `min_confidence=75` excludes lower-confidence sims, `sort=confidence_desc` ordered correctly, `limit=5` caps results, unpublished/incomplete excluded, `total_matching` correct after filter, combined params stack correctly, invalid `consensus` → 400.
2. Register `search_bp` in `backend/app/api/__init__.py` + `backend/app/__init__.py`. Add `<link rel="search" type="application/json" href="/api/search.json">` in the gallery page `<head>` for auto-discoverability. In the `/explore` gallery, add a small "JSON API" link near the search bar pointing to `/api/search.json?q={currentQuery}` — if a user searches in the HTML gallery, the link opens the equivalent JSON endpoint. No new frontend view required.
3. Add `GET /api/search.json` to `openapi.yaml` under Gallery & Discovery with a `SearchResults` schema and all query param definitions. Add to `docs/API.md` under Gallery & Discovery with a multi-param curl example. Add "Programmatic Simulation Search" to `docs/FEATURES.md`. Zero new deps.

---

## Selection Rationale

Today's batch operates at three layers: distribution reach, analytical depth, and community identity.

- **oEmbed** (#1) — Re-eligible from May 16. The auto-unfurl gap for writing platforms. Notion, Ghost, Substack are where researchers and analysts publish; every organic MiroShark citation in those platforms becomes a rich preview card. ~80 LoC, pure stdlib, zero frontend changes beyond two `<link>` tags.
- **Peak-Round Analytics** (#2) — Re-eligible from May 16. The analytical counterpart to trajectory.csv and chart.svg. Quant operators want a machine-readable inflection point without parsing 100 rounds of CSV. One O(n) scan, one JSON endpoint. Completes the analytical quadrant.
- **Operator Profile** (#3) — Re-eligible from May 16. 1,194 stars and multiple repeat operators, but no per-operator identity layer. Every share page becomes a backlink to the operator's profile; researchers can follow a specific operator's work. Medium effort but the network-effect payoff scales directly with star count. The community layer that was missing at 1,164 stars is still missing at 1,194 stars.
- **Agent Persona Export** (#4) — Net-new. The 17th publish-gated surface and the first per-agent data surface. Researchers studying swarm dynamics need structured agent data, not Markdown transcript parsing. Cross-sim agent analysis becomes a one-liner with `jq`. Follows the existing zero-deps surface pattern exactly.
- **Simulation Search JSON API** (#5) — Net-new. Distinct from the planned gallery.json full-index (excluded May 20): search is query-driven and filtered. LLM agents, research scripts, and external dashboards all need to query for specific sim characteristics rather than download a full index. AntFleet's benchmark pipeline is the immediate use case.
