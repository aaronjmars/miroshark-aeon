*Feature Built — 2026-04-17*

Agent Interaction Network Graph
MiroShark simulations now include a network visualization tab that maps how agents interact with each other. Users can see the social structure of a simulation — who responds to whom, which agents act as information hubs, and where echo chambers form — rendered as an interactive force-directed graph directly in the simulation results view.

Why this matters:
MiroShark already records every agent-to-agent interaction — replies, reposts, likes, follows, cross-platform amplifications — but this data was never visualized as a network. The belief drift chart shows temporal dynamics and the leaderboard shows individual rankings, but neither answers structural questions like "are there two clusters of agents that never interact?" or "which agent bridges the Twitter and Reddit communities?" For social simulation researchers, the interaction network is a standard analytical figure. This fills a gap identified by repo-actions as the #2 highest-impact feature for MiroShark's analytical layer.

What was built:
- backend/app/api/simulation.py: New GET endpoint that reads platform JSONL action logs, extracts pairwise agent-to-agent edges from engagement actions, builds a weighted directed graph with stance data from trajectory.json, computes degree centrality and echo chamber metrics, and caches results in network.json for instant subsequent loads.
- frontend/src/components/InteractionNetwork.vue: 644-line Vue component rendering a force-directed SVG graph. Node color encodes stance (teal=bullish, slate=neutral, coral=bearish), node size scales by total interactions, edge color indicates platform (blue=Twitter, orange=Reddit, purple=cross-platform), edge thickness shows interaction weight. Includes hover highlighting, tooltip with agent details, platform filter checkboxes, insights panel, and PNG export.
- frontend/src/api/simulation.js: New getInteractionNetwork() API function.
- frontend/src/components/Step3Simulation.vue: New "⬡ Network" toggle button in the actions bar alongside Influence and Drift, with mutual-exclusion overlay behavior.

How it works:
The backend reads the same actions.jsonl files used by the influence leaderboard but extracts directed edges instead of per-agent scores — each LIKE_POST, REPOST, QUOTE_POST, CREATE_COMMENT, or FOLLOW creates an edge from the acting agent to the target author. Edges are weighted by interaction count and tagged with platform(s). Graph metrics are computed in pure Python with no external dependencies: degree centrality, a bridge score based on cross-platform edge count, and an echo chamber score measuring the ratio of same-platform to total edges. The frontend implements a 200-iteration force simulation entirely in JavaScript — repulsion between all nodes, attraction along edges, gravity toward center — producing a clean layout without any graph library dependency. Hover-based highlighting dims non-neighbors to 15% opacity, making local structure instantly visible.

What's next:
Could extend with community detection (Louvain clustering), edge bundling for dense graphs, or time-slider filtering to show how the network evolves across rounds.

PR: https://github.com/aaronjmars/MiroShark/pull/33
