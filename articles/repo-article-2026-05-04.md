# The Way In: MiroShark's Ninth Surface Points the Other Direction, and Someone Knocks to Build Alongside

For thirteen days the pattern was one-way. Every share surface MiroShark shipped — gallery card, share-card PNG, replay GIF, transcript, RSS feed, trajectory CSV, watch page, gallery search — took a finished simulation and projected it into a different format. Eight readers over one folder. On May 4, two beats land on the same project that together describe the next chapter: PR #71 (merged 12:56 UTC) ships the *inverse* surface — the way *in* — and issue #70 (filed 07:59 UTC) is the first request from another builder asking to bring his own work onto the stack.

## Where the project sits

The day after a milestone is usually quiet. The day after MiroShark's 1K-stars crossing on May 3 looks like that: 1,064 stars / 212 forks / 0 open PRs / 1 open issue / 45 days old. +19 stars and +4 forks in the last 24 hours — slowed from yesterday's +45 / +9 spike, which is what natural cooling looks like after a milestone. `$MIROSHARK` is at $0.000003713 (-5.45% on the day), 0.89× buy ratio, $30K of volume — a mild hangover after May 3's +8.05% session. Bankr Terminal v2's May 3 nod ("most technically impressive micro-cap Base AI") is still circulating on X.

The interesting state isn't in the metrics. It's in the issue tracker and the merge log.

## What landed today

PR #71 — *Shareable Scenario Links* — adds four query parameters to the home page: `?scenario=...&url=...&ask=...&template=<slug>`. A click on `https://miroshark.com/?scenario=Aave%20gets%20exploited%20today` drops the reader at a pre-filled New Sim form. A `?url=https://example.com/post` triggers a one-shot fetch into the same `urlDocs` list a manual fetch would build. A `?template=corporate_crisis` redirects through the existing template-launch flow into `/process/new` with the seed staged. Each parameter validates independently — `MAX_SCENARIO_CHARS=500`, `MAX_ASK_CHARS=300`, `[a-z0-9_-]+` slug whitelist, http(s)-only URL parser, DOMPurify strips HTML and `javascript:` URIs while preserving `\n` so multi-line scenarios survive the round-trip.

The symmetry is the point. A new **🔗 Share as link** button beneath the Simulation Prompt copies the inverse URL from live form state. Every preset card in `TemplateGallery.vue` gets a small **🔗** sibling next to Launch that copies a `?template=<slug>` URL. The dismissible orange-edged banner above the console signals which fields were populated — copy varies per `text` / `url` / `ask` / `mixed` kind so the operator reviews before clicking Launch. Once any field is touched, `router.replace({ path: '/', query: {} })` strips the params so a refresh reflects the *edited* state, not the original shared link.

Pure frontend, zero new deps (DOMPurify was already pinned for the markdown renderer), `npm run build` green in 5.33 s, 27 standalone parser assertions pass on a jsdom-backed harness.

## The inverse surface

What makes #71 qualitatively different from the eight prior surfaces is structural. The first eight all share the same shape: `sim_dir/` is the source of truth, `_build_gallery_card_payload()` is the lookup, the ±0.2 stance threshold makes the rendered labels consistent across formats, each surface is a thin renderer that takes one finished simulation and projects it. Add a new surface, define a renderer, drift-detection test passes.

PR #71 doesn't read from `sim_dir/`. It can't — the sim doesn't exist yet. The ninth surface is the only one whose URL is tweetable *before* a sim has been run. PR #67's "Fork this scenario" buttons on `/share` and `/watch` cover the un-run-from-finished-sim direction (a viewer of a completed sim can launch their own variant); #71 covers the un-run-from-tweet-or-blog-post direction (an author who hasn't run anything can still hand a reader the form pre-loaded with the question). Eight read surfaces, one write — and the write surface is the one that lets the project's URLs propagate without requiring the operator to run the sim first.

## The other knock

While the merge happened at 12:56 UTC, an issue had landed at 07:59. Cyril, who's been building on top of MiroFish (MiroShark's predecessor) for "a few months," opened issue #70 with two proposals: a *Private Impact mode* that swaps the Twitter/Reddit social substrate for relational graphs (employees, clients, partners, family) — extending the OASIS profile with `trust_level`, `equity_tolerance`, `institutional_loyalty` and a new action vocabulary (`CONFRONT`, `COALITION_BUILD`, `SILENT_LEAVE`) — and *MiroResult*, a standalone scoring tool that imports raw simulation JSON and produces prioritized recommendations. The opening line: "I've been building on MiroFish for a few months and just discovered MiroShark."

The two beats describe the same shift on the same day. PR #71 says: the URL is the entry point now, not the screenshot. Issue #70 says: the architecture is the platform now, not the demo. Forty-five days old, 1K stars crossed yesterday, nine surfaces over one folder — and on the day the project ships its first surface that lets external authors instantiate a sim with a link, the first external builder shows up offering to bring his own engine alongside. The substrate stopped being a stream a week ago. Today it started being a fixture.

---

*Sources: [MiroShark repo](https://github.com/aaronjmars/MiroShark) · [PR #71 — Shareable Scenario Links](https://github.com/aaronjmars/MiroShark/pull/71) · [Issue #70 — Private Impact mode + MiroResult collaboration request](https://github.com/aaronjmars/MiroShark/issues/70) · [PR #67 — Live Watch Page (Fork this scenario)](https://github.com/aaronjmars/MiroShark/pull/67) · [PR #69 — Gallery Search & Filtering](https://github.com/aaronjmars/MiroShark/pull/69) · [MiroFish: Swarm-Intelligence with 1M Agents (Medium)](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663)*
