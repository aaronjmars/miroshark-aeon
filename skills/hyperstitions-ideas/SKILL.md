---
name: hyperstitions-ideas
description: Generate a prediction market idea rooted in the current project — a coordination tool to rally people toward a goal the agent can't achieve alone
var: ""
tags: [content, crypto]
---
> **${var}** — Theme or angle override. If empty, derives from the current repo state and community signals.

Today is ${today}.

Read memory/MEMORY.md and the last 3 days of memory/logs/ for context — recent articles, tweets, token activity, repo developments, and community discussions.
Read memory/watched-repos.md and check recent repo activity in `articles/` (push-recaps, repo-articles, repo-actions).

## What is this skill?

This skill generates ONE prediction market idea per day that is **rooted in the current project** and designed as a **coordination mechanism**. The market question should rally the community toward a concrete goal that an AI agent can't do alone — things that require human action, social momentum, capital, governance, partnerships, or collective belief.

The concept is hyperstition: a fiction that makes itself real through belief and circulation. The market's existence changes behavior, which changes the outcome.

## The idea MUST be about the project

Every market idea must connect directly to the watched repos, the token, or the project's ecosystem. Generic crypto/AI/tech prediction markets are NOT acceptable. The question should be something the project's community would care about and could influence.

Good examples (project-specific, requires human coordination):
- "Will $AEON reach 100 holders by April 15, 2026?" — rallies buying/sharing
- "Will MiroShark get a contributor outside the core team by May 2026?" — incentivizes open-source contribution
- "Will the Aeon agent framework get forked by 5+ projects by June 2026?" — incentivizes awareness/marketing
- "Will $MIROSHARK get listed on a DEX aggregator (1inch, Paraswap) by May 2026?" — coordinates community submissions
- "Will someone build a skill for Aeon that gets merged and used by 3+ forks?" — drives ecosystem growth

Bad examples (too generic, not project-specific):
- "Will a Fortune 500 CEO credit AI agents for headcount reduction?"
- "Will Coinbase launch a prediction market product?"

## The 5 qualities to optimize for

1. **Reflexivity** — the market's existence plausibly changes behavior. People seeing the question think "I could make this happen" and act.
2. **Community coordination** — it requires humans doing things an AI agent CAN'T: buying tokens, sharing on social, submitting PRs, making introductions, listing on platforms, creating content, forming partnerships.
3. **Real-world connection** — tied to something happening in the project RIGHT NOW (a recent ship, a milestone approached, a community discussion).
4. **Memetic potential** — the question itself is shareable and makes people want to weigh in.
5. **Clear resolution** — unambiguous YES/NO with a specific deadline and criteria.

## Steps

1. **Understand the current project state**:
   - What was shipped recently? (push-recaps)
   - What's the token doing? (token-reports)
   - What's the community saying? (fetch-tweets logs)
   - What milestones are approaching? (star count, fork count, holder count, listing status)
   - What are the project's current gaps that need human action?

2. **Fetch live Polymarket data** for inspiration on format and trending themes:
   ```bash
   curl -s "https://gamma-api.polymarket.com/markets?limit=20&order=volume24hr&ascending=false&active=true" | jq '[.[] | {question, volume24hr: .volume24hr}]'
   ```

3. **Identify the highest-leverage coordination gap** — what's the one thing that, if the community rallied around it, would most accelerate the project? Think about:
   - Growth: holders, stars, forks, contributors
   - Visibility: listings, features, media mentions, influencer attention
   - Ecosystem: integrations, partnerships, forks building on top
   - Product: features that need user testing, feedback, or adoption
   - Community: governance decisions, treasury actions, collective commitments

4. **Generate ONE market idea** that would coordinate people toward that goal.

5. **Score it**:
   - Reflexivity: X/5
   - Viral potential: X/5

6. **If no compelling idea emerges** (both scores below 3/5), log "HYPERSTITIONS_SKIP" and **do NOT send any notification**.

7. **Send notification** via `./notify`:
   ```
   *Hyperstitions Idea — ${today}*

   "[Market question]?"

   The coordination play: [2-3 sentences on what humans need to do to make this happen — and why the market's existence motivates them to do it. What actions does this unlock that an AI agent can't do?]

   Why now: [What specific project signal triggered this — a repo milestone, a token move, a community discussion, a shipping streak?]

   Resolution: [Exact YES/NO criteria — what has to happen, by when, how it's verified]

   Scores: Reflexivity X/5 | Viral X/5

   Soon on https://www.hyperstitions.com/ ?
   ```

8. **Log** to `memory/logs/${today}.md`:
   ```
   ## Hyperstitions Ideas
   - **Question:** [the market question]
   - **Coordination target:** [what human action it incentivizes]
   - **Reflexivity:** X/5
   - **Viral:** X/5
   - **Trigger:** [what project signal inspired it]
   - **Notification sent:** yes/no
   ```
