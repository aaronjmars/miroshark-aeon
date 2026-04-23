# Your OG Image Is Now Your UI

When Facebook published the Open Graph protocol in 2010, the social share card was a concession. A 1200×630 PNG tucked into a `<meta>` tag so that when someone pasted a link into Messenger, the platform would unfurl it into a little preview rectangle instead of a blue string. It wasn't architecture. It was compliance with a social network's display rules. The image was an afterthought most teams generated once in Photoshop and forgot about.

In October 2022, Vercel shipped `@vercel/og`, which let developers render these PNGs on demand from JSX at the edge — "5x faster" than the Chromium + Puppeteer approach it replaced, "160x cheaper," and "100x more lightweight" at 500KB versus 50MB. Within two years, OG image generation became a commodity: Bannerbear, Placid, Cloudinary, Imejis, Orshot, Abyssale all selling template-based PNG-rendering APIs, mostly to marketing teams who wanted a fresh unfurl per product page. The sales pitch was: automate your social previews, don't hand-paint them.

What happened next was less advertised. Once every page in an app had a PNG renderer attached to it, engineers realized the PNG was good for more than Twitter. It was the cheapest, most portable summary of the thing on the page — branding, title, status pill, chart, anything you chose to bake in. And the rendering pipeline already existed. So it started appearing in places the OG spec never intended: gallery thumbnails, email digests, dashboard cards, public feeds, embed previews. The social share card quit being metadata and got promoted to primary UI.

## The Pull-Forward Shipping Pattern

A concrete instance of this showed up today in MiroShark, an open-source multi-agent simulation engine that crossed 789 GitHub stars this morning. Yesterday — April 22 — the team merged PR #42, a share card endpoint: `GET /api/simulation/<id>/share-card.png` returns a 1200×630 PNG rendered with Pillow, with a dark header band, scenario headline, status and quality pills, and a stacked belief bar. It's cached on disk at `<sim_dir>/share-cards/<sha256-16>.png` with `Cache-Control: public, max-age=3600`. A companion `GET /share/<id>` HTML endpoint emits `og:image` and `twitter:card=summary_large_image` meta tags so that pasting a simulation link into any social client triggers the unfurl correctly. A standard, boring, 2026 implementation of a social card.

Twenty-four hours later — April 23, 13:38 UTC — the same team merged PR #43: a public simulation gallery at `/explore`. A responsive Vue card grid, 1,536 lines added, zero new dependencies, zero schema change. Here is the detail that earns this article: the gallery card thumbnail is the PR #42 PNG. `ExploreView.vue` references each card's `share-card.png` URL. The cache already exists. The layout is already opinionated. The thing a gallery really needs — a visually compact, information-dense preview of what's inside — was rendered yesterday for a different reason and is ready to be consumed today.

## One PNG, Three Surfaces

The share card in MiroShark is now consumed by three places in the product, each for different reasons, all pointing at the same bytes:

1. **Social unfurl** — emitted in `<meta property="og:image">` on `/share/<id>`. This is the original job the OG spec was written for.
2. **Embed preview** — the existing `EmbedDialog.vue` widget renders it under a "Social card" section, with a copyable share link and a download PNG button.
3. **Public gallery thumbnail** — every card in `ExploreView.vue` shows it above the quality pills, belief-split mini-bar, and `Open →` / `Fork this →` actions.

Three products, one renderer, one cache key (`sha256-16` of the input payload). Adding a fourth surface — a future email digest, a printable run summary, a Telegram preview — is a reference, not a project. This is the hidden reason PR #43 could ship in a day: the visual identity, the layout engine, and the caching story had been solved yesterday for what looked like a minor feature.

## What Gets Easier When the Image Is Infrastructure

When a team treats dynamic images as a one-off marketing chore, every new surface pays for its own design, its own rendering pipeline, and its own consistency problem. When a team treats the OG image as a primary component — versioned in code, rendered at the edge or via Pillow on the origin, cached by content hash — every new surface that needs a preview becomes two lines. Branding stays in sync automatically because there is only one renderer. The gallery unfurl on Twitter and the gallery card on `/explore` are literally the same pixels.

This is the deeper meaning of the `@vercel/og` essay from 2022 — by treating OG images as code, "you can version-control them, reuse components, and apply brand consistency across thousands of unique pages automatically, reducing manual design work to zero for new content." The industry mostly read that as *cheaper marketing automation*. The interesting projects are reading it as *one rendering pipeline, as many consumption surfaces as we need*. MiroShark just shipped a public discovery feed without building a thumbnail service, because it already had one and had never called it that.

The social share card, for fifteen years a rounding error in the `<head>` of an HTML document, has become one of the most useful structural components an application can own. Render it once, version it in code, cache it by content hash, and let every surface that needs to say "here's what this thing looks like" point at the same PNG. It's the quietest architectural decision of 2026, and it's the reason the gallery that went live today was a twenty-four-hour ship.

---
*Sources: [Vercel — Introducing OG Image Generation](https://vercel.com/blog/introducing-vercel-og-image-generation-fast-dynamic-social-card-images); [Sanity Learn — Creating dynamic Open Graph images with Vercel OG](https://www.sanity.io/learn/course/seo-optimization/creating-dynamic-open-graph-images-with-vercel-og); [Imejis — 10 Best Bannerbear Alternatives in 2026](https://www.imejis.io/blogs/comparisons/best-bannerbear-alternatives); [Abyssale — Image Generation API for Automated Creative Production 2026](https://www.abyssale.com/blog/image-generation-api-automated-creative-productionguide); [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark); [PR #42 — Social share card (Open Graph image + landing page)](https://github.com/aaronjmars/MiroShark/pull/42); [PR #43 — Public simulation gallery (/explore)](https://github.com/aaronjmars/MiroShark/pull/43).*
