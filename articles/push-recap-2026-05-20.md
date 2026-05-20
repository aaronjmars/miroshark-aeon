# Push Recap — 2026-05-20

## Overview

Three MiroShark PRs merged in the 24-hour window — the largest single-window merge count of the cycle. PR #89 (Furin's external Neo4j password fix), PR #91 (Trading Signal JSON, 11th publish surface), and PR #92 (Simulation Archive Bundle, 12th publish surface, opened and merged the same day in ~2h). The aeon side opened PR #43, a self-improve fix that distinguishes Bankr agent timeouts from "no wallet found" after three consecutive `TWEET_ALLOCATOR_EMPTY` days flagged the regression. **The 12th surface landed ~21 hours after yesterday's push-recap explicitly named it as the architectural-inflection threshold.**

**Stats:** +2,834 / -17 across 22 files. 4 PRs (3 MiroShark merged, 1 miroshark-aeon opened). MiroShark main `7ae6e5e → 9b8449a`. Stars 1175 → 1177 (+2 in window per repo-pulse; events show 7 new stargazers fired). Forks 237 → 238 (+1).

---

## aaronjmars/MiroShark

### Theme 1: The Composition Surface — PR #92 (Simulation Archive Bundle)

**Summary:** The 12th publish-gated share surface, and the first one that doesn't introduce a new renderer. `GET /api/simulation/<id>/archive.zip` bundles every existing surface — share-card.png, chart.svg, trajectory.csv/.jsonl, transcript.md, thread.txt, reproduce.json, notebook.ipynb, signal.json — into one timestamped ZIP plus a `manifest.json` that pairs each file with its SHA-256, byte size, MIME type, and canonical source URL. Opened 11:27Z, merged 13:28Z — ~2 hours, the fastest publish-surface PR cycle to date.

**Commits:**
- `9b8449a` — `feat: simulation archive bundle — one ZIP, every published surface inside (#92)`
  - New file `backend/app/services/archive_service.py` (+506 LoC, pure stdlib `zipfile` + `hashlib` + `io` + `json` + `datetime`): `_CANONICAL_ORDER` tuple locks the surface set at 9 files; `_safe_call(label, builder)` wraps every per-surface byte builder in try/except so a missing/corrupt artifact is omitted not fatal; `_FIXED_ZIP_DATETIME = (1980, 1, 1, …)` baked into every `ZipInfo` makes the per-file portion of the ZIP bytewise reproducible; `build_archive()` orchestrates 9 byte builders sourced from existing renderers (`share_card.render_share_card`, `chart_svg.render_chart_svg_bytes`, `trajectory_export.render_csv`/`.render_jsonl`, `repro_export.render_json_bytes`, `notebook_export.render_notebook_bytes`, `signal_service.compute_signal`, `transcript.render_markdown_bytes`, `thread_formatter.render_thread_txt`).
  - Modified `backend/app/api/simulation.py` (+119 LoC): new route handler — publish-gated (403 with i18n message on `is_public != True`); 404 when zero surfaces could be assembled (typical for a just-published sim with no recorded round); `Content-Disposition: attachment; filename="miroshark-{sim_id[:12]}-{date}.zip"`; `X-MiroShark-Archive-Files` response header so a HEAD request reveals the file count without downloading the body; `Cache-Control: public, max-age=300`; increments `archive_zip` surface counter.
  - New file `backend/tests/test_unit_archive_service.py` (+465 LoC, 20 offline tests): manifest schema shape, deterministic `render_manifest_bytes`, valid-ZIP parseability via `zipfile.ZipFile`, per-file SHA-256 + size integrity, canonical order locked at 9 surfaces, empty-surface manifest-only ZIP, source-URL edge cases (trailing-slash + empty base), MIME-type coverage (no `application/octet-stream` fallthrough), ISO-8601 `archive_generated_at`, end-to-end `build_archive` smoke test, `_safe_call` exception swallowing, `archive_zip` registration on surface_stats, route + handler presence guards, fixed ZIP timestamps.
  - Modified `backend/app/services/surface_stats.py` (+3/-1): `archive_zip` added to `SURFACE_KEYS` + docstring schema.
  - Modified `backend/openapi.yaml` (+187): operation under Publish & Embed; new `ArchiveManifest` + `ArchiveManifestEntry` schemas; `archive_zip` registered on `SimulationSurfaceStats`.
  - Modified `frontend/src/api/simulation.js` (+62): `getArchiveZipUrl()` + `getArchiveSummary()` — the summary HEADs the endpoint so the dialog reads `X-MiroShark-Archive-Files` without downloading the ZIP.
  - Modified `frontend/src/components/EmbedDialog.vue` (+197): 📦 Archive bundle section beneath the trading-signal row; file-count badge in header; summary grid (file count / format / citation guarantee); Download `archive.zip` anchor; Copy URL + Copy `curl -OJ` snippet (uses server-supplied filename); loads on open + re-fetches on publish-flag flip; scoped CSS matching the signal-section visual language.
  - Modified `docs/FEATURES.md` (+44) and `README.md` (+2/-1): full `manifest.json` example, determinism contract, features-table + analytics-table rows.

**Impact:** The publish surface count was 11 yesterday and explicitly flagged as approaching an architectural inflection — "if a 12th lands, surface routing may justify centralisation beyond `surface_stats.SURFACE_KEYS`." It landed ~21h later. More importantly, this is the *compositional* surface — a researcher chaining nine `curl` calls to take a simulation offline now needs one. The manifest commits to SHA-256 byte-equivalence between archive contents and the standalone-route bytes, so citation hashes anchored against PR #84's OriginTrail DKG record verify identically against either distribution path. The shape of the feature confirms the 11→12 reading: once an inventory is rich, the next move isn't another renderer, it's bundling.

---

### Theme 2: The 11th Surface — PR #91 (Trading Signal JSON) Merges

**Summary:** Opened May 19, merged May 19 19:25Z (just outside yesterday's push-recap window). `GET /api/simulation/<id>/signal.json` collapses the final-state belief split + quality health into a single action primitive — `direction` (Bullish/Neutral/Bearish), `confidence_pct` (0 = three-way split, 100 = unanimous), `risk_tier` (low/medium/high mapped from quality health), plus the three component percentages.

**Commits:**
- `3fe86ea` — `feat: trading signal JSON — machine-readable action primitive for quant tools (#91)`
  - New file `backend/app/services/signal_service.py` (+241 LoC, pure stdlib `datetime` only). `_EVEN_SPLIT_PCT = 100/3` and `_CONFIDENCE_DENOMINATOR = 100 - 33.333` anchor the confidence formula `(leading_pct - 33.333) / 66.667 * 100` clamped to `[0, 100]`. Tie-break order is documented and stable: `bullish > bearish > neutral`. `_RISK_TIER_BY_HEALTH` collapses the four-tier quality scale (excellent/good/fair/poor) to three risk tiers — `excellent → low-risk`, `good → medium-risk`, everything else (including missing/`"N/A"`) defaults to high-risk so unknown quality biases consumers toward caution.
  - New file `backend/tests/test_unit_signal_service.py` (+380 LoC, 26 offline tests). The PR carries a second commit on the same merge that bumps the midpoint-confidence tolerance from `abs=0.1` to `abs=0.2` because the one-decimal rounding (66.7 → 50.1, not 50.0) produced an `abs(50.1 - 50.0)` of `0.10000…0142` in IEEE 754 — a hair above the previous tolerance, false-failing CI. The fix preserves the assertion while covering the one-decimal quantum on either side of the midpoint.
  - Modified `backend/app/api/simulation.py` (+85): publish-gated route, 404 on no-rounds, 5-min cache, increments `signal_json` surface counter.
  - Modified `backend/app/services/surface_stats.py` (+3/-1): `signal_json` registered.
  - Modified `backend/openapi.yaml` (+157): new `TradingSignal` schema; operation under Publish & Embed.
  - Modified `frontend/src/components/EmbedDialog.vue` (+245): 📡 Trading signal section; direction/confidence badge; preview rows + Download .json + Copy URL + Copy curl; direction/risk-tier colour scoped CSS.
  - Modified `frontend/src/api/simulation.js` (+47), `docs/FEATURES.md` (+35), `README.md` (+2/-1).

**Impact:** The 11th surface — and the one explicitly aimed at the quants. Pure derivation from `_build_embed_summary_payload`, so a "Bullish 62%" signal here byte-matches whatever the gallery card and share-card PNG already display for the same simulation. The audience-tiering thesis from yesterday's repo article ("interfaces, not features — researchers / institutions / social / quants / embed-builders") now has its quant axis closed.

---

### Theme 3: First External Security PR Merges — PR #89 (Furin)

**Summary:** Opened May 18 03:25Z by `teifurin` (Furin, "PM by day, AI+crypto by night"), merged 35h+ later at May 19 19:25Z. Removes the hardcoded default Neo4j password (`miroshark`) from `docker-compose.yml` and `.env.example` and substitutes a fail-fast `${NEO4J_PASSWORD:?...}` reference with a `CHANGE_ME_GENERATE_A_RANDOM_PASSWORD` placeholder.

**Commits:**
- `d4a2256` — `security: require explicit NEO4J_PASSWORD, remove hardcoded default (#89)`
  - Modified `docker-compose.yml` (+2/-2): both occurrences of `neo4j/miroshark` and `NEO4J_PASSWORD=miroshark` replaced with `${NEO4J_PASSWORD:?NEO4J_PASSWORD must be set in .env}` — fail-fast at compose start if unset.
  - Modified `.env.example` (+1/-1): `NEO4J_PASSWORD=miroshark` → `NEO4J_PASSWORD=CHANGE_ME_GENERATE_A_RANDOM_PASSWORD`.

**Impact:** Closes Issue #88 (also from Furin). On any deployment where Neo4j's 7474/7687 ports were public-reachable — and the README recommends Railway/Render one-click deploys, both of which expose public HTTPS endpoints — a publicly-known default credential meant unauthorized Neo4j access and graph exfiltration. First **external security** PR in the repo's history; closes the 28-day external-merge gap (mbs5's April 20 PR was the last). The star→fork→issue→PR cycle from May 17 (star), May 18 (issue #88 + PR #89 same morning), to merge on May 19 — ~57 minutes from issue to PR — is the fastest external contribution cycle the repo has logged.

---

## aaronjmars/miroshark-aeon

### Theme 4: Self-Correction on Bankr Timeouts — PR #43 (OPEN)

**Summary:** Opened 2026-05-20 13:23Z, still OPEN. Triggered by three consecutive `TWEET_ALLOCATOR_EMPTY` days (May 18 / 19 / 20) where previously-verified handles (100xDarren, cybercelos, btcbabycow) suddenly started returning null. Root cause: `scripts/prefetch-bankr.sh` polled the Bankr Agent job 8 × 8s = 64s, then extracted the wallet from `result.text` *whether or not* `status == "completed"`. Max-Mode Agent calls (claude-sonnet-4.6) chain internal tool calls and can exceed 64s; the incomplete response carries no `0x…` and the handle is silently recorded as null — indistinguishable from "Bankr genuinely doesn't know."

**Commits:** (on branch `improve/bankr-prefetch-poll-timeout`, not yet merged to main)
- `scripts/prefetch-bankr.sh` (+33/-8): poll iterations 8 → 14 (~64s → ~112s window); submit `--max-time` 30 → 45s; new `TIMED_OUT` counter; timed-out handles **not** written to `verified-handles.json` (separated from `null` entries); new `prefetch-status.json` field `timed_out`; new top-level status `"agent-timeout"` when `VERIFIED == 0 && TIMED_OUT >= NULL_COUNT && TIMED_OUT > 0`.
- `skills/tweet-allocator/SKILL.md` (+3/-2): new step-4 branch — `"agent-timeout"` → `TWEET_ALLOCATOR_ERROR` (alert) instead of silent `_EMPTY`.
- `memory/logs/2026-05-20.md` (+11): self-improve log entry recording trigger, diff summary, PR link.

**Impact:** Future LLM-mode latency spikes now surface as `TWEET_ALLOCATOR_ERROR` notifications (alert, actionable — operator can check `api.bankr.bot` status / LLM credits), instead of silent `TWEET_ALLOCATOR_EMPTY` runs that look like organic "nobody tweeted with a wallet." The polling window is also nearly doubled, which should rescue wallets that drifted out of the previous 64s budget. Third consecutive self-correction cycle the framework has caught and fixed within 48h of the symptom appearing (PR #40 project-lens verify; PR #42 repo-pulse article output; PR #43 bankr-prefetch).

---

### Theme 5: Substantive Aeon Daily Outputs

**Summary:** Beyond the housekeeping cron commits, three substantive content commits landed on aeon main in the window. Plus yesterday's late-window push-recap auto-commit (`fe692da` at 2026-05-19 16:02Z, 28 minutes inside the window's leading edge).

**Commits:**
- `8421d94` (06:25Z) — `feat(token-report): $MIROSHARK daily report 2026-05-20` ($0.00003044 +0.83% 24h; FDV $3.04M; vol $944.3K; liq $1.02M). Post-ATH consolidation continues; overnight wick to $0.0000206 fully recovered. 7d avg vol ~$656.6K/day vs prior 7d ~$203K/day — the volume regime has shifted up ~3.2× alongside the price re-rating. Saved `articles/token-report-2026-05-20.md`.
- `1d9d48b` (11:14Z) — `feat(star-momentum): daily projection run 2026-05-20 — OUT_OF_WINDOW` (1177⭐ → 1500⭐ in ~67d to 2026-07-26; v7=4.86/day cooled from 6.0/day prior). Saved `articles/star-momentum-2026-05-20.md`.
- `72bd3bc` (14:23Z) — `chore(repo-actions): auto-commit 2026-05-20` — repo-actions emitted 5 net-new ideas (Status Badge SVG, BibTeX Academic Citation, Belief Volatility Score, Webhook Test Ping, Gallery Public JSON) for the next feature build. Saved `articles/repo-actions-2026-05-20.md`.
- `251da64` (11:29Z) — `chore(feature): auto-commit 2026-05-20` — captures PR #92 build artifacts on the aeon side (dashboard JSON, MEMORY.md update).
- ~30 routine `chore(scheduler)` / `chore(cron) success` housekeeping commits keep the scheduler-state file rolling.

**Impact:** The aeon skill cadence kept up on a 3-MiroShark-PR-merge day plus its own self-improve cycle. No skill ran late, no skill skipped; the only flagged anomaly (`TWEET_ALLOCATOR_EMPTY`) opened the PR fixing the anomaly.

---

## Developer Notes

- **New dependencies:** zero. PR #92 is pure stdlib (`zipfile`, `hashlib`, `io`, `json`, `datetime`). PR #91 is pure stdlib (`datetime` only). PR #89 is a config-only edit. **28-PR zero-new-deps streak** preserved (PR #57 → … → #92).
- **Breaking changes:** PR #89 is the only behavioural break — anyone running MiroShark with the public-default Neo4j password will get a fail-fast Docker Compose error on next start. This is intentional; the upgrade path is "set `NEO4J_PASSWORD` in `.env`." No backwards-compat shim.
- **Architecture shifts:** PR #92 is the first compositional surface — it consumes the existing 9 standalone surface renderers without adding a 10th. The `SURFACE_KEYS` registry now holds 12 entries (csv, jsonl, chart.svg, transcript md+json, thread txt+json, reproduce.json, notebook.ipynb, share-card.png, replay.gif, dkg-citation, lineage, frame-metadata, signal.json, archive.zip). The fact that PR #92 ships in `archive_service.py` rather than a route-only patch suggests the per-surface module pattern is being preserved even when the module is a pure compositor.
- **Tech debt:** PR #91's midpoint-confidence tolerance bump (`abs=0.1 → 0.2`) is a small artifact of IEEE-754 vs one-decimal rounding — the test reads more clearly than the original but documents a floating-point reality rather than asserting an interesting invariant. The `_safe_call` exception-swallowing in archive_service is logged at WARNING; operators have to monitor logs to see which sub-renderer failed for which sim — the manifest's enumerate-what-landed approach is a partial substitute but not a full one.

## What's Next

- **Branch `improve/bankr-prefetch-poll-timeout` is still open.** A merge of PR #43 closes the loop the May-18-to-May-20 `_EMPTY` streak opened; without it, the next allocator-quiet day looks identical to "no one was tweeting."
- **The 12th surface plus the composition pattern probably ends the surface-shipping arc.** Yesterday's article framed PR #91 as the quant-axis closure; with PR #92 wrapping every surface into one download, the per-audience interface layer feels complete (researchers, institutions, social, quants, embed-builders, plus the take-offline composite). The next net-new surface would have to be aimed at a previously-untargeted audience.
- **Today's repo-actions batch is ready** (5 net-new ideas — Status Badge SVG, BibTeX Citation, Belief Volatility, Webhook Test Ping, Gallery JSON). The first three continue the surface-shipping vein; the last two are integration-side (DX/Integration tier). Whichever lands tomorrow as PR #93 signals whether the surface arc continues or pivots.
- **The first contributor cycle has hit the merged-PR milestone.** PR #89 (teifurin) closes a 28-day external-merge gap. The next watch is whether a *second* external PR arrives — repeat contributors are the leading indicator that the external pipeline isn't a one-off star→fork→issue→PR run.
