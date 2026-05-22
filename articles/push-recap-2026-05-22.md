# Push Recap — 2026-05-22

## Overview

Two substantive PRs merged in the 24h window — PR #96 (BibTeX academic citation, MiroShark) and PR #44 (X.com reserved-paths filter, aeon) — alongside the standard daily skill-output stream. PR #96 lands the **14th publish-gated surface** on MiroShark and closes the academic citation arc (BibTeX → notebook → reproduce.json → DKG anchor); PR #44 is **aeon self-correction #4 in seven days**, this time with a 14-minute open-to-merge cycle. Zero new dependencies across both — the streak now sits at 30 consecutive MiroShark PRs.

**Stats:** 11 files changed, +1,227 / -2 lines across 2 substantive PRs · 26 cron / auto-commit housekeeping commits on the aeon side · 0 open PRs on either repo end-of-window.

---

## aaronjmars/MiroShark

### BibTeX Academic Citation Export — the citation arc closes (PR #96)

**Summary:** `GET /api/simulation/<id>/cite.bib` returns a one-call `@misc{…}` BibTeX entry for any published simulation. It drops directly into a LaTeX `\bibliography{}` block, imports cleanly into Zotero and Mendeley via "Import from URL" (both readers parse `text/plain` BibTeX at an HTTP URL directly), and chains the existing citation surfaces — `note` carries the `reproduce.json` SHA-256, `annote` carries the OriginTrail DKG UAL when the sim has been anchored on-chain. The hash precedence is DKG-anchor > fresh-compute > omit, so the on-chain literal is the source of truth whenever a sim has been published to DKG.

**Commits:**
- `4394d51` — `feat: BibTeX academic citation export — close the citation arc (#96)`
  - New file `backend/app/services/bibtex_service.py` (+338 lines): pure stdlib `hashlib` + `datetime` + `re`. Citation-key sanitizer (`miroshark-{simulation_id[:16]}` with non-`[A-Za-z0-9_-]` stripped — BibTeX grammar's citation-key allowlist, stable across re-renders so authors don't see their `\cite{}` references rewire). BibTeX special-character escaping for the seven specials (`& % $ # _ ^ ~`) plus backslash, brace, caret, tilde — uses a NUL-delimited sentinel for `\\` so `\textbackslash{}` doesn't get re-escaped on the brace pass. Bytewise-deterministic across calls with identical inputs.
  - New file `backend/tests/test_unit_bibtex_service.py` (+466 lines, 27 offline tests): citation-key shape · BibTeX escaping (all seven specials + brace + backslash + caret + tilde) · year/month derivation from ISO-8601 `created_at` · SHA-256 source precedence (DKG > fresh > omit) · annote UAL handling · URL composition · author default · bytewise determinism · route/MIME wiring · `surface_stats` registration · defensive fallbacks for missing/empty/non-string `simulation_id`.
  - Changed `backend/app/api/simulation.py` (+136 lines): new route handler. Reuses `_build_embed_summary_payload` for the `is_public` gate, sources `reproduce.json` bytes via `repro_export.render_json_bytes` (byte-for-byte identical to what the standalone `/reproduce.json` route serves — so a verifier's `curl reproduce.json | sha256sum` always matches the `note` field), reads DKG citation via `dkg_publisher.read_citation`. Returns `text/plain; charset=utf-8` (Zotero URL parser hint) with `Content-Disposition: inline; filename="miroshark-<id12>.bib"` (so `curl -OJ` lands a ready-to-include `.bib`), `Cache-Control: public, max-age=300` (matches reproduce.json + notebook cadence).
  - Changed `backend/openapi.yaml` (+94 lines): full endpoint spec under Publish & Embed; `cite_bib` added to `SurfaceStats` enum + properties block.
  - Changed `backend/app/services/surface_stats.py` (+1 line) and `test_unit_surface_stats.py` (+1 line) in lockstep — `cite_bib` joins `SURFACE_KEYS`. The locked-set test catches drift if the key is added to one but not the other.
  - Changed `frontend/src/api/simulation.js` (+26 lines): `getCiteBibUrl` helper.
  - Changed `frontend/src/components/EmbedDialog.vue` (+118 lines): 📖 BibTeX section between the notebook and DKG panels. Three copyable snippets (URL · `curl` command · LaTeX `\cite{miroshark-…}` reference, deterministic from sim id) plus a Download `.bib` button. Bilingual EN+ZH labels via existing `$tr()` pattern.
  - Changed `docs/API.md` (+1 line) and `docs/FEATURES.md` (+32 lines): endpoint table entry + full feature section.

**Impact:** This is the **fourteenth publish-gated surface** and the missing layer in MiroShark's citation chain. The chain a paper author now gets, for free, from a published sim:

1. **Paper bibliography** — `cite.bib` drops `@misc{miroshark-…}` into LaTeX.
2. **Verifiable parameters** — `reproduce.json` SHA-256 in the `note` field; reviewer runs `sha256sum --check` years later.
3. **Notebook analysis** — `notebook.ipynb` opens the same trajectory in Jupyter.
4. **On-chain provenance** — `annote` carries the DKG UAL when the sim has been anchored.

The architectural property: every step is a static HTTP URL on the MiroShark host. There is no publishing-house intermediary, no DOI registrar, no Zenodo upload step. A researcher cites a MiroShark simulation the same way they'd cite a paper — via a URL — and the citation tooling chain (Zotero "Import from URL", Mendeley "Import from URL", LaTeX `\bibliography{}`) consumes it without any custom adapter. This is DOI-grade citation infrastructure delivered as four static endpoints.

The PR also confirms the **architectural pattern lock**: PR #96 mirrors `signal_service` (PR #91) / `badge_service` (PR #94) / `repro_export` (PR #79) in every structural choice — pure stdlib (`hashlib` + `datetime` + `re`), bytewise-deterministic output, `is_public` publish gate, `<id12>` filename in Content-Disposition, 5-minute Cache-Control matching the watch-page poll cadence, `SURFACE_KEYS` + openapi-enum + property-block in lockstep. The next publish-gated surface won't need to invent any of these — the pattern is now load-bearing.

---

## aaronjmars/miroshark-aeon

### Self-Improve #4: filter X.com reserved paths from Bankr lookup (PR #44)

**Summary:** The `scripts/prefetch-bankr.sh` candidate-extraction grep treats every `x.com/<token>` URL fragment as a user handle. XAI annotation citations surface as `x.com/i/status/<id>` URLs (3–4/day in current fetch-tweets output), so `i` was leaking in as if it were a handle and consuming one Bankr Agent Max-Mode call (~112s polling budget) per prefetch run on a non-existent account. PR #44 adds a `RESERVED_X_PATHS` regex covering `i` plus the broader X.com URL surface (home, explore, compose, intent, messages, settings, search, hashtag, share, lists, bookmarks, topics, moments, analytics, following, followers, jobs, verified-orgs, tos, privacy, about, login, signup, logout, account, help) and chains it as a second `grep -viE` after the existing project-account exclusion.

**Commits:**
- `e662f9c` — `improve: filter X.com reserved paths from Bankr lookup candidates (#44)`
  - Changed `scripts/prefetch-bankr.sh` (+14, -2): one-line `RESERVED_X_PATHS=…` definition plus a `grep -viE "$RESERVED_X_PATHS"` chained after the existing `grep -viE '^(aaronjmars|miroshark_)$'`. The reserved-path list is anchored with `^…$` so a handle that happens to contain "help" as a substring (e.g. `@thinkhelpme`) passes through cleanly — only exact matches are dropped.
- `52b6bcd` — `log: self-improve PR #44 (filter X.com reserved paths from Bankr lookup)` — memory entry into `memory/logs/2026-05-22.md` recording diff, fixture-test validation, and impact estimate.

**Impact:** ~1 fewer wasted Bankr Agent Max-Mode call per daily prefetch run; tighter polling budget for real candidates; the `agent-timeout` status (added in PR #43 two days ago) now reflects only real-handle latency rather than including this silent waste of one slot. The bug was probably one of the 5/5 timed-out slots on May 21 that surfaced as `TWEET_ALLOCATOR_ERROR`.

The cadence is the load-bearing observation: bug diagnosed in yesterday's push-recap (May 21 19:25Z window), self-improve skill ran at ~13:17Z today, PR opened, PR merged at 13:31Z — **14 minutes from PR open to merge, <22 hours from diagnosis to ship**. That's now the fourth self-correction cycle in seven days, each tightening:

| # | PR | Symptom | Diagnosis → Merge |
|---|-----|---------|---|
| 1 | #40 | project-lens "merged"/"opened" verb drift | ~24h |
| 2 | #42 | repo-pulse article never written | ~36h |
| 3 | #43 | bankr-prefetch silent timeouts | ~30h |
| 4 | #44 | `@i` handle leaking from XAI citations | **<22h** |

### Substantive content commits on aeon main

- `3069798` — `feat(token-report): $MIROSHARK daily report 2026-05-22` (Sonnet 4.6 co-author). Post-ATH correction deepening: $0.00002141 (-23.85% 24h), FDV $2.14M, -50.9% from May-18 ATH $0.0000436. Volume halved to $318.3K (lowest since pre-breakout). Buy/sell ratio 1.09× — still marginally positive but compressing every session.

### Skill auto-commits

26 `chore(...)` commits cycled through every daily skill in the standard order: token-report → fetch-tweets → tweet-allocator → repo-pulse → star-momentum-alert → feature (= PR #96 build artifact) → self-improve (= PR #44 + log) → repo-actions. Plus yesterday's tail (heartbeat at 19:42Z May 21) that fell into this 24h window. The `chore(scheduler): update cron state` pattern interleaves each skill — visible cron-state ticks confirm the scheduler isn't drifting.

---

## Developer Notes

- **New dependencies:** none. PR #96 is pure stdlib (`hashlib` + `datetime` + `re`); PR #44 is bash (`grep -viE`). **30-PR zero-new-deps streak** preserved (PR #57 → … → #94 → #96).
- **Breaking changes:** none. `cite.bib` is a new surface; the reserved-paths filter is additive (a real handle named `@i` would now be dropped — but `i` is a reserved X.com path so this is the intended behavior).
- **Architecture shifts:** `SURFACE_KEYS` now holds **14 entries**. The citation arc has its canonical closing shape — four surfaces (BibTeX → notebook → reproduce.json → DKG) each at a static HTTP URL with bytewise-deterministic content and the same publish gate. Future "citation-grade" surfaces will graft onto this four-step chain rather than invent a new pattern.
- **Tech debt:** none introduced. Both PRs add tests in lockstep (PR #96 ships 27 offline unit tests; PR #44's validation is fixture-piped through the candidate filter).
- **Pattern lock confirmed:** PR #96 reuses every structural decision from `signal_service` / `badge_service` / `repro_export`. The next publish-gated surface will be implementation, not design.

## What's Next

- **May-20 batch: 2/5 addressed.** PR #94 (Status Badge SVG, idea #1) merged 2026-05-21; PR #96 (BibTeX, idea #2) merged today. Remaining: Belief Volatility Score (#3), Webhook Test Ping (#4), Gallery Public JSON (#5) — all "Small" infrastructure-precondition-free.
- **May-22 batch (new today, generated by repo-actions):** Private Share Link, French Locale Simulation Prompts (responds to issue #95), Polymarket-Ready Prediction JSON, Platform Aggregate Statistics API, Platform Stats Badge SVG. Polymarket-Ready (#3) is the highest-leverage external-integration play — `GET /<id>/polymarket.json` maps `signal.json` to YES/NO probability format, targeting the same use case that drove MiroFish to 32k stars.
- **Open issues on MiroShark:** #95 (French locale request) — directly addressed by repo-actions idea #2 today; #70 (Cyril Private Impact mode + MiroResult collaboration, substantial cross-builder feature track).
- **Open PRs:** 0 on both repos end-of-window. Clean slate for next feature-skill cycle.
- **Token watch:** $MIROSHARK -23.85% session, -50.9% from ATH, volume halved. Architecture cadence is now visibly decoupled from price action — PR #44 + PR #96 + token-report + 11 other skill cycles all landed cleanly while the token corrected through one of its deepest single-day pullbacks since pre-breakout.
- **Self-correction cadence trending up:** four PRs in seven days, latest cycle <22h diagnosis-to-ship. If a fifth lands inside three days, the cycle is sub-weekly and the framework is effectively self-tuning.
