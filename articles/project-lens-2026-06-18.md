# What to Do Before You Ask Your Community Anything

Sometime in the next month, a small protocol is going to make a decision about its fee structure. Not a big one — a 0.2% bump, defensible on the numbers. They've modeled the revenue. They haven't modeled the reaction. So they'll post to the governance forum, watch the community split, lose three of their five vocal contributors to a FUD thread, and reverse the proposal eight days later with less trust than they started with.

They will call this "community feedback." What they actually ran was a live governance incident without a safety net.

## The information paradox

The problem is structural. The only way to get reliable signal on how a change will land is to surface it to the people who will react. And the moment you surface it, you've already changed the situation. A survey telegraphs your hand. An informal temperature-check recruits opponents alongside supporters. A consultant's analysis can cost [$25,000–$65,000 for custom qualitative research](https://www.thefarnsworthgroup.com/blog/market-research-cost) and still can't tell you how *your* specific community, with its specific prior history, responds to *your* specific proposal.

What you're buying at those prices is cover, not signal. The research firm's brand stands behind the result. "We did our homework" becomes a PDF with a letterhead. Nothing about that transaction is auditable to anyone outside the room.

The adjacent market — AI-powered synthetic research — is making inroads on the cost problem. Studies [comparing AI-generated focus groups to live participant sessions show 85–92% correlation](https://strategaresearch.com/generative-ai-in-market-research-the-2026-strategy-guide/) on sentiment and theme detection, enough for directional screening. The emerging practice is a two-phase model: synthetic tools narrow the options first, real participants validate later. Sixty-four percent of market researchers reported increasing their AI tool usage in 2025. The category is forming.

But these tools are built for markets, not communities. A focus group samples respondents who answer in isolation. Governance communities don't work that way. How a key figure responds in round one changes what five hundred other members think in round two. The static snapshot misses the trajectory entirely.

## A world, not a poll

The engine that runs under a dollar doesn't ask agents for their opinion. It puts them in a world and watches what happens.

MiroShark seeds hundreds of agents from real demographic distributions, assigns each a persona generated from the locale-appropriate prompt modules in `backend/app/prompts/locales/` — as of [commit 5643802](https://github.com/aaronjmars/MiroShark/commit/5643802), a French-speaking governance community gets agents reasoning in French, not English personas translated after the fact — and runs them through multiple rounds on a simulated social graph. They post, argue, challenge each other's priors, and trade on an embedded prediction market AMM that tracks belief drift round by round.

The governance team feeds in a proposal as the starting condition. What they get back isn't a percentage. It's a trajectory: what the community believed at round one versus round five, after the vocal personas had spoken and the large-holder agents had moved price. And they can inject counterfactuals mid-run via director mode — fork the timeline, change the information environment ("a competitor announces the same change"), compare how belief evolves across branches.

This is the structural difference from a poll. A poll captures a static opinion. A simulation captures an emergent one. Those are not the same thing. A community that looks 60% in-favor on a survey might be 45% after two rounds of in-community debate. The trajectory is the signal.

## The non-obvious part

Here is the architectural detail that turns this into something more than a cheap demo.

Every simulation's output can be fetched as `GET /api/simulation/<id>/signed-result.json` — an HMAC-SHA256-signed envelope wrapping the canonical signal payload: direction, confidence tier, belief percentages, risk assessment. [PR #152](https://github.com/aaronjmars/MiroShark/pull/152) built this specifically so an integrator can store the result and prove, offline, that those bytes are what the engine actually returned — not revised, not selected from a favorable run.

The governance team that runs this sim before posting to Snapshot can publish the hash in the proposal body — timestamped before the vote was announced. Not a claim. A record.

This is a new property. A $25,000 focus group comes with a brand attached: trust accrues from the vendor's reputation, accumulated over decades of client work. A $1 simulation cannot carry that brand premium. But it can carry something a focus group has never offered: a proof. The signed-result endpoint is the architecture for a world where trust is built from artifacts, not credentials — where "we tested this" is a falsifiable statement, not a PR move.

## What this predicts

The [36% of new ventures now launching solo-founded](https://blog.mean.ceo/the-solo-founder-ai-agent-stack-that-is-replacing-entire-startup-teams/) can't afford the $25K research budget. Neither can most DAO governance teams acting on $200 in gas fees and a Notion doc. The two-phase model — sim first, validate second — is the only version of diligence that's economically reachable at that scale.

Here is the falsifiable claim: by mid-2027, at least three high-profile governance crises will be dissected in public post-mortems, and the question communities will ask won't be "why didn't you commission a study?" It will be "why didn't you publish a sim hash before you asked us?" The diagnostic has already shifted in commercial market research; it's one governance incident away from shifting in on-chain governance too.

The projects that wire pre-vote simulation into their standard process first will have an unusual edge — not necessarily better predictions, but a verifiable trail that separates preparation from improvisation. In a governance environment where attacks typically begin by questioning intent, that trail is worth more than any single vote outcome. The claim is specific enough to be wrong on a schedule: check back in eighteen months.

---
*Sources:*
- [Focus Group and Market Research Costs 2026 — The Farnsworth Group](https://www.thefarnsworthgroup.com/blog/market-research-cost) — focus group pricing ($7,000–$20,000+ per group), baseline custom research project costs ($25,000–$65,000), the "cover not signal" framing
- [Generative AI in Market Research: The 2026 Strategy Guide — Stratega Research](https://strategaresearch.com/generative-ai-in-market-research-the-2026-strategy-guide/) — 85–92% correlation between AI synthetic responses and live participant sessions; two-phase validation model; 64% of researchers increasing AI tool use
- [The Solo Founder AI Agent Stack — mean.ceo](https://blog.mean.ceo/the-solo-founder-ai-agent-stack-that-is-replacing-entire-startup-teams/) — 36% of new ventures solo-founded in 2026; economic context for teams that can't afford traditional research
- [MiroShark — feat: signed-result.json HMAC-SHA256 offline-verifiable signal payload (PR #152)](https://github.com/aaronjmars/MiroShark/pull/152) — signed-result endpoint architecture, HMAC-SHA256 envelope, offline verification property
- [MiroShark — feat(i18n): translate French prompt locale (commit 5643802)](https://github.com/aaronjmars/MiroShark/commit/5643802) — locale-authentic agent cognition via `backend/app/prompts/locales/fr/`
