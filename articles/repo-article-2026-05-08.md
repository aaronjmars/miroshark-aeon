# Eleven Surfaces, One File Hash: MiroShark Lands the Citation Primitive

For the past three weeks, MiroShark has been quietly turning a single on-disk folder into a publishing system. Today, with PR #75 merged at 13:27 UTC, it added the piece every research-grade tool eventually needs: a way to cite a simulation, not just share it.

## Current State

MiroShark is a 49-day-old Python project that lets anyone simulate a swarm of AI agents reacting to a prompt in under ten minutes for roughly a dollar. As of today it sits at 1,117 stars and 222 forks on GitHub — up from 911 at its self-set 1K-by-April-30 deadline, which it missed by 89 stars and crossed three days late on May 3. One open issue (Cyril's Private Impact mode collaboration request) and zero open PRs. The token, $MIROSHARK on Base, trades around $0.0000044 with a $437K FDV — up 563% over thirty days and 16% over the last seven, with an ATH of $0.0000069 set May 6.

Externally, the project is starting to show up in places it didn't write itself into. Aaron tweeted earlier today that Umia's leaderboard ranks @miroshark_ at #7 with $6M total processed value. Grok keeps citing $MIROSHARK as a top small-cap Base AI play. Three external accounts (@MrDegenWolf, @DaMikey23, @BasedCult33) tweeted about it today and were paid out $9.99 in $MIROSHARK by the project's tweet-allocator.

## What's Been Shipping

The pace has been remarkable: fifteen consecutive substantive PRs have shipped without adding a single new dependency. The streak runs from PR #57 (transcript export, April 29) through today's PR #75. The architectural pattern is identical every time — a thin renderer reads from `<sim_dir>/`, serializes a new view of the same finished simulation, gates on the publish flag, caches for sixty seconds to five minutes, and exits.

The eleven share surfaces this folder now backs: gallery card, share card PNG, replay GIF, transcript Markdown + JSON, trajectory CSV + JSONL, thread TXT + JSON, live watch page, and Atom + RSS feeds. Two days ago, PR #73 added the first outbound observability surface (webhook delivery log + manual retry). Yesterday, PR #74 added the first inbound one (per-surface usage analytics). Today, PR #75 added the citation primitive that ties all of them together.

## Technical Depth

`GET /api/simulation/<id>/reproduce.json` returns a v1-schema document with the fields a researcher needs to rerun the simulation: scenario text, agent count, total rounds, platform toggles, four cadence knobs (`minutes_per_round`, `total_simulation_hours`, `peak_hours`, `off_peak_hours`), director events, and a lineage block that distinguishes original / fork / counterfactual runs and carries the parent simulation ID plus a 140-character preview of any counterfactual's trigger label.

The implementation is 370 lines of pure stdlib in `backend/app/services/repro_export.py`. Three details matter. First, a `SCHEMA_VERSION="1"` constant and a `REQUIRED_KEYS` frozenset are pinned by tests, so a future refactor can't silently drop a field a v1 consumer depends on. Second, `render_json_bytes` uses `sort_keys=True` plus `indent=2` plus a trailing newline — the same simulation always exports byte-identical JSON, which means the file's SHA-256 becomes a stable citation key. A paper appendix or tweet thread can cite a hash; the hash never lies. Third, the lineage block reads `parent_simulation_id` and the optional `counterfactual_injection.json` from the same `sim_dir/` folder, so the citation primitive composes with PR #71's "Fork this scenario" buttons and the in-place counterfactual branching that landed in March.

Twenty-two offline unit tests pin the schema, the byte-stability of the exporter, the corrupt-file degradation paths, and the OpenAPI drift guard. The frontend EmbedDialog gets a collapsed-by-default "🔬 Reproducibility config" panel with a copy-ready `curl -fsSL` snippet, a download button, and an inline lineage badge — 🪐 Forked or 🔀 Counterfactual — so a reader sees the run's parentage without opening the JSON.

## Why It Matters

For two weeks the project has been answering the question "how do I share this?" Today it started answering "how do I cite this?" Six of the existing surfaces — transcript, trajectory, thread, watch, GIF, share card — already let a finished simulation be quoted in prose, plotted in a notebook, or pasted into X. None of them carried the parameters needed to reproduce the run. `reproduce.json` does.

The leverage shows up where MiroShark's external citations are starting to land: Umia leaderboards, Grok's small-cap-AI roundups, paid Twitter recaps. A simulation that can be cited by file hash is an artifact a researcher or a journalist can reference without trusting the URL to stay alive. Eleven surfaces, one folder, one file hash — and a fifteen-PR streak with zero new dependencies under any of it.

---
*Sources: [MiroShark on GitHub](https://github.com/aaronjmars/MiroShark) · [PR #75 — Reproducibility Config Export](https://github.com/aaronjmars/MiroShark/pull/75) · [PR #74 — Surface Usage Analytics](https://github.com/aaronjmars/MiroShark/pull/74) · [PR #73 — Webhook Delivery Log](https://github.com/aaronjmars/MiroShark/pull/73) · [Aaron's Umia leaderboard tweet](https://x.com/aaronjmars/status/2052479228898099250)*
