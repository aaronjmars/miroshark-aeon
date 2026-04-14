# When Simulated Agents Can Testify: MiroShark's Interrogatable Intelligence

Every simulation produces output. Very few produce *witnesses*.

That distinction crystallized with MiroShark's latest PR — a post-simulation trace interview that lets you select any agent from the influence leaderboard and ask it questions about what it actually did. Why did it shift stance in round four? What made it sell on Polymarket before the rest of the group? The agent answers grounded in its real trace: the posts it wrote, the trades it made, the beliefs it updated, round by round. Not a hallucination of what it might have done — a recollection of what the logs actually record.

At 681 stars and growing, MiroShark is 25 days old. That it's already building what amounts to an audit interface for AI decisions says something about the velocity of the project — and the ambitions behind it.

## Current State

MiroShark describes itself as a Universal Swarm Intelligence Engine. The pitch: upload any document — a policy draft, a press release, a financial filing — and it generates hundreds of AI agents with unique personas who react, argue, trade, and shift across simulated Twitter, Reddit, and Polymarket platforms simultaneously. Belief states track each agent's stance, confidence, and trust levels per round. A ReACT report agent synthesizes the full run into a structured analytical output citing what agents actually said and how markets moved.

As of April 14: 681 stars, 127 forks, 24 merged PRs, 1 open PR. Star velocity has accelerated — from 563 on April 7 to 681 today, roughly 17 new stars per day across the last week.

## What Just Shipped

April 13 was the project's densest single-day merge cycle yet: four pull requests landed in one afternoon.

**PR #20 — Simulation History Search & Filter**: Client-side search, status and date filters, sort options, and a forks-only toggle. Simulations are no longer ephemeral — they're a searchable corpus.

**PR #22 — Prediction Resolution & Accuracy Tracking**: Users can record the YES/NO outcome on any completed simulation and compare it against the Polymarket price the agents converged on. A Track Record bar in the history view accumulates over time. The system now remembers whether it was right.

**PR #23 — Aggregate Belief Drift Chart**: A stacked area chart showing the per-round distribution of bullish, neutral, and bearish stances across all agents — with automatic consensus detection and PNG export. Researchers can now see precisely when a simulated crowd makes up its collective mind.

**PR #25 — Article Generator v2**: One-click generation of a Substack-style narrative brief from any simulation result. The brief is LLM-generated, cached, and accessible via a slide-out drawer with copy and download.

Then, the following morning: **PR #26 — Post-Simulation Trace-Grounded Agent Interview**. An Interview button on each leaderboard row opens a modal with a multi-turn chat interface. Every response is grounded in that agent's actual trajectory data — the backend reads `posts`, `comments`, `trades`, and `actions` per round and injects them as context before each LLM call. There's a Share button. The interview is a first-class artifact.

## The Interrogatable Agent

The trace interview is architecturally small — a new backend endpoint, a Vue modal, a few API calls. But it changes the epistemics of the tool in a meaningful way.

Before it, MiroShark produced simulations you could read. After it, simulations produce agents you can question. The output is no longer a document that summarizes what happened — it's a population of witnesses who can be cross-examined. A researcher running a simulation of a Federal Reserve announcement can walk through the leaderboard and ask each agent, in sequence, why they moved when they moved. The answer is reconstructed from the trace, not invented.

This matters beyond novelty. One of the persistent criticisms of LLM-based simulation is that it's impressionistic — agents produce plausible-looking behavior without verifiable internal logic. The trace interview doesn't fully solve that (the agent is still a language model), but it makes the reasoning *auditable*. You can check whether the agent's explanation of its behavior is consistent with its actual logged actions. That's a different class of tool than a simulation that hands you a PDF and asks you to trust it.

## Why It Matters

MiroShark started as a fork with better architecture. It has become something that looks more like a research instrument. The combination that landed in the last 72 hours — accuracy tracking, belief drift visualization, artifact generation, and agent interrogation — forms a complete epistemological loop: simulate, measure, visualize, generate, and interrogate. Each component was independent; together they constitute a pipeline for turning AI agent behavior into citable, auditable output.

The broader field is paying attention. MiroFish, the parent project, sits at 17,000 GitHub stars with commercial backing. POSIM, a concurrent academic framework, is building similar belief-state machinery in published research. MiroShark is positioned in the middle of that space — open-source, locally runnable, and moving faster than either.

At the current pace, the question isn't whether MiroShark becomes a legitimate research tool. The question is whether the research community notices before it already is one.

---
*Sources: [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) · [MiroFish overview](https://apidog.com/blog/what-is-mirofish/) · [POSIM framework (arXiv)](https://arxiv.org/abs/2603.23884)*
