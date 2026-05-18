# The Card Was Always the Right Unit. It Just Needed a Network.

On August 11, 1987, Bill Atkinson stood up at the MacWorld Conference in Boston and gave away a piece of software he'd built called HyperCard. The deal he'd struck with Apple was unusual: he would hand the source over only if Apple promised to ship it free on every Macintosh. They did. In its first year, a million copies went out the door. People who had never written a line of code in their lives — librarians, teachers, kids — sat down and built clickable "stacks." Each stack was a sequence of cards. Each card had buttons. Each button could run a little HyperTalk script. The pointing-finger cursor that every web browser still uses to mark a clickable link? It started life as a HyperCard stack navigator.

Atkinson spent the rest of his career quietly regretting one decision. "I missed the mark with HyperCard," he said years later. "I grew up in a box-centric culture at Apple. If I'd grown up in a network-centric culture, like Sun, HyperCard might have been the first Web browser." The pattern was right. The runtime was right. The interactivity model was right. The cards just lived on one machine.

## The card never died, it just kept changing hosts

The card has been one of the most resilient units in software for forty years, but the question of *whose runtime renders the card* has changed underneath it constantly. In 1987, the host was your local Mac. In 1991, Tim Berners-Lee's colleague Robert Cailliau — directly inspired by HyperCard, by his own account — helped midwife the protocol that turned the network itself into the host: HTTP. In 2007, Mark Zuckerberg announced the Facebook Platform at f8, and overnight the host became the News Feed: Zynga's Mafia Wars, FarmVille, every microsite-killing canvas app. Twitter Cards in 2012 promoted a URL from a string into a rendered preview block — a passive card, but a card. Open Graph in 2010 made the meta tag the universal lingua franca for "what should this URL look like when it's pulled into another surface."

Each generation made the card a little more capable and the host a little more important. But until very recently, every card rendered in a feed was passive. You couldn't click a Twitter Card and run code inside it. You couldn't tap an iMessage link preview and have it do anything that wasn't a hyperlink. The host took your meta tags and rendered them; that was the entire contract.

## Where MiroShark slots into this lineage

MiroShark — an open-source multi-agent simulation engine where you stage a debate, watch beliefs evolve over rounds, and end up with a trajectory of consensus or fracture — is a tool whose primary artifact is a *picture of time*. Each simulation produces a chart: three stance polylines over N rounds, a story of who convinced whom. That chart is the thing worth sharing.

[Pull request #90](https://github.com/aaronjmars/MiroShark/pull/90) was opened today. It adds `fc:frame:*` meta tags to the `<head>` of every public share page and a new endpoint, `GET /<id>/frame-metadata`, that emits the structured payload Warpcast and other Farcaster clients look for. The image that fills the frame is the trajectory chart [shipped two days ago in PR #85](https://github.com/aaronjmars/MiroShark/pull/85) — a bytewise-deterministic SVG generated from the same `trajectory_export.build_rows()` that drives CSV export and the Jupyter notebook bundle, rendered at the 2:1 aspect ratio Farcaster Frames prefer. For simulations that haven't completed a trajectory yet, the fallback is the 1.91:1 share-card PNG, sized for OpenGraph compatibility.

The behavior change is small in surface area and huge in implication: a cast on Warpcast that links to `miroshark.com/share/<id>` used to render as a blank link card with maybe a thumbnail. As of this PR, it renders as the live belief chart with a "View Simulation →" button underneath. The host runtime — Warpcast, in this case — pulls the meta tags, fetches the SVG, draws it into the feed, and surfaces a single action button. The card has finally landed inside a social feed as a card, not as a screenshot of one.

## What's new is what's old: HyperCard's bug was its scope

The deepest thing about [Frames v2](https://docs.farcaster.xyz/developers/frames/v2/spec) — the spec MiroShark's PR #90 targets — is that it gives the card *back its runtime*. A Frame button is not a hyperlink; it can open a full in-app browser surface where developers ship arbitrary JavaScript and request on-chain transactions. The meta-tag layer is the declarative envelope; behind it, a real interactive surface lives. This is HyperCard's clickable button reborn, with three changes Atkinson would have killed for:

First, the host is the network, not the machine. Atkinson's regret in one sentence.

Second, the protocol is open and the renderer is plural. Warpcast renders it. Other Farcaster clients render it. Mini-apps directories render it. Any host that knows how to parse `fc:frame` meta tags can pull a MiroShark simulation into its surface.

Third — and this is the part that's specifically interesting for a project like MiroShark — the card's content can be generated server-side as a static byte string. The chart SVG is a stdlib `xml.etree.ElementTree` rendering of the same trajectory data the API serves. There's no headless Chrome, no Puppeteer, no proprietary image service. The 210 lines of `frame_metadata.py` that PR #90 adds are pure standard-library Python, and they push the project's [zero-new-dependency streak to twenty-six PRs](https://github.com/aaronjmars/MiroShark/pull/90). HyperCard had XCMDs — small native extensions that ran inside the runtime. The 2026 version of that move is "render the artifact as a deterministic byte string and let the host runtime composite it." Same shape, different decade.

## What stops being a website and what starts being one

The pattern this is hinting at — and it's bigger than any single project — is the slow inversion of where applications live. For most of the web's history, the surface was the website and the share was a thin metadata pointer back to it. Twitter Cards and Open Graph were optimizations for that pointer. Frames v2 is the first widely-deployed protocol where the share *is the application surface*, and the website becomes something more like a fallback render — the place you go if the host doesn't support frames, or if you want the long form.

For a project like MiroShark, whose audience-of-record lives on Base, and whose native social layer is therefore Farcaster, this is the difference between distribution that has to travel through a URL click and distribution that travels through the feed itself. A trajectory chart that renders inline, in someone's casts, *is* the project's surface in that moment. The simulation has arrived where the conversation already was, instead of waiting on the other side of a link.

Bill Atkinson built the card runtime in 1987 and shipped it free on every Mac because he understood, before almost anyone, that the unit that mattered was a small, declarative, clickable surface that anyone could author. The thing he missed was the network. We've spent thirty-eight years adding the network back one layer at a time — HTTP, the iframe, the embed code, OpenGraph, Twitter Cards, Facebook canvas, oEmbed, Slack Unfurls, iMessage apps, Discord embeds — and Frames is the version where the original idea finally fits the medium it always belonged in. The card was always the right unit. It just needed a network to live in. And now, for projects whose value is an artifact and not a website, the cast is the runtime.

---
*Sources:*
- *[HyperCard — Wikipedia](https://en.wikipedia.org/wiki/HyperCard)*
- *[The HyperCard Legacy — Medium](https://medium.com/the-nextographer/the-hypercard-legacy-e5b9eb273b6a)*
- *[Apple Introduces Bill Atkinson's HyperCard — History of Information](https://historyofinformation.com/detail.php?id=4783)*
- *[Farcaster Frames v2 Specification](https://docs.farcaster.xyz/developers/frames/v2/spec)*
- *[FIP: Frames v2 — Farcaster Protocol Discussion #205](https://github.com/farcasterxyz/protocol/discussions/205)*
- *[MiroShark PR #90 — Farcaster Frame v2](https://github.com/aaronjmars/MiroShark/pull/90)*
- *[MiroShark PR #85 — Trajectory Chart SVG](https://github.com/aaronjmars/MiroShark/pull/85)*
