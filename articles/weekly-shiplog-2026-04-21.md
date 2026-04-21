# Week in Review: The Week MiroShark Stopped Being a Simulator

*2026-04-21 — Weekly shipping update*

## The Big Picture

Seven days ago, MiroShark was a simulation engine with five analytics overlays and one open community PR. This evening it's a research substrate — an MCP-addressable knowledge graph with bi-temporal edges, persisted reasoning traces, Nash-equilibrium analysis, per-agent mid-simulation tool use, and 62 unit tests guarding it all. Twelve PRs merged on MiroShark over the seven-day window, seven on miroshark-aeon, plus two weighty direct pushes that together moved almost 10,000 lines. The repo went from 698 stars to 751, picked up its first sustained external backend contributor (`mbs5` / `builtbydesigninc`, two merged PRs), and closed the week at zero open PRs on both repos. The shape change is what matters: the product stopped describing itself in terms of what it *runs* and started describing itself in terms of what it *holds*.

## What Shipped

### The Blank-Canvas Trilogy — Setup friction, gone
Three PRs that together solve the "what do I even type" problem at the front door. **Scenario Auto-Suggest** (PR #39, Apr 20) drops three Bull/Bear/Neutral prediction-market cards under the prompt box whenever the user drops in a `.md`/`.txt` file or URL — a SHA-256-keyed LRU cache over a 2KB preview, a 20s LLM timeout, per-IP sliding-window rate limits, and a non-blocking contract that silently hides the panel if anything fails. **Counterfactual Explorer** (PR #37, Apr 20) gives researchers the post-run counterpart: pick up to three top-influence agents, recompute belief drift with them excluded, get back an original-vs-counterfactual split-line chart and a Strong/Moderate/Minimal impact badge — pure transform over cached `trajectory.json`, milliseconds per recompute, no re-simulation. **Trending Topics** (PR #40, Apr 21) closed the third door: for users with no document at all, five clickable cards from Reuters/TechCrunch/Verge/HN/CoinDesk appear below URL Import; one click feeds the URL into `fetchUrlDoc()` which in turn wakes Scenario Auto-Suggest. Stdlib-only parsing (`xml.etree.ElementTree` + `urllib.request`, zero new deps), SSRF-hardened with IPv4 normalization to block loopback-encoded bypasses. A user who lands on the page with nothing now gets to "three scenario cards" in two clicks.

### The Substrate Weekend — Graph memory stack + sibling-repo siphon
Two pushes, seventeen hours apart, that together reshape the backend. Sunday night (Apr 20 22:50 UTC) Aaron direct-pushed `b20f955` — a single commit adding **11 capabilities** to the storage layer: a BGE-reranker-v2-m3 cross-encoder on hybrid-search hits, an LLM-adjudicated entity resolver for fuzzy matches, contradiction detection that *invalidates* rather than deletes superseded edges (keeping history auditable), Leiden community clustering with LLM-generated summaries stored as `:Community` nodes with their own vector index, bi-temporal edges with `valid_at`/`invalid_at`/`as_of` point-in-time queries, Wonderwall activities kind-tagged `belief` vs `observation` at write time, ReACT reasoning traces persisted as `(:Report)-[:HAS_SECTION]->(:ReportSection)-[:HAS_STEP]` subgraphs, and an 8-tool MCP server over stdio at `backend/mcp_server.py`. The report agent can now answer *why* it concluded something by walking its own trace. Monday afternoon, **PR #41** landed — 14 more capabilities cherry-picked from sibling forks (MiroJiang, MiroWhale, OpenMiro, oracle-seeds). Per-agent MCP tools so simulated agents can call outside-world services mid-round. `POST /api/simulation/ask` question-only onboarding. Counterfactual branching via a director-event piggyback. `analyze_equilibrium` fitting a 2-player stance game and enumerating Nash equilibria with `nashpy`. FeedOracle MCP dispatch at template load. Anthropic prompt caching behind `LLM_PROMPT_CACHING_ENABLED`. A publish gate (`is_public` + `/publish`) so embed endpoints 403 until consent. A `miroshark-cli` entry point. **And the first standing CI test suite** — 62 unit tests, `.github/workflows/tests.yml` running on every push. Everything gated behind env flags or per-sim opt-ins; existing deployments see zero behavior change until an operator flips a switch.

### The Analytics Suite — Six overlays and the one that paints a gradient
Five of these landed earlier in the week, the sixth completed the set. **Director Mode** (PR #31, Apr 16) ships breaking events mid-simulation via a file-based queue with marker-replace injection; **Quality Diagnostics** (PR #32, Apr 17) grades every run on participation, stance entropy, convergence speed, and cross-platform rate with actionable suggestions; **Agent Interaction Network** (PR #33, Apr 17) draws a force-directed SVG of who liked/reposted/replied to whom with centrality and echo-chamber scoring; **Embeddable Widget** (PR #34, Apr 18) ships `/embed/:simulationId` with Compact/Standard/Wide presets and copy-ready iframe/Markdown snippets; **Demographic Breakdown** (PR #35, Apr 18) cross-tabs age, gender, country, actor type, and primary platform against final stance, volatility, and influence. And then the Counterfactual Explorer shipped on Apr 20. Every one is a transform over cached artifacts — no re-simulation, no new data collection — so the result grid on any finished run now carries six independent interpretive lenses where a month ago it carried one chart.

### The Outside Hand — First sustained external backend contributions
Two PRs from `mbs5` (Muhammad Bin Sohail, `builtbydesigninc`), both merged Apr 20 in the same nine-minute window as Aeon's own two. **PR #36** parallelizes `report_agent.py` section generation with a `ThreadPoolExecutor`, drops prior-sections context during the parallel phase, and cuts `MAX_REFLECTION_ROUNDS` from 3 to 1. Measured on a 5-section Claude Sonnet 4.6 / OpenRouter run: 20.8 minutes → ~4 minutes, 21 LLM calls → ~10, 270K input tokens → ~50K, $2.16 → ~$0.95. **PR #38** converts `EmbeddingService` to read `Config` via `@property` accessors, so `POST /api/settings` updates actually take effect after startup — a bug they hit running their own fork on Railway. The second PR is the more telling one: the contributor is deploying MiroShark, not just shipping a one-off drive-by.

## Fixes & Improvements

- **NER extraction quality** — chunk sizing, non-speaking entity filter, ontology identifier validation, citation artifact stripping (Apr 15)
- **OpenRouter observability** — proper attribution headers + per-agent event tracking inside the Wonderwall subprocess, closing the biggest gap in cost attribution (Apr 16)
- **Multi-model routing** — `fast_llm`, `smart_llm`, `OASIS_MODEL_NAME` so Gemini Flash handles mechanical work while the simulation loop runs on something smarter (Apr 16)
- **Director Mode polish** — event cap raised 3 → 10 per simulation; dashed amber markers on the drift chart at injection rounds (Apr 17)
- **Browser push notifications** — 🔕/🔔 toggle + Service Worker + VAPID + pywebpush, tab-hidden completion alerts (PR #30, Apr 15)
- **Wizard UX** — Step 2 sub-step status indicator with pulsing dots; wizard renumbered 5-step-with-skip → clean 1/4–4/4 (Apr 20)
- **17-commit cleanup sweep** (Apr 21 15:26–15:44 UTC) — circular deps broken, weak type annotations strengthened, defensive error-swallowing removed, AI slop and stale comments stripped, legacy/deprecated code paths removed, DRY consolidation pass, duplicate type definitions merged
- **OASIS → Wonderwall rename + CI unblock** (Apr 21) — terminology drift cleaned up across the agent subprocess
- **miroshark-aeon self-healing sweep** — heartbeat stuck-run timeout (PR #14), fetch-tweets persistent seen-file (PR #16), hyperstitions dedup guard (PR #17), repo-pulse idempotency (PR #18), XAI cache query sidecar validation (PR #19), XAI annotation citation harvest (PR #20), stale `XAI_API_KEY` flag removal (PR #21); plus Aaron's direct-push workflow fixes — chain-runner jq repair, scheduler catch-up dedup, `./notify` SHA-256 dedup with probe suppression, Telegram message chunking, `$GITHUB_REPOSITORY` article URL correction, `inputs.var` env-var passthrough, prefetch-xai 180s timeout with retry

## By the Numbers

- **MiroShark merged:** 12 PRs plus 2 major direct-push features, +~15,000 / −~1,100 lines across substantive commits
- **MiroShark in flight:** 0 open PRs (cleanest close since the analytics run began)
- **miroshark-aeon merged:** 7 PRs, +~700 / −~70 substantive lines plus ~220 automated chore commits
- **Stars:** ~698 → 751 (+53)
- **Forks:** ~137 → 146 (+9)
- **External contributors active this week:** 1 sustained (`mbs5` / `builtbydesigninc`, 2 PRs merged); total contributors: Aaron Elijah Mars, Aeon, aeonframework, mbs5
- **Test suite:** 0 → 62 unit tests (first standing CI gate on the MiroShark backend)
- **MCP tools exposed:** 0 → 8 (via `backend/mcp_server.py`)

## Momentum Check

Compared with last week (which itself was a five-to-six-analytics-feature seven-day sprint), *pace* is flat but *substrate* changed. Through Apr 19 every meaningful MiroShark PR was Aaron or Aeon; from Apr 20 forward two are not. Internal velocity stayed high — Counterfactual Explorer, Scenario Auto-Suggest, Trending Topics, the graph memory stack, PR #41 — but the striking move was the Sunday-night/Monday-afternoon pivot from "ship another analytics overlay" to "refactor the thing all overlays read from." That's a maturity signal. The weekly-shiplog delta from Apr 20 → Apr 21 is almost entirely the substrate shift: a day ago the story was "first external backend PR"; today it's "MCP-addressable knowledge graph with a test suite." You don't usually get to point at a single day that flips the shape of a project; this week had one.

## What's Next

- **Flag rampup on PR #41** — prompt caching is the lowest-risk / highest-immediate-cost-impact flip; per-agent MCP tools is the most interesting but needs a test sim before default-on
- **token-report XAI migration** — the only remaining skill still curling XAI inline in a sandboxed env-var; the "stale env / silent fail" anti-pattern's last hiding place
- **Second wave from `mbs5`** — zero open PRs, but the Apr 20 same-day second PR (embedding-config fix from a live deploy) suggests a returning contributor, not a drive-by
- **1,000-star target** — at 751 stars / 9 days remaining to Apr 30, needs ~28/day; current 7-day pace is ~7.5/day. PR #41 + PR #40 ship a lot of fresh demo surface (Just Ask, Live Oracle Data, MCP tools, Nash equilibrium, Trending Topics) — material for an organic push, but the curve still has to bend sharply
- **MIROSHARK price** — token bounced +40.6% off the Apr 19 low on Apr 20, faded today to $0.000002236 (-41.4% from Apr 14 ATH), liquidity $172.9K, balanced 75/75 order flow suggesting sideways consolidation
- **Next analytics candidate** — Multi-Document Comparative Mode has been deferred three times in repo-actions; with the substrate now bi-temporal and trace-aware, it's the obvious next feature to pull through the new plumbing

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [PR #30–#41 on MiroShark](https://github.com/aaronjmars/MiroShark/pulls?q=is%3Apr+is%3Aclosed), [PR #14–#21 on miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon/pulls?q=is%3Apr+is%3Aclosed). Per-day detail in `articles/push-recap-2026-04-15.md` through `push-recap-2026-04-21.md`.*
