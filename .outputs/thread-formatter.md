*Thread Draft — 2026-06-09*
Topic: Simulation Activity Feed — GET /api/activity.json (PR #153)

1/ Three keyless endpoints. Three polling questions. /api/status.json: is the platform running? /api/simulation/batch-status: what's the state of these sims? /api/activity.json, merged today as PR #153: what just completed? The polling loop is now fully wired.

2/ Before today, a keyless polling loop could confirm the platform was running (/api/status.json) and check a batch of known sim IDs (/api/simulation/batch-status). There was no endpoint to ask what had completed recently. Discovery required auth.

3/ GET /api/activity.json returns the most-recent public completed sims, reverse-chronological (?limit= clamped 1–50, default 20). direction/confidence_pct/quality_health match signal.json byte-for-byte — same compute path. 30s public cache, ETag short-circuit.

4/ Capacitr, AntFleet, and Aeon's push-recap skills are named in the PR as consumers. Each runs a polling loop against MiroShark surfaces. Now all three have an endpoint to ask what completed — without knowing sim IDs in advance, without authenticating.

5/ 35th catalogued surface, 43rd consecutive zero-dependency PR. The third discovery surface — alongside feed_atom and feed_rss — but the first shaped for machine polling, not subscription readers. https://github.com/aaronjmars/MiroShark/pull/153

(article: articles/thread-2026-06-09.md)
