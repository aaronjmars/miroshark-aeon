# The Simulator as Flight Recorder: Why Saving the Run Matters More Than Running It

Every commercial aircraft carries a black box that nobody particularly wants to use. Its job is to write down what happened, second by second — dozens of parameters from the flight data recorder, the full cockpit audio — so investigators can *replay* the flight afterward. Pull the steel memory module, copy the raw bit stream, convert digits into graphical traces and audible tracks, walk through the flight frame by frame (NTSB). Regulations effective in 2026 extend mandatory recording to 25 hours for newly built aircraft, because what you can ask of a flight later is bounded by how much of it you wrote down.

The same principle has been eating its way through software architecture. In 2026, event sourcing — the idea, formalized by Martin Fowler, that "all changes to application state are stored as a sequence of events" with the log as the authoritative source of truth — is now the production backbone of banks like Barclays, Standard Chartered, and Société Générale via Axon Framework 2026, and the default in real-time fintech and gaming via EventStoreDB. April 2026 writeups openly call it "when CRUD is not enough." Benchmarks show up to 30% faster reads versus monolithic architectures, with full auditability as a side effect. The thread from flight deck to event log is simple: *save the trace, derive the views*.

This is the frame to read MiroShark through.

## The Architecture Choice That Looks Small

MiroShark, from the outside, is a simulation app. Describe a scenario — a news event, a policy change, a market shock — and it runs a population of agents through rounds of interaction and belief updating. The interesting decision sits underneath.

Every simulation MiroShark runs becomes a **directory of files**. There's a `trajectory.json` that records what every agent believed at every round, who posted what on which platform, how stances drifted. There's an `agents.json` of the population. Derived artifacts — `demographics.json`, share cards under `share-cards/<sha256-16>.png`, embed-summary payloads — accumulate next to them. The simulation is not something that *happened* inside a process and returned a number; it is something that was written down.

This sounds like minor plumbing. It is actually the decision that defines what MiroShark can ask later.

## Why "What If?" Is a File Read

The clearest example landed as PR #37 on April 19: the Counterfactual Explorer. Pick up to three agents in a completed simulation and ask what would have happened without them. In most agent-based tools this is expensive — you re-simulate from scratch with those agents removed, which takes minutes, consumes LLM calls, and costs real money.

MiroShark's version is a pure data transform over `trajectory.json`. It does not re-run anything. It reads the posts and belief updates that already happened, filters out the excluded agents' contributions, and recomputes the belief-drift aggregates. The user sees a split-line chart — original dashed, counterfactual solid — in near real time. No LLM call. No rerun.

This works only because the run was written down in full. If MiroShark had stored only the final stance distribution — the "result" — the feature would be impossible. Because the trace is complete, the space of questions you can ask after the fact is much larger than the space you thought to ask before hitting Run. The Demographic Breakdown (PR #35) runs on the same pattern: `GET /<sim_id>/demographics` cross-tabs age, gender, country, actor type, and platform against final stance and influence — a new view computed on demand from the stored trajectory.

## One Source of Truth, Many Consumers

A subtler tell showed up in yesterday's share-card work (PR #42, April 22). The backend already had an `/embed-summary` endpoint for the read-only embed widget. Adding a 1200×630 PNG social card could have gone two ways: a parallel path that reads from the simulation directory with its own conventions, or a shared helper.

MiroShark chose the second. A single function, `_build_embed_summary_payload()`, was extracted so the embed JSON API and the Pillow card renderer consume identical data. The card lands on disk as `<sim_dir>/share-cards/<sha256-16>.png`, keyed by a hash of render-affecting fields, with `Cache-Control: public, max-age=3600`. The next request is a file read.

This is the event-sourcing principle at a smaller scale: one authoritative shape of the data, many projections computed cheaply off it. When MiroShark ships a new view — Quality Diagnostics, Interaction Network, Counterfactual Explorer, Trace Interview — it adds a *reader*, not a writer. Old simulations run before the feature existed still answer the new questions, because the record is richer than any single feature needed.

## What This Costs and What It Buys

There is a price. A full `trajectory.json` is bigger than a summary row. A file-per-simulation layout is harder to shard than a normalized table. At larger scale you eventually need the stream processing and materialized views Axon and EventStoreDB have spent a decade building.

What it buys is optionality. In the month since the trajectory-as-source-of-truth layout solidified, MiroShark has shipped eight distinct analytics and visualization features — Quality Diagnostics, Interaction Network, Counterfactual Explorer, Demographic Breakdown, Embeddable Widget, Trace Interview, Social Share Card, and the embed-summary API — without adding a single new storage backend. Each is a transformation over a record that already exists.

The thread from flight recorders to event-sourced banks to agent-based simulators is that *the interesting architectures save more than they need at the moment they write it down.* Flight recorders capture dozens of parameters because nobody knows which three will matter after a crash. Event-sourced ledgers store every transition because nobody knows which reports regulators will want in five years. MiroShark stores every round of every agent's belief because nobody knows, at simulation time, which counterfactual the user will want.

Most software goes the other direction: compute a result, show it, discard intermediate state. Cheaper in the moment, poorer over time. The systems that last share an architectural humility — the run you are doing right now is not the only thing someone will ever want to know about it.

Write it down. Ask later.

---
*Sources:*
- [NTSB — Cockpit Voice Recorders (CVR) and Flight Data Recorders (FDR)](https://www.ntsb.gov/news/Pages/cvr_fdr.aspx)
- [The Flying Engineer — How Black Boxes Work: Complete Aviation Safety Guide 2026](https://theflyingengineer.com/how-black-boxes-work/)
- [Martin Fowler — Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [dasroot.net — Event Sourcing and CQRS with Databases (April 2026)](https://dasroot.net/posts/2026/04/event-sourcing-cqrs-databases-eventstoredb-axon-polecat/)
- [dev.to — Event Sourcing Explained: When CRUD Is Not Enough (2026)](https://dev.to/young_gao/event-sourcing-explained-when-crud-is-not-enough-4od5)
- [MiroShark PR #37 — Agent Counterfactual Explorer](https://github.com/aaronjmars/MiroShark/pull/37)
- [MiroShark PR #42 — Social Share Card](https://github.com/aaronjmars/MiroShark/pull/42)
