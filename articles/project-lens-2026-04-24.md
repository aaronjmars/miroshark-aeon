# The Simulator Nobody Opens: A Workday Rebuilt Around MCP

It's Monday morning. Lena, a narrative research lead at a mid-size digital-asset fund, sits down with a coffee and opens Claude Desktop. She doesn't open anything else.

The first thing she types is: *"What have we simulated about the upcoming ETH staking bill this month, and how did the echo-chamber scores compare?"* The reply comes back sixty seconds later — a terse summary, a table of the four simulation runs her team kicked off over the past two weeks, a callout that two of them had echo-chamber quality above 0.7, a bulleted list of the entities (whales, L2 builders, retail delegators) that showed up across the high-quality runs.

Lena does not know, and has no reason to care, that Claude reached that answer by calling `list_graphs` and `search_graph` against a local MCP server bundled inside an open-source Python project called MiroShark. She stopped opening MiroShark's web UI three weeks ago.

## The Protocol That Replaced the Front Door

The Model Context Protocol crossed 97 million monthly SDK downloads in March 2026, up from two million at launch in November 2024. That's scale React needed three years to reach. Ten thousand active MCP servers now sit between AI assistants and the tools those assistants used to have to be told about. Sixty-seven percent of enterprise AI teams are using or evaluating MCP. Forrester expects 30% of enterprise app vendors to ship their own MCP servers in 2026.

Dry statistics, but they describe a change in how software is *used*, not how software is built. In 2024, an analyst ran a simulator by opening its dashboard. In 2026, she asks her assistant. The question "which tool?" is one the assistant answers by reading its MCP tool catalog. The question "which URL?" no longer comes up. An industry-side description of the shift puts it as "collapsing integration from a multiplication problem to an addition problem." For end-users, the collapse is quieter: the front door of every tool just stopped being a URL.

## The Simulator That Quit Being an App

MiroShark is a multi-agent narrative simulation engine — agents argue about a scenario across rounds, beliefs drift, the system records the drift in a bi-temporal knowledge graph. Its `/explore` page shipped last Thursday. Its social share cards shipped the Wednesday before that. Both were about turning the product into a URL someone could paste into places.

On April 24 its most recent pull request went the other direction. PR #44 shipped an `AI Integration · MCP` panel in the Settings view that surfaces a bundled `backend/mcp_server.py` and writes out a copy-pasteable config for Claude Desktop, Cursor, Windsurf, or Continue — auto-stamped with the user's absolute paths so the snippet pastes and works on first attempt. A health badge tells the user whether Neo4j is reachable before they try. A collapsed drawer lists eight MCP tools: `list_graphs`, `search_graph`, `browse_clusters`, `search_communities`, `get_community`, `list_reports`, `list_report_sections`, `get_reasoning_trace`.

Nothing in that list runs a new simulation. Every tool in it queries the graph of simulations Lena's team has already run. The MCP server is a read surface over months of accumulated research memory — the same memory that previously only existed as files inside her Docker volume and chart rectangles inside her browser.

## What Gets Queried, Not What Gets Clicked

The deeper detail: MiroShark's MCP server runs over stdio. There's no port to open, no daemon to keep alive, no second login. When Lena asks Claude Desktop a question, the client spawns `mcp_server.py` as a subprocess, feeds it JSON-RPC on stdin, reads responses on stdout, and kills the process when the conversation ends. The server inherits the backend's `.env` — same Neo4j credentials, same OpenRouter key — so the graph it reads is exactly the graph the web UI reads.

This sounds like plumbing. Its consequence is that the knowledge graph MiroShark built for itself — the bi-temporal entity store with Leiden-clustered communities, the contradiction detection, the persisted ReACT reasoning traces, all shipped as a direct push on April 21 — is now addressable by any LLM client that can speak MCP. Lena's question about echo-chamber scores reaches `search_graph`. A follow-up like *"zoom out — what are the dominant themes across these runs?"* hits `browse_clusters`. *"Show me the agent's decision chain for why it concluded X"* maps to `get_reasoning_trace`. These are eight specific verbs, each with a one-sentence description, exposed in a catalog any MCP-capable editor reads on startup.

She has never typed the word "Cypher." She has never opened a Neo4j browser. She does not know which tool answered which question. She only knows her assistant can now answer questions about her own research that she could not ask it a week ago.

## Tool Catalogs, Not Websites

The 30% Forrester number is interesting not because it predicts enterprises will ship MCP servers, but because of what it implies about end-users. A SaaS product in 2026 that *only* has a URL is the 2026 equivalent of a 2008 SaaS product that *only* has a desktop installer. The protocol is the new front door. The tool catalog is the new landing page. The chat window is the new dashboard.

MiroShark is a small example, but the shape holds whether the tool is a simulator, a CRM, or a data feed. The product surface collapses into a JSON array of verbs. The work moves from *making the UI navigable* to *making the verbs precise, well-described, and cheap to call.* When Lena asks Claude about her own simulations, the craft she's benefiting from is not the web UI — it's the eight tool descriptions that made the answer legible, and the bi-temporal graph those descriptions point at.

The analyst's workday in 2026 doesn't start by opening apps. It starts by typing. The app she's using is the one her assistant's tool catalog picked for her — the one she could not name if you asked.

---
*Sources: [MCP: The Protocol That Is Quietly Becoming the Infrastructure Layer of Enterprise AI — Braiviq](https://www.braiviq.com/blog/mcp-model-context-protocol-2026-business-strategy-guide); [What is MCP — The 2026 Guide for SaaS PMs — Truto](https://truto.one/blog/what-is-mcp-model-context-protocol-the-2026-guide-for-saas-pms); [Model Context Protocol: A Guide for Enterprise Leaders — Imagine Works](https://imagine-works.com/insights/model-context-protocol-for-enterprise-leaders); [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark); [PR #44 — AI Integration · MCP Onboarding](https://github.com/aaronjmars/MiroShark/pull/44); [MiroShark MCP docs](https://github.com/aaronjmars/MiroShark/blob/main/docs/MCP.md).*
