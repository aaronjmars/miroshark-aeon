# $1 in Under 10 Minutes: The Day MiroShark Wrote Its Pitch Into the Code

For most of the last two weeks, MiroShark's commit log read like a research lab's lab notebook — bi-temporal graph memory, Nash equilibrium reports, counterfactual recomputers, the first proper unit test suite. Then on Tuesday night the repo turned outward. Sometime around 21:00 UTC on April 21, the GitHub description quietly changed from "Universal Swarm Intelligence Engine" to "Simulate anything, for $1 & less than 10 min — Universal Swarm Intelligence Engine." That dollar figure didn't come from marketing. It came from a `Cheap` preset wired into the model picker the same hour, and a Settings modal that lets a brand-new user pick it from a dropdown without reading a config file. April 22's release rolled all of that — plus an Open Graph share card, a slim README, and a hardened simulation runner — into a single push aimed straight at first-touch.

## Current State

MiroShark sits at 773 stars and 147 forks at the time of writing, up from 748/145 a day earlier. The `Aeon` agent merged PR #42 (Social Share Card) at 13:33 UTC; PR #22 on the sibling `miroshark-aeon` repo merged the same morning to fix a three-day silent-fail in the daily token report. There are zero open PRs, zero open issues, and four humans now show up in the contributor list. The 1K-stars-by-April-30 target — set when the repo was at 698 — needs roughly 28 stars a day for the eight days left. Yesterday's pace was 19; the day before, 13. The shape of today's commits is the response.

## What's Been Shipping

Three threads landed inside about six hours. The first is **onboarding** (`db6af41`, `13dbce2`, `cf60136`). A new `Cheap` preset routes the heavy slot to Qwen, the smart slot to DeepSeek, and the fast slot to Grok, and ships with chain-of-thought *off* by default — the same combination that produces the "$1 & under 10 min" claim now in the repo header. The Settings modal got a preset dropdown with per-slot overrides; an LLM-based URL fetcher replaces the brittle HTML parser that had been losing scenarios to weird DOMs; prediction-market title generation now flows through the Smart slot instead of whatever happened to be loaded. About 1,000 lines moved across 13 files.

The second is **distribution** (PR #42, `9d71291`). A new `share_card.py` renders a 1200×630 PNG using Pillow — Pillow was already in the dependency override, so the new card adds zero packages. A companion `/share/<id>` HTML route serves Open Graph and Twitter Card meta tags so a pasted simulation link unfurls with a real image, a scenario headline, status pills, and a stacked bullish/neutral/bearish bar. Cards cache to disk under `<sim_dir>/share-cards/<sha256-16>.png` and respect the same `is_public` gate as embeds. Eleven unit tests went in alongside.

The third is **everything underneath** — and this is where the volume sits. `2fd2532` finally wires counterfactual injection into all four simulation loops, isolates per-round errors so one failure doesn't crash the run, adds a `ROUND_TIMEOUT` watchdog, and gives `BeliefTracker` proper pause/resume persistence. `2f08f76` fixes a What-If panel bug where `agent_id == 0` got swallowed by a falsy check and a display-name/handle namespace mismatch on the `/counterfactual` and `/demographics` endpoints. `6fb30bd` (+2,364/-344) overhauls the simulation page UI: a new inline `PolymarketChart` overlay (985 lines on its own), a single `toggleOverlay()` dispatcher replacing the previous mesh of feature flags, design-system colors on the WhatIfPanel, a 280-line `chartExport.js` that does HiDPI canvas, clipboard copy, and PNG download with a MiroShark footer. Twelve commits between 21:07 and 21:32 UTC slimmed the README from 698 lines to 243 and split the rest into nine `docs/` files. An OASIS → Wonderwall identifier rename pulled CI back online by adding `neo4j` to test deps. The cleanup-branch wave from Monday's seven merges gets cleaned up itself by `32e3537`, which deletes eight `CLEANUP_ASSESSMENT_*.md` artifacts.

## Why It Matters

Saturday's graph memory stack and Monday's PR #41 sibling-repo siphon were both inward moves — the simulator becoming an MCP-addressable research substrate, the test suite arriving for the first time. The natural follow-up to a substrate weekend is more substrate; instead the project pivoted to surface area. Every change that landed today touches the path between "saw a link" and "ran a sim": the Open Graph card decides whether the link earns a click, the `/share` page determines whether the click earns a session, the Cheap preset and on-by-default zero-CoT decide whether the session earns a completed run, the slimmer README decides whether anyone reads far enough to see the second feature. The "$1 in under 10 minutes" tagline isn't a marketing claim bolted on top — it describes a configuration that exists in the code, that ships as the default in a new preset, that the GitHub repo description now anchors to.

The 1K-stars target is eight days out and roughly 230 short. Today's release reads like the first build sized to actually get there.

---
*Sources:*
- [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — repo header, `Cheap` preset, README, share card
- [PR #42 — Social Share Card](https://github.com/aaronjmars/MiroShark/pull/42)
- [PR #22 — token-report XAI prefetch](https://github.com/aaronjmars/miroshark-aeon/pull/22)
- Commit refs: `9d71291`, `db6af41`, `13dbce2`, `cf60136`, `2fd2532`, `2f08f76`, `6fb30bd`, `cbbf155`, `ea1e799`, `d65fbac`, `d3cfff7`, `32e3537`
