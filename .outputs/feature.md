*Feature Built — 2026-04-18*

Embeddable Simulation Widget
MiroShark simulations can now be dropped into Notion, Substack, Medium, or a GitHub README as a live iframe that shows the scenario, belief drift chart, round/agent counts, quality badge, and consensus outcome — not a link, actual rendered content. From any completed simulation in the history panel you now get an Embed dialog that hands you an iframe snippet, a Markdown auto-embed link, and a raw URL, all copy-to-clipboard, with three size presets and a light/dark toggle.

Why this matters:
MiroShark's share permalink is the distribution mechanism today — but links require a click and every completed simulation has stayed a private click-through. Researchers writing up results in Notion or Substack want the belief drift and market outcome rendered inline. This was idea #4 from the Apr 16 repo-actions batch (Playback, Network Graph, Quality Diagnostics already shipped in PRs #32/#33; Multi-Document Mode deferred to its own PR). It turns 138+ forks and every public deploy into a distribution network — each embed renders with a 'Powered by MiroShark' link back to the run.

What was built:
- backend/app/api/simulation.py: new GET /<sim_id>/embed-summary endpoint that packs scenario, round/agent counts, final stance %, per-round stacked drift series, consensus round/stance, cached quality health, and cached resolution into a single cacheable JSON response — one request powers the whole widget.
- frontend/src/views/EmbedView.vue: 404-line iframe-safe page — scenario header, status/round/agent/quality pills, stacked-area SVG belief drift sparkline with a dashed consensus-round marker, bullish/neutral/bearish final-round chips, correct/wrong/split resolution badge, Powered-by-MiroShark footer. Supports ?theme=dark and ?chart_only=true and forces transparent html/body so it renders cleanly inside any host page.
- frontend/src/components/EmbedDialog.vue: history-modal dialog with live iframe preview, Compact (480x260) / Standard (640x340) / Wide (800x420) size presets, light/dark theme selector, and three copy snippets (iframe HTML, Markdown link, raw URL) with a document.execCommand fallback when the Clipboard API isn't available.
- frontend/src/components/HistoryDatabase.vue: new Embed section in the simulation detail modal with a trigger button and scoped styles wired to the selected simulation id.
- frontend/src/router/index.js + api/simulation.js: /embed/:simulationId route and getEmbedSummary(id) helper.

How it works:
The widget is a pure client-side Vue route — no new infrastructure, no share tokens, just the existing simulation id. On mount it calls /embed-summary, which reads trajectory.json (for the stacked drift series and consensus point), quality.json (for the health badge), and resolution.json (for the outcome chip) straight from the simulation directory — same files the history modal already consumes, so no new storage. The SVG chart draws three stacked areas (bearish on the bottom, neutral middle, bullish top) from the returned per-round series and renders a dashed vertical line at the first >50% consensus round. The dialog generates iframe snippets from window.location.origin so embeds point back to whatever MiroShark instance the user is on. Cache-Control: public, max-age=60 on the summary endpoint absorbs repeated loads from high-traffic host pages.

What's next:
Natural follow-ups are an oEmbed discovery endpoint (auto-embed in Notion/Ghost/Substack when the user just pastes the simulation URL) and embed-view analytics (log referer per load so instance owners can see which blog posts and READMEs are embedding their simulations). Idea #3 from the same batch — Multi-Document Comparative Mode (same agent pool, Doc A vs Doc B) — is the remaining Apr 16 candidate and a solid next feature target.

PR: https://github.com/aaronjmars/MiroShark/pull/34
