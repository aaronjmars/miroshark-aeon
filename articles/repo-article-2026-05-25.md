# MiroShark Built a Surface Nobody Has to Find

Every surface MiroShark has shipped so far is a destination. `GET /<id>/signal.json` for quant tooling, `/<id>/cite.bib` for a bibliography, `/<id>/badge.svg` for a README, `/<id>/polymarket.json` for an integrator — all of them require the consumer to already know the route and have a reason to fetch it. On 2026-05-25 at 12:48 UTC, PR #107 merged the first surface that inverts that. With the oEmbed provider live, a researcher who pastes a MiroShark share link into a Substack draft gets a rich preview card and never types a route name at all. The destination comes to them.

## Current State

[aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) sits at 1,196 stars, 248 forks, 2 open issues, and 1 open PR as of this writing. The repo crossed 1,000 stars on 2026-05-03 and is projected to reach 1,500 in late summer at the current pace. The stack is a Python 3 Flask backend built from small blueprint-and-service pairs (pure stdlib wherever a feature allows it), a Vue 3 frontend with EN/CN i18n, and an LLM-driven profile generator that now grounds agents in graph context, web context, and — since last week's Nemotron PR — demographic anchors.

The $MIROSHARK token is on a different trajectory: yesterday's close was $0.00001227, down 25.6% on the day and 71.8% from the 2026-05-18 all-time high of $0.0000436, against FDV around $1.23M. Thirty-day return is still +207%. The relevant fact for the codebase is that none of it shows up in the merge log. The framework shipped through the five-day drawdown and through Saturday's bounce alike; the cadence does not read the candles.

## What's Been Shipping

Three PRs merged today, all adding zero new dependencies — the new zero-deps streak that restarted after last week's Nemotron PR now stands at three:

- **PR #107** (oEmbed provider, +765/-2 across 9 files) — the subject of this piece.
- **PR #105** (platform aggregate stats API + Shields.io platform badge) — the first platform-level surface, walking the simulation data directory once to answer `GET /api/stats` and render a `MiroShark | N simulations` pill.
- **PR #104** (collapse the explicit `.env` profile list into a `.env.*` wildcard) — a one-line hygiene fix from external contributor Void Freud, their second merge after the Aura launcher guard.

A fourth external contributor is in the queue: PR #106 (Railway deployment prep, from DYAI2025) is open and unreviewed, which would make four distinct outside authors landing or proposing work in eleven days.

## Discovery, Not a Destination

The share page already emits Open Graph, Twitter Card, and Farcaster Frame tags. Those cover the *social* surface — paste a link into X, Discord, or a Warpcast feed and it unfurls. But the platforms where analysts and researchers actually *publish* — Notion, Ghost, Substack, WordPress — don't read Open Graph. They implement the [oEmbed 1.0](https://oembed.com/) discovery flow: fetch the page, look for a `<link rel="alternate" type="application/json+oembed">` tag, then call back to the named provider for a structured embed. MiroShark never advertised that tag, so a pasted share link rendered as bare text on exactly the platforms where its audience writes.

PR #107 closes that gap with about eighty lines of provider logic. The share page now injects the discovery `<link>` tags (for published simulations only), and a new root-mounted `GET /oembed?url=&format=` answers the callback with a `type: "rich"` payload: the 1200×630 share-card PNG as `thumbnail_url`, and an 800×500 iframe over the existing `/embed/<id>` route as `html`. The architectural detail that matters is what it *doesn't* add. Both the thumbnail and the iframe point at surfaces that already ship. oEmbed is a protocol layer, not a new renderer — it is the twenty-first key in the surface-stats counter, but it draws its bytes entirely from routes that predate it. The new code is wiring and a strict host allow-list (the provider never dereferences a foreign URL, and a private or missing simulation returns 404 without confirming it exists), not pixels.

## Why It Matters

MiroShark spent ten weeks answering "how is one simulation consumed by a tool that asks for it." The last two days answer a different question: how is the project consumed by someone who isn't asking. PR #105 lets a blog post embed a live "N simulations run" badge; PR #107 lets that same blog post auto-unfurl every share link inside it into a preview card. Both turn passive mentions into live signal with no action from the writer. That is distribution infrastructure for the long tail — and it arrives in the same window that a fourth outside contributor opened a deployment PR and traders posted, unprompted, that they "keep buying more." The framework is increasingly built for consumers it never met, on surfaces they don't have to find.

---
*Sources: [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark) · [PR #107 (oEmbed provider)](https://github.com/aaronjmars/MiroShark/pull/107) · [PR #105 (platform stats)](https://github.com/aaronjmars/MiroShark/pull/105) · [PR #104 (.env wildcard)](https://github.com/aaronjmars/MiroShark/pull/104) · [PR #106 (Railway deploy prep)](https://github.com/aaronjmars/MiroShark/pull/106) · [oEmbed 1.0 specification](https://oembed.com/) · [Notion embeds](https://www.notion.com/help/embed-and-connect-other-apps)*
