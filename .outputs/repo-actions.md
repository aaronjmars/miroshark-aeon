*Repo Action Ideas — 2026-05-04*
Generated from analysis of the current project — these are ideas that could be autonomously built by the feature skill tomorrow.

1. Embeddable Live Belief Widget (Feature, Small)
   `/embed/<id>` iFrame endpoint — a compact live belief-bar widget for Substack, Notion, and Discord. Follows the watch-page poller pattern; EmbedDialog gains a copy-ready `<iframe>` snippet. Closes the embed-vs-link gap the share card leaves open.

2. Webhook Delivery Log (DX, Small)
   Append `webhook-log.jsonl` in `sim_dir/` on each dispatch attempt (timestamp, masked URL, status code, latency); `GET /api/simulation/:id/webhook-log` + EmbedDialog delivery chips + a Retry button. Closes the did
