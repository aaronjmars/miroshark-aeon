*Push Recap — 2026-05-19*
aaronjmars/MiroShark — 1 PR merged on main, 1 PR opened (branch push); aaronjmars/miroshark-aeon — 1 PR merged on main. Authors: aeonframework + Aeon (CI).

*Farcaster Frame v2 lands:* PR #90 merged ~25.5h after opening. `fc:frame:*` meta-tag injection in `<head>` of public share pages + `GET /<id>/frame-metadata`. Chart SVG (PR #85 merged yesterday) becomes the Frame backing image at 2:1 — bullish/neutral/bearish curves visible directly in Warpcast feed. Single "View Simulation →" link button. Pre-trajectory sims fall back to share-card PNG at 1.91:1. Closes Base-chain audience gap: `$MIROSHARK` lives on Base, Base-native social = Farcaster.

*Trading Signal JSON opens (PR #91, OPEN):* 11th publish-gated share surface. `GET /<id>/signal.json` collapses final-state belief split + quality health into a single machine-readable action primitive — direction (Bullish/Neutral/Bearish) + confidence_pct (0=split / 100=unanimous) + risk_tier from quality health. Pure derivation from existing embed-summary payload; a "Bullish 62%" signal here matches every other surface byte-for-byte. Quant-tool surface twin to PR #80 (Jupyter, researcher) and PR #84 (DKG, institutional). 26 new offline tests.

*Aeon self-improve loop closes again:* PR #42 (repo-pulse article output) merged 48h after the May-17 skill-freshness audit flagged the gap. Step 7 added to `skills/repo-pulse/SKILL.md` to emit `articles/repo-pulse-${today}.md` with the canonical fields 5 consumer skills (operator-scorecard, thread-formatter, star-momentum-alert, show-hn-draft, skill-freshness) had been silently falling back to memory/logs parsers for. Second consecutive self-correction cycle merged <48h.

Key changes:
- `backend/app/services/frame_metadata.py` (+235 new, stdlib): `build_frame_metadata()` selects chart.svg at 2:1 or share-card.png at 1.91:1, suppresses Frame tags for private sims
- `backend/app/services/signal_service.py` (+241 new, stdlib): `compute_signal(summary)` with plurality + `bullish>bearish>neutral` tie-break, confidence anchors (33.3% ⇒ 0, 100% ⇒ 100), risk-tier from quality health
- `skills/repo-pulse/SKILL.md` (+33, -1): new step 7 closes the longest-standing producer/consumer gap in the aeon skill graph

Stats: +2,362 / -3 across 21 files (MiroShark main 1,140 LoC + MiroShark PR-branch 1,189 LoC + aeon main 33 LoC). 27-PR zero-new-deps streak preserved (#57 → #87 → #90 → #91 candidate). Stars 1172 → 1175 (+3); forks 236 → 237 (+1).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-19.md
