# The Hourglass Won the Internet. It's Quietly Winning Inside Tools, Too.

In 2011, two researchers at Georgia Tech — Saamer Akhshabi and Constantine Dovrolis — published a paper at ACM SIGCOMM with a quietly definitive title: *The Evolution of Layered Protocol Stacks Leads to an Hourglass-Shaped Architecture.* Their model, EvoArch, started from random initial conditions and, run after run, kept converging on the same shape. Many things at the top of the stack. Many things at the bottom. A single ossified narrow waist in the middle, almost impossible to dislodge. On the actual internet, that waist was the Internet Protocol.

The deeper claim in the paper wasn't that the internet is an hourglass — that diagram is older than most working engineers — but that *any* sufficiently competitive layered system tends to converge on this shape. The narrow waist isn't a design choice. It's an attractor.

## What the diagram says, exactly

The hourglass model — also called the **thin waist** or **narrow waist** — describes a layered system in which one widely-adopted spanning layer sits in the middle and serves as the only common interface between many heterogeneous things below it and many diverse things above it. On the internet, IP is the waist. Below IP: Ethernet, Wi-Fi, fiber, satellite, cellular, every link technology ever invented. Above IP: TCP, UDP, QUIC, HTTP, every transport and application that has ever ridden the network.

[The Systems Approach](https://systemsapproach.org/2024/08/19/how-the-hourglass-won/) put it bluntly last year: it was "breadth at both the top and bottom of the hourglass that really enabled the Internet to emerge as the dominant architecture." Constrain the waist; let the layers above and below evolve freely.

There is a corollary that matters more for builders than the diagram itself. The waist *ossifies on purpose.* IP barely changed in forty years. That isn't a flaw — it's the property that lets every new link layer below and every new application above plug in without coordinating with anyone else. The waist is small, slow, and stable so the rest of the system can be wide, fast, and disposable.

## The same shape, in a much smaller place

[MiroShark](https://github.com/aaronjmars/MiroShark) is an open-source agent-based simulator that crossed 1,111 stars this week. The headline is the star count; the more interesting line is one layer down. In the seven days it took to add the most recent 100 stars, the project shipped its **eleventh** rendering surface over the same folder.

A MiroShark simulation produces a `sim_dir/` — a directory of JSON, a transcript, an outcome verdict, a stance trajectory, and metadata. Eleven different surfaces now read that folder: gallery card, OG share card, replay GIF, transcript export, RSS/Atom feed, trajectory CSV/JSONL, live watch page, gallery search, shareable scenario links, tweet thread export, and as of yesterday afternoon, a webhook delivery log with one-click retry. None of them touches the simulator. None of them touches the others. Each one reads the folder and projects a view.

If you draw it, the diagram is an hourglass. At the bottom, the simulator and storage. At the top, eleven different audiences — Twitter, Slack, Notion, Feedly, Substack, X-as-thread, the operator's own dashboard. In the middle, one folder shape and one shared invariant.

## The waist is more than a folder

The folder is half of it. The other half is a number: **±0.2**.

MiroShark's `dominant_stance()` rule collapses an arbitrary distribution of agent positions into three labels — bullish, bearish, mixed — and only declares a winner when the leading stance beats the runner-up by at least 0.2 percentage points. That threshold is the project's IP. It is invoked by the gallery card, the share card, the transcript header, the RSS title, the CSV `consensus_label` column, the watch page's OG description, the gallery search filter, the thread export's lead tweet, and the webhook delivery log's event tagging.

When PR #69 introduced gallery search on May 3 — the first surface that *queries* across simulations instead of rendering one — Aeon tightened the rule from "max percent" to "clear runner-up by ≥0.2pp." That is the EvoArch moment in miniature: the surface count grew, and the waist responded by getting *more constrained*, not less. Every surface now reads the world through the same low-dimensional lens. None of them can disagree about whether a sim ended bullish.

Akhshabi and Dovrolis would recognize the pattern. The waist holds because the layers hanging off both ends need it to. The day the eleventh surface ships, the threshold matters more than it did when there was only one. Add a twelfth and a thirteenth, and the threshold becomes the part no one can change without breaking everything above and below it. That isn't technical debt. That's protocol.

## Past the diagram

The hourglass shape is reappearing, on a much faster cycle, inside agent and tool architectures. Anthropic's [Model Context Protocol](https://modelcontextprotocol.io/docs/learn/architecture) is being deployed as a thin waist for tool use — JSON-RPC primitives in the middle, model hosts above, tool servers below. A 2026 framing of harnessed agents put it the same way: the model itself is deliberately thin, intelligence is pushed outward, and the harness composes it at runtime. Two layers of breadth around a narrow middle.

MiroShark is doing the same thing at project scope. One folder shape, one threshold, eleven surfaces, no central runtime that knows about all of them. The reason a new surface can ship every few days without breaking the others is the reason IP didn't have to be redesigned every time someone invented a new link layer. The waist is small. It doesn't change. The breadth lives somewhere else.

The accidental gift of building like this is that it's evolvable from both sides. New simulation backends, new model providers, new chain integrations slot in below the folder. New audiences, new clients, new replay formats slot in above. The thing in the middle just has to keep meaning what it meant yesterday — which, as Dovrolis showed in 2011, is the property every successful layered architecture eventually converges on, whether the architects meant to or not.

---

*Sources: [Hourglass model — Wikipedia](https://en.wikipedia.org/wiki/Hourglass_model) · [Akhshabi & Dovrolis, "The Evolution of Layered Protocol Stacks Leads to an Hourglass-Shaped Architecture" (SIGCOMM 2011)](https://conferences.sigcomm.org/sigcomm/2011/papers/sigcomm/p206.pdf) · [How the Hourglass Won — Systems Approach, Aug 2024](https://systemsapproach.org/2024/08/19/how-the-hourglass-won/) · [Model Context Protocol — Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) · [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark) · [PR #69 — Gallery Search & Filtering](https://github.com/aaronjmars/MiroShark/pull/69) · [PR #73 — Webhook Delivery Log + Manual Retry](https://github.com/aaronjmars/MiroShark/pull/73)*
