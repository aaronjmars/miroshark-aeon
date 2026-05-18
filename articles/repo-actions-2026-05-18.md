# Repo Action Ideas — 2026-05-18

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,172 stars · 236 forks · 3 open issues · 2 open PRs (#89 Neo4j password security fix; #90 Farcaster Frame v2, opened today)
**Recent activity:** 4th consecutive ATH session today ($0.0000377 intraday, FDV $3.32M); PRs #79–#87 merged in 14 days; notification quadrant complete (webhook → Discord → Slack → SMTP email); Farcaster Frame v2 just opened as PR #90. 26-PR zero-new-deps streak (#57 → #87 → #90 candidate).

## Ecosystem Context

The last two weeks closed three independent arcs simultaneously: the notification quadrant (PR #83 Discord/Slack + PR #87 SMTP email), the on-chain provenance chain (PR #80 Jupyter → PR #84 DKG anchor → PR #85 chart SVG), and the Base-chain distribution gap (PR #90 Farcaster Frame v2, opened today). The token's move to $3.32M FDV — with btcbabycow's CN tweet "米罗莎要来了" on May 16 and the first JP coverage on May 17 — introduces an international audience dimension that the codebase doesn't yet address.

Three data-export gaps remain unfilled from the May 10 batch:

**The signal gap.** `trajectory.csv`, `chart.svg`, and `reproduce.json` give you the data; `peak-round` (May-16 batch, unbuilt) gives you inflection points. Neither gives you a machine-readable *trading signal* — a structured conclusion that a quant tool, alert system, or Zapier workflow can act on directly. `GET /api/simulation/<id>/signal.json` returns `{direction, confidence_pct, risk_tier, bullish_pct, neutral_pct, bearish_pct, quality_health, signal_generated_at}` — derived from the final belief distribution plus agent consensus quality. No new computation: it aggregates fields already present in `simulation_state.json` and `quality.json`.

**The archive gap.** A researcher finishing a sim has to download six separate surfaces (share card, chart SVG, trajectory CSV, reproduce.json, Jupyter notebook, DKG citation URL) from six separate routes. `GET /api/simulation/<id>/archive.zip` packages all of them into one timestamped ZIP with a `manifest.json` (surface name → filename → SHA-256 → URL). One command, offline copy. The feature skill pattern is established across `trajectory_export.py`, `notebook_export.py`, and `repro_export.py` — archive is a compositor.

**The agent-sparkline gap.** The chart SVG shows the aggregate belief curve; `trajectory.csv` gives per-round totals. Neither shows *how individual agents moved*. `GET /api/simulation/<id>/agent-sparklines` returns per-agent stance trajectories — either as an SVG grid (one 20px-tall sparkline per agent, labeled) or as JSON for client-side rendering. Lets researchers see disagreement scatter at a glance and identify which agent caused a consensus flip.

Two net-new ideas complete the batch:

**The viral loop gap.** PR #71 (shareable scenario links) added URL params that pre-fill the New Sim form. Every `/share/<id>` page shows a finished sim but has no path for a viewer to *run a variant*. A "Run this scenario →" button on the share page generates a `/new?title=...&config=...` URL from the sim's stored config and navigates to it — no auth, no new backend, ~30 minutes of frontend work. Converts passive share-page viewers into active sim runners; closes the viral loop that ends at `/share/<id>` today.

**The international audience gap.** Three signals this week: btcbabycow's CN tweet "米罗莎要来了" (May 16, 29L/3RT), first JP coverage @m000_crypto (May 17), and `$MIROSHARK` 24h volume $1.18M with the Base-chain buy cluster growing. A `README.zh.md` (Chinese translation) + `README.ja.md` (Japanese translation) + language-badge row in `README.md` directly lowers the contribution barrier for the audience that is already arriving. The CN-locale contributor hyperstition (target: 2026-06-15) needs this surface to exist before a contributor can file a PR against it.

Previously suggested ideas excluded from this batch (last 7 days, May 11–18): oEmbed Endpoint (May 16 #1, unbuilt); Farcaster Frame (May 16 #2, built as PR #90 today); Email Notifications (May 16 #3, built as PR #87); Peak-Round Analytics (May 16 #4, unbuilt); Operator Profile (May 16 #5, unbuilt); Private Share Link (May 14 #5, unbuilt); Director Events (May 14 #2, exists); Comparative Run View (May 14 #4, exists); Lifecycle Webhooks (May 12 #1, deferred). Trading Signal JSON, Simulation Archive Bundle, and Per-Agent Stance Sparklines are re-eligible from May 10 batch (8 days ago, unbuilt).

---

### 1. Trading Signal JSON

**Type:** Feature
**Effort:** Small (hours)
**Impact:** Turns every finished sim into a machine-readable trading signal that quant tools, alert pipelines, and Zapier/Make automations can consume directly — no CSV parsing, no chart reading. `direction` (Bullish/Neutral/Bearish) + `confidence_pct` (how far the leading stance is from 33.3%) + `risk_tier` (derived from quality health) gives a one-field action primitive. Closes the gap between "a sim produces data" and "a sim produces a signal."
**How:**
1. Add `backend/app/services/signal_service.py` (~90 LoC, pure stdlib). `compute_signal(sim_state: dict) -> dict | None`: reads `final_beliefs.bullish_pct`, `final_beliefs.neutral_pct`, `final_beliefs.bearish_pct`, and `quality_health` from `simulation_state.json`. `direction`: whichever of the three stances holds the plurality. `confidence_pct`: `(leading_pct - 33.333) / 66.667 * 100` rounded to 1 dp (0 = pure split, 100 = unanimous). `risk_tier`: map quality health strings (`"high"` → `"low-risk"`, `"medium"` → `"medium-risk"`, `"low"` / `"N/A"` → `"high-risk"`). Add `signal_generated_at` (ISO-8601 UTC from sim `completed_at`). Returns `None` if sim not completed. Add `GET /api/simulation/<id>/signal.json` (publish-gated; 404 with `{"error": "simulation not complete"}` when `None`). Add 8 offline unit tests: unanimous bullish → confidence near 100, pure three-way split → confidence 0, quality-to-risk-tier mapping for all 4 inputs, unpublished → 403, incomplete → 404, `signal_generated_at` present and ISO-formatted.
2. Add `getSignalJson(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "📡 Trading Signal" section (publish-gated; visible when sim is completed). Shows `direction` in the consensus color, `confidence_pct` as a horizontal bar, `risk_tier` as a badge. "Copy signal.json URL" button (same copy-URL pattern as `trajectory.csv`, `reproduce.json`).
3. Add `GET /api/simulation/<id>/signal.json` to `docs/API.md` under Data Export with field definitions. Add `SignalResponse` schema to `openapi.yaml`. Add "Trading Signal JSON" to `docs/FEATURES.md` under Data Export. Extend `SURFACE_KEYS` frozenset + `surface_stats` increment. Zero new deps.

---

### 2. Simulation Archive Bundle

**Type:** Feature
**Effort:** Small (hours)
**Impact:** A researcher finishing a sim currently fetches six surfaces across six HTTP calls. `GET /api/simulation/<id>/archive.zip` delivers all published data surfaces in one download: `share-card.png`, `chart.svg`, `trajectory.csv`, `reproduce.json`, `notebook.ipynb`, and `signal.json` (when available), plus a `manifest.json` listing each file's SHA-256 and source URL. Operators can "take a sim offline" in one curl command; citation workflows get a canonical archive. Compositional: delegates to `trajectory_export`, `notebook_export`, `repro_export`, `signal_service` — no new computation.
**How:**
1. Add `backend/app/services/archive_service.py` (~130 LoC, pure stdlib `zipfile` + `io` + `json` + `hashlib` + `datetime`). `collect_surfaces(sim_dir, sim_id, base_url) -> list[dict]`: builds a list of `{filename, content: bytes, source_url, sha256}` entries. Per surface: read `share-card.png` if present (fall through if missing); call `trajectory_export.build_csv_bytes()` and `notebook_export.build_notebook_bytes()` (or equivalent helpers — wrap if they don't expose byte-stream APIs); call `signal_service.compute_signal()`; serialize `reproduce.json` from `repro_export`. Each surface is optional — omit missing files rather than erroring. `build_archive_zip(surfaces: list[dict]) -> bytes`: creates an in-memory ZIP via `zipfile.ZipFile(io.BytesIO(), 'w', zipfile.ZIP_DEFLATED)`; writes each surface file; writes `manifest.json` last (`[{filename, sha256, source_url, size_bytes, generated_at}]`). `generated_at`: ISO-8601 UTC. Add `GET /api/simulation/<id>/archive.zip` (publish-gated; `Content-Disposition: attachment; filename="miroshark-{sim_id[:8]}-{date}.zip"`; `Content-Type: application/zip`). Add 8 offline unit tests: empty surface list → zip contains only `manifest.json`, manifest SHA-256 matches file content, missing surface skipped, `Content-Disposition` header present, unpublished → 403, `generated_at` in manifest is ISO-formatted, zip bytes parse without error, manifest has correct `size_bytes`.
2. Add `getArchiveUrl(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "📦 Archive Bundle" section (publish-gated; completed sims only). Single "Download archive.zip" button linking to the archive URL. Tooltip: "All data surfaces in one file — share-card, chart, trajectory, reproduce.json, notebook, manifest."
3. Add `GET /api/simulation/<id>/archive.zip` to `docs/API.md` under Data Export with the manifest schema. Add `ArchiveManifestEntry` schema to `openapi.yaml`. Add "Simulation Archive Bundle" to `docs/FEATURES.md`. Zero new deps.

---

### 3. Per-Agent Stance Sparklines

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** The aggregate belief chart (PR #85) shows where the consensus went; `trajectory.csv` shows per-round totals. Neither shows *how individual agents moved*. An agent-sparkline view reveals whether consensus was driven by a few outlier agents flipping late, whether a specific agent was a persistent contrarian, or whether the swarm converged uniformly. Quant researchers and model-auditors need this to trust a sim's conclusion — "bullish at 72%" is stronger when 18/20 agents moved monotonically toward it than when two agents oscillated wildly and pulled the final number. `GET /api/simulation/<id>/agent-sparklines.svg` returns an SVG grid of per-agent belief evolution.
**How:**
1. Add `backend/app/services/agent_sparklines.py` (~180 LoC, pure stdlib `xml.etree.ElementTree` + `json` + `os`). `load_agent_rounds(sim_dir) -> list[dict]`: reads `trajectory.json` for per-round, per-agent stance data (check whether this level of detail is stored — if per-agent stances are in `round_detail.json` or similar; if not, check `simulation_state.json`'s agent log entries; adapt to whichever source holds per-agent-per-round stance). `build_sparklines_svg(agent_rounds: list[dict], width=600, row_height=24, label_width=120) -> str`: deterministic SVG using `xml.etree.ElementTree`. Layout: one row per agent; x-axis = rounds; y-axis = stance (0 = Bearish, 0.5 = Neutral, 1 = Bullish); each row is a `<polyline>` with the three-level stepped trace. Color per stance: `#22c55e` / `#6b7280` / `#ef4444` (matching chart SVG). Agent label left-truncated to 20 chars. Header row with round tick marks. `Content-Type: image/svg+xml`. Add `GET /api/simulation/<id>/agent-sparklines.svg` (publish-gated; 404 `{"error": "no per-agent round data"}` when `agent_rounds` is empty). Add 10 offline unit tests: single-agent single-round → valid SVG bytes, multi-agent 5-round → correct `<polyline>` count, label truncated at 20 chars, deterministic (same input → same bytes), stance colors present in SVG output, header round ticks present, unpublished → 403, empty data → 404, SVG root tag is `<svg>`, width/height attributes set.
2. Add `getAgentSparklines(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "🫧 Agent Sparklines" section (publish-gated; gated on per-agent data availability — hide section if endpoint returns 404). Shows the SVG inline as `<img src="/api/simulation/{simId}/agent-sparklines.svg">`. "Copy agent-sparklines.svg URL" button. "Copy embed code" button with `<img>` tag.
3. Add `GET /api/simulation/<id>/agent-sparklines.svg` to `docs/API.md` under Data Export. Add "Agent Sparklines SVG" to `docs/FEATURES.md` under Data Export & Visualization. Add `AgentSparklinesRoute` description to `openapi.yaml` (note: binary SVG response, not JSON schema). Extend `SURFACE_KEYS` frozenset. Zero new deps.

---

### 4. Scenario Clone Button on Share Page

**Type:** Growth
**Effort:** Small (hours)
**Impact:** Every `/share/<id>` page ends the user journey — view the sim, nothing to do next. PR #71 (shareable scenario links) added `/new?title=...&config=...` URL params that pre-fill the New Sim form. Wiring a "Run this scenario →" button on the share page generates that URL from the current sim's stored config and navigates to it. No auth required, no new backend, no new deps. A share-page viewer who finds a sim interesting becomes an active user in one click. Closes the viral loop that currently dead-ends at the share page and turns every distributed share URL into a soft acquisition funnel.
**How:**
1. In `backend/app/api/share.py` (or wherever the share page HTML is assembled), add a `clone_url` field to the template context: `clone_url = url_for('new_sim') + '?' + urllib.parse.urlencode({'title': sim_state['scenario_title'][:200], 'config': json.dumps(sim_state.get('agent_config', {}))})`. Gate this on the sim being published (same condition as the Frame meta block). The URL format must match what PR #71's New Sim form expects — read PR #71's frontend code to confirm the exact param names before implementing. If `agent_config` is large, truncate or omit to stay within URL length limits (~2000 chars); title alone is sufficient if config pushes over the limit.
2. In the share-page template (the HTML block in `share.py` or the Vue share view — whichever is authoritative), add a "Run this scenario →" button below the scenario title and belief summary, before the embed section. Style: secondary button, not primary (the primary CTA remains the existing "Open in MiroShark" or sim-detail link). Label: "Run this scenario →". Opens the clone URL in the same tab (not `_blank` — keeps the user in the funnel). Add a "Share this sim" social-share bar next to it (the Warpcast compose URL from PR #90 + the existing share URL copy action). This groups all outbound actions in one place. Add 4 offline tests: `clone_url` present in published sim HTML, `clone_url` absent from unpublished sim HTML, `clone_url` contains `title` param, `clone_url` does not contain raw secrets.
3. No new backend route, no schema changes, no new deps. Add a one-sentence note to `docs/FEATURES.md` under Share & Discovery: "Published simulations include a 'Run this scenario →' link that pre-fills the New Sim form with the original scenario title and agent configuration."

---

### 5. Chinese + Japanese README Translations

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** This week delivered three external signals: btcbabycow CN tweet "米罗莎要来了" (May 16, 29L/3RT), first JP coverage @m000_crypto (May 17), and growing Base-chain buy volume concentrated in the crypto-native East Asian cluster. MiroShark's README is English-only. A `README.zh.md` (Simplified Chinese) + `README.ja.md` (Japanese) + language-badge row in `README.md` lowers the contribution barrier for the audience already arriving. Directly targets the CN-locale contributor hyperstition (target: ≥1 CN-locale PR by 2026-06-15). A CN star or fork in the GitHub star list is more likely when the first page they see is in their language.
**How:**
1. Add `README.zh.md` (Simplified Chinese) and `README.ja.md` (Japanese) as full translations of `README.md`. Translate: title, tagline, the Features table (feature names + one-line descriptions), Quick Start commands (keep code blocks as-is; translate surrounding prose), API Usage section, Configuration env-var descriptions, and the Contributing section. Do not translate code blocks, command outputs, env-var names, route paths, or the "Built autonomously by Aeon" footnote. For accuracy: use precise technical vocabulary for AI/ML terms (中文: 群体智能引擎, 信念分布, 共识方向; 日本語: 群集知能エンジン, 信念分布, コンセンサス方向). Do not machine-translate idioms — write clear, accurate technical prose. Keep the same heading hierarchy and section order as `README.md`.
2. Add a language badge row at the top of `README.md` (below the existing badges, above the tagline): `[🇨🇳 中文](README.zh.md) · [🇯🇵 日本語](README.ja.md)`. Use the existing badge styling pattern (Shields.io flat badges or inline Markdown links — match whichever the repo uses). Add reciprocal links at the top of each translation file pointing back to `README.md` and the other translation.
3. Add a "Translations" note to `CONTRIBUTING.md` (if it exists; otherwise add a comment in `README.md` under Contributing): "Translation improvements are welcome — open a PR against `README.zh.md` or `README.ja.md`." This makes CN/JP contributors feel explicitly invited and creates the first contribution surface targeted at non-English speakers. Zero new deps; no code changes.

---

## Selection Rationale

Today's batch operates in the space between the May-10 unbuilt ideas (now eligible after 8 days) and two new angles opened by this week's events.

- **Trading Signal JSON** (#1) — The data-to-action bridge. Five export surfaces exist (CSV, SVG, JSON, notebook, DKG); none produces a *signal*. One route, no new computation, closes the quant-tool integration gap.
- **Simulation Archive Bundle** (#2) — A researcher tax reduction. Six surfaces, one ZIP. The compositional pattern is established across three existing export services. Medium-value for operators, high-value for researchers building citation chains.
- **Per-Agent Stance Sparklines** (#3) — The transparency layer. Aggregate consensus is a number; the per-agent trace is the *argument*. Researchers who need to trust a sim's conclusion need to see how agents moved, not just where they ended. Medium effort due to per-agent data sourcing, but the SVG rendering pattern is proven in PR #85.
- **Scenario Clone Button** (#4) — The cheapest viral mechanic available. PR #71's pre-fill URL already exists; the button is 30 minutes of frontend work. Every share page is currently a dead end for an interested viewer; this converts dead-end shares into active-user acquisition events.
- **Chinese + Japanese README** (#5) — Timing-sensitive. Three external signals this week (CN tweet, JP coverage, East Asian buy cluster) converge on a single missing surface. The CN-locale contributor hyperstition has a June 15 deadline. A translation has to exist before a CN contributor can file a PR against it.
