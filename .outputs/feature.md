*Feature Built — 2026-04-22*

Social Share Card
MiroShark simulations now have a polished 1200×630 PNG that auto-unfurls when you paste a share link into Twitter/X, Discord, Slack, or LinkedIn. Instead of a flat URL preview, the post renders a card showing the scenario headline, status, quality badge, agent count, round count, and the final bullish/neutral/bearish belief split as a stacked bar — so a researcher sharing "the Director Mode run that called the Kelp/Aave cascade" now ships a visual story with the link, not just text.

Why this matters:
MiroShark's existing share permalinks always rendered as a generic page preview — no hook, no image, no reason for someone scrolling Twitter to click. With organic mentions accelerating around the Director Mode + Kelp/Aave coincidence and the repo at 767 stars chasing 1K by Apr 30 (~30/day needed), every shared simulation is a distribution channel, and a card-bearing share converts orders of magnitude better than a text URL. This was idea #2 in repo-actions Apr 20 and the highest-leverage growth lever still on the board.

What was built:
- backend/app/services/share_card.py: New 501-line Pillow renderer. Builds the card from the same data the embed-summary endpoint exposes — scenario, status, agent + round counts, belief final split, quality health, resolution accuracy. Deterministic output (same input dict → byte-identical PNG) so disk caching is trivial. Falls back through DejaVu / Helvetica / Arial / PIL bitmap default — never 500s on a missing font.
- GET /api/simulation/<id>/share-card.png: New endpoint, same is_public gate as embed-summary, on-disk cache at <sim_dir>/share-cards/<sha256-16>.png keyed by render-affecting fields, Cache-Control: public, max-age=3600. Repeat unfurler hits don't re-render.
- backend/app/api/share.py + share_bp: New 181-line module. GET /share/<id> serves an HTML page with og:image / og:title / twitter:card=summary_large_image / twitter:image meta tags. Bots scrape the tags; real browsers JS-redirect to the SPA simulation view (with <meta http-equiv="refresh"> as a JS-off fallback). Honors X-Forwarded-Proto / X-Forwarded-Host so URLs work behind Railway / Render / nginx. Mounted at root, no /api/ prefix, so the URL stays clean.
- frontend EmbedDialog.vue: Extended with a "Social card" section — live preview img, copyable share link, copyable card-image URL, download PNG button. Cache-busts the preview when the public toggle flips so the image reloads instead of staying broken. New getShareCardUrl() / getShareLandingUrl() helpers in api/simulation.js.
- backend/tests/test_unit_share_card.py: 11 new unit tests — PNG signature + IHDR size validation, cache-key stability + sensitivity, edge-case scenarios (empty / 600-char / single-word that overflows / failed status / minimal payload), OG meta-tag rendering with quote escaping, private-sim leak check.

How it works:
The PNG is rendered with Pillow (already pinned ≥12.0 via tool.uv.override-dependencies, so zero new dependencies). The renderer takes a summary dict, lays out a dark header band with the MiroShark wordmark + sim ID badge, the scenario headline with auto-shrink + 3-line wrap + ellipsis, a row of color-coded pills (status, quality, resolution, consensus round), three metric columns, a stacked bullish/neutral/bearish bar with legend, and a dark footer with the repo URL + creation date. The /share/<id> landing route is a separate Flask blueprint — bots see the OG tags and stop; humans hit window.location.replace() in the first inline script and never see the splash. The embed-summary data-loading code was extracted into _build_embed_summary_payload() so the embed widget and the share card share one source of truth and can never drift apart.

What's next:
Pivot for tomorrow: ideas #4 (Collaborative Review Comments) and #5 (Config Export/Import) from repo-actions Apr 20 are still on the board. The share landing URL also opens up future SEO work — a static og:type=article variant could let Google index simulation results.

PR: https://github.com/aaronjmars/MiroShark/pull/42
