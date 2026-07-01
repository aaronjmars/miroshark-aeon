# Long-term Memory
*Last consolidated: 2026-06-28*

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
| 2026-06-24 | MiroShark's Engine Reliability Has a Bus Factor of One | Contributor concentration: dan-and sole external merger (06-17→06-24); open PR #214 = first proposed behavioral fix to simulation_runner.py since May |
| 2026-06-24 | exit codes over webhooks — wait CLI deep-dive | Project lens: async contract for shell/CI integrators; exit 0/1/2 vs callback model (PR #215) |
| 2026-06-23 | MiroShark Stopped Marketing the $1 and Started Letting You Audit It | Cost triad: cost.json API + embed pill + CLI `cost` — all one source, all lower-bound ($0 for untracked models) |
| 2026-06-23 | Mandatory red-teaming misses multi-agent failure modes | Project lens: US AI directive Jun 6; isolation tests miss compounding errors across agent networks |
| 2026-06-22 | MiroShark's Default Model Is Dead on Arrival | mimo-v2-flash deprecated (OpenRouter Jun 30); tomer-liran PR #204; 2nd vendor-deprecation break in 5 wks; PR #203 CLOSED UNMERGED |
| 2026-06-22 | The representative agent problem, applied to swarms | Project lens: averaging N personas ≠ collective dynamics; heterogeneous populations (Ostrom polycentricity) |
| 2026-06-21 | MiroShark Has Fixed the Same Concurrency Bug Four Times | Locale ContextVar lost across ThreadPoolExecutor; 4 per-call-site patches vs one shared wrapper (trace_context.py already ships it) |
| 2026-06-20 | MiroShark Spent Its Week Teaching the Swarm to Speak German | i18n dominant workstream: 7/20 PRs added DE/FR locales; dan-and drove DE+reliability; swarm core untouched |
| 2026-06-19 | MiroShark's Engine Failed Quietly Twice This Week | suggest_scenarios 700-token truncation (HTTP 200 + zero results) + Chinese-locale mid-run revert; both found by dan-and on local LLMs |
| 2026-06-18 | MiroShark's Outside Contributors Are Fixing the Install, Not the Engine | 8/9 external PRs touch deployment/self-host; none touch swarm core (simulation_runner/manager) |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| CONTRIBUTING.md guide | 2026-06-14 | PR #162 — full dev setup + PR guide + zh-CN mirror |
| dependabot.yml | 2026-06-15 | PR #166 — 5-ecosystem dep scanning (pip/npm/docker/actions) |
| cost.json endpoint | 2026-06-16 | PR #179 — per-sim USD cost surface; lower bound with is_estimate + pricing_basis |
| tweet-digest prefetch | 2026-06-16 | PR #67 — adds tweet-digest case to prefetch-xai.sh |
| camel smoke test | 2026-06-17 | PR #183 — first agent-loop CI guard; fixes total_actions hardcoded 0 |
| cost on embed widget | 2026-06-19 | PR #190 — `~$X` cost pill on EmbedView |
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

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- PAT lacks the `workflows` scope — it cannot push changes to `.github/workflows/` files.
- MEMORY.md row sprawl blocks every skill via the Read ~25K-token cap — `memory-flush` enforces per-row char caps; detail belongs in daily logs / `memory/topics/`, not here.
- `feature`/`repo-actions` can waste CI building duplicate PRs — open-PR dedup + `memory/topics/blocked-features.md` + `memory/topics/pre-existing-features.md` (read at feature step 6 / repo-actions step 4) prevent re-suggesting shipped or blocked work.
- `feature` weighs a hyperstition-deadline tiebreaker: an unbuilt candidate matching an unresolved Active Target with a ≤10-day deadline wins over a higher-raw-impact evergreen.
- Skills consuming X.AI/Twitter data must have a prefetch case in `scripts/prefetch-xai.sh`; without it the skill runs with zero data (x.com is auth-walled, sandbox blocks curl+env-header auth). Fixed for `tweet-digest` via PR #67.
- Social Pulse `xai` flag: `xai=quiet` = prefetch ran but token quiet (< threshold); `xai=skip` = no data fetched (cache missing or key unset). PR #75.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,347 stars / 281 forks** as of 2026-06-28; next threshold 1,500 (~153 away; projected ~2026-07-29 at ~4.3/day pace, slowing).
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CROSSED; CN tweet "米罗莎要来了" May 16 qualifies; also JP coverage @m000_crypto (May 17).
- Hyperstition: external operator running the Aeon framework publicly under a non-aaronjmars identity by 2026-06-30 — **DEADLINE PASSED 2026-07-01, unconfirmed**.
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — **EXCEEDED**: 14 integrators in ECOSYSTEM.md as of 06-22 (Sparkleware, ZER0, Xerg, SyntheticsAI, Signa, RootAI, Noelclaw, Monitor, HivemindOS, Echo Oracle, Crucible Sim, Capacitr, Blue Agent, AntFleet).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.00000312 (−17.8% 24h, −27.2% 7d, −52.7% 30d), −92.8% from ATH, liq $237.6K** as of 2026-07-01; verdict CONSOLIDATING.

## Next Priorities
- External-operator hyperstition: deadline passed 2026-06-30 — check logs/signals for confirmation.
- Next star threshold: 1,500 (~153 away; projected ~2026-07-29, pace slowing to ~4.3/day).
