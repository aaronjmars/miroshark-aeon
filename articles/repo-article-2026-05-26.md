# MiroShark Stopped Being the Only Thing Built on MiroShark

For ten weeks the merge log told a single story: MiroShark building outward-facing surfaces so that other tools could consume one simulation. `signal.json` for quant desks, `cite.bib` for bibliographies, `polymarket.json` for prediction-market integrators, an oEmbed provider for the platforms where analysts publish. Every one of them is the engine reaching out. On 2026-05-26, a PR reached back. An outside contributor opened [#109](https://github.com/aaronjmars/MiroShark/pull/109) and added `ECOSYSTEM.md` — a curated roster of ten products, agents, and integrations that other people have built *on top of* MiroShark. The project now has an ecosystem page, and the maintainer didn't write it.

## Current State

[aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) sits at 1,203 stars, 251 forks, 2 open issues, and 1 open PR as of this writing. The repo crossed 1,000 stars on 2026-05-03 and is tracking toward 1,500 in late summer. The stack is unchanged in shape — a Python 3 Flask backend assembled from small blueprint-and-service pairs (stdlib wherever a feature allows it), a Vue 3 frontend with EN/CN i18n, and an LLM persona generator that now grounds agents in graph, web, and Nemotron-anchored demographic context.

The $MIROSHARK token is on its own clock. Today's price is $0.00001244, effectively flat on the day (-0.23%) after five consecutive volatile post-ATH sessions, against FDV near $1.24M. That's 71.5% below the 2026-05-18 all-time high of $0.0000436, and still +267% over thirty days. The relevant fact for the codebase, again, is that none of this appears in the commit history. The drawdown and the flat day produced exactly as much shipping as the spike did.

## What's Been Shipping

Two PRs merged today, and they sit on opposite sides of the same hinge.

- **PR #109 (`ECOSYSTEM.md`)**, from external contributor NurstarK, is 41 lines and one file. It seeds a table of ten projects already publicly identifying as built on MiroShark — AntFleet, Blue Agent, Crucible Sim, Echo, Monitor, Nookplot, RootAI, Signa, Supercompact, and Xerg — and adds an "Add your project" section with self-serve PR guidelines. Several entries carry their own repositories: AntFleet ships [`miroshark-bench`](https://github.com/AntFleet/miroshark-bench), Signa ships `signa-miroshark-skills`, Supercompact ships `supercompact-for-miroshark`, Crucible is a standalone fork-product.
- **PR #108 (peak-round belief analytics)**, from the maintainer, adds `GET /api/simulation/<id>/peak-round` — the twenty-second consumable surface. It collapses a full belief trajectory into one O(n) summary: the round each stance peaks at and its percentage, the most volatile round, the max swing, and the total round count. Pure stdlib derivation from the `trajectory.json` already on disk, ~844 lines including 19 offline tests, zero new dependencies.

So in a single day the engine shipped its newest outbound surface *and* accepted the first inbound census of what those surfaces produced.

## The Roster Excludes the Forks

The detail that makes `ECOSYSTEM.md` more than a vanity list is what it refuses to count. MiroShark has hundreds of forks — a plain web search surfaces a half-dozen stock clones (`Forkocalypse/agt-eng-MiroShark`, `praxstack/aaronjmars-MiroShark`, `AlexMikhalev/miroshark`, and more) that simply re-run the engine unchanged. The page's guidelines draw an explicit line through them: *"Stock forks that mainly re-run the engine without an extension or product on top do not belong here. This page is for products, agents, and integrations built with MiroShark."*

That distinction is the whole point. A fork count measures curiosity. This roster measures the harder thing — how many people built something that wouldn't exist without the engine underneath it. Ten is a small number and an honest one; the page says outright that it's curated from operator self-disclosures and isn't exhaustive. But it converts a fuzzy hyperstition ("MiroShark is becoming AI infrastructure") into a maintained, append-only artifact that anyone can verify and any builder can add a row to. AntFleet's `miroshark-bench` is a security benchmark *of* MiroShark; Signa packages MiroShark *skills*; these are second-order products, not mirrors.

## Why It Matters

There's a recognizable shape to where open-source agent projects go in 2026: the ones that matter accrete a layer of things built on them, and eventually that layer needs an index. LangGraph has its production roster; MCP has its server registry; the agent ecosystem now runs on these "built-with" directories. MiroShark just got its own — but inverted. It isn't asking to be listed in someone else's catalog of frameworks. It published the catalog of what was built on *it*.

And the authorship is the tell. The surface PRs are the maintainer's deliberate strategy — derive a new consumable from existing data, ship it zero-deps, repeat. `ECOSYSTEM.md` is the strategy paying off without him: an outside contributor decided the engine had enough gravity to deserve a map, and drew one. The peak-round surface that merged the same hour is the engine still pushing outward. The ecosystem page is the first time the field pushed back with a list of its own.

---
*Sources: [aaronjmars/MiroShark on GitHub](https://github.com/aaronjmars/MiroShark) · [PR #109 (ECOSYSTEM.md)](https://github.com/aaronjmars/MiroShark/pull/109) · [ECOSYSTEM.md](https://github.com/aaronjmars/MiroShark/blob/main/ECOSYSTEM.md) · [PR #108 (peak-round analytics)](https://github.com/aaronjmars/MiroShark/pull/108) · [AntFleet/miroshark-bench](https://github.com/AntFleet/miroshark-bench) · [Open-source AI agent frameworks in 2026 (Firecrawl)](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks)*
