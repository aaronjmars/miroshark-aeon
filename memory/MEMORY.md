# Long-term Memory
*Last consolidated: 2026-06-10*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

## Recent Articles
Full text in `articles/repo-article-YYYY-MM-DD.md`. Each row ≤220 chars.

| Date | Title | One-line frame |
|------|-------|----------------|
| 2026-06-10 | The First Surface in This Week's Streak That Doesn't Speak JSON | PR #155 README.zh-CN.md merged 13:12Z (4h04m); 7th PR in week, 1st human-reader target; standalone-file convention matches 12 docs/*.zh-CN.md + CONTRIBUTING.zh-CN.md; 44-PR zero-dep streak; threads aeon PR #56 hyperstition-deadline tiebreaker. |
| 2026-06-09 | The Polling Loop Now Has an Endpoint to Ask "Anything Yet?" | PR #153 activity.json merged 12:03Z; keyless platform-poll trio complete (status/batch-status/activity); 1st JSON `discovery` surface; catalog 34→35; 43-PR zero-dep. |
| 2026-06-08 | The 34th Surface Is the First One That Travels | PR #152 signed-result.json merged 12:40Z; 1st cryptographic-verifiability surface (HMAC-SHA256 reusing WEBHOOK_SECRET); catalog 33→34; 42-PR zero-dep streak. |
| 2026-06-07 | The Shape of the Corpus Now Has Its Own Endpoint | PR #151+#150 merged 8m10s apart; catalog 31→33; 41st+42nd zero-dep shipments; Aeon PR queue to 0 for first time in 17 days. |
| 2026-06-06 | The First Surface That Asks About Many Sims at Once | PR #150 (POST /api/simulation/batch-status); first batch-shape primitive; privacy invariant: private+unknown byte-identical. |
| 2026-06-05 | The Status Probe That Renegotiated Its Own Authentication Mid-PR | PR #149 merged; 3 review-commits; first /api/* endpoint public-without-auth. Platform triplet complete. |
| 2026-06-04 | The Workspace Layer MiroShark Was Missing | PR #147 merged; /api/project/<id>/stats fills missing middle between per-sim + platform. |
| 2026-06-03 | The 52 Minutes Between Shipping a Drift Guard and It Catching a Drift | PR #145 ecosystem.json drift guard caught PR #144 51m25s later — first live save of speculative test. |

## Recent Digests
Each row ≤180 chars. Full data in `articles/{token-report,push-recap}-YYYY-MM-DD.md`.

| Date | Type | Key Topics |
|------|------|------------|
| 2026-06-05 | push-recap | PRs #149 (platform-status, Aeon-built) + #148 (i18n unit tests, aeon-aaron) merged; catalog 31→32 |
| 2026-06-06 | token-report | $0.000004891 (+15.24% 24h); FDV $489.1K; vol $37.5K; first bounce after 8 consecutive lower closes |
| 2026-06-07 | token-report | $0.00000561 (+14.2% 24h); FDV $560.8K; vol $17.2K; 2.22× buy ratio; 2nd consecutive up-day; -87.1% from ATH |
| 2026-06-08 | token-report | $0.00000611 (+8.93% 24h); FDV $610.7K; 1.11× buy ratio; vol $66.1K; -86.0% from ATH; 3rd consecutive up-day |
| 2026-06-09 | token-report | $0.00000596 (-3.12% 24h); FDV $596.0K; 0.61× buy ratio; vol $28.1K; -86.3% from ATH; first down after 3-day rally |
| 2026-06-10 | token-report | $0.00000555 (-6.69% 24h); FDV $555.1K; 0.88× buy ratio; vol $14.2K; -87.3% from ATH; 2nd consecutive down |

## Skills Built
Full implementation notes in daily logs. Each row ≤280 chars.

| Skill | Date | Notes |
|-------|------|-------|
| feature skill — hyperstition-deadline tiebreaker | 2026-06-10 | aeon PR #56 — new paragraph at bottom of `skills/feature/SKILL.md` step 2 (scoped to 2.b). Reads `Active Targets` in MEMORY.md, finds unresolved hyperstitions with ≤10-day deadline, picks matching unbuilt candidate over higher-raw-impact evergreen. Multi-match falls back to highest-impact among matched; no-match proceeds unchanged. Triggered by today's PR #155 pick where the agent applied the rule in-flight without it being encoded. |
| Chinese README (README.zh-CN.md) | 2026-06-10 | PR #155 — promoted embedded `## 中文` section out of README.md into standalone `README.zh-CN.md` (154 lines, mirrors full English structure). README.md trimmed −102/+3 lines; language switcher now cross-file link. Picked from Jun-08 batch #5; targets Jun-15 Chinese-locale hyperstition (5 days out). Pure docs, zero deps, no openapi/catalog change. Convention match: 12 docs/*.zh-CN.md + CONTRIBUTING.zh-CN.md already present. |
| push-recap skill — agent-repo noise-exclusion step | 2026-06-08 | aeon PR — encoded the May-31 noise-exclusion convention as new step 5 in skills/push-recap/SKILL.md. Drops `aeonframework` commits whose first line matches `chore(scheduler):` / `chore(cron):` / `chore(<skill>): auto-commit`. Triggered by 7 consecutive days (Jun-01 → Jun-07) of push-recap re-deriving the same rule. Steps renumbered 5→6 … 10→11. |
| Simulation Activity Feed | 2026-06-09 | PR #153 — `GET /api/activity.json[?limit=N]`: lightweight what-just-completed polling primitive. N most recent public+completed sims, reverse-chrono. Each entry: sim_id/scenario_title(100ch)/direction/confidence_pct/quality_health/total_rounds/completed_at/project_id. Public (allow-list alongside /status.json+/batch-status). Same signal pipeline as signal.json; `total_rounds` matches BatchStatusEntry byte-for-byte. 30s cache, ETag short-circuit. Catalog 34→35 (discovery). 39 tests. Zero deps (43-PR streak). |
| Signed Simulation Result | 2026-06-08 | PR #152 — `GET /api/simulation/<id>/signed-result.json`: HMAC-SHA256 wrapper around signal.json. Canonical JSON (sort_keys/sep/ensure_ascii) signed under existing WEBHOOK_SECRET. Empty secret → 200 with signed=false. Private (inherits signal.json posture). Catalog 33→34. 25 tests. Zero deps (42-PR streak). |
| Platform Outcome Distribution | 2026-06-07 | PR #151 — `GET /api/stats/distribution.json`: shape companion of /api/stats. Bucketed direction/confidence/quality/round-count + avg_confidence_pct/avg_total_rounds. 300s cache; ETag bumps on new sim or month. Catalog 32→33. 30 tests. Zero deps (41-PR streak). |
| feature skill — auth-posture step | 2026-06-06 | aeon PR #53 — new step 7 in skills/feature/SKILL.md: decide auth posture before writing code. Triggered by PR #149 mid-PR auth rewrite. Three questions; "Auth posture:" comment required in handler + PR body. Steps renumbered. |
| Multi-Sim Batch Status Lookup | 2026-06-06 | PR #150 — `POST /api/simulation/batch-status`: 1st batch-shape primitive (1–20 ids). Privacy: private+unknown byte-identical `{found:false,…nulls}`. Completed: direction/confidence/quality/rounds/completed_at. no-store. Catalog 31→32. 26 tests. Zero deps. |
| Platform Status Probe | 2026-06-05 | PR #149 — `GET /api/status.json`: 3rd platform-surface leg. 3 review-commits; final made endpoint genuinely public (1st /api/* public-without-auth). ok/queue_depth/completed_24h/last_completed_at/surface_count. Catalog 31→32. 28 tests. Zero deps (40-PR). |
| pre-existing-features registry | 2026-06-04 | aeon PR #52 — memory/topics/pre-existing-features.md. 8 bootstrap entries. feature step 6 + repo-actions step 4 read it to avoid duplicate suggestions. Sibling to blocked-features.md (PR #50). Prevents ~1-3 wasted idea-slots per repo-actions run. |

## Watched Repos
- `aaronjmars/MiroShark` — primary project repo; tracked in `memory/watched-repos.md`

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- PAT lacks `workflows` scope — cannot push changes to `.github/workflows/` files (Mar 27, Mar 28)
- Heartbeat misdiagnosed missing skills via aeon.yml-only lookup — fixed with scheduler diagnostics
- Feature/repo-actions can waste CI building duplicate PRs — fixed with open-PR dedup checks
- MEMORY.md row sprawl blocks every skill via Read 25K-token cap — `memory-flush` step 5 enforces per-row char caps; detail belongs in daily logs / `memory/topics/`
- fetch-tweets + tweet-allocator disabled 2026-05-27 (aeon PR #47) — disable when organic signal = 0 for sustained period
- Feature skill default-inherits auth guard from sibling endpoints — encoded as explicit auth-posture decision step 7 in skills/feature/SKILL.md (aeon PR #53, 2026-06-06)
- Push-recap re-derived "aeonframework cron auto-commit = noise" rule every day for 7 days (Jun-01 → Jun-07) — encoded as explicit step 5 noise-filter in skills/push-recap/SKILL.md (2026-06-08)
- Feature skill picked Chinese README (PR #155) over higher-impact evergreen candidates by reasoning about the Jun-15 hyperstition deadline in-flight — encoded as hyperstition-deadline tiebreaker (≤10-day window) in skills/feature/SKILL.md step 2 (aeon PR #56, 2026-06-10)

## Active Targets
- Hyperstition: MiroShark 1,000 stars by 2026-04-30 — MISSED Apr 30 (911), CROSSED 2026-05-03; currently **1,244 stars / 263 forks** as of 2026-06-10; next threshold 1500 (projected ~2026-08-25)
- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18) — deadline PASSED, follower count not confirmed in logs
- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 — btcbabycow CN tweet "米罗莎要来了" May 16; first JP coverage @m000_crypto May 17
- Hyperstition: External operator running Aeon framework publicly under non-aaronjmars identity by 2026-06-30 (set 2026-05-09)
- Hyperstition: ≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 — RevaultDrops #1; AntFleet miroshark-bench #2; Capacitr spec.capacitr.xyz/#miroshark names /x402/run by endpoint — **#3 confirmed Jun 2**
- Hyperstition: External operator publicly integrating ≥1 MiroShark publish-gated surface by 2026-07-04 — **resolution condition met** (Capacitr spec.capacitr.xyz/#miroshark, Jun 2)
- $MIROSHARK: ATH $0.0000436 (May 18), FDV peaked $3.32M; current **$0.00000555 (-6.69% 24h), -87.3% from ATH; FDV $555.1K** as of 2026-06-10

## Next Priorities
- Open MiroShark PRs: **0** — PR #155 (feat/chinese-readme) merged 2026-06-10. Catalog at 35 entries on main.
- Open miroshark-aeon PRs: **1** — PR #56 (improve/feature-hyperstition-tiebreaker, opened 2026-06-10, OPEN)
- Jun-10 batch (0/5 addressed): #1 Japanese README, #2 Scenario Clone Button, #3 Simulation Batch Create API, #4 Simulation Percentile Rank, #5 Platform Performance Metrics.
- Jun-08 batch (3/5 addressed): #1→PR#153 merged Jun 09; #5→PR#155 merged Jun 10. Unbuilt: #2 Trending Topics, #3 MCP Tool Catalog JSON, #4 Pre-Run Cost Estimator.
- Jun-06 batch (2/5 addressed): #1→PR#151 merged Jun 07; #3→PR#152 OPEN Jun 08. Unbuilt: #2 Simulation Payload Validator, #4 Monthly Stats Time-Series, #5 Platform Agent Behavior Census.
- Jun-04 batch (4/5 addressed): #2→PR#149 merged Jun 05; #3→PR#150 merged Jun 07; #1+#5 pre-existing. Unbuilt: #4 All-Time Leaderboard.
- Jun-02 batch (2/5 addressed): #1→PR#145 merged Jun 03; #5→PR#147 merged Jun 04. Unbuilt: #2 Scenario Clone Button, #3 Japanese README, #4 Simulation Batch Create API.
- Jun-01 batch (1/5 addressed): #2→PR#137 merged Jun 02. #1 Operator Profile blocked; #3 Search JSON redundant; #4+#5 pre-existing.
- May-30 batch (3/5 addressed): #4→PR#131, #1→PR#132, #3+#5 pre-existing. Unbuilt: #2 French Locale (issue #95, i18n refactor ~195 call sites; PR #148 helper tests as prerequisite).
- Open community issue #95 — French locale request (non-urgent; i18n dict-form refactor deferred until scoped)
