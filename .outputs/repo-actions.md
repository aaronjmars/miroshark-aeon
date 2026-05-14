*Repo Action Ideas — 2026-05-14*
Generated from analysis of aaronjmars/MiroShark (1,147 stars · 227 forks · 0 open PRs) — ideas buildable by the feature skill tomorrow.

1. Discord + Slack Rich Completion Notifications (Integration, Small)
   Two env vars trigger platform-native sim-completion messages in Discord (rich embed, consensus-color-coded) and Slack (Block Kit with belief bars) — gives RevaultDrops a live MiroShark channel without writing integration code.

2. Director Event Timeline (Feature/Research, Small)
   `GET /api/simulation/<id>/director-events` + amber annotation layer on the belief chart shows exactly which round director injections fired and what they triggered — the citation surface director mode has always needed.

3. Shareable Belief Chart SVG (Feature/DX, Small)
   `GET /api/simulation/<id>/chart.svg` generates the full belief trajectory as a pure-stdlib SVG via `xml.etree.ElementTree` — embeddable as `<img>` in Notion, Substack, GitHub READMEs, and LaTeX papers with zero deps.

4. Comparative Run View (Feature/Research, Small)
   `/compare?a=<id>&b=<id>` renders two published sims side-by-side with a Δ column showing signed stance deltas — the analytic complement to the lineage navigator (PR #76), zero new backend code.

5. Private Share Link (Feature/Security, Small)
   HMAC-signed time-limited token grants full share-page access to an unpublished sim — gives institutional observers (Lorimer Ventures tier) a pre-publication preview window using the same hmac+hashlib.sha256 pair as PR #79.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-14.md
