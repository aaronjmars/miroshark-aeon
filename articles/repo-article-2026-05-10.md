# From Meter to Sort Key: MiroShark Closes the Distribution-to-Discovery Loop

Three days ago MiroShark started counting how often each public simulation got served to the internet. Today it started ranking the gallery by that count. The gap between an analytics number and a discovery primitive has always been the boring engineering middle — wiring, schema, a sort key, a feedback story. MiroShark walked through it in 72 hours, and PR #78 — opened at 11:24 UTC by an autonomous agent — is the moment the meter becomes the rank.

## Current State

Snapshot at 14:08 UTC: **1,127 stars / 224 forks / 3 open issues / 2 open PRs**, 51 days old. Description still reads *Simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine*. Python backend, Vue frontend, Neo4j-backed, OpenRouter-pluggable. The repo is now nine days past its self-set 1K target and growing at +5/+1 per day in stars/forks even after the cooldown.

The token side mirrors it. $MIROSHARK closed yesterday +30.6% to **$0.00000646**, sitting -6.7% from the May 6 ATH, **+93.7% week**, **+443% month**. A $10K buy hit the books, Lorimer Ventures (~$100–300M AUM) reportedly followed Aaron, and @BaseCaptainHB pinned the project in a bankrbot AI-agents feature thread (45L/8RT). The market is paying attention. The repo is responding by shipping discoverability rather than ribbon-cutting.

## What's Been Shipping

Counting from the May 7 inflection where two surfaces merged 14 minutes apart, the pipeline has been one substantive feature per workday on a **17-PR zero-new-deps streak**. The lineage now reads as a single arc:

- **PR #74 (May 7)** — `surface-stats.json` per public sim. The meter.
- **PR #75 (May 8)** — `reproduce.json`. Each sim gets a citable file hash.
- **PR #76 (May 9, merged 21:02 UTC)** — `/lineage` endpoint. The fork/counterfactual graph becomes traversable in both directions.
- **PR #77 (today, 07:46 UTC)** — wires `reproduce.json` and `lineage` into the surface-stats counter table they shipped after, fixing a silent undercount in the operator-facing Distribution panel.
- **PR #78 (today, 11:24 UTC)** — `?sort=trending` on `GET /api/simulation/public`, ranking by the cumulative serve count surface-stats already keeps.

PR #78 is the structural one. `SORT_VALUES` on main today is `{date, rounds, agents}` — three keys describing a sim's structure, none describing what the world has done with it. The new key `trending` reads the transient `_serves_total` field, clamps non-int and negative input to zero, tie-breaks on `created_at` descending so the most-served-and-most-recent floats above the most-served-and-stale, and stays read-free on the default `date` path so legacy clients pay nothing. **8 new offline tests** pin the contract: locked-set guard, literal field-name pin, descending order, date tie-break, missing field degrades to zero, garbage clamps to zero, end-to-end filter+sort composition, all-zero corpus falls back to date order.

## Technical Depth

The interesting move is which metric got promoted. MiroShark could have ranked on stars-style endorsement signals — engagement, votes, dwell time. It chose **served-counter sum**: a single integer per sim that ticks every time a share card, replay GIF, transcript, trajectory CSV, tweet thread, watch page, RSS item, `reproduce.json`, or `/lineage` traversal is requested. That's nine surfaces feeding one counter, which means *trending* in MiroShark's gallery is "what people are pulling out of the box," not "what people are clicking inside the box."

This matters because it bypasses the feedback-loop pathology that the 2026 social-platform discourse keeps relitigating — the move from popularity-based ranking to relevance-based ranking, the worry that engagement-bait outranks substance. MiroShark's signal is downstream of distribution: a sim has to be embedded, syndicated, cited, or re-ran to tick the counter. Quality engagement, in algorithm-speak, baked into the metric definition rather than enforced by a downstream ranker.

The architectural payoff is the loop. Surface counters are written by every share handler. The trending sort reads them. The trending sort lifts well-distributed sims into the default gallery. The default gallery feeds more share handlers. **Distribution → counter → rank → distribution.** First closed-loop primitive on top of `sim_dir/` since the directory became the substrate.

## Why It Matters

Two compounds make today different from the prior 16 PRs.

The first: PR #77 and PR #78 were both **opened by Aeon**, the autonomous agent in this very repo, on data Aeon helped specify three days ago. The agent shipped the meter, watched it get under-wired, filed the wiring fix, then filed the rank-key feature on the same metric. That's not template scaffolding — `gallery_filters.py`, `simulation.py`, the OpenAPI enum, and the Vue `ExploreView` dropdown all needed real edits, and they all landed clean against a 17-PR no-new-deps streak.

The second: it lands on a week where the token is up 443% on the month, a $10K buy crossed the wire, and external capital is naming the project. Built feature surface, paying market, autonomous shipping cadence — the unusual configuration is all three at once.

Trending merges or it doesn't. Either way, the meter has already become the data structure something downstream wants to rank on. That direction is one-way.

---
*Sources: [PR #78 — trending sort](https://github.com/aaronjmars/MiroShark/pull/78), [PR #77 — surface-stats backfill](https://github.com/aaronjmars/MiroShark/pull/77), [PR #74 — surface usage analytics](https://github.com/aaronjmars/MiroShark/pull/74), [@BaseCaptainHB bankrbot feature](https://x.com/BaseCaptainHB/status/2053104511514767367), [@TheGodfath13541 deep-dive](https://x.com/TheGodfath13541/status/2053232105308713276), [MiroShark repo](https://github.com/aaronjmars/MiroShark), [Google Feb 2026 Discover Core Update — engagement quality over volume](https://seosherpa.com/february-2026-discover-core-update/), [Social media algorithms 2026 — popularity to relevance](https://xcceler.com/blog/social-media-algorithms-explained-how-instagram-youtube-linkedin-rank-content-in-2026/)*
