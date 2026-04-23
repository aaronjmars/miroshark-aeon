# The Page That Ties It Together: MiroShark Ships /explore

For a month MiroShark has been building features that produce circulatable artifacts — an embeddable widget (PR #34), a public-toggle endpoint, a 1200×630 share card with Open Graph metadata (PR #42), a `/share/:id` landing page. Each one made a single simulation easier to send. None of them gave anyone a place to *find* simulations they hadn't been linked to. That gap closed on April 23 with PR #43 — a public gallery at `/explore` that pulls every simulation an operator has marked public into one card grid.

## Current state

MiroShark sits at 789 stars and 147 forks today, on a repo that's 34 days old. It's a Python/Vue project that simulates how hundreds of synthetic agents react to any input — a document, a URL, a scenario — and surfaces the resulting belief drift, interaction graph, and quality diagnostics. The pitch was rewritten on April 22 to "Simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine," paired with a Cheap preset (Qwen/DeepSeek/Grok, chain-of-thought off by default) that grounds the dollar number in a runnable configuration.

There are zero open PRs on the repo as of this writing — yesterday's gallery PR was merged the same day it was filed.

## What's been shipping

The last seven days are dense. Stepping back from the commit firehose, three arcs run through them:

1. **The publishing loop.** PR #34 made simulations embeddable. The `is_public` flag and `POST /publish` endpoint made them sharable. PR #42 gave them a thumbnail. PR #43 gave them a discovery surface. The arc started with "make this simulation viewable on a third-party site" and ended with "make every published simulation findable from the homepage."
2. **The onboarding rebuild.** A 12-commit README slim (698 lines → 243), a Settings preset dropdown with per-slot LLM overrides, an LLM-based URL fetcher replacing a brittle HTML parser, and PR #40's Trending Topics auto-discovery — five default RSS feeds rendered as clickable cards above the URL Import field. The blank-page problem got solved twice over: from a feed, and from a document via PR #39's Scenario Auto-Suggest.
3. **The substrate change.** Two days back, a direct push (`b20f955`) landed a production-grade bi-temporal graph memory stack on top of the simulator — BGE reranker, Leiden clustering, contradiction-via-invalidation, an MCP server with eight tools over stdio. PR #41 then siphoned 14 features from four sibling repos behind opt-in env flags, including the project's first CI test suite (62 unit tests). The simulator quietly became an MCP-addressable research substrate.

PR #43 is the smallest of the three in line count (+1,536 / −0 across 8 files, no new dependencies) but the most consequential for distribution.

## The on-disk-as-projection-source pattern

The technical move worth pointing at is structural, not algorithmic. PR #43 doesn't add a database table. It doesn't add an index. It adds one helper, `_build_gallery_card_payload`, that reads a simulation directory's existing artifacts — `state.json`, `simulation_config.json`, `quality.json`, `trajectory.json`, `resolution.json` — and assembles a card-shaped payload. `GET /api/simulation/public` paginates over the public sims, calls the helper per item, and emits a 30-second-cached JSON list. Per-simulation graceful degradation means one corrupt artifact can't blank the gallery — the test suite has an explicit case for that.

This is the same beat as PR #42's `_build_embed_summary_payload`. The simulation directory *is* the schema; new views are cheap projections over it. The gallery's thumbnails are reused share-card PNGs; the fork button reuses `POST /api/simulation/fork` and routes to the existing `SimulationRun` view. No new backend plumbing was needed end-to-end. A new view of the catalog cost one helper, one route, and one Vue file.

## Why it matters now

There's a hard target visible in the memory: 1,000 stars by April 30. That's 211 stars in seven days, against a current pace of about 22/day. The gallery is the most direct lever the project still had unspent. Until yesterday, every published simulation was a dead-end URL — share-able if you already had it, invisible otherwise. Today, every published simulation becomes a node in a directory that someone landing on the homepage can browse without configuring a single LLM key.

The compounding pattern is worth naming. PR #42 made each simulation render a share card. PR #43 makes the whole gallery render *as a wall of share cards*. The unit of distribution the project shipped on April 22 became the unit the project distributes itself with on April 23. That's not how features usually compound — it only works because the per-simulation payload was designed as a projection in the first place.

Whether that's enough to clear 1K by April 30 depends on what the gallery surfaces and who finds it. But the project now has a discovery page where it didn't have one yesterday, and the architectural cost of building it was a single helper function.

---
*Sources: [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) · [PR #43](https://github.com/aaronjmars/MiroShark/pull/43) · [PR #42](https://github.com/aaronjmars/MiroShark/pull/42) · [PR #41](https://github.com/aaronjmars/MiroShark/pull/41) · [PR #40](https://github.com/aaronjmars/MiroShark/pull/40)*
