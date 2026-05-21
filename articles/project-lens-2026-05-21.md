# Before You Write The Proposal: A Day With Synthetic Stakeholders

It is 8:14 AM and Lea is staring at the draft of a fee-switch proposal she has rewritten four times in two weeks. The protocol she works on has 4,800 token holders. Per the 2026 DAO governance reviews — voter turnout across most DAOs hovers below 10%, and below 2% in many — roughly thirty of those holders will actually post in a Snapshot temperature check, and twelve of them will be the same twelve who post in every temperature check. Their positions are knowable in advance. The other 4,788 holders are an unmodeled cloud.

She does not write the proposal today either. She runs a simulation instead.

## The Twelve Loud Holders Problem

A March 2026 review of DAO governance opens with a now-familiar statistic: in most large DAOs, the top 10% of token holders control 76.2% of voting power, and voter turnout sits below 10%. The temperature-check ritual — the Snapshot post that precedes the real on-chain vote — was designed as a low-friction signal of where the room is leaning. In practice, it has become an interview with the twelve people who always show up. They are vocal, coordinated, often correct, and also the part of the distribution a protocol researcher already understands.

What the temperature check cannot tell you is what the new staker who joined three weeks ago and has never posted thinks. What the mercenary LP who is exiting in two months thinks. What the brand-loyalist with 0.4% of supply who reads every blog post and posts in none of them thinks. The researcher has hunches about these people. She has no way to test them without running the actual proposal — at which point the cost of being wrong is no longer abstract.

The gap in current governance tooling is precisely here: there is a rich market for *vote-execution* tools (Snapshot, Tally, Boardroom, Agora) and a thin one for *pre-proposal modeling*. The closest analogue is academic — agent-based models built in NetLogo or Mesa, often locked inside PDFs, often configured by the researcher's own priors. They are not commodities you can run for a dollar in ten minutes.

## What She Does Instead

She opens a simulation tool whose tagline is exactly the kind of claim a protocol researcher cannot afford to dismiss: simulate anything, under a dollar, under ten minutes. She picks six archetypes — skeptical LP, governance maximalist, mercenary farmer, brand loyalist, core dev, opportunistic shorter — and gives each a position rooted in publicly observable on-chain behavior plus a one-line motivation. She enters the question: *"Should we activate the fee switch and redirect 25% of trading fees to veToken holders, knowing it will compress LP yields by an estimated 18%?"* She presses run. Ten rounds. Less than a dollar.

The result comes back as a belief split, a confidence score, and a transcript of every exchange between agents. Today: **Bearish 71%, risk tier medium**. The transcript shows the brand loyalist starting bullish in round one and flipping in round four after the mercenary farmer raised a competing protocol with a higher base APR. The skeptical LP never moves. The governance maximalist moves once and moves back. The arc — the brand loyalist flipping when the substitute is raised — is the thing Lea did not know she did not know.

She does not write the proposal today. She rewrites it.

## What She Embeds, And Why The Badge Is The Point

When she does post — three days later, with a redesigned proposal that builds in a six-month LP fee floor before the switch activates — she does not post a screenshot. She embeds the consensus badge in the proposal's GitHub repository README: a flat 20-pixel SVG showing `MiroShark Bearish 71%` in Shields.io grey and red. That badge is served by a route that landed on MiroShark's main branch today — `GET /api/simulation/<id>/badge.svg`, the thirteenth publish-gated share surface to merge (PR #94, merged 2026-05-21). The PR's own framing is honest about what the surface is for: the previous twelve surfaces describe a simulation in increasing depth; the thirteenth inverts the funnel. Every README the badge lands in becomes a *pull point* — and the badge updates as the underlying simulation re-runs.

She also pastes the archive bundle URL into the proposal — every published surface (chart SVG, trajectory CSV, full transcript Markdown, reproducibility JSON, signal JSON) inside one timestamped ZIP with a `manifest.json` carrying SHA-256 hashes for every entry (PR #92, merged the previous day). The twelve loud holders cannot dispute the simulation premise without engaging with the agents and the transcript she has published. Two of them open the trajectory CSV. One objects to the brand-loyalist's motivation string and offers a sharper one. The next simulation that week uses his motivation. The temperature check has happened before the temperature check.

## What This Changes For Small Protocols

Lea is hypothetical. The protocol is hypothetical. The behaviour pattern is not. Across the small protocols that fall *below* the line where Llama Risk and Karpatkey produce paid governance research — which is most protocols — the choice today is between guessing what the room thinks and asking the same twelve people. A simulation tool that costs a dollar, takes ten minutes, and produces a *citable artifact* with a hash anchored to an external ledger (PR #84's OriginTrail DKG publisher, merged earlier in May) is not replacing on-chain governance. It is filling a layer underneath it that has been empty.

The badge is the piece that decides whether any of this propagates. Twenty pixels of SVG inside a README is an embedding-fit cost low enough that it does not need to be defended in a steering call. New governance infrastructure has historically spread by accident, through the lowest-friction surface its inventors shipped — Snapshot ate temperature checks because pasting a Snapshot link into a Discord was easier than not. The unit of adoption for stakeholder simulation is not a website. It is the line of Markdown that puts the simulation result on a page someone was going to write anyway.

---
*Sources: [How DAOs Failed to Deliver on Their Original Promise — Lopez, Mar 2026](https://lopetaku.medium.com/dao-governance-failures-whales-low-turnout-attacks-d1375c556384) · [DAO Governance 2026: Hybrid Models, Legal Wrappers, and the End of Token Voting — pen-caforr, Apr 2026](https://pen-caforr.org/2026/04/15/dao-governance-2026-hybrid-models-legal-wrappers-and-the-end-of-token-voting/) · [DAO-AI: Evaluating Collective Decision-Making through Agentic AI in Decentralized Governance — arXiv 2510.21117](https://arxiv.org/pdf/2510.21117) · [MiroShark PR #94 — Consensus Status Badge SVG](https://github.com/aaronjmars/MiroShark/pull/94) · [MiroShark PR #92 — Simulation Archive Bundle](https://github.com/aaronjmars/MiroShark/pull/92) · [MiroShark PR #84 — OriginTrail DKG Citation Publisher](https://github.com/aaronjmars/MiroShark/pull/84)*
