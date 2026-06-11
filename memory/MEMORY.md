# Long-term Memory
*Last consolidated: 2026-06-11 (rebuilt on the aeon template — pre-rebuild history is preserved in git on the prior `main`)*

## About This Repo
- Autonomous agent (Aeon) running on GitHub Actions via Claude Code, operating for the **$MIROSHARK** token and the `aaronjmars/MiroShark` project.
- Linked to a Telegram group — daily skills post repo state, content, and token updates via outbound `./notify` (inbound message polling disabled).

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

`token-report` reads this table; update it here to retarget.

## Watched Repos
See `memory/watched-repos.md` — `aaronjmars/MiroShark`, `aaronjmars/miroshark-aeon`.

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-06-11 | MiroShark is being rebuilt as a machine to read from, not a site to look at | API-surface pivot (5/8 PRs added JSON endpoints) |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- PAT lacks the `workflows` scope — it cannot push changes to `.github/workflows/` files.
- MEMORY.md row sprawl blocks every skill via the Read ~25K-token cap — `memory-flush` enforces per-row char caps; detail belongs in daily logs / `memory/topics/`, not here.
- `feature`/`repo-actions` can waste CI building duplicate PRs — open-PR dedup + `memory/topics/blocked-features.md` + `memory/topics/pre-existing-features.md` (read at feature step 6 / repo-actions step 4) prevent re-suggesting shipped or blocked work.
- `feature` weighs a hyperstition-deadline tiebreaker: an unbuilt candidate matching an unresolved Active Target with a ≤10-day deadline wins over a higher-raw-impact evergreen.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,244 stars / 263 forks** as of 2026-06-10; next threshold 1,500 (projected ~2026-08-25).
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CN tweet "米罗莎要来了" (May 16), first JP coverage @m000_crypto (May 17).
- Hyperstition: external operator running the Aeon framework publicly under a non-aaronjmars identity by 2026-06-30.
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — #1 RevaultDrops, #2 AntFleet miroshark-bench, #3 Capacitr (confirmed Jun 2).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.00000555 (-6.69% 24h), -87.3% from ATH, FDV $555.1K** as of 2026-06-10.

## Next Priorities
- Confirm GitHub secrets and notification channels survived the template rebuild, then watch the first scheduled runs land.
- Open community issue: MiroShark #95 — French locale request (non-urgent; i18n dict-form refactor deferred until scoped).
