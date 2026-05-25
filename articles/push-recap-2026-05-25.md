# Push Recap — 2026-05-25

## Overview
Four substantive commits landed across the two watched repos in the last 24h, all authored/merged by `@aaronjmars` and one returning external contributor. The thrust was platform-level self-description: MiroShark merged its **oEmbed provider** (#107) and **Platform Stats API + badge** (#105) — back-to-back surfaces that describe and distribute the *platform itself* rather than any single simulation — plus a tiny `.gitignore` hardening from external contributor Void Freud (#104). On the agent side, miroshark-aeon merged a defensive crash sidecar (#45) so the tweet-allocator can tell a crashed prefetch from one that never ran. Both feature merges held the zero-new-dependencies line.

**Stats:** 22 files changed, +2,418 / -10 lines across 4 substantive commits. (miroshark-aeon logged 48 commits total in the window; 47 were scheduler/skill auto-commits — see Developer Notes.)

---

## aaronjmars/MiroShark

### Platform Self-Description & Distribution Surfaces
**Summary:** Two new HTTP surfaces shipped that operate one level above individual simulations. `#105` exposes the platform's aggregate state as JSON + a Shields.io badge; `#107` makes any `/share/<id>` link auto-unfurl into a rich card on the major writing platforms. Both reuse existing services (badge geometry, surface-stats schema, stance derivation) rather than inventing new renderers — composition, not new machinery.

**Commits:**
- `a3fcbda` — feat: platform aggregate stats API + Shields.io platform badge SVG (#105)
  - New `backend/app/services/platform_stats.py` (+444): single O(n) scan over `WONDERWALL_SIMULATION_DATA_DIR` returning one envelope across every public+completed sim — total count, consensus distribution (bullish/neutral/bearish counts + %, using the same plurality rules as `signal.json`), average `confidence_pct`, total surface views, unique projects, newest-sim metadata. Carries a 60s module-level cache and a `stats_etag` helper for the route layer.
  - New `backend/app/api/stats.py` (+140): `stats_bp` blueprint mounted at `/api/stats`. The JSON route emits an ETag derived from `total_sims + newest_sim_id` and short-circuits `If-None-Match` → `304`; the badge route always returns `200` (a zero-sim deployment renders "MiroShark | 0 simulations").
  - Changed `backend/app/services/badge_service.py` (+146): added `build_platform_badge_svg` + `render_platform_badge_svg_bytes` as a sibling to the per-sim renderer, with a pinned platform-blue `#0ea5e9` distinct from the three stance colours.
  - New `backend/tests/test_unit_platform_stats.py` (+577): 27 offline tests — empty / mixed / unpublished / incomplete fixtures, cache-TTL bypass, ETag derivation, badge well-formedness, OpenAPI drift.
  - Wiring: `backend/app/__init__.py` (+6/-1) and `backend/app/api/__init__.py` (+5) register the blueprint; `backend/openapi.yaml` (+256) adds a Platform tag, both endpoints, and a `PlatformStats` schema; `test_unit_openapi.py` (+3) adds `stats_bp` to the blueprint→prefix drift table; docs (+46) describe both surfaces.

- `6cde359` — feat: oEmbed provider — auto-unfurl share links on Notion / Ghost / Substack / WordPress (#107)
  - New `backend/app/services/oembed_service.py` (+207): pure-stdlib core. Parses an inbound `url` to a `sim_id` with **host allow-listing** (never dereferences the URL; a foreign domain is rejected), builds the oEmbed 1.0 `type:"rich"` payload (share-card thumbnail + `/embed/<id>` iframe), and serializes to JSON or XML.
  - Changed `backend/app/api/share.py` (+181): adds the root-mounted `GET /oembed?url=&format=` route (publish-gated, domain-validated, `json`/`xml`, `501` on unsupported format) and injects `application/json+oembed` and `text/xml+oembed` discovery `<link>` tags into the `/share/<id>` head for public sims — the tags the writing platforms read instead of Open Graph.
  - Changed `backend/app/services/surface_stats.py` (+3/-1): registers the `oembed` counter (the surface-key set grows to 21).
  - New `backend/tests/test_unit_oembed.py` (+220): offline tests — URL→id parsing, host rejection, payload shape, XML round-trip, route + doc wiring; `test_unit_surface_stats.py` (+1) adds `oembed` to the expected key set.
  - Frontend `frontend/src/api/simulation.js` (+25): `getOEmbedUrl` helper. `openapi.yaml` (+98) + docs (+30) document the endpoint.

**Impact:** MiroShark can now answer "is this platform active, and how big is it?" in one request (`/api/stats`) and drop a live badge into any community README — useful for press kits, external dashboards, and LLM-agent health checks. And a pasted MiroShark share link now renders as a rich sim card on Notion/Ghost/Substack/WordPress instead of a bare URL, which removes friction from anyone writing *about* a simulation. Both extend the platform's reach without adding a dependency.

### Repo Hygiene (external)
**Summary:** A one-line `.gitignore` simplification from a returning external contributor.

**Commits:**
- `87f1ef2` — gitignore: collapse explicit .env profile list into .env.* wildcard (#104) — by **Void Freud** (external)
  - Changed `.gitignore` (+2/-5): replaced five explicit lines (`.env.local`, `.env.*.local`, `.env.development`, `.env.test`, `.env.production`) with a single `.env.*` wildcard plus a `!.env.example` exception. One pattern now absorbs any future profile (`.env.aura`, `.env.staging`, …) instead of the list growing per profile. The PR notes confirm only `.env.example` is currently tracked under `.env*`, which the exception preserves.

**Impact:** Small but real — future env profiles are ignored by default, closing a class of "accidentally committed a new `.env.<thing>`" mistakes. Notable mainly as a *fourth distinct external contributor* landing on the repo (Void Freud also authored the #100 Aura launcher), reinforcing the sustained-external-contribution trend.

---

## aaronjmars/miroshark-aeon

### Agent Self-Hardening
**Summary:** A defensive crash sidecar for the Bankr prefetch, fixing an observability gap that produced a misleading alert on 2026-05-24.

**Commits:**
- `c4e0c49` — improve(bankr-prefetch): EXIT trap stamps 'crashed' status so tweet-allocator can diagnose silent prefetch failures (#45)
  - Changed `scripts/prefetch-bankr.sh` (+25): added an `EXIT` trap that, when the script exits non-zero *before* reaching one of its normal `write_status` calls and the status file is still empty, writes `{status:"crashed", note, timestamp, exit_code, …}` to `.bankr-cache/prefetch-status.json`. This distinguishes "script never ran" (workflow misconfigured → file truly absent) from "script ran but bailed early" (e.g. `set -e` tripping on an unexpected `jq`/`grep` failure → file present with an exit code).
  - Changed `skills/tweet-allocator/SKILL.md` (+3/-2): added a `"crashed"` branch to the status-file dispatch that surfaces the exit code in a `TWEET_ALLOCATOR_ERROR` alert, and clarified that a *truly absent* file now unambiguously means the script never started (because the trap would otherwise have stamped `crashed`).

**Impact:** Closes the root cause of a 2026-05-24 `TWEET_ALLOCATOR_ERROR` where `prefetch-status.json` was missing and the failure was unrecoverable from logs. The allocator now reports the prefetch exit code instead of guessing "workflow misconfigured," so the next silent prefetch crash is diagnosable from the alert alone.

---

## Developer Notes
- **New dependencies:** None. Both MiroShark features are pure stdlib (`os`, `json`, `time`, `threading`, `xml.etree.ElementTree`, `re`, `urllib`), continuing the zero-new-deps posture (the broader streak having been reset by #103's duckdb/HF additions two days ago).
- **New API surface:** `GET /api/stats`, `GET /api/stats/badge.svg`, and `GET /oembed` are now live; `PlatformStats` and `OEmbedResponse` schemas added to `openapi.yaml`. Surface-key inventory grows to 21.
- **Security posture:** `#107` never dereferences the inbound `url` and rejects foreign hosts via allow-listing; private/missing sims return `404` without confirming existence. `#104` keeps `.env.example` the only tracked env file under the new wildcard.
- **Repo noise:** miroshark-aeon's 48-commit window is 47 scheduler/skill auto-commits (`chore(cron): … success`, `chore(<skill>): auto-commit`, `chore(scheduler): update cron state`) from the agent's own daily run, plus the single substantive #45. The GitHub Events API returned empty commit arrays for every push (squash-merge artifact), so the commits API was the source of truth for this recap.

## What's Next
- **PR #106 (Railway deploy prep, ext/DYAI2025)** is the last of the four recently-open MiroShark PRs still unmerged — likely the next merge candidate now that #104/#105/#107 are in.
- The May-24 idea batch still has four unbuilt items (#2 Peak-Round Belief Analytics, #3 Operator Profile, #4 Agent Persona Export JSON, #5 Simulation Search JSON API); with oEmbed (#1) now merged, those are the visible open threads for the next feature run.
- No branches were left dangling in this window — the only non-`main` push (`feat/platform-stats-api-and-badge`) was the #105 merge itself.
