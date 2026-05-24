# Push Recap — 2026-05-24

## Overview

The 24-hour window straddles yesterday's recap cutoff (2026-05-23T15:19Z) and today's run (2026-05-24T15:08Z), and it landed five MiroShark PRs to `main` in a 95-minute burst — the densest single window of the month. Three are net-new product (Polymarket integrator surface, Nemotron-anchored personas, plus a CI catch-up) and two are externally authored fixes that merged in the same minute. The headline architectural shift: PR #103 introduces `duckdb` + `huggingface_hub`, ending the **31-PR zero-new-dependencies streak** that started at PR #71.

**Stats:** ~30 files changed, +3,004 / -18 lines across 5 MiroShark merges. 0 miroshark-aeon merges (all aeon traffic was skill auto-commits).

---

## aaronjmars/MiroShark

### Theme 1: The Post-Recap Merge Wave

**Summary:** Yesterday's push-recap (15:19Z) captured PR #97 as the only window merge and #98/#99/#100 as still-open. Between 17:09Z and 18:43Z — 110 minutes to 3 h 24 min after the recap cutoff — all three open PRs landed, plus a CI fix (#102) and a brand-new feature merge (#103). Today's window therefore carries the entire merge wave.

**Commits:**

- `f3b9401` (2026-05-23T17:09Z, aaronjmars) — **PR #99: Polymarket-ready prediction JSON — first integrator-shaped surface.** +1,276 / -1 across 10 files.
  - New `backend/app/services/polymarket_service.py` (+253 LoC, pure stdlib): `compute_polymarket()` calls `signal_service.compute_signal` and reshapes its `direction + confidence_pct + risk_tier` triple into the YES/NO envelope a Polymarket trading bot expects — `yes_probability` / `no_probability` summing to 1.0, four-bucket `confidence_tier` (`speculative` / `moderate` / `confident` / `high-conviction`, upper bounds exclusive), `bullish/neutral/bearish_pct` + `risk_tier` inherited verbatim, `suggested_market_title` synthesised as `"Will {scenario}?"`, `source_sim_id` field.
  - `backend/app/api/simulation.py` (+82 LoC): `GET /api/simulation/<id>/polymarket.json` with stricter publish gate — only `status == "completed"` emits a payload (mid-run sims 404; mirrors the no-flip-risk posture a Polymarket bot needs). 5-minute Cache-Control matching `signal.json` cadence.
  - `backend/openapi.yaml` (+192): path entry + `PolymarketPrediction` schema with 15 required fields documented.
  - `backend/tests/test_unit_polymarket_service.py` (+432 LoC): 30+ offline tests — payload shape, direction-aware probabilities, sum-to-1.0 invariant, four-bucket confidence_tier with exclusive boundaries, market-title shaping, non-completed/missing-belief returns None, ISO-8601 timestamp regex, route decorator presence.
  - `frontend/src/components/EmbedDialog.vue` (+201): 🎯 Polymarket prediction section with live YES/NO preview, confidence-tier chip, suggested-title rail, `curl | jq` snippet.
  - `surface_stats.py` (+4): `polymarket_json` counter; `surface_stats` expected-set test updated.

- `ec6eb26` (2026-05-23T17:19Z, aaronjmars) — **PR #102: CI fix — notifications-config + openapi waybackclaw drift on main.** +261 / -0 across 2 files.
  - `backend/openapi.yaml` (+233): documents `GET /api/simulation/{id}/waybackclaw-record` and `POST /api/simulation/{id}/publish-waybackclaw` alongside the existing DKG publish routes (same `[Publish & Embed]` tag, same admin-token gate on POST). New `WaybackClawRecord` schema mirroring the on-disk `waybackclaw-record.json` shape.
  - `backend/tests/test_unit_notifications_config.py` (+28): adds a `_clear_waybackclaw(monkeypatch)` helper that wipes `WAYBACKCLAW_AGENT_TOKEN`, calls it in each test, and adds `"waybackclaw_configured": False` to every full-dict assert.
  - **Backstory:** PR #97 (WaybackClaw) shipped without updating these unit-test fixtures or the OpenAPI spec, leaving `main` red on every subsequent PR. This is a follow-up bandage, not a feature.

- `cf692c7` (2026-05-23T17:37:18Z, **AntFleet** — external) — **PR #98: validate project_id to prevent path traversal.** +10 / -0 in `backend/app/models/project.py`.
  - Adds `_SAFE_PROJECT_ID = re.compile(r'^[a-zA-Z0-9_-]{1,128}$')` and a `_validate_project_id(project_id)` helper called at `_get_project_dir()` — the single entry point all downstream filesystem methods route through.
  - **Vuln class:** before this fix, `ProjectManager._get_project_dir` built filesystem paths with `os.path.join(PROJECTS_DIR, project_id)` and never validated the input. A caller passing `../../etc/passwd` could read or write arbitrary files on the server.
  - Found by AntFleet two-model consensus review (Claude Opus 4.7 + GPT-5). Benchmark at `AntFleet/miroshark-bench/pull/1` — first time MiroShark is publicly named as a security-benchmark target.

- `c3bd5fc` (2026-05-23T17:37:23Z, **Void Freud** — external) — **PR #100: launcher: skip local Neo4j startup when .env points at Aura.** +5 / -0 in `miroshark` launcher.
  - Adds a 5-line guard at the top of `ensure_neo4j()`: `if grep -qE '^NEO4J_URI=neo4j\+s://' "$SCRIPT_DIR/.env"` → early-return with `"Remote Neo4j (Aura) configured in .env — skipping local startup"`.
  - **The bug:** README documented Aura as supported, but the launcher hard-coded the local-Neo4j startup flow (Neo4j CLI / Docker). Aura users saw spurious local-startup errors before the backend's dotenv loader even read the remote URI/USER/PASSWORD.
  - Third external PR in 10 days (after teifurin's #89 May-18 and antfleet's #98 above).

- `58a80e5` (2026-05-23T18:43Z, aaronjmars) — **PR #103: demographic grounding — Nemotron-anchored personas.** +1,452 / -17 across ~20 files.
  - New `backend/app/services/demographic_sampler.py` (+360 LoC): single `sample_seeds()` entry point. DuckDB columnar filter over a Nemotron parquet glob. Lazy `huggingface_hub` snapshot download on first use per country. Graceful no-op when `duckdb` / `huggingface_hub` aren't installed.
  - New `backend/app/services/country_registry.py` (+78 LoC): JSON pack loader from `backend/app/countries/*.json`.
  - New `backend/app/countries/singapore.json` (+47) and `usa.json` (+47): pluggable demographic packs. Singapore = 39 planning areas + named groups (`north-east`, `north`, `east`, `west`, `central`); USA = 51 states + regional groups (`northeast`, `midwest`, `south`, `west`).
  - New `backend/app/api/countries.py` (+92): `countries_bp` blueprint serves `GET /api/countries` (active country + summary list) and `GET /api/countries/<code>` (full filter schema). Read-only, no auth.
  - `backend/app/services/wonderwall_profile_generator.py` (+99 / -13): adds `country_code` + `demographic_filters` constructor args; pulls one Nemotron row per entity and feeds it to the LLM as a `DEMOGRAPHIC ANCHOR` block (or `AUDIENCE ANCHOR` for group entities — institutional voice stays intact while tone localizes).
  - `backend/app/services/simulation_manager.py` (+28 / -1): `SimulationState` gains `country: Optional[str]` and `demographic_filters: Optional[Dict[str, Any]]`; persisted across `to_dict()` / `_load_simulation_state()`.
  - `backend/app/api/simulation.py` (+26 / -2): `POST /api/simulation/create` accepts `country` + `demographic_filters` (geography_values, min_age, max_age, occupations…); invalid filter dicts silently coerced to None.
  - `backend/app/config.py` (+15): `DEMOGRAPHICS_COUNTRY` env var (empty by default — fully opt-in).
  - `backend/tests/test_unit_demographic_grounding.py` (+233): 15 pytest cases covering registry, sampler graceful-degradation, schema introspection, seed→entity pairing, and the `WonderwallProfileGenerator` smoke path.
  - `frontend/src/components/CountryPicker.vue` (+235, new): country dropdown + geography chips with i18n strings (`'Demographic country' / '人口国别'`). Auto-hides when no packs are registered.
  - `frontend/src/components/Step1GraphBuild.vue` (+7): mounts `<CountryPicker>` on the New Sim form; passes `country` + `demographic_filters` into `createSimulation()`.
  - `frontend/src/api/countries.js` (+41, new): `listCountries()`, `getCountry(code)`, `getCountryFilterSchema(code)`.
  - `docs/DEMOGRAPHICS.md` (+110, new) + `docs/CONFIGURATION.md` (+1) + `docs/FEATURES.md` (+13): full feature docs.
  - **`backend/pyproject.toml` (+5) + `backend/requirements.txt` (+8): adds `duckdb >= 1.0.0` and `huggingface_hub >= 0.23.0` as runtime deps.** This is the first new runtime dependency since PR #71 (Apr 24, 2026) — ending the **31-PR zero-new-dependencies streak**. Both deps are framed as "optional, degrades to graph-only" in code, but they're listed under unconditional `dependencies = [...]` in pyproject.toml, so a fresh `pip install` always pulls them.

**Impact:** The Polymarket integrator pattern (PR #99) and the Nemotron-grounded persona track (PR #103) are two independent moves in opposite architectural directions on the same day. Polymarket is the integrator-facing endpoint that requires *no* new infrastructure — pure derivation from a primitive that already shipped (`signal.json`, PR #91). Demographics is the *opposite* posture: a substantive new data dependency (HuggingFace + DuckDB + parquet) for a feature that genuinely needs it. The same maintainer made both calls in the same window, and the dependency cost was paid where the value can't be derived from anything already in the repo.

### Theme 2: External Contributors Now Outnumber Internal Open Work

**Summary:** Two external PRs merged in the same minute (17:37:18Z and 17:37:23Z, five seconds apart). The third external contributor in 10 days. At end-of-window, of the **3 open MiroShark PRs**, 2 are externally authored.

**Commits:** `cf692c7` (AntFleet) + `c3bd5fc` (Void Freud) — already detailed above.

**Open PRs at end-of-window (3):**
- **PR #104** (voidfreud, opened 2026-05-23T23:44Z) — `gitignore: collapse explicit .env profile list into .env.* wildcard`. Cleanup PR from the same external contributor who shipped #100 six hours earlier.
- **PR #105** (aaronjmars, opened 2026-05-24T11:33Z) — `feat: platform aggregate stats API + Shields.io platform badge SVG`. Coupled May-22 batch ideas #4 + #5 (badge route reuses platform-stats scan). 32 PRs is the new zero-deps streak length pending this merge.
- **No third open PR remained externally authored from yesterday's set** — antfleet's #98 and voidfreud's #100 both merged; the remaining externally authored open work is voidfreud's #104.

**Impact:** AntFleet running MiroShark as a public security-benchmark target (`AntFleet/miroshark-bench/pull/1`) is the kind of *integrator-product feedback loop* the May-23 hyperstition asked for. Combined with #100 + #104 (both voidfreud, both quality-of-life fixes), the external-contributor track is now sustaining itself across consecutive days — not a one-off spike.

### Theme 3: The 31-PR Zero-Dependencies Streak Ends

**Summary:** PR #103 explicitly adds `duckdb >= 1.0.0` and `huggingface_hub >= 0.23.0` to both `backend/pyproject.toml` and `backend/requirements.txt`. The streak started at PR #72 (post-Apr-24) and held for 31 consecutive PRs (#72 → #102). PR #102 was the last zero-deps PR; PR #103 breaks it.

**Commits:** `58a80e5` (PR #103) — detailed above.

**Impact:** The streak was load-bearing in the "framework decoupled from price, externally validated" narrative — every PR for a month had shipped a new surface or fix while adding zero runtime dependencies, holding the line that MiroShark is a *composition* of stdlib services. PR #103's framing is careful: the deps are "optional, degrades to graph-only persona generation when these aren't importable" *in code*, but they're listed under unconditional `dependencies = [...]` in `pyproject.toml`, so the install surface grows. The streak is over, but the *behavioral* posture (degrades cleanly when deps absent) is preserved. The next zero-deps streak begins from PR #104 (already +0 deps) — currently 2 PRs long including PR #105 if it merges clean.

---

## aaronjmars/miroshark-aeon

**Summary:** 0 PRs merged. All commits in the window are skill auto-commits (token-report, fetch-tweets, tweet-allocator, repo-pulse, star-momentum, feature, self-improve, repo-actions, heartbeat) + scheduler `cron(state)` bookkeeping. No code or skill changes shipped to `main`.

**Open PRs at end-of-window (1):**
- **PR #45** (aaronjmars, opened 2026-05-24T13:20Z) — `improve: bankr-prefetch EXIT trap stamps 'crashed' status on silent failure`. From today's self-improve run after this morning's `TWEET_ALLOCATOR_ERROR` (prefetch-status.json missing). Adds a `trap ... EXIT` in `scripts/prefetch-bankr.sh` that stamps `{status:"crashed", exit_code, note, timestamp}` when the script exits non-zero before a `write_status` call; new `"crashed"` branch in `skills/tweet-allocator/SKILL.md` status switch.

---

## Developer Notes

- **New dependencies (first time in 31 PRs):** `duckdb >= 1.0.0`, `huggingface_hub >= 0.23.0` (both via PR #103 in `backend/pyproject.toml` + `backend/requirements.txt`).
- **Breaking changes:** None — PR #98's `_validate_project_id` is a strict regex but project_ids in active use are already alphanumeric+hyphen+underscore; PR #100's launcher guard is purely additive (only triggers on `neo4j+s://` URIs); PR #103's `country` / `demographic_filters` create-payload fields are optional with safe defaults.
- **Architecture shifts:**
  1. First *opt-in remote dataset dependency* (HuggingFace) in MiroShark history. Local fallback path exists (`backend/data/nemotron/<country>/data/train-*.parquet`), but the default path downloads on first use.
  2. First *pluggable JSON registry* pattern (`backend/app/countries/*.json` → `country_registry`). Drop a new file, no code changes — same shape MiroWorld's YAML country configs use; pure stdlib loader.
  3. `SimulationState` now carries `country` + `demographic_filters` — first persisted per-run metadata that's neither a config knob nor an output channel. New axis for sim-comparison and filtering.
- **Tech debt:** PR #102 backfilled openapi + tests that PR #97 should have shipped — pattern-lock evidence that the openapi/test drift only gets caught after `main` goes red. Adding a pre-merge CI step to fail on openapi drift would close this.

## What's Next

- **PR #105** (Platform Stats API + Badge) is the active-build candidate — already opened today, restarts the zero-deps streak at PR-count 2.
- **PR #104** (voidfreud gitignore) is a same-author follow-up to #100 — likely to merge inside 24h given the velocity pattern.
- **PR #45** (aeon bankr-prefetch EXIT trap) is queued; the trigger condition (silent script crash) is reproducible by removing `write_status` calls in a fixture.
- **Demographic grounding follow-ups:** the `country` field exists on `SimulationState` but no SPA filter / gallery facet consumes it yet. Likely next surface: `GET /api/gallery.json?country=sg` or a sim-comparison view that groups by `country`.
- **No active branches surfaced for the May-22 unbuilt items** (#1 Private Share Link, #2 French Locale).
