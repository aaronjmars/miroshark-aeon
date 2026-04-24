*Feature Built — 2026-04-24 (2/2)*

What was built:
- backend/app/api/mcp.py: New GET /api/mcp/status endpoint returning the 8-tool catalog, resolved absolute paths (backend_dir, mcp_script, python_executable), pre-rendered config snippets for every supported client, and a Neo4j liveness probe (graph + entity count). The probe never raises — the panel renders guidance even when Neo4j is down.
- frontend/src/components/SettingsPanel.vue: New AI Integration · MCP section with a health badge (Ready / Neo4j down / Server file missing), a summary grid, tabbed client picker (Claude Desktop / Cursor / Windsurf / Continue / fallback-direct), a dark code block + copy-snippet button (with execCommand fallback for non-secure-context browsers), per-client config-file path hints, a collapsed tool catalog, and a docs link.
- docs/MCP.md: Expanded from Claude-Desktop-only to cover all four MCP clients with config snippets, a verification checklist, and a 5-row troubleshooting matrix.
- backend/tests/test_unit_mcp_api.py: 9 offline unit tests including a regex-based tool-catalog drift detector that scans mcp_server.py and fails CI if the API tool list goes stale.

How it works:
The endpoint resolves its own on-disk location with Path(__file__).resolve().parent.parent.parent so the snippets it returns reference the user's actual backend/ directory and the same Python interpreter currently serving the API — paste-and-go, no manual editing. The MCP server itself runs over stdio (no port to open, no daemon) and is launched by the MCP client on demand, inheriting the backend's .env for Neo4j + LLM credentials. The frontend uses the modern Clipboard API with a textarea+execCommand fallback for HTTP/older browsers. The Continue snippet uses experimental.modelContextProtocolServers (a different shape than mcpServers) so Continue users don't end up with an empty tool list.

What's next:
History Search & Tags (#4 from repo-actions Apr 22) is the next unbuilt candidate — power-user organization for the simulation library, with tags also bridging to the public gallery as a clickable filter taxonomy.

PR: https://github.com/aaronjmars/MiroShark/pull/44
