# Repo Action Ideas — 2026-05-20

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,179 stars · 239 forks · 0 open issues · 0 open PRs (PR #92 archive bundle opened today; PRs #89/90/91 merged 2026-05-19)
**Recent activity:** PR #92 (Simulation Archive Bundle, 12th publish-gated surface, 28-PR zero-new-deps streak) opened today. Token consolidating at $0.00003044 / FDV $3.04M after ATH $0.0000436 on May 18. External integrators: @revaultdrops, @blueagent_, @Concept_felipe ("100M+ potential as autonomous internet infrastructure"). 1,179 stars, 4th consecutive external contributor week.

## Ecosystem Context

The last ten days closed three arcs simultaneously: the quant-tools surface layer (signal.json → archive.zip), the Base-chain social layer (Farcaster Frame v2), and the notification quadrant (SMTP email). Twelve publish-gated surfaces now ship from a single sim: researchers pull CSV/JSONL/notebook/reproduce.json/cite.bib; institutions anchor DKG; social audiences share card/replay-GIF/frame-metadata; quants consume signal.json; embed-builders link chart.svg/thread; and now everyone grabs archive.zip in one shot.

The surface count is no longer the bottleneck. Three new gaps become visible from the 12-surface baseline:

**The badge gap.** Every published sim produces a signal.json with a direction and confidence_pct. But a researcher or operator who wants to link to a live belief state from a GitHub README, Notion page, or personal site has no lightweight embed. A `badge.svg` endpoint returns a Shields.io-compatible flat badge — left half "MiroShark", right half "Bullish 72%" in the belief color — that any `<img>` tag or Markdown `![]()` reference can embed. The badge is a live signal that updates as the sim state changes, not a static screenshot.

**The citation gap.** reproduce.json exports every parameter; the DKG Knowledge Asset anchors the hash on-chain. But academic papers cite sources as BibTeX. A `cite.bib` endpoint completes the citation arc: reproduce.json (reproduce it) → notebook.ipynb (analyze it) → cite.bib (cite it). One curl command drops a citation-ready `@misc{miroshark-...}` block into a `.bib` file, with the reproduce.json SHA-256 in the `note` field and the DKG Asset URI in `annote` (when available). Zotero and Mendeley import from URL — the endpoint address is the import URL.

**The volatility gap.** signal.json answers "what direction did the sim conclude?" and "how confidently?" But two sims can both conclude "Bullish 65%" — one converged monotonically in round 5, the other oscillated for 50 rounds before landing there. A volatility score quantifies that difference. `GET /api/simulation/<id>/volatility` computes round-over-round stance deltas: mean absolute swing, max-swing round, standard deviation, and a `regime` label (Monotonic / Noisy / Oscillating). High confidence + low volatility = strong signal; high confidence + high volatility = unstable consensus that might reverse. The risk metric missing from the current quant stack.

Two operational gaps round out the batch:

**The webhook setup gap.** Operators configure `WEBHOOK_URL` and immediately face an unknown: did it work? The only current verification path is running a full simulation and reading the delivery log (PR #73). A `POST /api/config/webhook/test` fires a realistic test payload — HMAC-signed if `WEBHOOK_SECRET` is set, same format as real dispatches — and returns status code, latency, and response preview. 2 seconds, not 10 minutes. The DX gap every Zapier / n8n / n8n workflow setup hits first.

**The LLM-discoverability gap.** The gallery (`/explore`) is HTML. Automated consumers — scripts, bots, downstream LLM agents — can't query what simulations exist without scraping HTML. `GET /api/gallery.json` returns all public sims as a machine-readable JSON array with `{sim_id, title, direction, confidence_pct, quality_health, total_rounds, surface_views}`. Cacheable with ETags for polling. The endpoint that makes @Concept_felipe's "autonomous internet infrastructure" framing literal: an agent can index what simulations exist with one curl call.

Previously suggested ideas excluded from this batch (last 7 days, May 13–20): Private Share Link (May-14 #5); oEmbed (May-16 #1), Peak-Round Analytics (May-16 #4), Operator Profile (May-16 #5); Per-Agent Stance Sparklines (May-18 #3), Scenario Clone Button (May-18 #4), CN+JP README (May-18 #5). Status Badge SVG, BibTeX Academic Citation, Belief Volatility Score, Webhook Test Ping, and Gallery Public JSON are all net-new.

---

### 1. Consensus Status Badge SVG

**Type:** Growth
**Effort:** Small (hours)
**Impact:** Any GitHub README, Notion page, or blog can embed a live belief badge — `![MiroShark Badge](https://your-instance/api/simulation/{id}/badge.svg)` — that updates as the sim state changes. Flat Shields.io-compatible layout: left "MiroShark" on `#555`, right "{direction} {confidence_pct}%" on `#22c55e` / `#6b7280` / `#ef4444`. Turns every distributed share URL into a pull point for new visitors who see the badge in a researcher's README. EmbedDialog adds a "Status Badge" section with live preview, Copy badge URL, and Copy Markdown.
**How:**
1. Add `backend/app/services/badge_service.py` (~80 LoC, pure stdlib `xml.etree.ElementTree`). `build_badge_svg(direction, confidence_pct) -> str`: flat Shields.io-style SVG — 27px height, proportional widths, `font-family="DejaVu Sans,Verdana,Geneva,sans-serif"`, 11px font, pill ends via `rx="3"`, left label "MiroShark" on `#555555`, right value "{direction} {confidence_pct}%" on `#22c55e` (Bullish) / `#6b7280` (Neutral) / `#ef4444` (Bearish). Add `GET /api/simulation/<id>/badge.svg` (publish-gated; `Content-Type: image/svg+xml`; `Cache-Control: max-age=60`). Add 8 offline unit tests: valid XML root, direction text present, fill color matches direction for all three stances, width/height set, cache header present, unpublished → 403, incomplete → 404, SVG is well-formed. Extend `SURFACE_KEYS` + `surface_stats` with `badge_svg`.
2. Add `getBadgeUrl(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue` add a "🏷️ Status Badge" section (publish-gated). Shows `<img src="...badge.svg">` live preview, "Copy badge URL" button, "Copy Markdown" button (`![MiroShark Belief Badge]({badgeUrl})`).
3. Add `GET /api/simulation/<id>/badge.svg` to `docs/API.md` under Publish & Embed. Add to `openapi.yaml` as SVG binary response. Add "Status Badge" to `docs/FEATURES.md`. Zero new deps.

---

### 2. BibTeX Academic Citation Export

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Closes the academic citation arc: reproduce.json (reproduce it) → notebook.ipynb (analyze it) → cite.bib (cite it). `GET /api/simulation/<id>/cite.bib` returns one `@misc{miroshark-{id[:12]}, author={...}, title={...}, year={...}, url={...}, note={SHA-256: ...}, annote={DKG URI: ...}}` block — paste into LaTeX, import to Zotero by URL, or drag into Mendeley. The reproduce.json SHA-256 in `note` ensures the citation is reproducible-linked. Researchers writing papers citing a MiroShark sim currently have no machine-readable citation format; this adds one in ~70 LoC of stdlib.
**How:**
1. Add `backend/app/services/bibtex_service.py` (~70 LoC, pure stdlib). `build_bibtex(sim_state, sim_id, base_url) -> str`: citation key `miroshark-{sim_id[:12]}`; `author` from `sim_state.get("operator", "MiroShark")`; `title` from `scenario_title[:200]` with BibTeX special-char escaping (`&`, `%`, `_`, `#`, `~`, `^`); `year`/`month` from `completed_at`; `url` = share URL; `howpublished` = reproduce.json URL; `note` = SHA-256 from reproduce.json (read from sim_dir if present); `annote` = DKG Knowledge Asset URI if stored in sim_state. `Content-Type: text/plain`; `Content-Disposition: inline; filename="miroshark-{sim_id[:12]}.bib"`. Add 8 offline unit tests: key contains sim_id prefix, special chars escaped in title, SHA-256 in note when available, DKG URI in annote when present, year/month correct, author defaults to "MiroShark" when blank, unpublished → 403, `@misc` prefix in output. Extend `SURFACE_KEYS` + `surface_stats` with `cite_bib`.
2. Add `getCiteBibUrl(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue` add a "📖 BibTeX Citation" section (publish-gated; completed sims only). Shows a `<pre>` block with the first 4 lines of the BibTeX entry, "Download .bib" anchor, "Copy cite.bib URL" button (for Zotero URL import).
3. Add to `docs/API.md` under Reproducibility with Zotero + LaTeX import workflow. Add to `openapi.yaml` as `text/plain` response. Add "BibTeX Academic Citation" to `docs/FEATURES.md` under Reproducibility & Citation. Zero new deps.

---

### 3. Belief Volatility Score

**Type:** Feature / Analytics
**Effort:** Small (hours)
**Impact:** signal.json tells you *where* the sim landed (direction + confidence). volatility tells you *how cleanly* it got there. Two sims both at "Bullish 65%" are different bets if one converged monotonically in 5 rounds and the other swung Bearish twice before snapping back. `GET /api/simulation/<id>/volatility` returns `{mean_abs_delta, max_delta, max_delta_round, std_delta, regime, total_rounds}` in one call — the risk metric missing from the current quant stack. `regime`: Monotonic (σ < 5, max < 15), Noisy (σ ≥ 5 and max < 30), Oscillating (max ≥ 30). Quant tools pairing signal.json + volatility get both the conclusion and the stability measure.
**How:**
1. Add `backend/app/services/volatility_service.py` (~130 LoC, pure stdlib `json` + `os` + `math`). `load_trajectory_rounds(sim_dir)`: reads `trajectory.json` per-round `{round, bullish_pct, neutral_pct, bearish_pct}` (same source as `trajectory_export`). `compute_volatility(rounds) -> dict | None`: returns `None` for < 2 rounds. `per_round_delta[i] = |Δbullish| + |Δneutral| + |Δbearish|` comparing round i to i−1; `mean_abs_delta`, `max_delta`, `max_delta_round` (1-indexed), `std_delta` (population std dev) all rounded to 2 dp; `regime` from thresholds above; `total_rounds`; `volatility_computed_at` ISO-8601 UTC. Add `GET /api/simulation/<id>/volatility` (publish-gated; 404 when None). Extend `SURFACE_KEYS` + `surface_stats` with `volatility`. Add 10 offline unit tests: monotonic → `"monotonic"`, oscillating → `"oscillating"`, mean/max/std round to 2 dp, max_delta_round correct, 1-round input → None → 404, published → 200, unpublished → 403, `volatility_computed_at` ISO-formatted, `total_rounds` matches input.
2. Add `getVolatility(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue` add a "📈 Volatility" section (publish-gated; gated on endpoint returning 200). Four compact fields: `Regime: {chip}` (green/yellow/red), `Mean swing: {mean}% / round`, `Max swing: {max}% at round {n}`, `Volatility σ: {std}%`. Copy volatility JSON URL button.
3. Add to `docs/API.md` under Analytics with regime threshold definitions. Add `VolatilityResponse` schema to `openapi.yaml`. Add "Belief Volatility Score" to `docs/FEATURES.md` under Analytics. Zero new deps.

---

### 4. Webhook Test Ping Endpoint

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Operators configure `WEBHOOK_URL` and immediately face one unknown: did it work? The delivery log (PR #73) records real dispatches — but reading it requires running a full simulation first. `POST /api/config/webhook/test` fires a realistic test payload on demand: HMAC-signed (if `WEBHOOK_SECRET` is set), same JSON schema as production dispatches, returns `{status_code, latency_ms, response_preview, signed, timestamp}`. Connection errors return `{status_code: null, error: "Connection refused"}` rather than raising. The webhook-setup DX gap that every Zapier / n8n / Make integration hits first — closes in 2 seconds rather than 10 minutes.
**How:**
1. Add `POST /api/config/webhook/test` to `backend/app/api/config.py` (or wherever the existing config routes live; check `GET /api/config/notifications` for the pattern). `WEBHOOK_URL` unset → 400 `{"error": "WEBHOOK_URL not configured"}`. Build test payload: `{event: "test", sim_id: "test-sim-0000", scenario_title: "MiroShark Webhook Test", status: "completed", direction: "Bullish", confidence_pct: 72.4, quality_health: "good", share_url: base_url + "/share/test-sim-0000", triggered_at: ISO-8601 UTC}`. Sign with `compute_signature` from `webhook_hmac.py` if `WEBHOOK_SECRET` set. POST to `WEBHOOK_URL` with `urllib.request.urlopen` (timeout=10s). Return `{status_code, latency_ms (2 dp), response_preview (first 200 chars), signed: bool, timestamp}`. Do NOT write to the sim delivery log (it's a test). Add 6 offline unit tests: `WEBHOOK_URL` unset → 400; dispatches to mocked URL → returns status_code + latency_ms; `signed=True` when `WEBHOOK_SECRET` set; `signed=False` when not; connection error returns `error` field; `response_preview` capped at 200 chars.
2. In the EmbedDialog.vue Notifications section (or the config panel showing `webhook_configured` status), add a "Test webhook" button next to the existing Webhook URL display. On click: POST to `/api/config/webhook/test`; show inline result: `✓ Delivered (200, 45ms)` in green, `✗ Connection refused` in red. Auto-clear after 10s. No new component needed.
3. Add `POST /api/config/webhook/test` to `docs/API.md` under Configuration. Add to `openapi.yaml` with `WebhookTestResult` schema. Add one-line note to `docs/NOTIFICATIONS.md` under Webhook section: "Test your webhook before running a simulation with `POST /api/config/webhook/test`." Zero new deps.

---

### 5. Gallery Public JSON (Machine-Readable Simulation Index)

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The gallery (`/explore`) is HTML — usable by humans but opaque to scripts, bots, and downstream LLM agents. `GET /api/gallery.json` returns all public simulations as a cacheable JSON array: `{sim_id, title, created_at, direction, confidence_pct, quality_health, total_rounds, agent_count, surface_views}`. ETag-based (`If-None-Match`) so polling clients get 304 responses when nothing changed. A `<link rel="alternate">` tag on `/explore` makes the endpoint auto-discoverable. Turns "100M+ potential as autonomous internet infrastructure" into a concrete API call — any agent can index what simulations exist without scraping HTML. Enables downstream: RSS aggregators, Zapier "new sim published" triggers, research indexers, leaderboard sites.
**How:**
1. Add `GET /api/gallery.json` to the gallery routes (parallel to the existing HTML gallery endpoint). `build_gallery_json(sim_root, limit=500) -> list[dict]`: enumerate all `sim_dir/` directories, load `simulation_state.json`, filter `is_public=True` + `status="completed"`. Per sim: `{sim_id, title: scenario_title[:100], created_at, direction: final_beliefs.direction, confidence_pct: float (2 dp), quality_health, total_rounds: int, agent_count: int, surface_views: sum of surface-stats.json counters}`. Sort by `created_at` descending; cap at 500. `Content-Type: application/json`; `Cache-Control: public, max-age=60`; `ETag: SHA-256(sorted sim_id list)[:16]`. Return 304 when `If-None-Match` matches. Add 8 offline unit tests: returns list; unpublished/incomplete sims excluded; `direction` one of Bullish/Neutral/Bearish; `confidence_pct` in 0–100 range; sorted descending by `created_at`; capped at 500; `ETag` header present; `surface_views` is integer.
2. In the `/explore` gallery page `<head>` (same pattern as sitemap's `<link>` injection), add `<link rel="alternate" type="application/json" href="/api/gallery.json" title="MiroShark Simulation Index">`. In the gallery page header area, add a small "JSON API" link pointing to `/api/gallery.json` — developers browsing the gallery discover the endpoint without reading docs.
3. Add `GET /api/gallery.json` to `docs/API.md` under Gallery & Discovery with a curl example + ETag polling pattern. Add `GalleryItem` schema to `openapi.yaml`. Add "Programmatic Gallery Index" to `docs/FEATURES.md` under Gallery & Discovery. Zero new deps.

---

## Selection Rationale

Today's batch operates one layer above the 12-surface publish system — it's about what you do *with* those surfaces once they exist.

- **Status Badge SVG** (#1) — Distribution amplifier. Every operator's GitHub README is a passive billboard; a live badge turns it into a dynamic one. The Shields.io format means zero effort from the embedder. Same zero-deps pattern as chart.svg.
- **BibTeX Academic Citation** (#2) — The final citation layer. reproduce.json + DKG anchoring already serve institutional verifiability. BibTeX is how academic papers actually cite sources. Zotero/Mendeley import from URL means the endpoint address doubles as the import URL — no download required.
- **Belief Volatility Score** (#3) — The missing risk metric. signal.json gives quant tools a conclusion; volatility gives them a confidence interval on how stable that conclusion is. Two sims at "Bullish 65%" are different risk profiles if one arrived monotonically and the other oscillated.
- **Webhook Test Ping** (#4) — The highest-ROI DX fix available. Every integration that uses webhooks starts with a configuration step that has no feedback loop today. One endpoint, one button, closes the gap.
- **Gallery Public JSON** (#5) — The machine-readable entry point. Twelve surfaces serve individual sims; nothing serves the index of all sims in a format a script can consume. ETag polling means a cron job can watch for new published simulations without hammering the server.
