# Push Recap — 2026-05-19

## Overview

Two MiroShark surfaces moved this cycle: PR #90 (Farcaster Frame v2) merged ~25h after opening, and PR #91 (Trading Signal JSON) opened as the 11th share surface. On the aeon side, PR #42 (repo-pulse article output) merged — closing the architectural gap flagged just 48h earlier by skill-freshness. The Base-chain audience loop and the quant-tool action primitive both shipped or moved into review on the same day.

**Stats:** +2,362 / -3 lines across 21 files merged or pushed. 1 MiroShark PR merged (main), 1 MiroShark PR opened (branch), 1 aeon PR merged. 27-PR zero-new-deps streak preserved (PR #57 → #87 → #90 → #91 candidate).

---

## aaronjmars/MiroShark

### Theme 1: Farcaster Frame v2 — the Base-chain audience loop closes

**Summary:** PR #90 introduces `fc:frame:*` meta-tag injection to public share pages and a new `GET /api/simulation/<id>/frame-metadata` route. A `/share/<id>` URL pasted into a Farcaster cast now renders as an interactive belief-chart card directly inside the Warpcast feed with a single "View Simulation →" link button — the same unfurl every other paste context (Twitter, Discord, Slack, iMessage, Notion) already had. This is the audience-side completion of the chart-SVG arc that started with PR #85 yesterday.

**Commits:**
- `4d5c576` — feat: Farcaster Frame v2 — interactive belief-chart cards in Warpcast (#90)
  - **New** `backend/app/services/frame_metadata.py` (+235 lines): `build_frame_metadata()` + `warpcast_compose_url()` helpers; pure stdlib; selects `chart.svg` at 2:1 as the Frame image for sims with recorded rounds, falls back to `share-card.png` at 1.91:1 for pre-trajectory sims, suppresses Frame tags entirely for private sims.
  - **Modified** `backend/app/api/share.py` (+84): emits `fc:frame:*` meta-tag block in `<head>` alongside existing Open Graph / Twitter Card tags. Suppressed for private sims.
  - **Modified** `backend/app/api/simulation.py` (+75): `GET /<id>/frame-metadata` route — publish-gated, 5-min cache, proxy-aware base URL.
  - **New** `backend/tests/test_unit_frame_metadata.py` (+403 lines, 13 offline tests).
  - **Modified** `backend/openapi.yaml` (+165): endpoint definition + `FrameMetadata` + `FrameMetadataButton` schemas under Publish & Embed.
  - **Modified** `frontend/src/components/EmbedDialog.vue` (+124): 🟣 Farcaster Frame section with Warpcast composer link, dialog-open + publish-toggle loaders.
  - **Modified** `frontend/src/api/simulation.js` (+39): `getFrameMetadata()` + `buildWarpcastComposeUrl()` helpers.
  - **Modified** `docs/FEATURES.md` (+13), `docs/API.md` (+1), `README.md` (+1).
  - **Pace:** opened 2026-05-18 12:26Z → merged 2026-05-19 13:50Z (~25.5h).

**Impact:** $MIROSHARK lives on Base; the Base-native social network is Farcaster. Until today, a cast containing a `/share/<id>` URL rendered as a blank link card while every other platform got a rich preview. PR #90 makes the Frame backing image the per-round belief chart SVG (PR #85 merged yesterday), so the audience reads the simulation's trajectory directly inside the feed without expanding. PR #85 unlocked this — it was the prerequisite Frame image format. Two adjacent PRs, one citation-chain stop.

### Theme 2: Trading Signal JSON opens — the 11th share surface

**Summary:** PR #91 (open) collapses the final-round belief split + quality health into a single machine-readable action primitive at `GET /api/simulation/<id>/signal.json`. Direction (Bullish / Neutral / Bearish), confidence_pct (0 = pure split, 100 = unanimous), risk_tier (low/medium/high from quality health), plus the three component percentages. Pure derivation from the existing embed-summary payload — a "Bullish 62%" signal here is byte-identical to what every other surface reports.

**Commits:**
- `5d9ddd5` — feat: trading signal JSON — machine-readable action primitive for quant tools
  - **New** `backend/app/services/signal_service.py` (+241 lines): `compute_signal(summary)` — plurality with `bullish > bearish > neutral` tie-break, confidence anchors (33.3% ⇒ 0, 100% ⇒ 100, 66.7% ⇒ ~50), 1-dp rounding, ISO-8601 UTC + Z timestamp.
  - **New** `backend/tests/test_unit_signal_service.py` (+372 lines, 26 offline tests covering payload shape, plurality + tie-break, confidence anchors, risk-tier mapping for excellent/good/fair/poor/N/A/empty, every None-returning input path, route + counter registration).
  - **Modified** `backend/app/api/simulation.py` (+85): `GET /<id>/signal.json` route, publish-gated, 404 on no-rounds, 5-min cache, increments `signal_json` surface counter.
  - **Modified** `backend/app/services/surface_stats.py` (+3, -1): `signal_json` added to `SURFACE_KEYS` + docstring schema.
  - **Modified** `backend/openapi.yaml` (+157): `/api/simulation/{id}/signal.json` operation; new `TradingSignal` schema; `signal_json` registered on `SimulationSurfaceStats`.
  - **Modified** `backend/tests/test_unit_surface_stats.py` (+2): locked-set + parametrized counter test updated.
  - **Modified** `frontend/src/components/EmbedDialog.vue` (+245): 📡 Trading signal section with direction/confidence badge, preview rows, Download .json + Copy URL + Copy curl, scoped CSS for direction/risk-tier colours.
  - **Modified** `frontend/src/api/simulation.js` (+47): `getSignalJsonUrl()` + `getSignalJson()` helpers, 403/404 → null.
  - **Modified** `docs/FEATURES.md` (+35), `README.md` (+2, -1).
  - **Status:** open (~4h old at recap time).

**Impact:** Closes the gap between "a sim produces data" and "a sim produces a signal." MiroShark output can now land directly in a Zapier / Make / n8n workflow or alert pipeline without a notebook step. This is the quant-audience surface — same posture as PR #80 (Jupyter) for the researcher audience and PR #84 (DKG citation) for the institutional audience. Surface count: 11 (trajectory.csv/.jsonl, chart.svg, transcript.md/.json, thread.txt/.json, reproduce.json, notebook.ipynb, share-card.png, replay.gif, dkg-citation, lineage, **signal.json**).

### Theme 3: Three open PRs at recap close

- **#89** (Neo4j password security, +3/-3, opened 2026-05-18 03:25Z by `teifurin`) — first external-contributor security PR, ~36h old, no maintainer touch yet.
- **#90** — merged in this window.
- **#91** (Trading Signal JSON, +1,189/-2, opened today 11:39Z by aeon-feature) — ~4h old.

---

## aaronjmars/miroshark-aeon

### Theme 4: repo-pulse article output lands — 48h from audit to merge

**Summary:** PR #42 adds step 7 to `skills/repo-pulse/SKILL.md`, instructing repo-pulse to write `articles/repo-pulse-${today}.md` with canonical fields (`stargazers_count`, `forks_count`, `New stars (24h)`, `New forks (24h)`). Five downstream consumer skills (operator-scorecard, thread-formatter, star-momentum-alert, show-hn-draft, skill-freshness) had been referencing this article path for weeks, but the producer never wrote the file — they were silently falling back to memory/logs parsers. The May-17 skill-freshness audit explicitly flagged the gap; the May-18 self-improve skill opened the fix; today it merged.

**Commits:**
- `7ea2f61` — improve: have repo-pulse write articles/repo-pulse-YYYY-MM-DD.md (#42)
  - **Modified** `skills/repo-pulse/SKILL.md` (+33, -1): new step 7 "Write the article" with format rules + idempotency-skip handling; renumbered existing log step to 8; added `**Article:**` pointer in step 8.
  - **Pace:** opened 2026-05-18 13:37Z → merged 2026-05-19 13:50Z (~24h).
  - **Backward compat:** memory/logs remains the deltas source-of-truth; existing consumer fallbacks keep working unchanged; same-day reruns overwrite (idempotent, matches token-report / operator-scorecard pattern).

**Impact:** Closes the longest-standing producer/consumer gap in the aeon skill graph. From the May-17 audit observation to merged fix: 48h. The self-improve → PR → merge loop is operating as designed; this is the second consecutive self-correction cycle to close within 48h (PR #40 project-lens verify on 2026-05-16 was the first).

### Theme 5: Substantive aeon main commits in window

- `f29f587` — token-report 2026-05-19: $0.0000309 (-1.31% 24h), post-ATH consolidation, FDV $3.09M (was $3.32M at yesterday's ATH peak), buy/sell 1.34×, 7d +106%. New article (+48), log entry (+14).
- `86bc37d` — repo-pulse log: 1175 stars (+4: Gawc1uuu, skylarbarrera, BXSWSSMBDX, ALPHAlcl), 237 forks (+1: aigen-x/MiroShark).
- `2022069` — feature auto-commit for PR #91 build (dashboard JSON output, memory log, MEMORY.md update). +221/-4 across 6 files.
- `363c098` — project-lens HyperCard→Farcaster article (yesterday's project-lens skill output, committed 16:07Z May 18, inside today's window by 9 minutes).

Plus ~30 `chore(scheduler)` and `chore(cron) success` housekeeping commits.

---

## Developer Notes

- **New dependencies:** none. **27-PR zero-new-deps streak** preserved (PR #57 → #87 → #90 → #91 candidate). PR #90 and PR #91 both ship pure stdlib (`xml`-free; #90 uses string templating for meta tags, #91 uses `dict` → `json.dumps`).
- **Breaking changes:** none on either repo's main. PR #89 (still open, not in this window's merges) carries an intentional Neo4j-password break.
- **Architecture shift:** MiroShark now has 11 publish-gated share surfaces, all registered in `SURFACE_KEYS` and counted in `SimulationSurfaceStats`. PR #91 brings the surface count past 10 — the registry pattern is starting to feel load-bearing rather than incidental. The 11 surfaces split cleanly along audience lines: researchers (csv/jsonl/ipynb/transcript), institutions (dkg-citation/lineage), social (share-card/replay-gif/frame-metadata), quants (signal.json), embed-builders (chart.svg/thread).
- **Tech debt:** none flagged. PR #91 notes sandbox blocked `pytest` against `/tmp/build-target`; CI on the PR branch will execute the full suite. No TODOs introduced.

## What's Next

- **PR #91 review.** ~1,189 LoC, 26 new offline tests, zero-dep. Merge pace should be ≤24h based on the last six MiroShark PRs (#79–#87 + #90 all merged inside 36h).
- **PR #89 still stalled.** ~36h old, first external security PR. No maintainer comment yet. This is the longest-open MiroShark PR right now.
- **May-18 batch remainder unbuilt** (4/5): #2 Simulation Archive Bundle, #3 Per-Agent Stance Sparklines, #4 Scenario Clone Button on Share Page, #5 Chinese + Japanese README translations. Trading Signal JSON (#1) shipped to PR today.
- **May-16 batch remainder unbuilt** (3/5): #1 oEmbed, #4 Peak-Round Analytics, #5 Operator Profile.
- **Issue #88** on MiroShark (Neo4j hardcoded password) — has corresponding PR #89 from teifurin; will close on merge.
