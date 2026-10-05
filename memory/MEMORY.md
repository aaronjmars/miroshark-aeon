---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-10-04*
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
| 2026-10-01 | shiplog | PayAI Bazaar listing (MiroShark-x402#261) + x402aff 0.3.1 launch (11-PR website day: claims dashboard, agent-ready MCP/WebMCP/REST, agent skill); public engine repo's 5th straight window with 0 engine-code PRs; stars 1,460 (+3), forks 302 (+2) |
| 2026-10-01 | fetch-tweets | 3 new posts: x402aff launch, PayAI listing announcement, @miroshark_'s first public post of the HuggingFace sim dataset |
| 2026-09-28 | shiplog | HuggingFace dataset (8,201 decisions/16 sims) published 09-25; 22 merged hardening PRs in private MiroShark-x402 vs 2 in public repo this window; weekly match-sim content streak broke after 5 straight weeks |
| 2026-09-27 | fetch-tweets | Week 09-21→09-27 content push: Substack launch + intro-blog refresh (channel expansion), x402 Spaces event w/ @thecultos announced, dataset-release quote-tweet (aaronjmars HuggingFace drop: 8,201 decisions linking @miroshark_ sim conversations to trades) |
| 2026-09-21 | shiplog | Shipped agent hand-off (skill.md copy button + x402 Tier1/2 agent control) in MiroShark-x402 + miroshark-website; same window @svector_eth got @bankrbot to autonomously pay $1 + run the skill for a real Musebook Town Hall governance preview (unprompted, confirmed live). Public engine repo back to 0 real PRs (4 dependabot only). Stars 1,452 (+3, best of last 3 weeks) |
| 2026-09-12 | tweet-digest | @miroshark_ resumed posting 09-10 after 6-day silence (since 09-04): product-ship + research-drop tweets (09-10) → weekly 3-league match-sim series opened (09-11: Serie A, LaLiga, Premier League) → x402aff adoption post (09-12); quiet again by 09-13 |
| 2026-09-07 | shiplog | Public engine repo 4th straight idle window (0 engine-code PRs) but private companion repo MiroShark-x402 merged 43 real sim-engine PRs — engine work continues, just not where stars/forks read it; stars +2 (well off +9 pace), forks −1 (first decline) |
| 2026-09-04 | tweet-digest | Weekly match-sim cadence continues (Premier League MD3, LaLiga MD4 reports); TikTok cross-platform push |
| 2026-08-31 | tweet-digest | x402aff week recap; 2nd organic press pickup — reply to @Amrit_Mirch's GTA VI agent-argument sim (10 agents, 10 rounds, release-odds call) |
| 2026-08-28 | tweet-digest | x402aff affiliate program launch (4 tweets: announcement, guide, article, video) — drove the same-day BREAKOUT |
| 2026-08-27 | tweet-digest | Bundesliga season sim launch; "simulation credibility" claim tweet |
| 2026-08-26 | tweet-digest | Champions League match sims (2 tweets); CMC listing tease |

*Older rows archived to `memory/topics/digests-history.md`.*

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
| aeon-update enabled | 2026-08-18 | PR #135 — weekly canon framework sync from upstream aeonfun/aeon (3-way merge, never clobbers operator config). Latest: **PR #183** (2026-09-28, `ba01e9f..531f575`, 13 commits) — 42 applied (33 clean-update, 6 clean-add, 3 three-way-merged); headline: HivemindOS credit-token LLM gateway + hunter-22 expiry gate. Resolved 2 long-stuck conflicts via 3-way merge: `aeon.yml` (carried since #180) and `messages.yml`. 13 pending_conflicts remain (7 new: arc-studio skill, dashboard package bump, ci-tests.yml, fork README, llms.txt, skill-packs.md; 4 carried-forward: miroshark-matchday, webhook pkg, competitor-monitor, submit-hook). eyebrow v0.4.3 fetched+checksum-verified but not yet applied as the running CI pin (scan step isn't committable in this sync env — CI still pins v0.4.2). Known bug: this run's cron-state entry got stuck reporting `last_status: dispatched` for 128h+ (09-28→10-03) despite completing cleanly — see Lessons Learned. |

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
- token-movers: the 14-session DexScreener-vs-GeckoTerminal liquidity divergence (09-16→09-29, ~$120-159K DS vs ~$278-350K GT) closed on 09-30 — GT's pool reserve dropped 57% overnight ($320.6K→$137.9K) to land within 0.07% of DS's $137.8K, with no swap in the trades feed large enough to explain the drop (likely an LP add/remove event, or a GT reserve-calc correction — can't distinguish from swap data alone). Reframes the prior two weeks: DS's lower figure may have been closer to true reserve the whole time. Still an open decision item for the operator — pick a canonical source now that they agree, or watch 1-2 more sessions to confirm the convergence holds rather than reverting.
- Zero-token "completed" harness runs (terminal_reason=completed, total_cost_usd=0, no error) recurred 2026-09-22 — 4 consecutive token-movers failures (06:10/07:00/07:38/13:48 UTC), same signature as the 2026-08-31 Claude-subscription-exhaustion incident. Recovered same day without intervention (clean 09-23 onward). `skill-repair` is disabled in `aeon.yml`, so the auto-filed issue (#182) doesn't auto-close on recovery — issue #182 is still open as of 2026-10-04 (12+ days) with no recurrence since 09-23; expect it to stay open until skill-repair is re-enabled or it's closed manually.
- token-movers: the mmETH/MiroShark pool ($2.6M reserve, created 2026-09-14) has logged zero real trades through 2026-09-20 (6 days) — treat as seeded/inactive liquidity, not organic; keep excluding it from volume/whale calcs until it shows activity.
- `aeon-update` cron-state entries can get stuck reporting `last_status: dispatched` for 100+ hours even though the run completed successfully (PR opened and merged, skill-health already scored it via a filed issue) — a lost outcome-write in the state-tracking pipeline, not a live hang. First confirmed after the 2026-09-28 11:05 UTC run: PR #183 merged 14:03 UTC same day and issue #184 scored the run, yet cron-state stayed on `dispatched` through at least 10-03 (128h+). `heartbeat` correctly deduped it as already-reported rather than re-flagging daily — before treating a `dispatched` cron-state entry as a live stuck run, cross-check the PR-merge timestamp and any skill-health issue first.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,460 stars** as of 2026-10-01 (shiplog; +3 this window, continuing ACTIVE pace); forks 302 (+2, reversing 09-28's first-ever net fork decline of 301→300); 40 to 1,500; repo-pulse's own weekly snapshot (1,457/09-28) still due its next check 2026-10-05.
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CROSSED; CN tweet "米罗莎要来了" May 16 qualifies; also JP coverage @m000_crypto (May 17).
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — **EXCEEDED, deadline passed**: 14 integrators in ECOSYSTEM.md as of 06-22 (Sparkleware, ZER0, Xerg, SyntheticsAI, Signa, RootAI, Noelclaw, Monitor, HivemindOS, Echo Oracle, Crucible Sim, Capacitr, Blue Agent, AntFleet).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.000002578 (+7.5% 24h, -16.2% 7d, -9.0% 30d), ~−94% from ATH, liq $140.0K** as of 2026-10-05; verdict RALLYING — two whale buys ($1.98K, $1.42K, first whale activity since 10-01) drove the bounce on 2.0× avg volume, even as trade-count stayed sell-heavy (26 buys/37 sells). Liquidity flat (+0.5%), no new liquidity event. x_search: only 1 qualifying tweet 10-05 (below the 2-tweet bar; xai=skip).
- MIROSHARK team/treasury holdings: 12.21% of supply (12.21B tokens) as of 2026-09-28 (up from 12.09% on 09-21), tracked via `holdings` skill (9th straight accumulating snapshot; 7d +1.0% token-amount growth, reaccelerating from the prior week's +0.48%; 30d +3.6%, decelerating from +7.20% as the high-accumulation period rolls off the 30d window).

## Next Priorities
- Next star threshold: 1,500 (~40 away as of 2026-10-01; 1,460 stars, +3 this window; next repo-pulse weekly check due 2026-10-05).
- Engine dev velocity (priority-1 "ship the engine"): `MiroShark/MiroShark` shipped **0 engine-code PRs across 5 consecutive shiplog windows** (~08-11→10-01; 5th window = 1 docs PR + 3 dependabot). Private companion repo `MiroShark-x402` continues carrying real engine work instead (22 hardening PRs merged 09-28 window alone: prompt-cache, memory/observability) — same gap flagged to operator since 09-07 (queued notify 591b3b49), still unresolved: worth a decision on whether to upstream more into the OSS repo that the star/ecosystem metrics actually read off of.
- `products.md` config gap (flagged by shiplog 10-01): `x402aff-website` (private, 11 PRs shipped this window — claims dashboard, agent skill, canonical domain) isn't listed under the Miroshark product's repo line — low urgency but worth a bd-radar/operator pass so scouting doesn't miss mentions of it.
