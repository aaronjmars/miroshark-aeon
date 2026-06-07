*Feature Built — 2026-06-07*

Platform Outcome Distribution

MiroShark's `/api/stats` endpoint already tells you *how big* the platform is — a sim count, a consensus distribution, an average confidence. It does not tell you what those sims *look like* in aggregate. PR #151 adds `GET /api/stats/distribution.json`, the shape companion: bucketed breakdowns of every public, completed sim across four dimensions plus two scalar averages — direction (bullish / neutral / bearish), confidence tier (high ≥70 / medium 40-70 / low <40), quality tier (excellent / good / fair / poor), and round count (short <10 / medium 10-20 / long >20).

Why this matters:
Until today, the question *"what fraction of MiroShark sims clear a high-confidence threshold?"* could only be answered by scraping the gallery and computing it client-side. A researcher citing the platform in a methods section, an Aeon digest reporting *"high-confidence sims rose from 28% to 36% of the corpus over the last 30 days,"* a directory builder displaying *"32% excellent / 52% good"* alongside the sim total, an integrator picking a `confidence_pct` cutoff that lands in the top quartile of historical sims — all four of those use-cases needed shape data the platform exposed as totals only. `repo-actions` flagged the gap on Jun 6 as the highest-impact net-new platform-analytics surface; this PR fills it.

What was built:
- `backend/app/services/outcome_distribution.py`: new ~440-LoC stdlib service. `build_distribution(sim_root)` walks `WONDERWALL_SIMULATION_DATA_DIR`, applies the same `is_public AND status==completed` publish gate `/api/stats` uses, and buckets each sim across the four dimensions. Reuses `signal_service.compute_signal` and the same trajectory-walk pattern as `platform_stats` / `project_stats` so a sim's contribution is byte-for-byte identical across the three platform surfaces.
- `backend/app/api/stats.py`: new `/distribution.json` route on the existing `stats_bp` blueprint. Sets `Cache-Control: public, max-age=300` (slower than `/api/stats`' 60-second cache — the consumer profile is press unfurls and slow-beat dashboards, not status-page polls) and supports `If-None-Match` short-circuit to 304.
- `backend/app/services/surfaces_catalog.py`: new `outcome_distribution` entry (type `analytics`). Catalog grows 32 → 33 entries.
- `backend/openapi.yaml`: full `OutcomeDistribution` schema with per-bucket field definitions and inline descriptions for each tier boundary.
- `frontend/src/api/simulation.js`: `getOutcomeDistribution()` + `getOutcomeDistributionUrl()` helpers.
- `docs/API.md` + `docs/FEATURES.md`: endpoint row and dedicated **Platform Outcome Distribution** section with example envelope and the four-audience framing.
- `backend/tests/test_unit_outcome_distribution.py`: 30 offline cases covering all four bucket dimensions, the publish gate, confidence boundaries (inclusive lower edge), case-insensitive quality matching, missing-trajectory handling, 5-minute cache TTL, ETag derivation and its distinctness from the platform / project sibling ETags, plus route / catalog / openapi / frontend wiring drift guards.

How it works:
Direction buckets follow the same plurality + `bullish > bearish > neutral` tie-break the per-sim `signal.json` uses, so a sim labelled Bullish on its per-sim verdict lands in the `bullish` bucket here byte-for-byte. Confidence tiers are inclusive on the lower edge — a sim landing exactly at 70 reads as `high`, not `medium`, so a corpus shift past the threshold reads as a jump in `high` rather than as boundary noise. Quality buckets read `quality.json.health` case-insensitively; sims with missing or unrecognised health values are still counted in `total_analyzed` but excluded from the four quality buckets, so the bucket sum is conservative on purpose. Round counts derive from the number of recorded `trajectory.json` snapshots — same source `peak_round.total_rounds` uses, so a sim's bucket here matches its per-sim peak-round count exactly. The ETag is `"distribution-<total_analyzed>-<YYYY-MM prefix of newest_completed_at>"` — a polling consumer's `If-None-Match` GET short-circuits to 304 until either a new sim completes (bumps the count) or the first sim of a new calendar month completes (bumps the month prefix).

What's next:
Four ideas from the Jun-06 batch are still net-new and unbuilt: Simulation Payload Validator (dry-run validate before spending $1 + 10 minutes on a malformed sim config), Signed Simulation Result (HMAC-SHA256 over the canonical signal JSON for offline integrator verification), Monthly Statistics Time-Series (month-by-month activity for growth dashboards), and Platform Agent Behavior Census (aggregated agent trajectory data for ML researchers).

PR: https://github.com/aaronjmars/MiroShark/pull/151
