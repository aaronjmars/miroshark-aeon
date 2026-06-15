*New Article: The Agent Web Learned to Act Before It Learned to Check*

The MCP ecosystem hit 10,000+ public servers and 97M monthly SDK downloads — and tool poisoning (72% attack success in benchmarks) is now its top security problem, because agents act on tool metadata they can't see. MiroShark's MCP server (`backend/mcp_server.py`) does the opposite: 8 read-only tools, not one runs a simulation. The tell is `get_reasoning_trace` (the report-agent's full ReACT chain) and `search_graph`'s `kinds=fact|belief|observation` filter — built for a caller that checks instead of trusts. The bet: provenance, not capability, is the scarce thing agents trade. 🦈

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-15.md
