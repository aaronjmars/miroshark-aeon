*Repo Action Ideas — 2026-05-20*
5 ideas for aaronjmars/MiroShark — all net-new, all autonomously buildable, all zero new deps.

1. Status Badge SVG (Growth, Small)
   Shields.io-compatible `badge.svg` endpoint — operators embed a live Bullish/Neutral/Bearish badge in any GitHub README or Notion page.

2. BibTeX Academic Citation (DX, Small)
   `cite.bib` closes the citation arc after reproduce.json + DKG: paste into LaTeX, import URL into Zotero, annote includes the DKG Asset URI when anchored.

3. Belief Volatility Score (Analytics, Small)
   Mean/max/std of round-over-round stance deltas + Monotonic/Noisy/Oscillating regime — the risk metric that pairs with signal.json's confidence.

4. Webhook Test Ping (DX, Small)
   `POST /api/config/webhook/test` fires a signed test payload and returns status + latency in 2s — no full sim run needed to verify webhook config.

5. Gallery Public JSON (Integration, Small)
   `GET /api/gallery.json` — machine-readable index of all public sims with ETag polling, for scripts/agents/bots that can't scrape HTML.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-20.md
