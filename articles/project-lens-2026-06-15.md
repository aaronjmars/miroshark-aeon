# The Agent Web Learned to Act Before It Learned to Check

A year ago, connecting an AI model to an outside tool was a weekend hack. Now it's an ecosystem. The Model Context Protocol — the standard that lets an agent call a tool the way a browser calls an API — has gone from one vendor's idea to the connective tissue of the field. By Anthropic's December 2025 count there were [10,000+ active public MCP servers and 97 million monthly SDK downloads](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol); the official registry listed 9,652 server records as of May 24, 2026. ChatGPT, Gemini, Cursor, Microsoft Copilot, and VS Code all speak it now.

Almost every one of those servers does the same thing: it lets an agent *act*. Send the email. File the ticket. Run the query. Move the money. The race is to hand models more verbs.

## The verbs are the vulnerability

The trouble with a tool that acts is that the agent has to trust it before it can use it — and the thing it trusts is text it reads but you never see.

That gap is now the headline security problem in the field. It's called tool poisoning: an attacker hides instructions inside a tool's description or its returned output, the agent reads that metadata as a legitimate instruction, and acts on it. As one 2026 enterprise security writeup puts it, ["the user sees nothing unusual. They asked the agent to send an email; the agent sent an email. They never see the tool description."](https://itecsonline.com/post/mcp-tool-poisoning-enterprise-ai-agent-security-2026) The MCPTox benchmark recorded attack success rates as high as 72%. Roughly 200,000 MCP instances were found exposed by a May 2026 disclosure. A [recent threat-modeling paper](https://arxiv.org/abs/2603.22489) catalogs the pattern across major clients and finds most of them defend against it poorly.

The deeper point is structural. The danger isn't any single verb. It's the combination — once an agent can read untrusted content, touch sensitive data, and reach the outside world in one session, a poisoned tool description becomes a privilege-escalation vector. The ecosystem optimized for capability and is now paying for it.

So here's a question worth asking of any tool an agent can call: what does it let the agent *do* — and what does it let the agent *check*?

## A server that exposes no verbs

There's an open-source engine whose pitch is "simulate anything, for $1 and less than 10 minutes" — hundreds of language-model agents, seeded from real demographics, that argue and trade until their aggregate belief settles into a number and a report. It ships its own MCP server (`backend/mcp_server.py`) so any MCP-aware client can plug in. You'd expect the obvious move: expose a `run_simulation` tool, let foreign agents fire off sims on demand. More verbs.

It doesn't. The server exposes eight tools, and not one of them runs anything. `list_graphs`, `search_graph`, `browse_clusters`, `get_community`, `list_reports`, `list_report_sections`, `get_reasoning_trace`. Every one is a read. The MCP surface is deliberately query-only — a way to *interrogate* a simulation that already happened, not to trigger a new one.

That's a strange choice in a gold rush built on action, and it's not an accident. The same repo spent the last two weeks shipping nothing but provenance plumbing: an HMAC-signed result payload you can verify offline (`signed_result.py`), a platform-wide outcome-distribution endpoint, a polling feed of what just completed. The MCP server is the same bet wearing a different hat. When another agent reaches into this system, the thing it gets handed is not the power to act. It's the evidence to judge.

## The tool that hands over the agent's own doubts

The tell is `get_reasoning_trace`. Point it at a report section and it returns the report-agent's full ReACT decision chain — its thoughts, the tools it called, what it observed, and the conclusion it drew. A foreign agent doesn't just get the answer; it gets the work behind it, step by step, and can decide whether the chain holds.

`search_graph` goes further in a way that matters more than it looks. It supports time-travel (`as_of`, query the graph as it stood at a past moment) and — the real move — epistemic filtering: `kinds=fact|belief|observation`. The graph tags whether a node is a grounded fact, a thing an agent merely *believed*, or something it *observed*. A querying agent can ask for only the facts, or specifically inspect the beliefs. That line — between what the swarm believed and what was actually established — is exactly what a synthetic simulation must not blur; most tools collapse it into one confident output.

Set that against tool poisoning. The whole attack depends on an agent treating tool-supplied text as trustworthy instruction. A surface that exposes only reads, returns its own reasoning trace, and labels belief separately from fact is built for an agent that *doesn't* extend that trust by default — one that pulls the evidence and checks it. The design assumes the caller is skeptical. In 2026, that assumption is the security feature.

## What the next ten thousand servers get wrong

A claim specific enough to be wrong on a schedule: by the time the registry passes its next order of magnitude — call it 100,000 servers — the ones that survive real agent-to-agent traffic won't be the ones with the most verbs. They'll be the ones that let a calling agent verify what they return. Read-only surfaces, signed payloads, reasoning traces, fact-versus-belief labels: the boring provenance layer the action gold rush skipped.

Gartner expects [40% of enterprise applications to embed task-specific agents by the end of 2026](https://itecsonline.com/post/mcp-tool-poisoning-enterprise-ai-agent-security-2026), up from under 5% a year earlier. Every one will call tools it cannot see the insides of. The engines that win that world are the ones that stopped asking "what else can I let an agent do" and started asking "what do I have to prove before an agent should believe me." One simulation engine answered that question with a server that has no verbs at all. The rest of the registry hasn't read it yet.

---
*Sources:*
- [MCP Adoption Statistics 2026 — Digital Applied](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol) — 10,000+ public servers and 97M monthly SDK downloads (Anthropic, Dec 2025); 9,652 registry records and 86,148 stars as of May 24, 2026; provider adoption list
- [MCP Tool Poisoning: Enterprise AI Agent Security in 2026 — ITECS](https://itecsonline.com/post/mcp-tool-poisoning-enterprise-ai-agent-security-2026) — tool poisoning mechanism, the "they never see the tool description" asymmetry, 72% MCPTox success rate, ~200,000 exposed instances (May 2026), the lethal-trifecta framing, Gartner 40% enterprise-agent projection
- [Model Context Protocol Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning — arXiv 2603.22489](https://arxiv.org/abs/2603.22489) — threat model of tool poisoning across MCP clients and their weak defenses
- [MiroShark repository](https://github.com/aaronjmars/MiroShark) — `backend/mcp_server.py` exposes 8 read-only tools (none run a simulation); `get_reasoning_trace` returns the report-agent's ReACT chain; `search_graph` supports `as_of` time-travel and `kinds=fact|belief|observation` epistemic filtering; `signed_result.py` HMAC payload
