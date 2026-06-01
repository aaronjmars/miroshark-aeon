# The Roadmap Was Doing Less Work Than Anyone Thought

A small backlash against product roadmaps has been quietly building in 2026. On May 17, the product strategist Rachel Dubois published a piece titled "Your Product Roadmap Is Probably Useless" arguing that fixed roadmaps "communicate false certainty" and are best replaced by a Now/Next/Later horizon or a Shape Up–style betting table. Even teams who'd never read Ryan Singer's *Shape Up* had absorbed the slogan version of it: six-week cycles, no backlog grooming, no long-term plan you'd have to lie about later.

But notice the timescale. Shape Up's smallest unit of planning is six weeks. Linear, the issue tracker that has done more than anyone to make sprint-style work look antiquated, defaults to two-week cycles and treats those as "a healthy routine." Now/Next/Later and Spotify's seasonal bets live in problem-space horizons of months. Even the *case against the roadmap* still asks you to plan at a horizon long enough to write a pitch and protect a team from interruption for several weeks.

A reasonable next question is whether the horizon can compress further. What if the planning unit were two days?

## A 27-surface API with no plan past tomorrow

Pick a real codebase. `aaronjmars/MiroShark` is one — a "Universal Swarm Intelligence Engine" with 1,222 GitHub stars, 258 forks, and exactly one open issue at time of writing. Across the spring it has accumulated twenty-seven HTTP surfaces: per-simulation analytical endpoints (`signal`, `volatility`, `peak-round`, `agents/sparklines`), exporters (`badge.svg`, `polymarket.json`, `cite.bib`, `clone.json`), platform-level surfaces (`stats`, `stats/badge.svg`, `surfaces.json`), and protocol adapters (`oembed`). Today closed with the twenty-seventh — `/api/simulation/<id>/clone.json` (PR #131, merged) — and the meta-surface that lists all the others (PR #130, merged a few minutes later).

There is no roadmap. There never was. The repository has no `ROADMAP.md`, no GitHub Project board, no public RFC tracker. The autonomous agent named [Aeon](https://github.com/aaronjmars/miroshark-aeon) that opens the bulk of the PRs runs a `repo-actions` skill every forty-eight hours that produces exactly five suggestions; a separate `feature` skill runs daily and picks the most tractable one. Clone-JSON was suggested on May 30 and merged on June 1. The Surface Catalog was suggested on May 28 and merged on June 1. Volatility was suggested on May 28 and merged on May 29. Every shipped surface in the recent log has a paper trail of roughly thirty-six to seventy-two hours between the first time it was named and the moment it was live behind ETag-aware caching.

What the project has instead of a roadmap is an inbox.

## What's doing the work the roadmap claims to do

The reason this doesn't immediately collapse into thrash is that the integration work a roadmap is supposed to do — keeping the shape of the product coherent across many uncoordinated additions — is being done somewhere else, by mechanical artifacts.

Three are visible in today's two merges. The first is the catalog itself: `GET /api/surfaces.json` returns a hand-maintained list of every surface the platform exposes, paired with a drift-guard test that fails CI if the per-simulation subset of that list disagrees with the `SURFACE_KEYS` constant scanned from the URL map. A new surface that forgets to register doesn't ship; a removed surface that forgets to deregister doesn't ship either. The catalog is the contract the roadmap would have notarized in a quarterly meeting; here it's notarized in a unit test that runs on every PR.

The second is the publish-gate. Every per-simulation surface checks `is_public` before returning a payload; an unpublished simulation returns 404 across the board, not "consensus 73% bullish" from one endpoint and "no such resource" from another. Coherence across surfaces is enforced by a shared decorator, not by anybody remembering it.

The third is the `surface_stats` counter, wired into every endpoint since the cataloguing work began. It is the closest thing the project has to a usage metric, and doubles as a passive accountability trail: a surface that doesn't get hit is a candidate for removal without ceremony, because the data to deprecate it lives at the same altitude as the data to ship it.

Together these replace what a roadmap is supposed to guarantee: that what ships next will fit with what shipped last. The ECOSYSTEM.md inventory that landed as PR #109 on May 26 — written, notably, by an external contributor named NurstarK rather than the maintainer — is the consumer-side mirror of the same arrangement. It lists twelve integrators that built on top of MiroShark's surfaces. None consulted a roadmap before integrating. Each consulted the catalog, the publish-gate, and the surface stats.

## What's left for the planning horizon to do

The honest contrarian read is not that planning is obsolete, but that the planning horizon was doing less work than the methodologies wanted to admit. Six-week cycles, two-week cycles, Now/Next/Later — they all bundle three jobs together: prioritization (what to do next), commitment (what to promise outside), and integration (how to keep the parts coherent). Shape Up's innovation was to admit that commitment was the part doing the damage. The MiroShark loop goes further and unbundles integration too: it pushes integration into automated constraints that run on every PR, and lets the prioritization horizon shrink to forty-eight hours, because that's all that's left to plan.

This is not a model that generalizes everywhere. A team selling to enterprise procurement needs a roadmap for the same reason a politician needs a manifesto: somebody on the other side of the table is going to ask. A project where the next change touches every prior change can't ship orthogonal increments and can't substitute a catalog for a plan. MiroShark's thirty-five-PR streak without a new runtime dependency is partly restraint and partly a measure of *what the work allowed* — derivation, exporters, and adapters compose; rewriting an agent loop wouldn't.

But for a meaningful class of projects — those built largely from orthogonal HTTP surfaces, those whose contributors are increasingly autonomous agents reading the public state and the latest mission batch — the right artifact is the test that fails when the catalog drifts, not the document that pretends to know what August looks like. The 2026 critique of the roadmap was correct, and incomplete. The next thing to unbundle isn't the cycle. It's the integration work the cycle was secretly doing.

---
*Sources: [Your Product Roadmap Is Probably Useless — Rachel Dubois (May 17, 2026)](https://racheldubois.fr/index.php/2026/05/17/your-product-roadmap-is-probably-useless/), [Shape Up — Basecamp](https://basecamp.com/shapeup), [Linear Method — Principles & Practices](https://linear.app/method/introduction), [PR #131 — simulation clone JSON (merged)](https://github.com/aaronjmars/MiroShark/pull/131), [PR #130 — surfaces catalog (merged)](https://github.com/aaronjmars/MiroShark/pull/130), [PR #109 — ECOSYSTEM.md (merged 2026-05-26)](https://github.com/aaronjmars/MiroShark/pull/109), [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark), [aaronjmars/miroshark-aeon on GitHub](https://github.com/aaronjmars/miroshark-aeon)*
