---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-08-30*
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
| aeon-update enabled | 2026-08-18 | PR #135 — weekly canon framework sync from upstream aeon-agent into this instance (3-way merge, never clobbers operator config); synced through PR #151 (`b7a909a`→`8b8d719`, merged 2026-08-25) with 9 pending conflicts tracked in `memory/topics/aeon-update-state.json` (eslint-lint-gate bundle held back as one coupled change) |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- PAT lacks the `workflows` scope — it cannot push changes to `.github/workflows/` files.
- MEMORY.md row sprawl blocks every skill via the Read ~25K-token cap — `memory-flush` enforces per-row char caps; detail belongs in daily logs / `memory/topics/`, not here.
- `feature`/`repo-actions` can waste CI building duplicate PRs — open-PR dedup + `memory/topics/blocked-features.md` + `memory/topics/pre-existing-features.md` (read at feature step 6 / repo-actions step 4) prevent re-suggesting shipped or blocked work.
- `feature` weighs a hyperstition-deadline tiebreaker: an unbuilt candidate matching an unresolved Active Target with a ≤10-day deadline wins over a higher-raw-impact evergreen.
- Skills consuming X.AI/Twitter data must have a prefetch case in `scripts/prefetch-xai.sh`; without it the skill runs with zero data (x.com is auth-walled, sandbox blocks curl+env-header auth). Fixed for `tweet-digest` via PR #67.
- Social Pulse `xai` flag: `xai=quiet` = prefetch ran but token quiet (< threshold); `xai=skip` = no data fetched (cache missing or key unset). PR #75.
- token-movers: during multi-day reporting gaps, compute 24h Δ from GT/DS native `h24` fields rather than the stale stored price (used 2026-08-04 after a 5-day gap).
- Shell `>` redirection is blocked by the Bash permission layer even for allowed-workspace paths (curl `-o` and the Write tool still work) — stage command output under `output/scratch/` (gitignored) instead of piping to files. Found by `shiplog` 2026-08-18.
- Root-level `notify`/`notify-jsonrender`/`secretcurl` are generated copies of `scripts/*.sh`, regenerated by the run harness — expect them as untracked/modified in `git status` (harmless generated-artifact drift, not lost work). First traced 2026-08-24 after aeon-update's PR #146 sync; confirmed via `gh api` that the merge commit remains an ancestor of `main`.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,446 stars** as of 2026-08-31 (repo-pulse, events source; +9 w/w, weekly series +1→+7→+9, avg4w=4.0 → ACTIVE; 54 to 1,500; forks 299 with 299th = WorkWeonline boundary case 08-24T16:08Z; next check 2026-09-07).
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CROSSED; CN tweet "米罗莎要来了" May 16 qualifies; also JP coverage @m000_crypto (May 17).
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — **EXCEEDED, deadline passed**: 14 integrators in ECOSYSTEM.md as of 06-22 (Sparkleware, ZER0, Xerg, SyntheticsAI, Signa, RootAI, Noelclaw, Monitor, HivemindOS, Echo Oracle, Crucible Sim, Capacitr, Blue Agent, AntFleet).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.000003413 (−6.2% 24h, −0.9% 7d, +102.4% 30d), ~−92% from ATH, liq $336K** as of 2026-08-30; verdict CONSOLIDATING. Week arc: 08-24 CONSOLIDATING (+16.9%) → 08-25/26 pulled back (−18.8%, −12.1%, 2 straight down days) → 08-27 recovered (+5.1%) → **08-28 BREAKOUT +54.8%** on the x402aff affiliate-program launch (3.44x avg volume, liq +23.5% to $391K) → 08-29 unwound most of it (−22.2%) → 08-30 settled CONSOLIDATING; net ~flat 7d despite the breakout, 30d trend still strongly up.
- MIROSHARK team/treasury holdings: 11.78% of supply (11.78B tokens) as of 2026-08-31 (up from 11.28% on 08-24), tracked via `holdings` skill (5th straight accumulating snapshot, +507.7M in 7d).

## Next Priorities
- Next star threshold: 1,500 (~54 away as of 2026-08-31; ACTIVE/surge signal — +9 this week, 2nd straight week > 1.5×avg4w; next repo-pulse weekly check due 2026-09-07).
- Engine dev velocity (priority-1 "ship the engine"): `MiroShark/MiroShark` shipped **0 engine-code PRs across 3 consecutive shiplog windows** (~08-11→08-31; 3rd window = 5 merged PRs, all dependabot + README founder credit #292). 3rd-idle-window watch condition met on both shiplog and changelog sides — **flagged to operator in the 08-31 shiplog notify** (queued 3b87f143).
