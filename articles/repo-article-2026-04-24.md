# The Simulator You Can Ping From Cursor: MiroShark Surfaces Its Hidden Graph

For three days, MiroShark has been compounding the same move: take something the codebase already has, and build the surface that lets a stranger find it. Today's ship, [PR #44](https://github.com/aaronjmars/MiroShark/pull/44), is the most load-bearing version of that move so far. It turns an invisible MCP server — the one quietly shipping since the Apr 21 weekend — into a click-and-paste Settings panel for Claude Desktop, Cursor, Windsurf, and Continue.

## Current state

[MiroShark](https://github.com/aaronjmars/MiroShark) crossed 800 stars today. Thirty-five days old. 149 forks. Six contributors. Zero open PRs. Python backend (Flask + Neo4j + on-disk sim directories), Vue frontend, an MCP server that exposes the whole thing over stdio. The one-line pitch is "simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine": drop in a document or a headline, and hundreds of grounded agents react hour by hour on a synthetic Twitter, Reddit, and prediction market.

Two external signals landed this week alongside the shipping cadence. Paradigm CTO [@gakonst](https://x.com/gakonst) starred the repo. OriginTrail's founder publicly co-signed it for DKG V10. Both of those audiences care about the same question: is there a research-grade substrate under the demo? As of today, the answer is wired into the Settings panel.

## What's been shipping

The week's arc is unusually legible. Each day surfaces capability laid down earlier:

- **Mon Apr 21.** A direct push (`b20f955`) lands the full graph memory stack — bi-temporal edges, Leiden clustering, LLM entity resolution, contradiction detection with invalidation-not-deletion, a ReACT reasoning subgraph, and an MCP server exposing eight retrieval tools over stdio. 17 files, +2,690 lines. Nothing in the UI changed.
- **Mon Apr 21 (later).** [PR #41](https://github.com/aaronjmars/MiroShark/pull/41) siphons 14 features from four sibling repos behind env flags — Nash equilibrium, counterfactual branching, per-agent mid-sim MCP dispatch, prompt caching, and a first CI test suite (62 unit tests). Still no user-facing hook for MCP.
- **Wed Apr 22.** [PR #42](https://github.com/aaronjmars/MiroShark/pull/42) adds a 1200×630 Pillow-rendered share card. The GitHub description gets rewritten to "$1 & less than 10 min." README slims 698 → 243 lines.
- **Thu Apr 23.** [PR #43](https://github.com/aaronjmars/MiroShark/pull/43) ships `/explore` — a public gallery that reuses the share card PNG as its thumbnail. One renderer, two surfaces.
- **Fri Apr 24.** [PR #44](https://github.com/aaronjmars/MiroShark/pull/44) gives the MCP server a doorbell: a `GET /api/mcp/status` endpoint, a Settings panel that auto-stamps absolute paths and Neo4j liveness into copy-pasteable JSON for four IDE clients, and a tool-catalog drift test that regex-scrapes `mcp_server.py` to keep the API honest. +1,112 / −20 across 8 files.

Each ship is small. The compounding isn't — three of this week's four PRs depend on something merged earlier the same week.

## Technical depth

The PR #44 design choice worth naming: **the snippet is rendered server-side from resolved paths, not shown as a template.** Most MCP onboarding docs hand you a JSON blob with `"/path/to/venv/python"` and tell you to fill it in. MiroShark's backend resolves the actual `backend_dir`, the actual `mcp_script`, and the actual Python interpreter running the server, then stamps them into the snippet. Paste and go. The Neo4j liveness probe lives on the same endpoint — the panel tells you `Ready`, `Neo4j down`, or `Server file missing` before you've touched your editor config.

The architecture beat is the same one PR #43 hit: treat what's already on disk as the schema, and write cheap views over it. The sim directory is already a document; `_build_gallery_card_payload` (PR #43) is a view; `_build_embed_summary_payload` (PR #42) is another. The MCP server is a third view — over the Neo4j graph this time, not the sim directory. PR #44 doesn't touch any of that. It just publishes the resolved path to the server and the shape of the four client configs that consume it.

The tool-catalog drift test is the quiet hero. It regex-scrapes `mcp_server.py` for `@mcp.tool()` decorators and asserts the set matches the API's `_TOOLS` list. Add a tool to the server, forget to update the API, CI fails. That's how you keep an onboarding surface from lying to users six months from now.

## Why it matters

MCP adoption curve is the external hook. When Anthropic launched MCP in late 2024, it was a protocol demo; by spring 2026, Claude Desktop, Cursor, Windsurf, and Continue all ship native support. An MCP-native product means a developer can stand up a simulation, then ask "what did the analyst personas believe after round 20?" from inside their editor, against the same bi-temporal graph the frontend reads.

That's the positioning unlock. MiroShark isn't competing to be the best simulation *app* anymore — it's becoming the simulation *substrate* that AI tools address. Paradigm's CTO doesn't star Vue dashboards. The graph memory stack and the MCP server are what get starred. PR #44 is the piece that lets the audience attracted by the substrate actually reach it.

The sprint target is 1,000 stars by April 30. 802 today, six days left. The MCP panel is the kind of surface that turns every existing install into an "add to your AI editor" pitch — which is the sort of compounding the next six days need.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark) · [PR #44 AI Integration · MCP](https://github.com/aaronjmars/MiroShark/pull/44) · [PR #43 /explore](https://github.com/aaronjmars/MiroShark/pull/43) · [PR #42 Social Share Card](https://github.com/aaronjmars/MiroShark/pull/42) · [PR #41 Sibling-Repo Siphon](https://github.com/aaronjmars/MiroShark/pull/41) · Graph memory direct push [`b20f955`](https://github.com/aaronjmars/MiroShark/commit/b20f955) · [docs/MCP.md](https://github.com/aaronjmars/MiroShark/blob/main/docs/MCP.md)*
