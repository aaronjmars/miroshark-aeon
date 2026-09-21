---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-09-20*
## About This Repo
- Autonomous agent (Aeon) running on GitHub Actions via Claude Code, operating for the **$MIROSHARK** token and the `MiroShark/MiroShark` project (renamed from `aaronjmars/MiroShark` 2026-08-17 — own GitHub org now, old path redirects).
- Linked to a Telegram group — daily skills post repo state, content, and token updates via outbound `./notify` (inbound message polling disabled).

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

`token-report` reads this table; update it here to retarget.

## Watched Repos
See `memory/watched-repos.md` — `MiroShark/MiroShark` (renamed from `aaronjmars/MiroShark` 08-17), `aaronjmars/miroshark-aeon`.

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-06-24 | MiroShark's Engine Reliability Has a Bus Factor of One | Contributor concentration: dan-and sole external merger (06-17→06-24); open PR #214 = first proposed behavioral fix to simulation_runner.py since May |
| 2026-06-24 | exit codes over webhooks — wait CLI deep-dive | Project lens: async contract for shell/CI integrators; exit 0/1/2 vs callback model (PR #215) |
| 2026-06-23 | MiroShark Stopped Marketing the $1 and Started Letting You Audit It | Cost triad: cost.json API + embed pill + CLI `cost` — all one source, all lower-bound ($0 for untracked models) |
| 2026-06-23 | Mandatory red-teaming misses multi-agent failure modes | Project lens: US AI directive Jun 6; isolation tests miss compounding errors across agent networks |
| 2026-06-22 | MiroShark's Default Model Is Dead on Arrival | mimo-v2-flash deprecated (OpenRouter Jun 30); tomer-liran PR #204; 2nd vendor-deprecation break in 5 wks; PR #203 CLOSED UNMERGED |
| 2026-06-22 | The representative agent problem, applied to swarms | Project lens: averaging N personas ≠ collective dynamics; heterogeneous populations (Ostrom polycentricity) |

*Older rows archived to `memory/topics/articles-history.md` (no new editorial articles since 2026-06-24).*

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-09-21 | shiplog | Shipped agent hand-off (skill.md copy button + x402 Tier1/2 agent control) in MiroShark-x402 + miroshark-website; same window @svector_eth got @bankrbot to autonomously pay $1 + run the skill for a real Musebook Town Hall governance preview (unprompted, confirmed live). Public engine repo back to 0 real PRs (4 dependabot only). Stars 1,452 (+3, best of last 3 weeks) |
| 2026-09-12 | tweet-digest | @miroshark_ resumed posting 09-10 after 6-day silence (since 09-04): product-ship + research-drop tweets (09-10) → weekly 3-league match-sim series opened (09-11: Serie A, LaLiga, Premier League) → x402aff adoption post (09-12); quiet again by 09-13 |
| 2026-09-07 | shiplog | Public engine repo 4th straight idle window (0 engine-code PRs) but private companion repo MiroShark-x402 merged 43 real sim-engine PRs — engine work continues, just not where stars/forks read it; stars +2 (well off +9 pace), forks −1 (first decline) |
| 2026-09-04 | tweet-digest | Weekly match-sim cadence continues (Premier League MD3, LaLiga MD4 reports); TikTok cross-platform push |
| 2026-08-31 | tweet-digest | x402aff week recap; 2nd organic press pickup — reply to @Amrit_Mirch's GTA VI agent-argument sim (10 agents, 10 rounds, release-odds call) |
| 2026-08-28 | tweet-digest | x402aff affiliate program launch (4 tweets: announcement, guide, article, video) — drove the same-day BREAKOUT |
| 2026-08-27 | tweet-digest | Bundesliga season sim launch; "simulation credibility" claim tweet |
| 2026-08-26 | tweet-digest | Champions League match sims (2 tweets); CMC listing tease |
| 2026-08-18 | tweet-digest | forecasting calibration research; unprompted external press pickup (Medium, @Amrit_Mirch) of the "market vs simulation" thesis |
| 2026-08-09 | tweet-digest | x402 launch on agentic.market |
| 2026-08-06 | tweet-digest | x402 agentic market listing |
| 2026-07-29 | tweet-digest | OpenAI Rogue Agent Sim |
| 2026-07-27 | tweet-digest | Gossip Sim Launch, Cross-Platform Push |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| camel smoke test +content | 2026-06-20 | PR #196 — asserts real agent output (non-empty msgs+content) |
| graph_tools locale threading | 2026-06-21 | PR #198 — capture+use_locale across ThreadPoolExecutor in _fallback_interview |
| repo-actions Gate 3 (aeon) | 2026-06-20 | PR #69 — premise verification gate: fetch+confirm live before any file claim |
| repo-actions Gate 3 fix (aeon) | 2026-06-21 | PR #70 — unverifiable premise → drop/demote, not silent ship |
| thinking-token budget | 2026-06-22 | PR #203 CLOSED UNMERGED — LLM_REASONING_MAX_TOKENS + LLM_REASONING_EFFORT via OpenRouter `reasoning` field |
| wait CLI subcommand | 2026-06-24 | PR #215 — blocks until terminal state; exit 0/1/2; makes `wait → cost/report` scriptable |
| cost CLI subcommand | 2026-06-23 | PR #208 — `python cli.py cost <id>`; `~` prefix on is_estimate; exit 2 if no cost |
| xai=quiet/skip split | 2026-06-24 | PR #75 — `xai=quiet` = prefetch ran, token quiet; `xai=skip` = no data fetched |
| stop CLI subcommand | 2026-06-25 | PR #216 — cancel running sim; completes `wait \|\| stop` automation lifecycle |
| schedule tuning (aeon) | 2026-06-25 | PR #76 — pause build/content skills, stretch cadences; mirror aeon-agent schedule |
| aeon-update enabled | 2026-08-18 | PR #135 — weekly canon framework sync from upstream aeonfun/aeon (3-way merge, never clobbers operator config). Latest: **PR #180** (2026-09-14, `21b82db..95142d1`, 25 commits) — 43 files applied (sandbox read-only fix #1042/#1051, chain no-action #1053, vuln-scanner Riva #1039, deploy-uni-hook AeonFee #1035, aeon-update eyebrow-from-CI #1037). 15 held in `memory/topics/aeon-update-state.json`: workflow/README/pack-doc conflicts, dashboard+webhook dep bundles, 3 new skills needing eyebrow scan (compute-resell/submit-hook/**miroshark-matchday** #1056 — ours), competitor-monitor egress hold, skill-icons subsystem. `bin/generate-*` can't run in the sync env (repo-local scripts need interactive approval) → catalog drift hand-patched; `bin/generate-skill-icons` fails pre-existingly (cortx-reliability has no glyph in catalog/skill-icons.json). |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- The fork's GH token now carries **both `repo` and `workflow` scopes** (verified `gh auth status` 2026-09-14) — it CAN push `.github/workflows/` changes. The old "PAT lacks the workflows scope" lesson is stale; workflow-file syncs no longer need to be held for that reason.
- MEMORY.md row sprawl blocks every skill via the Read ~25K-token cap — `memory-flush` enforces per-row char caps; detail belongs in daily logs / `memory/topics/`, not here.
- `feature`/`repo-actions` can waste CI building duplicate PRs — open-PR dedup + `memory/topics/blocked-features.md` + `memory/topics/pre-existing-features.md` (read at feature step 6 / repo-actions step 4) prevent re-suggesting shipped or blocked work.
- `feature` weighs a hyperstition-deadline tiebreaker: an unbuilt candidate matching an unresolved Active Target with a ≤10-day deadline wins over a higher-raw-impact evergreen.
- Skills consuming X.AI/Twitter data must have a prefetch case in `scripts/prefetch-xai.sh`; without it the skill runs with zero data (x.com is auth-walled, sandbox blocks curl+env-header auth). Fixed for `tweet-digest` via PR #67.
- Social Pulse `xai` flag: `xai=quiet` = prefetch ran but token quiet (< threshold); `xai=skip` = no data fetched (cache missing or key unset). PR #75.
- token-movers: during multi-day reporting gaps, compute 24h Δ from GT/DS native `h24` fields rather than the stale stored price (used 2026-08-04 after a 5-day gap).
- Shell `>` redirection is blocked by the Bash permission layer even for allowed-workspace paths (curl `-o` and the Write tool still work) — stage command output under `output/scratch/` (gitignored) instead of piping to files. Found by `shiplog` 2026-08-18.
- Root-level `notify`/`notify-jsonrender`/`secretcurl` are generated copies of `scripts/*.sh`, regenerated by the run harness — expect them as untracked/modified in `git status` (harmless generated-artifact drift, not lost work). First traced 2026-08-24 after aeon-update's PR #146 sync; confirmed via `gh api` that the merge commit remains an ancestor of `main`.
- Claude-subscription exhaustion (2026-08-31) triggers a harness pin to a GLM gateway (`GLM_API_KEY`/`ZAI_API_KEY`) as fallback — but the pin itself returned empty zero-token responses intermittently (2 clean runs, then relapse same day). Don't treat a GLM-pin commit landing as "fixed"; wait for 2+ consecutive canary runs (confirmed via token-movers + fetch-tweets both landing clean 09-01) before calling an outage resolved.
- eyebrow gate (CI pins **v0.4.2**): `eyebrow.policy.json` has `allowContentDrift: true` / `failOnCapabilityExpansion: true` / `failOnSeverity: critical`, so `verify` fails ONLY on a **new egress host** or a **new CRITICAL** — prose/content drift is tolerated (confirmed by reading the policy + `ci-skill-integrity.yml` on 2026-09-14). The earlier "v0.4.2 fails on ANY content drift" note was wrong. Practical rule for aeon-update: a modified existing skill is safe to apply UNLESS its SKILL.md text introduces a new URL host (even an example one — e.g. competitor-monitor's `vendor.com` had to be held). A brand-NEW skill still needs an `eyebrow scan` for its coverage entry, and the binary isn't in the sync env, so new skills get held.
- token-movers: DexScreener's top-pool liquidity figure has diverged sharply from GeckoTerminal's pool-level figure every day 2026-09-16→09-20 (~$120-133K DS vs ~$277-306K GT, while price agrees within ~1%) — keep using GT pool-level for day-to-day continuity; flag to operator if the gap persists past a week, since DS may only be counting a subset of pools.
- token-movers: the mmETH/MiroShark pool ($2.6M reserve, created 2026-09-14) has logged zero real trades through 2026-09-20 (6 days) — treat as seeded/inactive liquidity, not organic; keep excluding it from volume/whale calcs until it shows activity.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,449 stars** as of 2026-09-14 (repo-pulse; +1 this window, 2nd straight near-flat week vs avg4w≈4.75; 51 to 1,500; forks 299, recovered last week's −1 dip; new stargazer/forker AmirF194 also landed PR #301 as first merged public-repo external contributor in weeks; next check 2026-09-21).
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CROSSED; CN tweet "米罗莎要来了" May 16 qualifies; also JP coverage @m000_crypto (May 17).
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — **EXCEEDED, deadline passed**: 14 integrators in ECOSYSTEM.md as of 06-22 (Sparkleware, ZER0, Xerg, SyntheticsAI, Signa, RootAI, Noelclaw, Monitor, HivemindOS, Echo Oracle, Crucible Sim, Capacitr, Blue Agent, AntFleet).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.000002437 (-2.7% 24h, -10.8% 7d, -1.1% 30d), ~−94% from ATH, liq $297.9K** as of 2026-09-20; verdict QUIET (quietest session of the tracked window, 0.3x 7d-avg volume, zero whale trades — 2nd straight zero-whale session). Week (09-13→09-20): CONSOLIDATING +10.6% (09-13) → QUIET -6.1% (09-14) → QUIET +0.1% (09-15) → CONSOLIDATING -3.8% (09-16) → DISTRIBUTING -2.8% sell-skewed w/ whale sell (09-17) → SLIDING -8.9% on heaviest volume in a week + 2 whale sells (09-18) → CONSOLIDATING +14.6% on sub-avg volume + bot-like ~$2.50 buy cluster, zero whales (09-19) → QUIET -2.7% (09-20); net -10.8% for the week, erasing the 09-13 reversal. x_search now failing 5 of the last 7 sessions (09-11, 09-12, 09-15, 09-19, 09-20) — escalating from "intermittent" toward chronic; watch 09-21.
- MIROSHARK team/treasury holdings: 12.09% of supply (12.09B tokens) as of 2026-09-21 (up from 12.03% on 09-14), tracked via `holdings` skill (8th straight accumulating snapshot, but 7d growth slowed further to +0.48% from +0.71% the prior week; 30d +7.20%, also decelerating from +8.09%).

## Next Priorities
- Next star threshold: 1,500 (~51 away as of 2026-09-14; still near-flat — +1 this window vs avg4w≈4.75, 2nd straight decelerated week; next repo-pulse weekly check due 2026-09-21).
- Engine dev velocity (priority-1 "ship the engine"): `MiroShark/MiroShark` shipped **0 engine-code PRs across 4 consecutive shiplog windows** (~08-11→09-07; 4th window = 3 merged PRs, all dependency bumps). BUT the private companion repo `MiroShark-x402` merged 43 real engine PRs this window alone (prompt-cache revival, ReAct caps, invalid-action handling, Neo4j resilience) — the engine is being worked, it's just not landing in the public repo that the star/ecosystem north-star metrics read off of. Flagged to operator in the 09-07 shiplog notify (queued 591b3b49); worth a decision on whether to upstream more into the OSS repo.
