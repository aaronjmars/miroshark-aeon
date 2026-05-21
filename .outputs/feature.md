*Feature Built — 2026-05-21*

Consensus Status Badge SVG
MiroShark sims now have a Shields.io-compatible status badge. Any researcher, operator, or token holder can drop one line of Markdown into a GitHub README, Notion page, Substack post, or personal site and the page renders a live 20-pixel badge showing the current consensus (e.g. "Bullish 72%"). The badge updates as the underlying simulation runs — paste it once and the embed never goes stale.

Why this matters:
The previous 12 share surfaces (chart SVG, replay GIF, trajectory CSV, notebook, signal.json, archive.zip, Farcaster Frame, …) all describe a sim in increasing depth — but every one waits for a reader to navigate to the share page. The badge inverts the funnel direction. Every embedding README becomes a pull point: a reader skimming a researcher's repo sees the live consensus, recognises the colour vocabulary from any other MiroShark surface, and clicks through. This was #1 in the May-20 repo-actions batch and the cheapest visible pointer back the surface stack still lacked.

What was built:
- backend/app/services/badge_service.py (new): pure stdlib xml.etree.ElementTree renderer (~330 LoC). Flat Shields.io layout — left half `MiroShark` on `#555555`, right half `{direction} {confidence_pct}%` on stance colour (`#22c55e` Bullish / `#6b7280` Neutral / `#ef4444` Bearish). Pill ends via clipPath rx=3; bytewise-deterministic output; defensive on unknown direction (neutral grey + `Unknown` label) and clamping on out-of-range confidence.
- backend/app/api/simulation.py: new GET /<id>/badge.svg route. Same publish gate as every other share surface; 404 when no `belief.final` yet so an embedded <img> renders a broken-image placeholder rather than a misleading `Unknown 0%`. `Cache-Control: public, max-age=60` so live-sim stance flips propagate within one polling cycle.
- backend/tests/test_unit_badge_service.py (new): 22 offline unit tests covering well-formed SVG + namespace, aria-label contents, all three stance colours + case variants, integer-rounded confidence display, unknown / None / empty fallbacks, clamping (negative / >100 / non-numeric), route + mimetype + cache header, surface_stats registration + counter increment, bytewise determinism, rounded pill corners, and a viewBox-matches-width-height invariant.
- frontend/src/components/EmbedDialog.vue + api/simulation.js: new 🏷️ Status badge section with in-place live preview plus Copy URL / Copy Markdown / Copy HTML snippet buttons. Same template + i18n conventions as the surrounding sections.
- backend/openapi.yaml + docs/API.md + docs/FEATURES.md: documents the endpoint, adds `badge_svg` to the SimulationSurfaceStats schema, and explains the distribution-amplifier framing.

How it works:
The handler resolves the simulation's embed-summary payload, runs it through the existing `compute_signal` pipeline to derive direction + confidence_pct (same numbers signal.json returns), and passes the pair to `build_badge_svg(direction, confidence_pct)`. The SVG is assembled element-by-element with xml.etree.ElementTree — clipPath with rx=3 for the pill ends, one rect per half with the stance colour on the right, two `<text>` elements centred inside each section, and a `<title>` + `role="img"` + `aria-label` block for accessibility. The colour vocabulary is pinned to the same `#22c55e` / `#6b7280` / `#ef4444` triplet every other belief surface uses, so a reader who saw the chart in the same README recognises the badge immediately. Bytewise determinism is preserved (deterministic element order + `short_empty_elements=True`), so a future ETag layer can hash the body directly.

What's next:
The remaining four May-20 ideas — BibTeX Academic Citation, Belief Volatility Score, Webhook Test Ping, Gallery Public JSON — are still unbuilt. The badge surface also opens the door to `badge.json` (machine-readable status equivalent for tools that don't render SVG), a `?style=for-the-badge` parameter to ship a taller Shields.io variant, and a Discord-flavoured embed thumbnail variant that pairs with PR #83's rich notifications.

PR: https://github.com/aaronjmars/MiroShark/pull/94
