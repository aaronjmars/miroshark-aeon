# The Folder Won: Why 2026's Most Interesting Tools Keep Choosing Files Over Databases

In November 2019, four researchers at Ink & Switch published an essay called "Local-first software." It made an unfashionable claim — that the cloud-first, database-as-source-of-truth architecture dominating the prior decade was actually fragile, and that "old-fashioned apps continue to work forever, as long as you have a copy of the data and some way of running the software." The piece circulated, was widely admired, and was largely ignored in production. It is being re-litigated now.

Six and a half years later, in April 2026, a developer essay on dev.to declared that "tolerance for fragile online-only systems is finally over" and named local-first as the architectural pattern of the year. DuckDB — an analytics engine that runs SQL directly against Parquet files without importing them into anything — has eaten enough of the small-analytics market that it's now the default tool taught alongside pandas in 2026 data-engineering tutorials. Parquet files are roughly 60–70% smaller than equivalent SQLite databases for analytical workloads and need no setup, no migrations, no schema evolution. The new stack quietly unwinds the old one.

This is the backdrop for a small but concrete architectural decision being made by almost every interesting open-source tool shipped in the last six months: keep the file. Not as a backup. Not as an export format. As the actual unit of memory.

## The Filesystem as Schema

Look inside a single simulation run on MiroShark, an open-source multi-agent simulation engine that crossed 722 GitHub stars this morning, 25 days after launch. There is no Postgres. There is no MongoDB. There is one folder per simulation, named by a UUID, and inside it a small collection of JSON files. From the production source in `backend/app/api/simulation.py`:

- `state.json` — current state of the run
- `simulation_config.json` — scenario, agent counts, model selection
- `reddit_profiles.json` / `twitter_profiles.csv` — the personas
- `run_state.json` — round-by-round progress
- `trajectory.json` — every agent's belief position at every round
- `resolution.json` — the YES/NO outcome and computed accuracy (PR #22)
- `quality.json` — participation rate, stance entropy, convergence speed (PR #32)
- `demographics.json` — the new cross-tab cache (PR #35, shipped today)
- `meta.json` — report metadata

The pattern is consistent. Every new analytics feature shipped over the last ten days adds a file to the folder, not a column to a table. When a user requests the demographic breakdown of a completed run, the API endpoint computes it once, writes `demographics.json`, and serves it from disk on every subsequent request. A `?refresh=1` query parameter forces a recompute. There is no migration. There is no contention between writers. There is no backfill job to run when the schema changes — there is no schema.

## Why This Choice Matters More Than It Sounds

Three things become possible the moment a simulation is a folder of files instead of a row in a database, and none of them are obvious until you look at the features that have shipped on top.

**Forking becomes a directory copy.** PR #17, the simulation fork feature, lets a user duplicate any historical run, override the scenario, and re-run with new settings. The implementation is essentially `cp -r`. There is no "create a new entity, then deep-clone the foreign keys, then update the join table." There is one folder, then there are two folders, then one of them runs. Forking is what ten thousand researchers will do with any useful simulation, and it is trivially cheap because the unit of memory was chosen well.

**Embedding becomes a URL.** The widget shipped today (PR #34) reads its `embed-summary` payload from the same files the main UI uses. There is no separate "embed-friendly database view." The same trajectory and quality JSON that powers the analyst's dashboard powers the iframe rendered inside someone else's Substack. A user can also download the entire folder and replay the run offline — which is exactly the property the Ink & Switch essay was originally advocating for.

**Analytics layers compose without a meeting.** Each cached file is a tiny atomic unit. Quality Diagnostics (PR #32), Agent Interaction Network (PR #33), and Demographic Breakdown (PR #35) all shipped in nine days because none of them had to negotiate with a shared database schema. They each grab `trajectory.json`, compute their own metric, write their own file, and stop. A team of one ships infrastructure that a team of five would otherwise be coordinating around.

## The Bigger Bet

The DuckDB community has a phrase for this: *small data is most data*. The argument is that the median analytical workload runs on a few hundred megabytes, fits in memory, and gets dramatically simpler if you stop pretending it's the workload Snowflake was built for. MiroShark is making the same bet at the application layer: the median simulation is a folder, and almost every interesting feature can ship as another file inside that folder.

This sounds like a small architectural choice. It is actually the choice that decides whether a tool survives the company that built it, whether its outputs are citable, whether researchers can fork it, and whether the analytics layer ships in nine days instead of nine months. The folder is back as a first-class data structure in a way it has not been since the early 2000s — and the projects making this bet now are building on the same insight Ink & Switch published into a quiet room six years ago. The room is no longer quiet.

---

*Sources: [Ink & Switch — Local-first software](https://www.inkandswitch.com/essay/local-first/); [DEV Community — The Architecture Shift: Why I'm Betting on Local-First in 2026](https://dev.to/the_nortern_dev/the-architecture-shift-why-im-betting-on-local-first-in-2026-1nh6); [DuckDB — CSV Files: Dethroning Parquet?](https://duckdb.org/2024/12/05/csv-files-dethroning-parquet-or-not); [KDnuggets — Building a Modern Data Analytics Stack with Python, Parquet, and DuckDB](https://www.kdnuggets.com/building-your-modern-data-analytics-stack-with-python-parquet-and-duckdb); [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark); [PR #17 Simulation Fork](https://github.com/aaronjmars/MiroShark/pull/17); [PR #32 Quality Diagnostics](https://github.com/aaronjmars/MiroShark/pull/32); [PR #33 Interaction Network](https://github.com/aaronjmars/MiroShark/pull/33); [PR #34 Embeddable Widget](https://github.com/aaronjmars/MiroShark/pull/34); [PR #35 Demographic Breakdown](https://github.com/aaronjmars/MiroShark/pull/35).*
