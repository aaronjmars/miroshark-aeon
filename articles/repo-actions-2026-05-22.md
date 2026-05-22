# Repo Action Ideas — 2026-05-22

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 1,190 stars · 243 forks · 1 open issue (#95 French locale request, opened today) · 0 open PRs
**Recent activity:** PR #96 (BibTeX cite.bib — 14th publish-gated surface) opened today; PR #93 (Telegram, 5th channel-notifier) + PR #94 (Status Badge SVG) merged yesterday. 30-PR zero-new-deps streak. Token post-ATH correction: $0.00002141 (-50.9% from ATH $0.0000436 set May 18; FDV $2.14M).

## Ecosystem Context

The last 7 days closed two arcs simultaneously: the citation layer (reproduce.json → notebook.ipynb → cite.bib) and the channel-notifier pentagon (webhook + Discord + Slack + SMTP + Telegram). With 14 publish-gated surfaces and 5 channel-notifiers, the per-sim publish stack is comprehensive.

Three new angles emerge from today's signals:

**The private collaboration gap.** MiroShark's sharing model is binary: published (public) or unpublished (locked). Research teams and operators running competitive sims need a third state — share the result with a collaborator without publishing publicly. The HMAC infrastructure from PR #79 (webhook signatures) is already in the codebase. A private share link is a signed URL with an expiry, not a new abstraction. Re-eligible from May-14 batch (8 days old, outside the 7-day exclusion window).

**The French locale gap.** Issue #95 (opened today) directly asks: "Would you accept a French (fr) locale PR?" PR #65 already established the pattern — `LOCALE_ZH`, French-language prompt templates, experimental warning in the UI. French is the 5th most-spoken language globally with dense DeFi and Base-chain activity. The correct answer to this issue is a shipped PR, not a "yes" comment.

**The prediction-market gap.** MiroFish's viral breakout (32,000+ GitHub stars in 2026) was driven by a documented Polymarket trading bot use case: 2,847 simulations before trades, $4,266 profit over 338 trades. MiroShark already has `signal.json` (direction + confidence_pct). A `polymarket.json` adapter maps that signal to Polymarket's YES/NO probability format in one call — the one endpoint a Polymarket bot developer needs before they can wire MiroShark into their trading pipeline.

Two infrastructure gaps round out the batch:

**The platform stats gap.** Fourteen endpoints describe individual simulations. Zero describe the platform itself. `GET /api/stats` — total published sims, consensus distribution, average confidence, total surface views, unique operator count — is the endpoint press kits, external dashboards, and LLM agents use to ask "how active is this platform?" Same O(n) scan pattern as the gallery.

**The platform badge gap.** Individual sims have `badge.svg` (PR #94) for third-party READMEs. The platform has no equivalent. `GET /api/stats/badge.svg` returning "MiroShark | N simulations" completes the badge layer: sim-level badges for research READMEs, platform-level badge for community and operator READMEs. Reuses `badge_service.py` established in PR #94.

Previously suggested ideas excluded from this batch (last 7 days, May 15–22): oEmbed (May-16 #1, unbuilt); Peak-Round Analytics (May-16 #4, unbuilt); Operator Profile (May-16 #5, unbuilt); Per-Agent Stance Sparklines (May-18 #3, unbuilt); Scenario Clone Button (May-18 #4, unbuilt); CN+JP README (May-18 #5, unbuilt); Belief Volatility Score (May-20 #3, unbuilt); Webhook Test Ping (May-20 #4, unbuilt); Gallery Public JSON (May-20 #5, unbuilt). Private Share Link (May-14 #5) is re-eligible at 8 days. All 5 ideas below are net-new.

---

### 1. Private Share Link

**Type:** Security / Feature
**Effort:** Small (hours)
**Impact:** Operators running private research or competitive sims can share results with specific collaborators via a time-limited signed URL — without publishing the sim publicly. A `POST /api/simulation/<id>/share-link` generates a URL (`/share/<id>?token=<hmac_token>`) that bypasses the publish gate for 24 hours (configurable). The existing HMAC pattern from PR #79 (`compute_signature`) handles the cryptographic work. No new deps; no new abstraction — just a third sharing state between "public" and "locked". Converts the publish/unpublish binary into a three-state model for real research and institutional use cases.

**How:**
1. Add `backend/app/services/private_share.py` (~80 LoC, stdlib `hmac` + `hashlib` + `time` + `base64` + `os`). `generate_share_token(sim_id, expires_in_hours=24, secret) -> str`: `msg = f"{sim_id}:{expires_at_unix}"`, sign with `HMAC-SHA256(secret, msg.encode())`, return `base64url(f"{msg}.{hex_sig}")`. `verify_share_token(sim_id, token, secret) -> bool`: split on `.`, verify HMAC, verify `expires_at_unix > time.time()`, verify embedded sim_id matches. `SHARE_SECRET` env var (fall back to `WEBHOOK_SECRET` if blank; if neither set, endpoint returns 503 with `{"error": "SHARE_SECRET not configured"}`). Add `POST /api/simulation/<id>/share-link` (auth-gated via `X-Admin-Token` or same auth as existing config endpoints; returns `{share_url, expires_at_iso}`). Modify `GET /share/<id>` to check `?token=` against `verify_share_token` when `is_public=False` — grant access if valid, 403 otherwise. Add 8 offline unit tests: valid token → 200 on unpublished sim, expired token → 403, wrong sim_id in token → 403, public sim accessible without token, `SHARE_SECRET` unset → 503 on generation, token roundtrip generates/verifies cleanly, expiry arithmetic correct, base64url has no `=` padding.
2. In `EmbedDialog.vue`, add a "🔒 Private Share Link" section visible on unpublished sims only (hide on published, where the public share URL is already shown). "Generate private link" button → POST → show URL + "Expires in 24h" note. "Copy private link" button. "Publish publicly" shortcut link. Add `generateShareLink(simId)` helper to `frontend/src/api/simulation.js`.
3. Add `SHARE_SECRET` to `.env.example` with comment. Add "Private Share Links" to `docs/FEATURES.md` under Share & Distribution. Add `POST /api/simulation/<id>/share-link` to `docs/API.md`. Zero new deps.

---

### 2. French Locale Simulation Prompts

**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** Issue #95 (opened today) directly requests French locale support — the first locale-request issue in repo history. PR #65 established the Chinese locale pattern: a `LOCALE_ZH` env var, French-language prompt templates, and an "experimental" warning. Applying the same pattern to French responds to the open issue, captures 300M+ French-speaking users (including dense DeFi and Base-chain clusters in France, Quebec, and Francophone Africa), and continues building toward the CN-locale contributor hyperstition by demonstrating that non-English locales are a first-class concern. Closes issue #95 via the PR description.

**How:**
1. Add `backend/app/prompts/locale_fr.py` (or a `locale_fr.json` if PR #65's Chinese locale uses JSON templates — match the existing pattern exactly). Translate the core simulation prompt templates: `system_prompt_template`, `agent_persona_template`, `scenario_framing_template`, `consensus_evaluation_template`. Use precise technical vocabulary: _simulation multi-agents_, _essaim d'agents_, _distribution des croyances_, _direction du consensus_, _santé de la qualité_. Add `LOCALE_FR` env var to the locale lookup (after `LOCALE_ZH`; default `false`). In the prompt-dispatch logic (wherever `LOCALE_ZH` branches to Chinese prompts), add the equivalent `LOCALE_FR` branch. Add 5 offline unit tests: `LOCALE_FR=true` → French prompt returned (check for at least one French term like "distribution des croyances"), `LOCALE_FR=false` → English returned, French prompt does not bleed into non-prompt outputs, `LOCALE_FR` and `LOCALE_ZH` both false → English returned, `LOCALE_FR=true` env correctly parsed as boolean.
2. In the UI locale selector (wherever the Chinese locale toggle lives — likely `NewSimView.vue` or a settings panel), add a 🇫🇷 French option mirroring the Chinese one. Add the same "experimental" caveat: "French locale (experimental) — prompts and agent personas will be in French." If the locale selector is a single-select control, add `fr` to the options list; if it's a boolean toggle, replicate the pattern with a separate `LOCALE_FR` toggle.
3. Add `LOCALE_FR=false` to `.env.example` with comment. Add "French Locale" to `docs/FEATURES.md` under Language & Locale alongside the Chinese entry. Update `docs/API.md` simulation config docs: `locale` field now accepts `"en"`, `"zh"`, `"fr"`. Add "Closes #95" to the PR description so GitHub auto-closes the issue on merge. Zero new deps.

---

### 3. Polymarket-Ready Prediction JSON

**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** The use case that made MiroFish go viral in 2026: a developer plugged swarm simulation into a Polymarket trading bot, ran simulations before every trade, and documented $4,266 profit over 338 trades. MiroShark already has `signal.json` (Bullish/Neutral/Bearish + confidence_pct). A `GET /api/simulation/<id>/polymarket.json` adapter maps that output to Polymarket's YES/NO probability format — `{yes_probability, no_probability, confidence_tier, suggested_market_title, source_sim_id}` — in one call. Any developer building a Polymarket bot gets from "simulation result" to "actionable market signal" with a single curl command. Pre-build grep: `polymarket`, `yes_probability`, `prediction_market` — if no matches, unbuilt.

**How:**
1. Add `backend/app/services/polymarket_service.py` (~120 LoC, stdlib only). `compute_polymarket(sim_state, sim_id) -> dict | None`: reads `final_beliefs.bullish_pct`, `final_beliefs.neutral_pct`, `final_beliefs.bearish_pct` from sim_state. `yes_probability`: if direction=Bullish → `round(bullish_pct / 100, 4)`; if Bearish → `round(bearish_pct / 100, 4)`; if Neutral → `0.5`. `no_probability = round(1 - yes_probability, 4)`. `confidence_tier`: map `confidence_pct` buckets — `<25` → `"speculative"`, `25-50` → `"moderate"`, `50-75` → `"confident"`, `≥75` → `"high-conviction"` (derive from the `compute_signal` confidence formula or re-derive directly from leading_pct). `suggested_market_title = f"Will {scenario_title[:120]}"`. `source_sim_id = sim_id`. `polymarket_generated_at` = ISO-8601 UTC `completed_at`. Returns `None` if `status != "completed"`. Add `GET /api/simulation/<id>/polymarket.json` (publish-gated; 404 with `{"error": "simulation not complete"}` when None; `Cache-Control: public, max-age=60`). Extend `SURFACE_KEYS` + `surface_stats` with `polymarket_json`. Add 10 offline unit tests: bullish sim → `yes_probability > 0.5`, bearish sim → `yes_probability < 0.5`, neutral → `yes_probability = 0.5` exactly, `yes + no = 1.0` within float tolerance (1e-9), confidence_tier maps correctly for all 4 buckets, `suggested_market_title` starts with "Will ", unpublished → 403, incomplete → 404, `source_sim_id` matches input, `polymarket_generated_at` is ISO-formatted.
2. Add `getPolymarketJson(simId)` to `frontend/src/api/simulation.js`. In `EmbedDialog.vue`, add a "🎯 Prediction Market" section (publish-gated; completed sims only). Layout: `YES probability: {pct}%` horizontal bar (green, same style as existing bars), `NO probability: {pct}%` bar (red), `Confidence tier: {chip}`, `Suggested title: {str}` (copyable). "Copy polymarket.json URL" button.
3. Add `GET /api/simulation/<id>/polymarket.json` to `docs/API.md` under Analytics with a Polymarket bot pattern (curl → parse `yes_probability` → POST to Polymarket API). Add `PolymarketResponse` schema to `openapi.yaml` under Analytics. Add "Polymarket-Ready Prediction JSON" to `docs/FEATURES.md`. Zero new deps.

---

### 4. Platform Aggregate Statistics API

**Type:** Integration
**Effort:** Small (hours)
**Impact:** Fourteen simulation surfaces describe individual sims; nothing describes the platform itself. `GET /api/stats` returns aggregate metrics across all public simulations: total published sims, consensus distribution (bullish/neutral/bearish count + pct), average confidence_pct, total surface views, unique operator count, newest sim metadata. One O(n) scan with 60s caching. Powers press kit numbers ("MiroShark has run N simulations"), external dashboards, LLM-agent health checks ("is this platform active?"), and is the data backing for idea #5 (platform badge). The first endpoint that makes `@Concept_felipe`'s "autonomous internet infrastructure" framing concrete at the platform level.

**How:**
1. Add `backend/app/services/platform_stats.py` (~120 LoC, stdlib `json` + `os` + `time`). `compute_platform_stats(sim_root) -> dict`: scan `sim_root/` for `simulation_state.json` files; filter `is_public=True` + `status="completed"`. Aggregates: `total_sims: int`, `consensus_distribution: {bullish: int, neutral: int, bearish: int, bullish_pct: float, neutral_pct: float, bearish_pct: float}` (all pcts rounded to 1 dp), `avg_confidence_pct: float` (mean of per-sim `compute_signal`-derived confidence, 1 dp; use the same leading-pct formula from `signal_service.py` or inline it), `total_surface_views: int` (sum all counters in all `surface-stats.json` files), `unique_operators: int` (count non-empty `sim_state.get("operator", "")` distinct values), `newest_sim_id: str | null`, `newest_sim_created_at: str | null`. 60s module-level cache: `_cache = {}; _cache_at = 0.0`. Add `GET /api/stats` (no auth; public; `Cache-Control: public, max-age=60`; `ETag: f"{total_sims}-{newest_sim_id}"[:16]`). Return `304` when `If-None-Match` matches ETag. Add 8 offline unit tests: empty sim_root → all-zero result, 3 sims with mixed directions → correct counts, unpublished/incomplete sims excluded, `avg_confidence_pct` rounded to 1 dp, `unique_operators` de-duplication correct, ETag header present, `newest_sim_created_at` is ISO-8601, `total_surface_views` sums correctly.
2. No new frontend page required. Optionally: in `App.vue` footer or the `/explore` gallery page header, add a small "N simulations run" stat pulled from `GET /api/stats` on mount — a 3-line `fetch` call in the existing component lifecycle. Skip if the app has no persistent footer.
3. Add `GET /api/stats` to `docs/API.md` under Gallery & Discovery with a `PlatformStats` response schema. Add `PlatformStats` to `openapi.yaml`. Add "Platform Statistics" to `docs/FEATURES.md` under Gallery & Discovery. Zero new deps.

---

### 5. Platform Stats Badge SVG

**Type:** Growth
**Effort:** Small (hours)
**Impact:** `GET /api/stats/badge.svg` returns a Shields.io-compatible flat badge showing live simulation count: `MiroShark | N simulations`. Any operator, contributor, or community member can add it to a GitHub README or portfolio — `![MiroShark](https://your-instance/api/stats/badge.svg)` — turning every community README into a live signal that the platform is active. Reuses `badge_service.py` from PR #94 (same `build_badge_svg` function, different label + color). Updates every 60 seconds. A second-order amplifier: sim badges (PR #94) link third-party READMEs to specific sims; platform badges link community READMEs to MiroShark itself. Note: if idea #4 (Platform Stats API) is built first, this endpoint shares its `compute_platform_stats` call; if built independently, a standalone 30-line sim-count function suffices.

**How:**
1. Add `GET /api/stats/badge.svg` route (no auth; public; `Content-Type: image/svg+xml`; `Cache-Control: public, max-age=60`). Handler: count public completed sims (either call `compute_platform_stats` from idea #4, or a standalone inline count: scan `sim_root/` for `is_public=True` + `status="completed"`). Call `build_badge_svg("MiroShark", f"{count} simulations", color="#0ea5e9")` (platform blue, not direction green/red). The `build_badge_svg` function in `badge_service.py` already accepts arbitrary label/value/color — no modification needed. Return SVG bytes. Add 6 offline unit tests: returns valid SVG bytes, SVG text contains "MiroShark", SVG text contains the simulation count integer, `Content-Type` is `image/svg+xml`, `Cache-Control` header includes `max-age=60`, SVG root tag is `<svg>`.
2. Add a `getBadgeStatsUrl()` helper (no simId param) to `frontend/src/api/simulation.js`. In `README.md`, add the platform badge to the existing badge row (alongside the GitHub stars + forks shields): `[![MiroShark simulations](https://your-instance/api/stats/badge.svg)](https://github.com/aaronjmars/MiroShark)`. Add a "Platform badge" row to `docs/FEATURES.md` under Share & Distribution noting the self-hosted URL pattern.
3. Add `GET /api/stats/badge.svg` to `docs/API.md` under Gallery & Discovery as an SVG binary response (no JSON schema needed). Zero new deps.

---

## Selection Rationale

Today's batch operates at two layers above the per-sim publish stack: the sharing model itself (private links), the international surface (French locale + open issue), and the platform-level API layer (stats + badge, Polymarket adapter).

- **Private Share Link** (#1) — Re-eligible from May 14. Converts the binary publish/unpublish gate into a three-state model. The HMAC infrastructure is already in the repo; this is a 1-day wiring job. Critical for institutional and research use cases that can't make sims public.
- **French Locale** (#2) — Issue #95 opened today directly requests this. PR #65's Chinese locale is the complete template. The pattern is established; the time cost is translation + one env var branch. Closing a community-opened issue within 24h is itself a signal.
- **Polymarket-Ready JSON** (#3) — The most growth-leveraged idea in the batch. MiroFish's entire viral moment was driven by one Polymarket bot case study. MiroShark has `signal.json`; `polymarket.json` is a 120-LoC adapter that turns it into the exact format a Polymarket bot needs. Direct competition on the use case that drove 32,000 GitHub stars for the sister project.
- **Platform Stats API** (#4) — The first endpoint about the platform itself. Enables press kits, dashboards, and LLM-agent health checks. O(n) scan with 60s caching; no new computation beyond what the gallery already does.
- **Platform Stats Badge** (#5) — Completes the badge layer. Sim badges (PR #94) are discovery surfaces for specific simulations; the platform badge is a discovery surface for MiroShark itself. Reuses `badge_service.py` exactly as written; the only new code is the route handler and the sim-count logic.
