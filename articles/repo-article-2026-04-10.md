# Inside the Black Box: MiroShark's Observability Week Turns a Demo into Infrastructure

Three weeks ago, MiroShark was a remarkable prototype — a document-to-simulation engine that could spin up 500 AI agents arguing on fake Twitter. This week, it started looking like production infrastructure. Between April 3 and April 10, the project shipped a complete observability system, a 2x performance overhaul, simulation forking, side-by-side comparison mode, and drew its first external community contribution. The result is a tool that's no longer just impressive to run — it's designed to be extended, debugged, and trusted.

## Current State: 642 Stars and Accelerating

MiroShark currently sits at 642 stars and 116 forks on GitHub — up from 563 just four days ago. That's 26 new stars on April 10 alone. The project's description, "Universal Swarm Intelligence Engine," increasingly earns that label: this week's commits touched the simulation runner, the frontend, the knowledge graph pipeline, the build system, and the developer tooling layer simultaneously.

Two open pull requests capture where things stand. One (PR #20) adds client-side search, status filters, date filters, sort options, and localStorage persistence to the simulation history view — making the history database feel like a real archive, not just a list. The other (PR #18) is a community-contributed CLI/TUI layer with ICP graph caching and `/runs` commands, submitted by an external contributor. That second PR matters: it's the clearest sign yet that developers outside the core team are reading the code and wanting to build on top of it.

## What Shipped This Week

The headline commit landed April 8: a unified observability system exposing every LLM call, agent decision, and graph build step in real time. Accessible via a debug panel (Ctrl+Shift+D), the system streams color-coded events over SSE, provides a table of all LLM calls with model, token counts, and latency, and renders per-agent decision timelines showing exactly what each agent observed, what the LLM responded, what action was parsed, and whether it succeeded. With `MIROSHARK_LOG_PROMPTS=true`, full prompt and response bodies are logged. This is not typical for a project at this age or star count.

The same day brought a performance push: NER prompt trimming, chunk size doubled, NER model routing, and a frontend network panel rewrite that cut graph build time in half. A separate commit added lazy route loading, build compression, response gzip, and JSONL scan optimization. The effect is a noticeably faster experience from document upload through first simulation round.

Earlier in the week, Simulation Fork shipped (PR #17, merged April 9). From the history view, any completed simulation can now be forked — profiles copy instantly, a new scenario can be set, and the forked simulation gets a ⑂ badge so lineages stay traceable. Combined with Comparison Mode (PR #13, merged April 7) — which renders two simulations side by side with a divergence score and rank delta badges — MiroShark now supports something closer to experimental iteration than one-off runs.

## The Observability Decision and What It Signals

Building first-party observability into a simulation engine is an unusual choice. Tools like Langfuse and OpenTelemetry exist precisely because most LLM applications bolt observability on after the fact, usually with an external service. MiroShark's decision to ship a native debug panel, SSE event stream, and per-agent decision timeline as core features — not integrations — tells you something about how the project sees itself.

The implication is that MiroShark is being designed for people who will extend it. When you can see every LLM call's input, output, latency, and token cost alongside the agent decision it produced, you can actually reason about why a simulation went the way it did. You can tune prompts, identify bottlenecks, and trace a belief state shift back to a specific round and model call. That's the level of introspection researchers and engineers need when they're building on top of a system rather than just running it.

The CLI/TUI contribution from the community reinforces this: a developer looked at the architecture, found a missing interface layer, and built it. That's a different kind of engagement than starring a repo because a tweet went viral.

## Why It Matters

The multi-agent simulation space is crowded with demos. What separates durable tools from viral experiments is the moment a project starts treating itself as infrastructure — adding observability, investing in performance, designing for extensibility. This week was that moment for MiroShark.

At 642 stars and 21 days old, MiroShark is accumulating the properties of a platform: a knowledge graph backend, a cross-platform simulation engine, cloud deploy options, an LLM selector UI, forking and comparison primitives, a public share layer, and now first-party debug tooling. The question isn't whether it works anymore. The question is what people build with it next.

---
*Sources: [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) · [MiroShark on Microlaunch](https://microlaunch.net/p/miroshark)*
