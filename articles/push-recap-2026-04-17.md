# Push Recap — 2026-04-17

## Overview
96 commits across two repos by 2 authors (aaronjmars, Aeon). The day's main thrust: MiroShark gained a full post-simulation analytics suite — quality diagnostics and an agent interaction network graph — while the Aeon agent framework got a hardened tweet pipeline, a new $MIROSHARK-denominated reward allocator, a late-afternoon upstream sync + Opus 4.7 upgrade, and a missing-secret forwarding fix. A large OpenRouter observability commit on MiroShark also overhauled model configuration, agent tracking, and UI polish across 24 files.

**Stats:** ~110 files changed, +3,230/-830 lines across 96 commits

---

## aaronjmars/MiroShark

### Simulation Analytics Suite (PRs #32 and #33)
**Summary:** Two new post-completion analysis tools landed back-to-back. Quality Diagnostics gives every finished simulation a health badge (Excellent/Good/Low) computed from participation rate, stance entropy, convergence speed, and cross-platform interaction rate. The Interaction Network renders a force-directed SVG graph of agent-to-agent interactions — who liked, reposted, or replied to whom — with centrality metrics, echo chamber scoring, and platform filters.

**Commits:**
- `7177217` — feat: simulation quality diagnostics with health badge and actionable suggestions (#32)
  - Changed `backend/app/api/simulation.py`: New `GET /<sim_id>/quality` endpoint — computes four metrics (participation rate, stance entropy, convergence speed, cross-platform rate), caches results to `quality.json`, returns health badge and actionable suggestions for improving low-quality runs (+214 lines)
  - Changed `frontend/src/api/simulation.js`: New `getSimulationQuality()` API function (+9 lines)
  - Changed `frontend/src/components/HistoryDatabase.vue`: Quality dot (colored by health grade) on simulation history cards, full diagnostic metrics in the detail modal with progress bars and suggestion list (+194 lines)
  - Changed `frontend/src/components/Step3Simulation.vue`: Clickable quality chip in the events bar for completed simulations, expandable diagnostics panel with metric bars and improvement suggestions (+194 lines)

- `b87920d` — feat: Agent Interaction Network Graph (#33)
  - Changed `backend/app/api/simulation.py`: New `GET /<sim_id>/interaction-network` endpoint — parses JSONL action logs to extract agent-to-agent edges (likes, reposts, quotes, replies), builds a weighted directed graph, computes degree centrality, echo chamber score, and bridge agent detection; caches to `network.json` (+272 lines)
  - Changed `frontend/src/api/simulation.js`: New `getInteractionNetwork()` API function (+9 lines)
  - New file `frontend/src/components/InteractionNetwork.vue`: 644-line SVG force-directed graph visualization — nodes colored by stance (bullish green / bearish red / neutral gray), sized by degree centrality; edges colored by platform; hover highlighting that dims unconnected nodes; platform toggle filters; insights panel showing top hub, bridge agent, and echo chamber score; PNG export button (+644 lines)
  - Changed `frontend/src/components/Step3Simulation.vue`: New "⬡ Network" toggle button in the toolbar, InteractionNetwork overlay integration, mutual exclusion with other overlays (+25/-4 lines)

**Impact:** Simulation runs now produce two layers of post-hoc analysis that didn't exist before. Quality Diagnostics lets users know whether a run's results are trustworthy (low participation or zero cross-platform interaction degrades signal quality). The Interaction Network reveals emergent social structure — who's the hub, where are echo chambers forming, which agents bridge communities. Together they move MiroShark from "run simulation, read output" to "run simulation, understand its dynamics."

---

### OpenRouter Observability, Wonderwall Agent Tracking & UI Polish
**Summary:** A large 24-file commit overhauled how MiroShark talks to LLM providers and tracks what its agents are doing. OpenRouter gets proper attribution headers and metadata, the Wonderwall agent subprocess now emits structured events that merge with Flask-process events for a unified run summary, and the frontend gets dynamic page titles, collapsed profile previews, and numerous UI cleanups.

**Commits:**
- `ac8d964` — feat: OpenRouter observability, Wonderwall agent tracking, and UI polish
  - Changed `.env.example`: Rewrote model configuration docs — now documents three modes (Local/Ollama, Cloud Cheap, Cloud Best) with benchmarked OpenRouter presets; added `FAST_LLM_MODEL` and `OASIS_MODEL_NAME` vars (+93/-33 lines)
  - Changed `README.md`: Updated configuration section to match new cloud presets; replaced old model table with slot-based explanation (+54/-70 lines)
  - Changed `backend/app/config.py`: Added `FAST_LLM_MODEL` env var for lightweight tasks (embedding, classification); documented model slot purposes (+11/-4 lines)
  - Changed `backend/app/utils/llm_client.py`: Added OpenRouter metadata headers (`User-Agent`, `X-OpenRouter-Categories`); new per-request metadata injection for cost tracking (+28 lines)
  - Changed `backend/app/utils/run_summary.py`: Unified run summary now reads both global `events.jsonl` (Flask) and per-simulation `events.jsonl` (Wonderwall subprocess), deduplicates by `event_id`, and merges into one summary (+41/-20 lines)
  - Changed `backend/wonderwall/social_agent/agent.py`: Renamed from "OASIS" to "Wonderwall" throughout; added per-agent event tracking — each agent call now emits a structured event to the simulation's JSONL log, enabling fine-grained cost attribution and token usage per agent (+121/-3 lines)
  - Changed `backend/scripts/run_parallel_simulation.py`: Belief state injection from `belief_state.py`, multi-model routing support (+66/-20 lines)
  - Changed `backend/scripts/run_twitter_simulation.py` and `run_reddit_simulation.py`: OpenRouter attribution headers added to Wonderwall agent model creation (+13/-1 lines)
  - Changed `backend/app/services/report_agent.py`: Progressive fallback for action matching — tries OR-separated phrases first, then individual words, then returns all actions (+46/-13 lines)
  - Changed `backend/app/services/simulation_config_generator.py`: Clamped `total_simulation_hours` to 24–336h range to prevent absurd values from LLM config generation (+8/-2 lines)
  - Changed `backend/app/services/simulation_runner.py`: Clears director event files on fresh simulation starts (prevents leakage from previous runs) (+12 lines)
  - Changed `backend/app/api/simulation.py`: Director Mode event limit raised from 3 to 10 per simulation (+3/-3 lines)
  - Changed `backend/wonderwall/social_agent/agents_generator.py`: Switched `agent_info[i]["field"]` to `.get("field", "")` for safer profile access (+8/-8 lines)
  - Changed `frontend/src/components/Step2EnvSetup.vue`: Profile preview now shows 4 profiles collapsed by default with "Show all" toggle (+45/-9 lines)
  - Changed `frontend/src/components/Step3Simulation.vue`: Button icons (↻ Restart), compact toolbar, removed redundant status dot (+138/-188 lines)
  - Changed `frontend/src/components/BeliefDriftChart.vue`: Shortened header from "BELIEF DRIFT" to "DRIFT" (+5/-5 lines)
  - Changed `frontend/src/components/InfluenceLeaderboard.vue`: Removed per-QA share button from trace interview modal (+7/-15 lines)
  - Changed 5 frontend view files (`MainView`, `SimulationView`, `SimulationRunView`, `ReportView`, `InteractionView`): Added `watchEffect` for dynamic browser tab title based on simulation status (running/completed/failed) (+46/-5 lines)

**Impact:** The OpenRouter metadata headers mean simulation runs are now properly attributed in OpenRouter's dashboard, enabling cost-per-simulation tracking. Wonderwall agent-level event tracking closes a major observability gap — previously only Flask-side LLM calls were logged, but the actual agent simulation subprocess calls (which represent the bulk of token usage) were invisible. The UI polish across 5 views adds professional touches (dynamic titles, collapsed profiles) that compound into a more polished product.

---

## aaronjmars/miroshark-aeon

### Tweet Allocator — $MIROSHARK Rewards
**Summary:** The tweet-allocator skill was created, iterated, and hardened in a single day. It identifies the top 5 tweets about the project, verifies each author has a Bankr wallet, and allocates $10/day worth of $MIROSHARK tokens proportional to engagement scores. Originally designed for USDC, it was switched to $MIROSHARK payouts within the first few hours. A new `prefetch-bankr.sh` script works around the GitHub Actions sandbox limitation by pre-fetching wallet verifications before Claude runs.

**Commits:**
- `10b0d74` — fix: prefetch-xai reads var from aeon.yml + add tweet-allocator skill
  - New file `skills/tweet-allocator/SKILL.md`: 201-line skill definition — score formula (likes + 2×RTs + replies), top-5 selection, Bankr wallet verification, allocation proportional to score, article generation, dedup against prior payments (+201 lines)
  - Changed `aeon.yml`: Added tweet-allocator to skill roster with 4×/day schedule (+4/-1 lines)
  - Changed `scripts/prefetch-xai.sh`: Reads `var` from `aeon.yml` when not passed as argument, eliminating manual var passing (+14 lines)
  - Changed `.github/workflows/aeon.yml`: Added `BANKR_API_KEY` to workflow environment (+4 lines)

- `3b33a72` — feat: tweet-allocator pays in $MIROSHARK, add BANKR_API_KEY to workflow
  - Changed `skills/tweet-allocator/SKILL.md`: Switched from USDC to "$X in $MIROSHARK" wording throughout (+15/-15 lines)
  - New file `articles/tweet-allocator-2026-04-16.md`: First allocator report with reward table (+64 lines)

- `39464ff` — feat: broaden fetch-tweets, cache-first bankr, "$X in $MIROSHARK" wording
  - New file `scripts/prefetch-bankr.sh`: 133-line bash script — queries Bankr Agent API for wallet verification of X handles, saves results to `.bankr-cache/verified-handles.json` for sandbox-safe reading (+133 lines)
  - Changed `skills/tweet-allocator/SKILL.md`: Cache-first Bankr workflow — read `.bankr-cache/` before attempting API calls (+28/-21 lines)

- `0d93ff9` — simplify(tweet-allocator): Bankr wallet is the single gate
  - Changed `skills/tweet-allocator/SKILL.md`: Major simplification — removed complex multi-step verification flow, made Bankr wallet the single qualification gate. If no wallet, they get a "sign up" nudge instead (+57/-144 lines)

- `3a0210d` — fix(tweet-allocator): apply required-token filter to candidates
  - Changed `skills/tweet-allocator/SKILL.md`: Added defensive filter — tweets must contain at least one of the OR-separated tokens from the fetch-tweets var ($MIROSHARK, @miroshark_, github URL) to qualify (+2 lines)

**Impact:** Organic community engagement on Twitter now has a direct economic incentive. The $10/day in $MIROSHARK creates a flywheel: tweet about the project, get paid in the project's token, which gives recipients skin in the game. The Bankr prefetch pattern is reusable for any auth-required API in the sandbox.

---

### Fetch-Tweets Hardening
**Summary:** The fetch-tweets skill underwent rapid iteration to fix false positives, tune dedup behavior, and add a post-filter pipeline. Grok's x_search sometimes returns tweets that mention "miroshark" or "aeon" in unrelated contexts — a new Python post-filter now enforces that tweets must contain at least one of the required tokens ($MIROSHARK, @miroshark_, github URL). The persistent seen-file (PR #16) supplements log-based dedup with a file that persists across conversations.

**Commits:**
- `1abc20f` — improve(fetch-tweets): persistent dedup via seen-file (#16)
  - New file `memory/fetch-tweets-seen.txt`: Persistent URL list — every reported tweet URL gets appended here, surviving across conversation boundaries (+24 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Dual-source dedup — union of seen-file + last 3 days of logs → SEEN_TWEETS (+7/-1 lines)

- `1dba460` — fix(fetch-tweets): tighten Grok prompt + add post-filter for false positives
  - New file `scripts/filter-xai-tweets.py`: 110-line Python script — reads Grok's raw text output, checks each tweet block for required tokens (case-insensitive substring match against OR-separated var tokens), drops false positives (+110 lines)
  - Changed `scripts/prefetch-xai.sh`: Pipes Grok output through post-filter before caching (+8/-1 lines)

- `ff9fa2a` — fix(fetch-tweets): 1-day window, github.com/ in var, untrack .xai-cache
  - Changed `aeon.yml`: Updated fetch-tweets var to include full `github.com/aaronjmars/miroshark` URL (+1/-1 lines)
  - Changed `.gitignore`: Added `.xai-cache/`, `.bankr-cache/`, `.pending-notify/` to ignore list (+4 lines)
  - Changed `skills/fetch-tweets/SKILL.md`: Narrowed fallback API window from 7 days to 1 day (+1/-1 lines)

- `90341ee` — fix(fetch-tweets): re-enable dedup (broader search + 1d window kept)
  - Changed `skills/fetch-tweets/SKILL.md`: Re-enabled dedup after a brief experiment without it; broader search terms + 1-day window is the right balance (+9/-9 lines)

**Impact:** False positive rate drops significantly — spam tweets tagging $MIROSHARK without real context (like the $LOL presale promotions) now get filtered before they reach the skill. The persistent seen-file eliminates the window where a tweet could be re-reported if it fell outside the 3-day log lookback.

---

### Infrastructure Fixes
**Summary:** Three targeted fixes for the notification pipeline and workflow system.

**Commits:**
- `e5a7361` — fix(notify): switch Telegram to HTML mode to preserve handle underscores
  - Changed `.github/workflows/aeon.yml`: Telegram `parse_mode` changed from legacy Markdown to HTML — single underscores in handles like `miroshark_` were being eaten by Telegram's Markdown parser, breaking handle rendering (+20/-2 lines)

- `a483cfa` — fix: don't ignore .outputs/ — workflow's chain-runner needs those tracked
  - Changed `.gitignore`: Removed `.outputs/` from ignore list — chain-runner writes skill outputs there for downstream steps to consume, so they need to be tracked (+0/-1 lines)

**Impact:** Telegram notifications now render handles correctly. Chain-based skill composition works end-to-end with output passing.

---

### Late-Afternoon Upstream Sync, Opus 4.7 Upgrade & Secret Forwarding
**Summary:** Between 15:20 and 16:42 UTC Aaron landed eight follow-up commits that reconcile the fork with upstream Aeon, bump the default model to Opus 4.7, and fix a silent-failure class where skills referenced env secrets the workflow never forwarded. Nearly every skill file was touched — mostly to inject the `tags:` frontmatter line that upstream now expects.

**Commits:**
- `468e62b` — harden: XAI 429 retry + GH_GLOBAL token fallback on checkouts
  - Changed `scripts/prefetch-xai.sh`: single 30s-backoff retry on HTTP 429 responses; 401/403/curl failures still fail fast (+25/-13 lines)
  - Changed `.github/workflows/aeon.yml` and `messages.yml`: checkout tokens now fall through `GH_GLOBAL || GITHUB_TOKEN`, unblocking cross-repo pushes when GH_GLOBAL is the configured secret (+3/-3 lines)

- `a924cff` — sync(skills): backport upstream polish + normalize fetch-tweets frontmatter
  - Changed 16 skills (changelog, code-health, defi-overview, fetch-tweets, github-issues, github-trending, issue-triage, pr-review, reddit-digest, reflect, research-brief, rss-digest, search-skill, security-digest, token-movers, weekly-review): tags frontmatter added; `reflect` now runs a skill-health trend check; fetch-tweets frontmatter normalized (capitalized name, `tags: [social]`) — body unchanged since upstream just adopted the hardened pipeline (+46/-1 lines)

- `5c21220` — chore(skills): inject tags frontmatter from upstream aeon
  - Changed 32 skills: added missing `tags:` lines to every skill shared with upstream that was behind on frontmatter metadata. 100% of shared skills now tagged (+32 lines)

- `dab7e2c` — chore(skills): tag fork-only skills + fix stale output/ paths + images/
  - Changed 11 fork-specific skills (build-skill, feature, hn-digest, hyperstitions-ideas, memory-flush, polymarket, search-papers, self-review, trending-coins, tweet-digest, wallet-digest): tags frontmatter added
  - Changed `channel-recap`, `tool-builder`, `vuln-scanner`: replaced stale `output/articles/` → `articles/` and `output/skills/` → `.outputs/` path references
  - New `images/.gitkeep`: reserved folder for hero-image post-process writes (+18/-7 lines)

- `cf30c98` — chore: standardize .gitignore, remove tracked scratch + dead gitlinks
  - Changed `.gitignore`: aligned with upstream aeon format, explicit patterns (+44/-2 lines)
  - Removed 2 stale gitlink submodules (`.build-target`, `build-target`) pointing at abandoned repos
  - Removed 11 tracked scratch files (`.ghtoken`, 6× `tmp_*` notify/grok files, `fetch_tweets.sh`, `fetch_tweets_run.sh`, `grok_search.py`) — one-off scripts superseded by `scripts/prefetch-xai.sh` and `skills/fetch-tweets/` (-154 lines)

- `debd724` — chore: remove stale memory/extract_patches.py
  - Removed `memory/extract_patches.py`: 34-line scratch Python script left behind by a push-recap run on 2026-03-27, unreferenced by any current skill. `memory/` should only hold logs, topics, issues, skill-health, and core state files (-34 lines)

- `654c98d` — feat: upgrade default opus model 4.6 → 4.7
  - Changed `aeon.yml`, `.github/workflows/aeon.yml`, `.github/workflows/messages.yml`, `README.md`, `dashboard/lib/constants.ts`, `skills/cost-report/SKILL.md`: runtime default model switched from claude-opus-4-6 to claude-opus-4-7 across runtime config, workflow dropdowns, UI picker, and pricing table. Pilot run on aeon-aaron/memory-flush verified 4.7 runs cleanly in 2m49s with correct token accounting. Historical references in `memory/token-usage.csv`, `memory/logs/`, `articles/` intentionally left untouched — they record what actually ran at the time (+10/-10 lines)

- `898c51e` — fix: forward DEVTO/NEYNAR/VERCEL (+BANKR in aeon/aaron) to skill runtime
  - Changed `.github/workflows/aeon.yml`: added `BANKR_API_KEY`, `VERCEL_TOKEN`, `DEVTO_API_KEY`, `NEYNAR_API_KEY` to the Run env block. Audit against the new architecture showed 100+ skills reference these secrets at runtime (WebFetch Bearer auth, curl, env checks) but the workflow was silently dropping them — tweet-allocator, vercel-projects, deploy-prototype, syndicate-article, and farcaster-digest would have silently failed at first auth call (+3 lines)

**Impact:** The fork is now in frontmatter parity with upstream Aeon — `tags:` metadata exists on every skill, enabling skill-filter/skill-discovery features that depend on it. The Opus 4.7 upgrade pulls in the latest model across every entry point in one commit, avoiding the split-state problem of some workflows running 4.6 and others running 4.7. The secret-forwarding fix prevents a whole class of silent auth failures — without it, the tweet-allocator would have worked in the prefetch step but failed the moment any skill tried to hit Bankr directly from inside Claude. Housekeeping removes 13 tracked scratch files and 2 dead gitlink submodules that had accumulated across prior Aeon runs.

---

## Developer Notes
- **New dependencies:** None (all features built with existing stack)
- **Breaking changes:** Director Mode event limit raised from 3 to 10 per simulation — existing simulations with events are unaffected. Default runtime model changed from Opus 4.6 → 4.7 (all workflow dispatch defaults and UI pickers moved together; no split state)
- **Architecture shifts:** Wonderwall agent subprocess now emits structured JSONL events that merge with Flask events; this is a prerequisite for per-agent cost attribution. The Bankr prefetch pattern (`scripts/prefetch-bankr.sh`) establishes a reusable sandbox workaround for any auth-required API. Workflow env block now forwards DEVTO/NEYNAR/VERCEL/BANKR secrets, closing a silent-failure gap for auth-requiring skills
- **New scripts:** `scripts/prefetch-bankr.sh` (wallet verification), `scripts/filter-xai-tweets.py` (Grok post-filter)
- **Frontmatter parity:** All 59+ skills shared with upstream Aeon now carry `tags:` frontmatter; all 11 fork-specific skills also tagged — enables tag-based skill filtering/discovery
- **Tech debt:** fetch-tweets went through 5 rapid-fire config changes (dedup on → off → on, window 7d → 3d → 1d) — the skill definition is stable now but the log has churn. Cleaned up 13 stale scratch files and 2 dead gitlink submodules accumulated from prior runs

## What's Next
- MiroShark at 706 stars (+10 today) — continued organic growth
- The tweet-allocator is operational with 5 verified Bankr wallets and 6 unallocated tweets carrying to Apr 18
- Quality Diagnostics and Interaction Network are merged — next likely step is surfacing these in the history search filters or using quality scores to auto-flag low-quality runs
- OpenRouter observability opens the door to cost-per-simulation dashboards and model comparison analytics
- Opus 4.7 is now the baseline — monitoring token-usage.csv for cost/perf deltas vs 4.6 baseline
- 2 new forks today (ghostbyte0x, growth88) suggest growing developer interest
