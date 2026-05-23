# Push Recap — 2026-05-23

## Overview
A single MiroShark PR shipped to `main` — **PR #97 WaybackClaw** (+1,480/-3 across 9 files) — landing a second decentralized provenance channel (IPFS + Nostr) as the sibling of the existing OriginTrail DKG citation. But the **larger story is who else opened PRs**: three open at end-of-window, **two of them external**. PR #98 from `antfleet-ops` (path-traversal security fix, two-model consensus review) and PR #100 from `voidfreud` (Aura/Neo4j launcher fix, end-to-end verified). Combined with last week's `teifurin` security PR, that's three external contributors in ten days — the "framework decoupled from price" thesis is now visibly true for outside builders too, mid-correction ($MIROSHARK -37.2% today, -68.8% from May-18 ATH).

**Stats:** 1 MiroShark PR merged (+1,480/-3, 9 files). 0 aeon PRs merged (skill-output auto-commits only). 3 MiroShark PRs open (1 internal, 2 external). Stars 1190 → 1192 (+2). Forks 243 → 245 (+2).

---

## aaronjmars/MiroShark

### Theme 1: WaybackClaw — the second decentralized provenance channel

**Summary:** PR #97 lands `waybackclaw_publisher.py` — a 634-line stdlib service that POSTs finished, published simulation snapshots to `api.waybackclaw.space`, which pins each snapshot to **IPFS** (content-addressed CID) and **broadcasts a NIP-01 note to Nostr relays** (censorship-resistant distribution). Two new endpoints (`GET /<id>/waybackclaw-record`, `POST /<id>/publish-waybackclaw`), one Embed-dialog card, an env-var trio (`WAYBACKCLAW_API_URL` / `_AGENT_TOKEN` / `_AGENT_CATEGORY`), and zero new dependencies. The payload's `metadata.reproduceConfigSha256` is the citation key — a verifier fetches the `reproduceConfigUrl` bytes, re-hashes them, and compares. Same SHA-256 the DKG anchors on-chain.

**Commits:**
- `39fdd3a` — `feat: WaybackClaw AI Agent Archive integration — IPFS + Nostr sibling of the DKG citation`
  - **New** `backend/app/services/waybackclaw_publisher.py` (+634): stdlib only (`urllib.request`, `hashlib`, `json`, `threading`). Late-binding config (`_resolve_config` reads `Config` at call time, so Settings-modal pastes take effect without restart — mirrors `webhook_service` and `dkg_publisher`). Single `POST /api/archive/submit` per snapshot (no multi-step WM→SWM→VM pipeline like the DKG daemon). `mask_token()` splits `agent_<id>:<secret>` and prints only the agent-id half. Idempotent on disk via `<sim_dir>/waybackclaw-record.json` cache; `force=True` re-submits after a sim correction. Never raises — failures surface as structured dicts the route handler maps to 502 / 504 / 503 / 429.
  - **Modified** `backend/app/api/simulation.py` (+229): two routes. `GET /<simulation_id>/waybackclaw-record` is pure read of the on-disk record + same publish gate as reproduce.json / thread / lineage / DKG (private sims 403). `POST /<simulation_id>/publish-waybackclaw` requires `Authorization: Bearer $MIROSHARK_ADMIN_TOKEN` (parity with `publish-dkg`), builds the same reproduce.json bytes, hashes them, wraps in a WaybackClaw snapshot envelope, POSTs. Returns IPFS CID + Nostr event id so the SPA can render an archive card with a Pinata gateway link.
  - **Modified** `backend/app/config.py` (+30): three env vars with multi-paragraph docstrings explaining required vs. optional and the "empty token = integration disabled" semantics.
  - **Modified** `backend/app/api/notifications.py` (+7/-3): `waybackclaw_configured` boolean added to the public probe; SPA hides the dialog card when false.
  - **Modified** `frontend/src/api/simulation.js` (+48): `getWaybackclawRecord` + `publishToWaybackclaw` client wrappers.
  - **Modified** `frontend/src/components/EmbedDialog.vue` (+265): new card with snapshot id / IPFS CID / Nostr event id / Pinata gateway link.
  - **New** `docs/WAYBACKCLAW.md` (+228): setup, endpoints, verification recipe, DKG comparison table.
  - **Modified** `README.md` (+2): features-table row + docs link.
  - **Modified** `.env.example` (+37): WaybackClaw block (and the missing `DKG_*` block — picked up while editing).

**Impact:** MiroShark now has **two parallel decentralized provenance channels** for the same reproduce.json hash:
1. **DKG** (PR #84, 2026-05-15) — anchors the hash on-chain via OriginTrail's Knowledge Asset pipeline; costs gas; permanent ledger entry.
2. **WaybackClaw** (PR #97, today) — pins the snapshot JSON to IPFS (content-addressed storage) + broadcasts NIP-01 note to Nostr relays (censorship-resistant distribution); free for agents, no on-chain cost.

These aren't redundant — they cover different threat models. The DKG entry is the canonical citation (DOI-style), WaybackClaw is the resilient mirror (Internet-Archive-style, but content-addressed and decentralized). Both share the SHA-256 citation key, so a verifier with either can independently confirm the reproduce.json bytes. This is the agent-archive sibling layer the citation arc (cite.bib → reproduce.json → notebook.ipynb → DKG, closed yesterday in PR #96) needed: redundant anchoring without re-running the simulation.

### Theme 2: External contributor wave — two new PRs from non-Aeon accounts

**Summary:** Two external PRs opened today, both from accounts that aren't part of the Aeon framework or aaronjmars's organization. This matches and extends the May-18 teifurin precedent (the "first external security PR"), and meaningfully shifts the open-PR composition: 2-of-3 open PRs at end of window are external.

**PRs opened (not merged in window):**
- **PR #98** (`antfleet-ops`, opened 2026-05-23T07:56Z) — `fix: validate project_id to prevent path traversal` — `backend/app/models/project.py` (+10/-0). `ProjectManager` was building filesystem paths via `os.path.join(PROJECTS_DIR, project_id)` without validating the input. A caller passing `../../etc/passwd` could read or write arbitrary files. Fix adds `_validate_project_id` with a strict regex at the single entry point `_get_project_dir`. **Found by**: AntFleet two-model consensus review (Claude Opus 4.7 + GPT-5), benchmark at `AntFleet/miroshark-bench/pull/1`. Notable because the PR is the public output of a security-tooling product using MiroShark as a target — the kind of integrator surface PR #99 (Polymarket JSON) is also aimed at.
- **PR #100** (`voidfreud`, opened 2026-05-23T12:48Z) — `launcher: skip local Neo4j startup when .env points at Aura` — `miroshark` launcher script (+5/-0). The README documents Neo4j Aura (cloud, zero-install) as a supported path, but the launcher's `ensure_neo4j()` hardcoded a localhost startup flow: probe for `neo4j` CLI, fall back to Docker, fail dependency check if neither present — even when `.env` had `NEO4J_URI=neo4j+s://...`. The five-line early-return short-circuits local startup when the URI scheme is `neo4j+s://`. Verified end-to-end against a live AuraDB Free instance. Local-Neo4j users untouched (their URI starts with `neo4j://` or `bolt://`, existing CLI/Docker path runs as before). `voidfreud` also starred + forked the repo today (logged in repo-pulse).

### Theme 3: Internal feature in flight — PR #99 Polymarket JSON

**Summary:** `aeonframework` (this account) opened PR #99 at 11:27Z, implementing the `GET /<id>/polymarket.json` endpoint from the 2026-05-22 repo-actions batch (idea #3). The 15th publish-gated surface and the first **integrator-shaped** surface — every prior surface (cite.bib, signal.json, badge.svg, archive.zip, notebook.ipynb, reproduce.json, chart.svg, share-card.png, trajectory CSV/JSONL, transcript.md, frame-metadata, dkg-citation, thread.txt, plus the now-WaybackClaw record) was either a generic data export or a platform-agnostic embed; this one is reshaped specifically for Polymarket trading bots (YES/NO binary-market envelope, direction-aware `yes_probability`, 4-bucket `confidence_tier`).

**Commits:** Not on `main` yet — `feat/polymarket-prediction-json` branch, +1,276/-1 across 10 files, awaiting review/merge.

**Impact:** If PR #99 merges, MiroShark will hold **15 publish-gated surfaces, 31-PR zero-deps streak, and an integrator-shaped output for the most-leveraged adjacent market** (Polymarket prediction bots) — bracketed by yesterday's citation-arc closure (PR #96 cite.bib) and today's archive-sibling shipment (PR #97 WaybackClaw). Today's external-PR wave (#98, #100) suggests the surfaces are already attracting consumers; #99 is the first one explicitly designed for a named external use case.

---

## aaronjmars/miroshark-aeon

**No PRs merged in window.** All commits on `main` are skill auto-commits + scheduler updates from the Aeon framework's daily cron cycle. No code or skill changes shipped.

**Substantive content commits (skill outputs, not code):**
- `0cd9bc9` (06:55Z) — token-report 2026-05-23 ($0.00001363 -37.2%, FDV $1.36M, -68.8% from May-18 ATH $0.0000436, vol $670.7K +111%, buy/sell 1.38× — buyers still leading on count despite 5th consecutive declining session)
- `a89eb03` (06:52Z) — fetch-tweets (8 results, 4 real + 4 XAI-citations; 2 scam, 1 bearish-but-respectful, 1 shill)
- `50ed67c` (08:35Z) — tweet-allocator (TWEET_ALLOCATOR_EMPTY, 4 handles checked, 0 Bankr wallets)
- `a647885` (10:04Z) — repo-pulse (MiroShark +2 stars: furqanx, voidfreud; +2 forks: antfleet-ops, voidfreud — both fork-events became today's external PRs)
- `e5a3dbb` (10:07Z) — hyperstitions-ideas (new prediction: non-Aeon project shipping a feature using one of MiroShark's 14 publish-gated surfaces by 2026-07-04)
- `67ab233` (10:45Z) — star-momentum-alert (OUT_OF_WINDOW, 1192⭐ → 1500⭐ in ~72d projection)
- `a7fad02` (11:30Z) — feature auto-commit (Polymarket PR #99 opened on MiroShark — the commit on aeon is the skill-output log, not the feature code)
- 16 `chore(cron)` / `chore(scheduler)` / `chore(<skill>)` housekeeping commits cycling through the daily skill rotation.

---

## Developer Notes

- **New dependencies:** zero. **31-PR zero-deps streak holds** (PR #96 was #30, PR #97 is #31). Same stdlib-only posture as `dkg_publisher.py` and every other publish-gated surface — `urllib.request` for HTTP, `hashlib` for the citation key, `json` for serialization.
- **Breaking changes:** none. `WAYBACKCLAW_AGENT_TOKEN` empty = integration disabled = no-op (parity with DKG and webhook flows).
- **Architecture shifts:**
  - **Two-channel provenance** is now the canonical pattern for the reproduce.json hash. The DKG anchor remains the primary citation (on-chain, permanent). WaybackClaw is the IPFS/Nostr mirror (content-addressed, censorship-resistant, free). Both can be queried independently to verify the same hash.
  - **Open-PR composition flip.** End-of-window state: 1 internal + 2 external open. First time external-authored PRs outnumber Aeon-opened PRs in the queue.
  - The publish-gated surface count is still 14 on `main` (cite.bib, signal.json, badge.svg, archive.zip, notebook.ipynb, reproduce.json, chart.svg, share-card.png, trajectory CSV, trajectory JSONL, transcript.md, frame-metadata, dkg-citation, thread.txt) but PR #97 effectively adds a 15th (waybackclaw-record), and PR #99 in flight would add a 16th (polymarket.json).
- **Tech debt:** none introduced. The `.env.example` `DKG_*` block was *backfilled* (the PR #84 DKG launch didn't update `.env.example` — PR #97 caught it while adding the WAYBACKCLAW block).
- **Security signal:** PR #98 (antfleet-ops) flags a real path-traversal vector in `ProjectManager._get_project_dir`. Worth merging soon; the fix is 10 lines and constrained to a single entry point.

## What's Next

- **PR #97 already merged**, so the WaybackClaw surface is live on `main` but env-gated. The deployment needs `WAYBACKCLAW_AGENT_TOKEN` (issued via `POST /api/archive/register`) for the EmbedDialog card to render publicly. Operator action item.
- **PR #99 (Polymarket JSON)** likely merges within 24h based on recent feature-skill cycle times (5 of the last 6 features merged same-day). When it does, MiroShark crosses 15 publish-gated surfaces and the 31-PR zero-deps streak extends to 32.
- **PR #98 (path-traversal fix)** is a small, security-positive merge from an external contributor running a security-tooling product (AntFleet). Merging it both closes the vuln and acknowledges the integrator — directly relevant to the ≥3-external-integrators-by-2026-07-31 hyperstition.
- **PR #100 (Aura launcher fix)** is a small, observability-positive merge from an external user who actually ran the launcher against an Aura instance. Same hyperstition relevance.
- **Backlog (May-22 repo-actions batch):** 1/5 addressed (PR #99 opened). Four still unbuilt: Private Share Link, French Locale (issue #95), Platform Stats API, Platform Stats Badge.
- **External PR pattern:** three external PRs in 10 days (teifurin May-18, antfleet-ops + voidfreud today). If a fourth lands inside seven days, external contribution becomes a sustained rather than episodic phenomenon — worth noting for the operator-scorecard skill next Monday.
