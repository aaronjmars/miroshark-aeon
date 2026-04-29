*Repo Action Ideas — 2026-04-28*
Generated from analysis of aaronjmars/MiroShark (854 stars · 162 forks · 0 open PRs). PRs #51 Langfuse trace metadata + #52 tool retry loop fix (30-40% cost reduction) both merged today — Langfuse wiring is done, cost data is in traces but invisible in product. Five net-new ideas:

1. Langfuse Cost Breakdown Panel (Feature, Small)
   Expose per-sim cost in the UI — setup/rounds/research breakdown from Langfuse traces. Makes the "$1 & under 10 min" tagline verifiable inside the app.

2. Simulation Transcript Export (Feature, Small)
   GET /api/simulation/:id/transcript.md — round-by-round agent dialogue, downloadable from EmbedDialog. PR #52 cleaned the conversation history; the text is now readable. Research-quotable companion to the GIF.

3. RSS Feed for Public Gallery (Integration, Small)
   GET /api/feed.rss serving the 20 most recent public sims as Atom 1.0. Zero new deps (stdlib xml). Researchers subscribe in Feedly/Readwise the same way they follow newsletters.

4. Scenario Template Library (DX, Small)
   Static JSON of 12-15 curated templates (DeFi vulnerability, token launch, governance vote, regulatory action) accessible from a "Browse templates" picker on the new-sim form. Eliminates the blank textarea conversion barrier.

5. Comparative Run View (Feature, Medium)
   /compare?a=$id&b=$id — side-by-side belief charts, consensus delta pills, quality comparison. Makes fork-then-change-preset a first-class research workflow with a shareable URL format.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-04-28.md
