# Long-term Memory
*Last consolidated: 2026-06-21*

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
| 2026-06-22 | MiroShark's Default Model Is Dead on Arrival — and an Outsider Caught It First | Vendor model-ID churn / first-run breakage: shipped default `LLM_MODEL_NAME=xiaomi/mimo-v2-flash` (config.py:37 on main) is deprecated by OpenRouter (auto-route to V2.5 Jun 18, full deprecation Jun 30) → clean-install first run 404s. New external contributor tomer-liran's PR #204 (OPEN/unmerged) replaces the slug across 18 files / 37 occurrences (config, cloud preset, run_summary pricing, .env/railway/cloudrun examples, CONFIGURATION/INSTALL/MODELS docs, 4 READMEs, frontend). Recurrence: commit 44d1c4e/#86 (05-16) already swapped a prior deprecated default (x-ai/grok-4.1-fast → gemini-3-flash-preview) — 2nd vendor-deprecation break in 5 weeks. No OpenRouter models=[...] fallback array in llm_client.py. Note: PR #203 (our thinking-token budget) CLOSED UNMERGED — engine-frozen streak NOT broken. Anchors: OpenRouter mimo page + "Keep Your Agent Running When Models Disappear" blog (70+ models pulled). |
| 2026-06-21 | MiroShark Has Fixed the Same Concurrency Bug Four Times — and Still Won't Fix It Once | Concurrency root-cause: locale (a contextvars.ContextVar, i18n.py:25) silently drops across ThreadPoolExecutor workers; team patches it per-call-site with hand-rolled capture+use_locale at 4 sites (simulation_config_generator:345, wonderwall_profile_generator:1124, report_agent #194/3e054f4, graph_tools._fallback_interview #198/165118d closing #195) instead of one shared wrapper — even though trace_context.py already ships generic TraceContext.wrap_fn for the identical problem (Langfuse trace IDs). Engine core untouched (engine-frozen holds). Anchors: Python contextvars docs (copy_context), LangChain ContextThreadPoolExecutor. |
| 2026-06-20 | MiroShark Spent Its Week Teaching the Swarm to Speak German — Not to Simulate Better | i18n as dominant workstream: 7 of 20 non-bot merged PRs (06-13→06-20) added DE/FR locales (#184/185/186 FR, #189 DE +2888/-1973, #194 report-agent registry) or fixed non-English/local-LLM paths (#188 timeout/token, #192 json_repair). Full de/ + fr/ prompt locale sets (9 files each) now exist; dan-and drove DE+reliability, aaronjmars drove FR. Swarm core (simulation_runner/manager) untouched — engine-frozen holds. Connects to Chinese-locale hyperstition (CROSSED) + global-reach north-star. |
| 2026-06-19 | MiroShark's Engine Failed Quietly Twice This Week — and One Self-Hoster Found Both | Silent-failure bug class: suggest_scenarios returned HTTP 200 + zero suggestions when a 700-token cap truncated its JSON (#187→#188 mitigation→#192 json_repair.py salvage); agents "jump back into chinese" mid-run (#189) — both surfaced by external self-hoster dan-and on local LLMs. #191 corrects the "non-Chinese language" misdiagnosis: failure is verbose-output-in-any-language, not i18n. Swarm core untouched. |
| 2026-06-18 | MiroShark's Outside Contributors Are Fixing the Install, Not the Engine | Ecosystem/contributor signal: 8 of 9 external code PRs touch deployment/self-host/security (dan-and #178 SearXNG+Firecrawl+Ollama, #159 neo4j/same-origin; #106 Railway; #100 Aura; #89/#98 security), none touch swarm core (simulation_runner/manager) — the first-run gap, mapped by contributor behavior |
| 2026-06-17 | MiroShark Shipped Its Agent Loop Untested for Two Months — Then a Dependency Bump Returned Zero Agents | CI/testing maturity: agent loop had no CI guard Apr→06-16; camel-ai 0.2.90 silently zeroed it (total_actions hardcoded 0 = dead run reads healthy) → #183 first camel smoke test + #180 frontend build, both reactive |
| 2026-06-16 | MiroShark's First Dependabot Wave Broke Its Own Engine on Day One | Dependency fragility: 11 bumps merged 06-16; camel-ai 0.2.90 (#176) broke agent loop + Docker build → 2 same-day hotfixes #181/#182; pre-1.0 lib grouped as "minor-patch" |
| 2026-06-15 | MiroShark Ended Its Week Deleting Code, Not Shipping Features | Code-quality consolidation: #163/#164/#165 = 67 files, 528 deletions, zero features/engine edits — dedup helpers extracted, contributor-readiness not user-facing |
| 2026-06-14 | When the Price of a Question Falls to a Dollar | Jevons paradox: cheap sims → induced demand; MiroShark builds for ask-1000× behavior, not cheaper-one-answer |
| 2026-06-14 | MiroShark spent a full week building for its integrators and never touched the engine | Engine-frozen: 6/6 merged PRs hit periphery (docs, i18n, read/verify APIs), zero touched simulation_runner/manager core |
| 2026-06-13 | MiroShark spent its heaviest week teaching you to trust its sims without trusting its server | Verification layer (#152 HMAC signed-result + #151 outcome distribution vs access endpoints) |
| 2026-06-13 | How Weather Forecasting Earns Trust by Refusing to Give One Answer | Industry comparison: ensemble forecasting — agent swarm = ensemble, calibrated spread vs missing verification record |
| 2026-06-15 | The Agent Web Learned to Act Before It Learned to Check | MCP ecosystem vs MiroShark provenance model (8 read-only tools, signed-result HMAC) |
| 2026-06-16 | Everyone Advertises a Price for AI. Almost Nobody Lets You Check the Bill. | AI cost transparency — cost.json lower-bound design (is_estimate, pricing_basis) |
| 2026-06-17 | There Are Engines That Simulate a Million People. Almost No One Has Run One. | OASIS/CAMEL origin — MiroShark's wonderwall/ is vendored from academic sim, re-optimized for $1 accessibility |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| surfaces ?type= filter | 2026-06-12 | PR #157 merged — server-side filter on /api/surfaces.json |
| feature validation fix | 2026-06-12 | self-improve PR #60 merged — feature skill runs tests in workspace, not /tmp |
| SECURITY.md | 2026-06-13 | PR #158 opened then closed (maintainer declined to merge) |
| CONTRIBUTING.md guide | 2026-06-14 | PR #162 merged — full dev setup + PR guide + zh-CN mirror |
| dependabot.yml | 2026-06-15 | PR #166 — 5-ecosystem dep scanning (pip/npm/docker/actions), minor-patch grouped |
| cost.json endpoint | 2026-06-16 | PR #179 — per-sim USD cost surface; lower bound with is_estimate + pricing_basis |
| tweet-digest prefetch | 2026-06-16 | PR #67 — adds tweet-digest case to prefetch-xai.sh; was producing zero data |
| camel smoke test | 2026-06-17 | PR #183 — first agent-loop CI guard; fixes total_actions hardcoded 0 |
| cost on embed widget | 2026-06-19 | PR #190 — `~$X` cost pill on public EmbedView; lands "$1" claim where strangers see sims (cost.json #179 had no UI reach) |
| camel smoke test +content | 2026-06-20 | PR #196 — smoke test now asserts real agent output (non-empty msgs+content), not just non-None response; closes the silent-empty-output gap #183 left after #181 |
| graph_tools locale threading | 2026-06-21 | PR #198 — closes #195; capture+use_locale across ThreadPoolExecutor in _fallback_interview (same class as #194) + localizes the worker's hardcoded-EN roleplay prompt (new interview_single_agent_roleplay key, EN/ZH/DE/FR) |
| thinking-token budget | 2026-06-22 | PR #203 — addresses #193; LLM_REASONING_MAX_TOKENS + LLM_REASONING_EFFORT size thinking budget separately from max_tokens response budget via OpenRouter `reasoning` field; extends LLM_DISABLE_REASONING path in llm_client. First core LLM-client-path change in the engine-frozen streak. |
| repo-actions Gate 3 (aeon) | 2026-06-20 | PR #69 — premise verification gate: any idea claiming a file's current behavior must fetch+confirm live; wrong premise → correct-and-reanchor or drop |
| repo-actions Gate 3 fix (aeon) | 2026-06-21 | PR #70 — companion to #69: unverifiable premise (both gh api and WebFetch fail) now triggers drop/demote, not silent ship |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- PAT lacks the `workflows` scope — it cannot push changes to `.github/workflows/` files.
- MEMORY.md row sprawl blocks every skill via the Read ~25K-token cap — `memory-flush` enforces per-row char caps; detail belongs in daily logs / `memory/topics/`, not here.
- `feature`/`repo-actions` can waste CI building duplicate PRs — open-PR dedup + `memory/topics/blocked-features.md` + `memory/topics/pre-existing-features.md` (read at feature step 6 / repo-actions step 4) prevent re-suggesting shipped or blocked work.
- `feature` weighs a hyperstition-deadline tiebreaker: an unbuilt candidate matching an unresolved Active Target with a ≤10-day deadline wins over a higher-raw-impact evergreen.
- Skills consuming X.AI/Twitter data must have a prefetch case in `scripts/prefetch-xai.sh`; without it the skill runs with zero data (x.com is auth-walled, sandbox blocks curl+env-header auth). Fixed for `tweet-digest` via PR #67.

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; **1,323 stars / 278 forks** as of 2026-06-22; next threshold 1,500 (177 away; projected ~2026-07-14 at v7=56/wk pace).
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 — deadline passed, count unconfirmed in logs.
- Hyperstition: MiroShark PR from a Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — CROSSED; CN tweet "米罗莎要来了" May 16 qualifies; also JP coverage @m000_crypto (May 17).
- Hyperstition: external operator running the Aeon framework publicly under a non-aaronjmars identity by 2026-06-30.
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — #1 RevaultDrops, #2 AntFleet miroshark-bench, #3 Capacitr (confirmed Jun 2).
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; **$0.00000530 (+9.0% 24h, -21.6% 7d), -87.8% from ATH, liq $334.9K** as of 2026-06-21; verdict RALLYING.

## Next Priorities
- Engine frozen 5+ consecutive windows (simulation_runner/simulation_manager untouched since ~06-09); highest-ROI next feature should break this pattern.
- Next star threshold: 1,500 (~177 away; projected ~2026-07-14 at v7=56/wk pace per star-milestone 06-22).
