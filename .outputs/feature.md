*Feature Built — 2026-04-23*

Public Simulation Gallery
MiroShark now has a community gallery. Visit `/explore` and you see every simulation that anyone has published as a visual card grid — the scenario, the final belief split across hundreds of agents, the quality score, the real-world outcome if the run has been resolved. You can open any card to dig into the full simulation, or click "Fork this →" to copy the agent population and run your own variant of the same scenario.

Why this matters:
MiroShark already had every piece of the sharing stack — `is_public` toggle and `POST /publish` (PR #41), the 1200×630 share card that unfurls on Twitter/Discord/Slack (PR #42), a public `/share/<id>` landing page with Open Graph tags. But there was no page listing the published simulations together. Every public run was invisible unless you already had its URL. This was the #1 idea on today's repo-actions article because it turns every "Publish" press into a referral node. At 788 stars with 7 days left on the 1K-by-Apr-30 target (and we need ~30/day to get there), a visitor landing on `/explore` sees real research instead of a blank setup form — meaningfully higher conversion than the current empty homepage.

What was built:
- `backend/app/api/simulation.py`: new `GET /api/simulation/public` endpoint — paginated, `limit`/`offset` query params (clamped 1–100 / ≥0), sorted by `created_at` desc. Reads existing on-disk artifacts (`state.json`, `simulation_config.json`, `quality.json`, `trajectory.json`, `resolution.json`) via a new `_build_gallery_card_payload()` helper to produce card payloads with scenario (truncated to 180 chars), agent count, quality health, belief split, resolution outcome, share-card URL, share-landing URL.
- `frontend/src/views/ExploreView.vue`: new 730-line responsive card grid — share-card PNG thumbnails, quality + dominant-stance pills, belief-split mini-bar, agent/round/date metadata, paired `Open →` and `Fork this →` actions, loading skeleton, error + empty states, Load more pagination. Fork reuses `POST /api/simulation/fork` and routes directly to the new `SimulationRun`.
- `frontend/src/router/index.js`: registers the new `/explore` route.
- `frontend/src/api/simulation.js`: new `getPublicSimulations()` helper.
- `frontend/src/views/Home.vue`: added a compass-icon `◎ Explore` link to the nav bar.
- `frontend/src/components/EmbedDialog.vue`: new "Submit to the public gallery" callout in the Social Card section that flips to "Live on the public gallery" + `Open gallery ↗` the moment the operator toggles Public on.
- `backend/tests/test_unit_public_gallery.py`: 5 offline unit tests over the card helper — minimal dir, fully-populated dir, scenario truncation, empty trajectory, and corrupt-JSON tolerance so one bad sim can't blank the whole gallery.
- `README.md`: Public Gallery row added to the features table.

How it works:
The endpoint sits on the existing simulation blueprint (same prefix as `/list` and `/history`), filters the full simulation list by `is_public=true`, sorts by `created_at desc`, then walks each published sim's directory to build a card payload — so it piggybacks on artifacts the runner already writes and needs zero DB schema changes or new dependencies. One bad artifact is swallowed per-sim rather than per-request, so a single malformed simulation never blanks the gallery. The frontend uses the server-rendered 1200×630 share-card PNG as each card's thumbnail (the same image that unfurls on Twitter/Discord), so the visual identity is consistent across the share card, the landing page, and the gallery.

What's next:
Natural follow-ups: idea #4 from today's repo-actions (search + tags) would let the gallery be filterable by topic, and the `/?fork=:sim_id` URL pattern is still worth adding so gallery cards could deep-link into a pre-filled setup form instead of only the fork-in-place action. For the 1K-star sprint, the next wire to pull is probably #3 (Claude Desktop / MCP onboarding) — makes the graph-memory MCP server visible to the Cursor/Windsurf crowd.

PR: https://github.com/aaronjmars/MiroShark/pull/43
