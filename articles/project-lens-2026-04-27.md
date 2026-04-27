# Polymarket Settles. Metaculus Scores. Simulators Just Ended.

If you trade an event contract on Kalshi, the contract terms list the **Source Agencies** — the federal agencies, news outlets, or data feeds whose published number Kalshi will read to settle the trade. The list is written into the contract as part of the CFTC self-certification before the market opens. There is no ambiguity about who grades it.

If you trade the same event on Polymarket, the [resolution loop](https://defirate.com/prediction-markets/how-contracts-settle/) runs through UMA's Optimistic Oracle. Anyone proposes an outcome by posting a $750 USDC bond. A two-hour window opens; if nobody disputes, the trade settles. If someone disputes, the question escalates — eventually to a vote of UMA token holders. Adversarial. Mechanical. Public.

If you forecast on Metaculus, you get a [Brier score](https://www.metaculus.com/questions/track-record/) attached to your username. Forecasts at 70% should resolve YES 70% of the time; the deviation from that is your calibration error. The platform's own community prediction sits at 0.111 across thousands of resolved questions — Manifold's at 0.168, individual amateurs at much worse. Your track record is a URL.

Three different mechanisms. Same idea: a forecast isn't a forecast until you can grade it later, in public, against something other than vibes.

## The genre that never built one

Now look at the adjacent genre — agent-based simulators. Tools that take a scenario, populate it with agents that hold beliefs and stances, run a few rounds of interaction, and produce a chart of how a system *would* behave. The output is structurally the same kind of object as a forecast: a claim about a future state of the world.

But the resolution layer that prediction markets and forecasting tournaments spent fifteen years standardizing? It does not exist for simulators. A sim runs, the chart looks compelling, somebody screenshots it, and the loop ends. There is no Source Agency. There is no oracle. There is no Brier score. There isn't even a verified-vs-unverified column on the file system. Every demo is a one-shot — credible at publication, unfalsifiable forever after.

This is why the loudest "did the AI agents predict X" stories of late 2025 and early 2026 always landed as screenshots on Twitter and never as receipts on a dashboard. The receipts surface didn't exist.

## The first simulator with a track record

Today — April 27, 2026 — MiroShark, an open-source agent-based simulator, [shipped one](https://github.com/aaronjmars/MiroShark/pull/47).

PR #47 adds two endpoints. `POST /api/simulation/<id>/outcome` writes a record `{label, outcome_url, outcome_summary, submitted_at}` into `outcome.json` inside the simulation's directory. `GET /api/simulation/public?verified=1` filters the public gallery to runs that have one. Three label values: `correct`, `incorrect`, `partial`. A new route `/verified` renders the filtered set as a gallery hall — colored left-edge accents per outcome label, 📍/⚠/◑ outcome pills clickable through to the receipt URL, a verified stat chip, dynamic empty state.

The publisher of a simulation marks its outcome from the embed dialog: a three-way radio, a 280-character textarea with a live counter, an outcome URL input. The outcome cannot be set on a simulation that hasn't been published — gating prevents grading hidden runs, which would defeat the point.

That is the surface. The interesting part is below it.

## Why this isn't just a tag

The outcome record lives as a JSON artifact on disk, in the same simulation directory as the config, the trajectory, the resolution, and the share-card payload. The simulation directory *is* the schema — public gallery cards (PR #43), share-card OG images (PR #42), and webhook payloads (PR #46) all read from it. The verified-gallery view is a cheap projection on top.

The boring decision matters. A simulation that ran six weeks ago can be retroactively graded without a database migration. The social card, the webhook event, and the verified gallery card never disagree about what the simulation said. And the new artifact carries one quietly load-bearing detail: when `_read_outcome_file()` reads the record from disk, it strips any URL whose scheme isn't `http` or `https`. Defense-in-depth on a public surface. A corrupt `outcome.json` cannot land `javascript:` on a card a stranger clicks.

A few hours after PR #47 merged, [PR #48](https://github.com/aaronjmars/MiroShark/pull/48) merged behind it. Once you have an outcome ledger, the next question writes itself: *who can write to it?* The PR added a `require_admin_token` decorator over `/publish`, `/resolve`, and `/outcome`, with two failure modes that look different on purpose — 503 if the admin token isn't configured (an operator forgot), 401 with a generic "Unauthorized" if the token is wrong (a stranger is probing). Constant-time compare. Seventeen unit tests. The track-record substrate and the auth surface around it shipped on the same afternoon — the same idea from two angles.

## Why it matters that the loop now exists

Outcome-grading is what turned forecasting from an opinion sport into a discipline. Tetlock's Good Judgment Project worked because every forecast had a resolution date and a known-truth source. Brier scores worked because they attached to identities that persisted. Polymarket and Kalshi work because settlement is mechanical and public. The discipline lives in the loop, not in the predictions.

Simulators never had the loop. Their adjacent ecosystems do — [SWE-bench Verified](https://www.swebench.com/) grades autonomous coders against hidden tests; τ2-Bench grades customer-service agents against scripted users — but those grade *agent behavior*, not *predictive theses*. SWE-bench can tell you Claude Opus 4.7 patches 87.6% of issues. It cannot tell you whether your sim of Aave's January rsETH wobble was actually right.

The value of `/verified` shows up later, not at launch. On April 26 — the day before this PR landed — Bankr Terminal v2 cited a MiroShark Aave-vulnerability simulation in a quote-tweet thread estimated at 15 million views. That citation lived on X — not queryable, not filterable, not durable. The page that shipped today is where citations like that one accrete into something a stranger can read as evidence rather than as a screenshot.

A simulator with a track record is a different kind of object than one without. It can be wrong out loud to learn from, right out loud to compound from, partial in public to refine from. That object didn't exist in this genre yesterday. There is now one. The interesting question is which simulator ships the second.

---
*Sources: [How Kalshi and Polymarket settle event contracts — DeFi Rate](https://defirate.com/prediction-markets/how-contracts-settle/) · [Metaculus track record](https://www.metaculus.com/questions/track-record/) · [Metaculus FAQ](https://www.metaculus.com/faq/) · [SWE-bench leaderboard](https://www.swebench.com/) · [τ2-Bench — Sierra](https://sierra.ai/blog/benchmarking-ai-agents) · [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) (838 stars / 158 forks) · [PR #47 — Predictive Accuracy Ledger + `/verified`](https://github.com/aaronjmars/MiroShark/pull/47) · [PR #48 — admin-token auth on mutation surfaces](https://github.com/aaronjmars/MiroShark/pull/48)*
