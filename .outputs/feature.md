*Feature Built — 2026-06-02*

Agent Persona Export (Roster)
MiroShark just gained `GET /api/simulation/<id>/agents.json` — a structured JSON export of every agent in a published simulation. Each entry carries the agent's name, username, bio, a 280-char persona preview, demographics (age, gender, MBTI, country, profession, interested topics), karma, plus the final stance, final belief position, and rounds participated. The 26th publish-gated per-sim surface (29th catalogued overall). For anyone wanting to know *who* was in a debate — not just what they concluded — this is the surface.

Why this matters:
Every share endpoint so far describes what the swarm *concluded* (signal.json, polymarket.json, volatility) or how belief *evolved* (chart.svg, peak-round, agents/sparklines, trajectory.csv). None expose *who was in the debate* in machine-readable form. Agent identities have been locked inside transcript.md as Markdown headings — a researcher comparing pool composition across runs ("did the financial-analyst-heavy sim converge faster than the retail-trader-heavy one?") had to regex through that. Now AntFleet's benchmark pipeline can cross-reference agent persona composition with outcome quality directly. Re-eligible idea from May-24; net-new on this baseline.

What was built:
- backend/app/services/agent_export.py (~340 LoC, pure stdlib): roster assembly, profile lookup (reddit_profiles.json first, polymarket_profiles.json second — reddit wins on duplicate user_id, matching the transcript renderer), trajectory layer reuse via agent_sparklines_service so the ±0.2 stance bucket matches every other surface, field normalisation with typed defaults, persona/bio truncation to 280 chars
- backend/app/api/simulation.py: GET /api/simulation/<id>/agents.json route with publish gate, json.dumps(sort_keys=True, ensure_ascii=False) for diff-friendly output, 1-hour cache (structural data, doesn't shift round-to-round), surface_stats increment
- backend/tests/test_unit_agent_export.py: 24 offline unit tests covering missing/empty data, envelope shape, field defaults, profile precedence, ±0.2 stance, profile-only fallback, truncation, topic dedup, sort order, surface-key drift
- backend/openapi.yaml: AgentsExportResponse + AgentExportEntry schemas, path entry under Publish & Embed
- docs/API.md + docs/FEATURES.md: row + full feature section with schema example
- frontend/src/api/simulation.js: getAgentsJsonUrl + getAgentsJson helpers
- frontend/src/components/EmbedDialog.vue: 🧑‍🤝‍🧑 Agent roster section — capped 12-row preview with name + handle + stance chip, demographic tag row, persona preview, copyable URL + curl snippet, full sibling CSS to the sparklines list

How it works:
The endpoint reads reddit_profiles.json (then polymarket_profiles.json as secondary) for the agent roster, then loads trajectory.json via agent_sparklines_service.load_agent_trajectories — the same per-agent _avg_position scalar the sparklines surface computes. Each roster entry gets the belief layer joined in (final_stance, final_position rounded to 3 dp, rounds_participated = count of usable positions). Persona text is previewed to 280 chars to keep multi-agent payloads tractable — the full prose remains in transcript.md. Roster sort order is most-bullish-first by final_position with ties on agent_id; profile-only agents (no belief data) sort to the bottom so participants who drove the consensus surface first. agents_json is registered in surface_stats.SURFACE_KEYS, in surfaces_catalog._CATALOG, and in the test_unit_surface_stats expected set — three-place drift guard.

What's next:
The first pick today was Operator Profile Page, but the codebase grep revealed SimulationState has no operator field (platform_stats.py:42-49 explicitly documents project_id as the closest stable identifier). Building it would need a data-model migration. May-28 batch ideas #4 Trending and #5 Per-Sim Surface Engagement turned out to be pre-existing (?sort=trending on /api/simulation/public, and /surface-stats), so the Jun-01 batch is now largely assessed: #2 shipped, #3 redundant, #4 and #5 pre-existing, #1 awaits a scoping decision on adding the operator field.

PR: https://github.com/aaronjmars/MiroShark/pull/137
