*Thread Draft — 2026-06-05*
Topic: Platform Status Probe — /api/status.json (PR #149)

1/ PR #149 ships GET /api/status.json — a status probe for MiroShark. The PR took three commits because the first implementation inherited auth from its neighbors. A status probe behind authentication is useless for the tools that actually read it.

2/ MiroShark's platform-surface family had two legs: /api/stats for aggregate corpus shape and /api/surfaces.json for the capability catalog. Neither is designed for uptime monitors — they return large envelopes and are not the probe format status-page tools poll.

3/ The envelope is minimal: ok: true (a literal, not derived), queue_depth (running sims, case-insensitive), completed_24h (uses updated_at not created_at), surface_count sourced from surfaces_catalog. 30-second HTTP cache is the only smoothing. 28 offline tests.

4/ /api/stats answers corpus shape. /api/surfaces.json answers capability. /api/status.json answers health. The third leg completes the set a status page, a new integrator, and an uptime monitor each need to hit first. All three are public — none require credentials.

5/ PR #149 — 12 files, +1,120 lines, 28 offline tests, 40th consecutive zero-dependency PR. https://github.com/aaronjmars/MiroShark/pull/149

(article: articles/thread-2026-06-05.md)
