# The Last Format: MiroShark Closes the Share-Anywhere Trio on Deadline Eve

April 29 is the day before MiroShark's self-set 1K-stars-by-April-30 deadline. The repo sits at 865 stars and 167 forks — a hundred-and-thirty-five stars short with a single day to land them. With that shape of math, today's headline merge had to pull weight beyond *another file format on disk*. It does. PR #57 — Simulation Transcript Export — is the third and last quote-friendly share format to land on top of the same on-disk simulation folder. It closes a three-week arc of distribution surfaces the project has been building under the same one-line tagline: *Simulate anything, for $1 & less than 10 min.*

## Current State

aaronjmars/MiroShark is 40 days old. Python and Vue, four contributors, zero open PRs, zero open issues, MIT-licensed. The README has settled into a shape that scans in 30 seconds: install line, three preset cost tiers (Cheap / Balanced / Quality), gallery link, MCP block, Swagger UI link. $MIROSHARK closed Tuesday at $0.000002909, -39.2% from Monday's $0.000004784 ATH but +388% over 30 days — orderly pullback on light volume, not capitulation. The 1K-stars target announced April 11 is tomorrow's deadline; the math says it almost certainly slips. What does *not* slip is the surface that's been getting built for it.

## What's Been Shipping

Today's three merges:

**13:25 UTC — PR #56: Observability pagination guard.** A small fix that swaps `int(request.args.get("from_line"))` for `request.args.get("from_line", default=0, type=int)` on `/events` and `/llm-calls`. Bad input no longer 500s; non-numeric query strings come through as the default. Forty-eight hours ago `/llm-calls` was a Langfuse-adjacent diagnostic; today it's robust enough to leave on a public dashboard.

**13:40 UTC — PR #58: CI fix splitting env-compact into a stdlib-only module.** Yesterday's PR #55 dropped agent-env input tokens by 57%, but its tests imported `wonderwall.social_agent.agent_environment`, which transitively pulls camel → numpy → torch. CI's thin install list omits numpy. Three iterations to land cleanly: add numpy → still failed (transitive torch); move helpers to `wonderwall.social_agent._env_compact` → `wonderwall/__init__.py` eager-imports the heavy chain anyway; finally land them in `backend/lib/env_compact.py`, sibling of `wonderwall/`, bypassing package init entirely. New top-level location for any future stdlib-only helper that needs to be importable from CI without dragging the camel surface in.

**13:43 UTC — PR #57: Simulation Transcript Export.** The merge of the day. `GET /api/simulation/<id>/transcript.md` and `transcript.json` — both publish-gated with the same `is_public` check as the share card, both 60-second-cached. The Markdown form opens with a YAML front-matter block (`sim_id`, `scenario`, `agent_count`, `total_rounds`, `consensus_label`, `quality_health`, `outcome_label`) so Notion, Obsidian, Bear, and Substack pick it up as page metadata; the body is one `## Round N` section per recorded round, with each agent post block-quoted and tagged with the agent's stance. The JSON form is pretty-printed for SDK and pipeline consumers. EmbedDialog gains a third row beneath the share-card and replay-GIF rows: Download .md, Download .json, copyable Markdown URL. 80-round Markdown cap with first-20 + last-20 preservation and a "skipped N rounds" annotation pointing at the JSON form for the full series; JSON keeps every round.

## Three Formats, One Folder

The under-the-hood pattern is the part worth pausing on. The transcript renderer is pure standard-library Python: it reads `trajectory.json`, `reddit_profiles.json`, `polymarket_profiles.json`, `quality.json`, `resolution.json`, and `outcome.json` — every one of which is already on disk inside the simulation folder, written by other parts of the engine. No new schema, no DB migration, no join. It uses the same ±0.2 stance threshold to label agents as bullish / neutral / bearish that the gallery, the share card, the replay GIF, and the webhook all use. Five surfaces, one threshold, one folder. *Sim_dir IS the schema* — the architectural beat the team has now hit weekly since the gallery shipped April 23.

That same pattern is what lets the share-anywhere story close cleanly. April 22's share card (PR #42) gives Twitter / Discord / Slack a still preview that auto-unfurls. April 28's replay GIF (PR #50) gives those same surfaces motion — Discord and Slack auto-play GIFs from a direct URL. April 29's transcript gives the prose-quoting channels — Hacker News comments, blog posts, Notion writeups, Substack issues — a Markdown form that lands in their editors *as a document* rather than a screenshot. Three formats; three audiences; one underlying folder.

## Why It Matters

The 1K-stars target probably misses by tomorrow. What it produced is more durable: a 40-day-old simulator with three orthogonal share surfaces, four machine-readable contracts (MCP, OpenAPI, Webhook, transcript JSON), and a `sim_dir/` directory whose layout has now outlasted three consecutive weeks of new endpoints reading off it without needing to change. The transcript is the last piece a serious researcher needs to quote a run inline in a paper or a long-form post. With it, MiroShark has stopped being a thing you screenshot and started being a thing you cite.

---
*Sources: [PR #56](https://github.com/aaronjmars/MiroShark/pull/56), [PR #57](https://github.com/aaronjmars/MiroShark/pull/57), [PR #58](https://github.com/aaronjmars/MiroShark/pull/58), [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)*
