# Push Recap — 2026-06-01

## Overview
Three substantive merges to `main` in the 24h window — two on `aaronjmars/MiroShark` (PR #131 Simulation Clone JSON, PR #130 Surface Catalog API) and one on `aaronjmars/miroshark-aeon` (PR #49 token-report Path B Top Trades fallback). The MiroShark pair was authored by Aeon and merged four minutes apart on Aaron's afternoon (14:07Z and 14:11Z), shipping a discoverability primitive and a reusability primitive together — the catalog of surfaces and the surface that returns a sim's create-body inputs. The aeon merge is a self-improvement landing the May-30 fix for the daily token-report's empty Social Pulse section.

**Stats:** 26 files changed, +2,603 / −11 across 3 commits (cron auto-commit churn on `miroshark-aeon` excluded as noise).

---

## aaronjmars/MiroShark

### Theme 1 — Two new surfaces, shipped paired
**Summary:** Two Aeon-built PRs that had been sitting open (PR #130 since 2026-05-30, PR #131 since 2026-05-31) both landed today, four minutes apart. They're complementary: one tells an integrator *what surfaces exist here*, the other tells them *how to recreate a published sim*. The MiroShark backend now exposes 28 distinct surfaces (26 publish-gated per-sim + 2 platform-level), up from 25 at start of window.

**Commits:**

- `c8e743a` — **feat: clone.json surface — return the inputs a sim was built with (#131)** (merged 14:07:46Z)
  - New file `backend/app/services/clone_service.py` (+279) — `build_clone_payload(simulation_id, sim_dir)` reads `state.json` + `simulation_config.json` and returns a block wire-compatible with `POST /api/simulation/create`: same field set, same defaults, same `polymarket_market_count` clamp `[1,5]`, same country normalisation (lowercased + stripped), same `demographic_filters` pass-through. `build_example_curl(clone_payload)` produces a deterministic one-line `curl` with `https://your-host` placeholder. Pure stdlib (`json`+`os`).
  - Modified `backend/app/api/simulation.py` (+89) — new `get_clone_json` handler at `GET /<simulation_id>/clone.json`. Same publish gate as every other share surface; 1h cache (vs the 5min cache on analytical surfaces — inputs are structural, they don't shift round-to-round); `Content-Disposition: inline; filename=miroshark-<id12>-clone.json`; increments `clone_json` surface counter; returns 404 when `state.json` doesn't exist (mid-prepare / pruned), 403 when sim is private — so consumers can distinguish "not ready" from "not allowed".
  - Modified `backend/app/services/surface_stats.py` (+1) — `clone_json` added to `SURFACE_KEYS` frozenset.
  - Modified `backend/openapi.yaml` (+161) — path entry + `CloneResponse` + `ClonePayloadBody` schemas.
  - New file `backend/tests/test_unit_clone_service.py` (+411, 24 offline tests) — payload shape, defaults, clamps, country normalisation, unicode survival, demographic_filters pass-through, curl format determinism, static wiring guards.
  - Modified `backend/tests/test_unit_surface_stats.py` (+1) — `clone_json` added to expected set.
  - Modified `frontend/src/api/simulation.js` (+42) — `getCloneJsonUrl` + `getCloneJson` helpers.
  - Modified `frontend/src/components/EmbedDialog.vue` (+180) — 🔁 Clone configuration section beneath the Polymarket row, with a live summary plus Download / Copy URL / Copy snippet / Copy POST body buttons, and dialog-open + publish-flip hooks.
  - Modified `docs/API.md` (+1) + `docs/FEATURES.md` (+40) — row in the publish/embed table + a new FEATURES section between Polymarket and Badge SVG.

- `29b3ea4` — **feat: machine-readable surface catalog API at /api/surfaces.json (#130)** (merged 14:11:33Z)
  - New file `backend/app/services/surfaces_catalog.py` (+443) — hardcoded list of every share/platform surface the deployment exposes, each carrying `key` / `endpoint` (with `<simulation_id>` placeholder) / `method` / `type` (analytics / visualization / export / embed / integration / platform / discovery) / one-line `description` / `added_in_pr` / `example_curl`. `SCHEMA_VERSION="1"`, `SURFACE_TYPES` frozenset, `catalog_etag()` = `"surfaces-v<schema>-<count>"`. Pure stdlib. Per-call dict copies so a caller mutating the response can't poison subsequent reads.
  - New file `backend/app/api/surfaces.py` (+98) — Flask blueprint mounted at `/api` with one route (`/surfaces.json`). `ETag` short-circuit to 304 on `If-None-Match`; `Cache-Control: public, max-age=3600`. Always 200 or 304 — no input the caller can supply produces a 404.
  - Modified `backend/app/__init__.py` (+7/−1) and `backend/app/api/__init__.py` (+5) — register `surfaces_bp` at `/api` (sibling of `stats_bp` rather than nested under `/api/simulation`).
  - Modified `backend/openapi.yaml` (+195) — `/api/surfaces.json` path under Platform with `SurfaceCatalog` + `SurfaceCatalogEntry` schemas.
  - New file `backend/tests/test_unit_surfaces_catalog.py` (+307, 18 offline tests) — schema invariants (locked field set, key uniqueness, valid methods/types/endpoints, description length bounds, `example_curl` references its own endpoint verbatim), drift guards (the per-sim subset of the catalog must match `surface_stats.SURFACE_KEYS`; the self-referential entry must be present; platform_stats + polymarket + signal + volatility entries must all be present), `ETag` determinism, envelope shape, JSON serialisability, immutability of returned objects, blueprint wiring static-text guards, and OpenAPI spec presence.
  - Modified `backend/tests/test_unit_openapi.py` (+4) — `surfaces_bp → /api` added to `_BLUEPRINT_PREFIXES` so the openapi route-drift test stops flagging `/api/surfaces.json` as a phantom path. (8 passed → 8 passed; the merge commit message notes this was a pre-merge fix.)
  - Modified `docs/API.md` (+1) + `docs/FEATURES.md` (+44) — row + section "Surface Catalog API" between Platform Stats Badge SVG and BibTeX Academic Citation.
  - Modified `frontend/src/api/simulation.js` (+33) — `getSurfacesCatalogUrl()` + `getSurfacesCatalog()` helpers.
  - **Inline follow-up:** the PR description records a third commit on the branch that registered PR #131's `clone_json` entry in the catalog (count 27 → 28) and bumped the FEATURES.md example. So the merged main now ships the two surfaces *and* the catalog already knows about both — no follow-up drift PR is needed.

**Impact:** Together these close a discoverability/reusability loop that has been one HTTP call short for the past six months of surface-shipping. An integrator landing on a deployment can now `GET /api/surfaces.json` to learn the menu, then `GET /api/simulation/<id>/clone.json` on any published sim to retrieve the exact `POST /api/simulation/create` body that produced it — and pipe that to `/api/simulation/compare` (already shipped) to fork-and-diff without ever opening the UI. The static-and-hardcoded design choice in `surfaces_catalog.py` (drift-guarded against `SURFACE_KEYS`, not auto-derived) is the same posture as `platform_stats.py` and `surface_stats.py` — explicit data, not introspection — so the catalog can list surfaces that aren't even publish-gated yet (the platform stats endpoint and its badge SVG) without leaking private mutation routes off the Flask URL map. Zero new dependencies on either PR — the 35th and 36th consecutive zero-deps PRs since the Nemotron addition.

---

## aaronjmars/miroshark-aeon

### Theme 2 — Self-improvement: token-report's empty section gets repaired
**Summary:** One substantive merge — Aeon's own May-30 self-improve PR (#49) finally landed today. It fixes a recurring filler problem in the daily token-report skill. The remaining 30+ commits on this repo in the window are cron / scheduler / auto-commit churn from skill runs (`chore(scheduler): update cron state`, `chore(<skill>): auto-commit YYYY-MM-DD`) and per the May-31 recap convention are excluded as noise.

**Commits:**

- `b2d2a1b` — **improve: replace empty Social Pulse with Top Trades fallback on Path B (#49)** (merged 12:45:17Z)
  - Modified `skills/token-report/SKILL.md` (+9/−4) — the heart of the change. Step 4 footnote now flags the GeckoTerminal `/pools/POOL/trades` response as the Path B fallback source (previously it was used only implicitly for the prose Volume & Liquidity bullet). Step 5 Path B rewritten: instead of writing "X/Grok data unavailable for this run", the section becomes **Top Trades (24h)** — the 3 largest trades by `volume_in_usd` from the trades response, each rendered as `kind` (Buy/Sell) · USD value · token amount · time-ago · basescan tx link from `tx_hash`, with a one-sentence buy/sell-mix lead-in. Step 6 template updated so the report has *either* a "Social Pulse" heading (Path A) *or* a "Top Trades (24h)" heading (Path B), explicitly marked mutually exclusive. New log convention `Social: Path A` / `Social: Path B (top-trades fallback)` so future self-improve runs can verify which path fired without re-reading the article.
  - New file `dashboard/outputs/self-improve-2026-05-30T13-22-34Z.json` (+225) — pre-rendered json-render spec for the dashboard.
  - Modified `.outputs/self-improve.md` (+7/−6) — the day's self-improve narrative.
  - Modified `memory/MEMORY.md` (+1) — new Skills Built row for PR #49.
  - Modified `memory/logs/2026-05-30.md` (+18) — full self-improve log entry with trigger, fix, design decisions, and validation notes.
  - Modified `memory/token-usage.csv` (+1) — May-30 self-improve token row added (claude-opus-4-7, 17,441 output tokens).

**Impact:** This is Aeon noticing a degradation in its own daily flagship output and repairing it from inside the loop. The May-28 spam filter (PR #48) was working correctly — it screened all Grok candidates because all candidates were spam — but the downstream consequence was a dead "X/Grok data unavailable for this run" line every day for three days running (May 28/29/30). The fix doesn't disable Path B or paper over the spam filter; it replaces filler with signal that was already in scope but unused (the trades response). Operators reading the article now see three concrete trade flows with on-chain-verifiable hashes on every Path B day — currently 100% of days since the spam filter shipped — rather than a one-line apology. Path A is byte-for-byte unchanged; the moment organic X signal returns (a fresh ATH session, a notable mention), Social Pulse re-appears automatically without any further skill change. Zero new API calls — the data was being fetched and thrown away.

---

## Developer Notes
- **New dependencies:** none on any of the three PRs. MiroShark's zero-deps PR streak since Nemotron is now 36 (was 34 at start of window — PR #130 and PR #131 each extend it by one).
- **Breaking changes:** none. Both new MiroShark endpoints are additive — they don't touch any existing route's contract. PR #49 changes the *shape* of the token-report article's third section (Social Pulse → Top Trades) on Path B days, but the article isn't a versioned API surface and downstream consumers parse by markdown headings.
- **Architecture shifts:** `surfaces_bp` mounts at `/api` (no sub-prefix), making it a sibling of `/api/stats`, not a child of `/api/simulation` — a deliberate choice flagged in the diff's blueprint registration comment. Reason: the catalog is a discovery surface, and an integrator querying "what's here?" shouldn't need to know the per-sim namespace exists. Static-and-hardcoded over introspection: `surfaces_catalog.py` is a literal list of dicts, not a Flask URL-map scan — drift-guarded by a test that fails if `SURFACE_KEYS` and the per-sim subset of the catalog ever disagree.
- **Tech debt:** none introduced. PR #130's merge bundled the test_unit_openapi blueprint-prefix fix (registering `surfaces_bp → /api` in the drift test's map) into the same merge commit, so the route-drift test stays green on main rather than failing into a follow-up.

## What's Next
- The two MiroShark surfaces shipped today are the first time the Aeon-driven feature pipeline has put a *pair* of complementary surfaces on `main` in the same hour rather than serially. Worth watching whether the next 5–7 days produce a similar cluster around the "inputs / outputs / discovery" frame, or whether this was a one-off because both PRs had been sitting open.
- Open MiroShark PRs at end of window: **0**. PR #130 and PR #131 both merged in the same UTC afternoon; no Aeon-built PR is currently waiting on review.
- Open miroshark-aeon PRs at end of window: **0**. PR #49 closed today.
- The Surface Catalog API now has a `clone_json` entry in its hardcoded list (the PR #131 follow-up commit). If a future surface ships without an entry, the drift-guard test in `test_unit_surfaces_catalog.py` will fail before merge — so the next per-sim surface PR will need a 2-line edit to `surfaces_catalog.py` alongside whatever it ships. Worth flagging in the `feature` skill's pre-flight checklist.
- The Social Pulse section will start re-appearing in the daily token-report the next time organic non-spam X signal lands in the XAI cache (e.g. on a fresh ATH session). Until then, every daily run prints the new Top Trades section.
