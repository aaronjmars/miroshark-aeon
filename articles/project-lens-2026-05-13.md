# The Three URLs That Joined 137 Others in Her Reeder

Reeder is the app that survived. Twitter shrank, then forked. Google Reader went away in 2013 and the cottage industry of replacements — Feedly, Inoreader, NewsBlur, NetNewsWire, Reeder — kept going anyway, because the same set of people kept needing the same thing.

A 2026 industry tally pegged RSS adoption among professionals as up 34% year-over-year, driven by people fed up with algorithmic timelines deciding what they see. Inoreader's free tier still holds 150 subscriptions; Pro at $7.50/month adds rules and filters. The median power user runs somewhere between 80 and 200 active feeds, and the r/rss subreddit is full of people closer to 500. These aren't casual readers. They're analysts, librarians, journalists, lawyers, traders — anyone whose work depends on noticing things, and who has decided that a notification feed is the wrong shape for noticing.

## A Tuesday morning in Reeder

Maya is one of them. She covers Asia-Pacific tech regulation for a small political-intelligence shop in Washington. Her clients are corporate-strategy teams who need to know what the State Council is about to do six weeks before it ships. Six years in, she has 137 feeds in Reeder — Lawfare, Bloomberg's chip section, two CSIS think-tank tracks, a Hacker News slice that drops anything under thirty points, a dozen .gov press feeds that hardly anyone subscribes to, and a long tail of trade publications.

This Tuesday she adds three more URLs:

- `https://miroshark.app/api/feed.atom?q=Taiwan&consensus=true`
- `https://miroshark.app/api/feed.atom?quality=excellent&sort=trending&limit=25`
- `https://miroshark.app/api/feed.atom?q=export+control&outcome=verified`

On the wire they are the same shape as the other 137: an Atom XML document, an `<entry>` per item, a `<title>`, a `<summary>`, a `<link>`. Reeder doesn't care that the entries describe multi-agent simulations of contested geopolitical scenarios. To Reeder they're just items, dated, deduped, sortable next to the Lawfare brief that posted twenty seconds later.

## The lens, not the project

This is the part of the story that's about the lens, not about the product. The three URLs joined the other 137 *without changing Maya's workflow*. She didn't install an app. She didn't sign up for an account. She didn't add a tab to her browser. Her work surface — the four-pane Reeder layout she's used five days a week for years — looks identical.

This is, in 2026, unusual. Most products in this space are built around the assumption that you want to come to them: dashboards with charts, configurable layouts, a heavy left-nav. They want to be open in a tab. They send digest emails. In product-strategy language, they are "a destination."

MiroShark, the simulation gallery underneath the three Atom feeds, is a destination too — there is a gallery, with cards, a filter row, and seventeen surface-format toggles per result. But the Atom feeds don't ask Maya to be there. They go where she already is.

## How the filter URL is composed

The detail that makes this work doesn't show up in a screenshot.

The URLs in Maya's example use six query-string parameters — `q`, `consensus`, `quality`, `outcome`, `sort`, `limit` — and any combination composes. The same six knobs run the gallery search page. They're applied by a single function, `gallery_filters.select_filtered_cards`, that the feed route imports and re-uses unchanged. The Atom serializer wraps the result; the filter logic doesn't fork. That's the part PR #81 actually shipped: not a new feed, but the existing gallery filter threaded through the existing feed endpoint.

The payoff is downstream. When Maya tomorrow wants a fourth feed — say, only excellent-quality simulations of AI export policy — she doesn't file a feature request. She edits the URL: `?q=export+control&quality=excellent`. The feed responds. There is no per-feed configuration screen. There is no "saved view" object in any database. The URL *is* the saved view, Reeder is the persistence layer, and the cost of a fifth feed tomorrow is zero engineering effort on either side.

A quieter choice underneath: the feed route caps the limit at 50 — smaller than the gallery's 100 — because aggregators re-fetch every fifteen minutes and someone could otherwise build a 50,000-row Atom doc by accident. The filter knobs are wide; the surface area for abuse is narrow.

## What the three URLs do for the rest of Tuesday

By midmorning Maya has looked at one item from the verified-outcome feed — a simulation of an AI-chip export-license tightening, run with eight agents, ending in 78% consensus that the executive order would land before the end of June. The simulation is, by itself, not actionable. It is one analyst with one model. But she clicks through to the `reproduce.json` link, sees the parameter set, sees that two simulations from the prior week with similar agent weights landed within four points of each other, and notes it. The note goes into her Friday client memo. The Friday memo earns the retainer.

The thing she did not do is open a new app, set up an account, or change her workflow. Three URLs.

## What tools that meet you where you are get right

The interesting question is why most products don't ship this surface. The answer is usually attention economics: a feed-reader subscriber is a customer you've largely lost the ability to monetize. They don't see your dashboard, your sparklines, your upsell. They see your `<entry>`s.

The counter-strategy is to build for the people who aren't the modal user, on the bet that they're the most valuable. The professional-reader population is small but it is the population that makes things into news. Analysts running 137-feed Reeder setups are the ones whose memos land in front of people who fund the next thing. Meeting them where they already are is cheaper than convincing them to come to you — and it is the closest thing to organic reach a 2026 product still has.

Maya's afternoon will involve a hundred more items in Reeder. Three of them will be hers, and she'll know it.

---
*Sources: [Why RSS Still Matters in 2025 — SimpleFeedMaker](https://simplefeedmaker.com/blog/why-rss-still-matters/); [Best RSS Readers in 2026 — Readless](https://www.readless.app/blog/best-rss-readers-2026); [Best Android RSS Reader Apps in 2026 — Readless](https://www.readless.app/blog/best-android-rss-reader-apps-2026); MiroShark `/api/feed.{atom,rss}` filter parameters (PR #81); `gallery_filters.select_filtered_cards` shared filter helper (PR #69).*
