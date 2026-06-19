*Feature Built — 2026-06-19 — aaronjmars/MiroShark* 🦈

Cost on the embed widget
Every public MiroShark embed now shows what the run actually cost — a little `~$0.87` pill right next to the status and agent count. Share a sim in a tweet or a blog and the dollar figure rides along. The "$1" claim stops being a tagline and becomes a number you can read.

Why this matters:
"simulate anything for ~$1" is the whole pitch, and until now nothing in the UI ever showed it. PR #179 already built the proof — a queryable cost.json with an honest lower-bound figure — but it had zero reach: you had to curl it. The embed is where a stranger first meets a MiroShark result, so that's where the price belongs. Repo-actions flagged this 06-18 (#4); the move was routing it to the surface where the publish gate actually lets it through.

What was built:
- frontend/src/api/simulation.js: new getSimulationCost() — fetches the cost.json share-surface blob, mirrors getReproduction, rejects cleanly on 403/404 so callers treat it as "nothing to show".
- frontend/src/views/EmbedView.vue: fetches cost after the summary loads, only for completed runs, in its own try/catch so a $0 or unpublished run never breaks the widget. costLabel renders `~$X.XX`, collapses sub-cent runs to `<$0.01`, drops the pill when there's nothing. New embed-pill cost in the meta row with an EN/中文 tooltip.

How it works:
The embed already pulled getEmbedSummary; cost is bolted on as a non-blocking extra. No backend touched — the figure stays single-sourced through cost_service → run_summary, so the embed and run_summary.md can never disagree. The pill reuses the existing pill styling (purple accent, tabular nums), so it looks native in light/dark and the compact preset. Validated with a clean `npm run build`; repo CI rebuilds the frontend on push.

What's next:
Same pattern fits the in-app result view once the publish gate is solved there, and the gallery cards are the obvious follow-on. Note: the DE-locale top pick was already taken by dan-and's open PR #189 — built this instead.

PR: https://github.com/aaronjmars/MiroShark/pull/190
