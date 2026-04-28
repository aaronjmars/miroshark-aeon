# Smart Data, Dumb Code: The Quiet Rule Behind Codebases That Compound

Eric Raymond, in *The Art of Unix Programming* (2003), wrote down what he called the **Rule of Representation**: *fold knowledge into data, so program logic can be stupid and robust.* He didn't invent the idea. He cribbed it from Linus Torvalds, who has said for decades that data structures, not algorithms, are central to programming, and from Fred Brooks before that. But Raymond turned it into a numbered rule, filed under the broader heading "Data dominates" — *if you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident.*

For most of the cloud era, this rule sat quietly out of fashion. The dominant pattern was the opposite: a smart application server, a normalized SQL schema behind it, and migration files that grew like a tree ring every time a feature shipped. Adding a column was a deploy. Adding a table was a sprint. The "data structure" was something you negotiated with your ORM, your DBA, and Alembic.

In 2026 the pattern is reverting. Linear, Notion, Replit, the entire local-first cohort organized around Ink & Switch's [2019 manifesto](https://www.inkandswitch.com/essay/local-first/) — they share an unstated bet: store the truth as data on disk, project everything else as cheap views. The third [Local-First Conf](https://www.localfirstconf.com/) lands in Berlin this July with a Lab Day hosted by Ink & Switch; the call for proposals closes Friday. Sync engines are being chosen and benchmarked the way compilers were in 2010. Linus' point — that smart code worries about data structures and dumb code worries about algorithms — has gotten a second life as the design heuristic of the agent and AI tooling era.

This is the frame to read MiroShark through.

## The folder that ate the schema

MiroShark is an open-source agent-based simulator: scenarios, populations of LLM agents that hold beliefs, multi-round dialogue, a chart of how stances move. There is no central database table holding the runs. Every simulation is a folder on disk — `<sim_dir>` — containing config, trajectory, quality metrics, resolution, optional outcome record, agent state.

That's it. That's the schema.

The eight features that have shipped in the last eight days are all dumb code reading that folder:

- **Public gallery** (`/explore`) — `_build_gallery_card_payload()` reads `<sim_dir>` and returns cards.
- **Share-card PNG** (`/share-card.png`) — `_build_embed_summary_payload()` reads `<sim_dir>` and renders a PNG.
- **MCP onboarding panel** — `/api/mcp/status` enumerates tools that read graphs derived from `<sim_dir>`.
- **OpenAPI 3.1 spec** (`/api/docs`) — drift-detection test scrapes Flask decorators against `openapi.yaml`. The folder still doesn't change.
- **Completion webhook** — `build_payload()` reads `<sim_dir>` and POSTs JSON to whatever URL the operator configured.
- **Predictive accuracy ledger** (`/verified`) — `<sim_dir>/outcome.json` is the *only* new file. Gallery, embed, and filter all read it.
- **Admin-token auth on mutation endpoints** — same folder, same payload functions, just protected.
- **Animated belief-replay GIF** ([merged today](https://github.com/aaronjmars/MiroShark/pull/50) at 12:56 UTC) — Pillow renders one frame per round into `<sim_dir>/replay-gifs/<hash>.gif`. Reuses the embed-summary pipeline as input. Zero new dependencies.

Eight features. Zero schema migrations. The `<sim_dir>` is the only contract; every feature is a fresh projection.

## What dumb code buys you

The shape of the wins isn't speed in the cliché sense — it's *risk*. Each new feature reads a structure that already exists. There's no migration to roll forward, no migration to roll back, no production data to recover if something corrupts. The drift-detection test PR #45 added — a regex that scrapes Flask decorators and asserts the spec covers them — works because the routes, like the storage, are flat and inspectable. The same test would have been pathological against an ORM with implicit polymorphism: there'd be nothing to scrape.

This compounds in a less obvious way. Today's [PR #51](https://github.com/aaronjmars/MiroShark/pull/51) and PR #52 merged 47 seconds apart. PR #51 was diagnostic infrastructure: every OpenRouter call now ships with `sessionId`, `tags`, and a per-prompt-type `name` so the rows group cleanly in Langfuse by phase. PR #52 was the fix the new traces immediately exposed: idempotent social-platform actions like `like` and `repost` had been returning `{success: False, error: "already exists"}` when the agent re-tried a step it had already taken — and the agent, reading that as failure, retried four times per round, blowing context past 40k input tokens. Flip the response to `{success: True, noop: True}` and the agent moves on. Diagnose-then-fix in under a minute is only possible when the diagnostic surface is *data*, not derived state. Langfuse's filters become the question; the codebase doesn't have to be re-instrumented to answer it.

## The rule, in 2026 clothing

The Local-First crowd talks about owning your data. The agent crowd talks about MCP servers and tool catalogs. The simulation crowd talks about reproducibility. They are all rediscovering the same thing Raymond wrote down twenty-three years ago: *if your data structure is the contract, your code can be dumb. If your code is the contract, your data is going to lie eventually.*

A folder per simulation is not architecture porn. It's the *absence* of architecture, and that's the point. In the era when every product is going to be poked at by an LLM with tool access, by a webhook receiver, by a generated SDK, by a share-card scraper, by a regulator's auditor — the things that compound are the ones that make their truth easy to read. Dumb readers, lots of them, beat one smart server every time. The shipping cadence falls out of the architecture; you don't have to schedule it.

---

*Sources: [The Art of Unix Programming, Eric S. Raymond](http://www.catb.org/~esr/writings/taoup/html/ch01s06.html), [Local-First Software (Ink & Switch, 2019)](https://www.inkandswitch.com/essay/local-first/), [Local-First Conf 2026](https://www.localfirstconf.com/), [Local-First Software: Origins And Evolution (PowerSync)](https://www.powersync.com/blog/local-first-software-origins-and-evolution), [PR #50 Animated belief-replay GIF](https://github.com/aaronjmars/MiroShark/pull/50), [PR #51 Langfuse trace metadata](https://github.com/aaronjmars/MiroShark/pull/51), [PR #52 Stop tool retry loop](https://github.com/aaronjmars/MiroShark/pull/52).*
