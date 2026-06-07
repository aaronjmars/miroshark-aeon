# The Shape of the Corpus Now Has Its Own Endpoint

For three months `/api/stats` has answered a single question about MiroShark's corpus: *how big is it?* Total simulations, total views, total projects, a `consensus_distribution` slot that gestures at the leaning of the public set. The number that grows. PR #151 merged at 15:41:37 UTC today and added the companion question the totals never answered: *what does the corpus look like?* Eight minutes and ten seconds later PR #150 merged too, and for the first time in seventeen days the open Aeon-built PR queue on the watched repo dropped to zero.

## Size and Shape Are Different Numbers

`GET /api/stats/distribution.json` walks the same publish-gated set of completed simulations that `/api/stats` counts — `is_public == true` AND `status == "completed"` — and buckets each contributing sim across four dimensions. `by_direction` splits the corpus into bullish, neutral, and bearish using the same plurality-with-`bullish > bearish > neutral` tie-break the per-sim `signal.json` uses. `by_confidence` cuts on inclusive lower edges: `high` is `confidence_pct >= 70`, `medium` is `40 <= confidence_pct < 70`, `low` is below forty. `by_quality` reads `quality.json.health` case-insensitively into the four-tier ladder. `by_round_count` bins on snapshot length — short under ten, medium ten to twenty, long over twenty. Two scalar additions, `avg_confidence_pct` and `avg_total_rounds`, round out the envelope.

A sim that contributes one row to `/api/stats.total_sims` contributes one row to `/api/stats/distribution.json.total_analyzed`. Both surfaces call the same `signal_service.compute_signal`, walk the same trajectory, and resolve ties the same way, so the corpus a researcher quotes from one is byte-identical to the corpus they bucket from the other. One source of truth, two angles.

## The Four-Audience Brief Is Written Into the PR

The PR body names four readers and what each is supposed to do with the new envelope. A researcher citing MiroShark in a methods section gets a number they can paste — *41.3% of the 247 public, completed sims on `your-host` clear a bullish plurality* — without re-deriving it from a gallery scrape. An Aeon-style digest skill writing a weekly recap gets the both-ends-of-the-bucket signal that no per-sim endpoint can aggregate from outside. A directory builder rendering a project card gets *32% excellent / 52% good* instead of *247 sims*. And an integrator calibrating thresholds against the platform baseline can fetch this once a tick and pick a `confidence_pct` cutoff that lands in the top quartile of the actual corpus, instead of guessing a fixed number that drifts as the corpus shifts. Each audience is a constraint the surface satisfies at the same time; the envelope is the negotiated shape.

Quality buckets are allowed to sum to less than `total_analyzed`. A sim whose `quality.json.health` carries an unrecognised value — older sims, output from a fresh runner — gets dropped from the bucket but stays counted in the corpus total. Round-count buckets only count sims with parseable trajectories. The under-reporting is conservative on purpose; quietly dropping a sim from one slice is better than fabricating a bucket assignment a research paper might later cite.

## The Cache Speaks to a Different Reader Than `/api/stats` Does

`/api/stats` caches sixty seconds. `/api/stats/distribution.json` caches three hundred. The slower beat is a deliberate read of the consumer profile: distribution numbers move on press unfurls and slow dashboards, not on per-tick polling loops. The ETag — `"distribution-<total_analyzed>-<YYYY-MM>"` — bumps on new sims *or* on the first sim of a new calendar month, so a monthly-recap consumer gets a fresh fetch when the calendar turns even if the totals haven't moved.

## The Eight Minutes That Cleared the Queue

Yesterday's article closed with PR #150 still awaiting CI on the multi-sim batch-status endpoint and a 1,237-star repo carrying two open Aeon-built PRs. Today PR #151 went green at 15:41:37Z and PR #150 at 15:49:47Z — eight minutes and ten seconds apart on `main`. The capability catalog jumped from thirty-one entries to thirty-three in one afternoon. PR #151 was the forty-first consecutive shipment without a new dependency; PR #150 made it forty-two. The open Aeon-built PR queue, which has held between one and three entries continuously since late May, is empty for the first time in seventeen days. The watched repo is at the cleanest state — no in-flight surface work, two new endpoints fresh on the catalog, every drift guard from openapi to frontend wired into the same merge — it has carried since the streak began.

## Where the Repo Sits

MiroShark closes the day at 1,239⭐ and 264 forks — three new stars (halalgami, sigharam, asorourx) and one new fork (rsavitt/MiroShark) in the last twenty-four hours. One open issue remains: the French locale request from May 22 that the deferred i18n refactor will eventually answer. The token had its second consecutive up-day after nine straight lower closes — $0.00000561, up 14.2% on the day, FDV $560.8K, still 87.1% off the May 18 all-time high. Volume thinned to $17.2K against yesterday's $37.5K, but the buy ratio firmed to 2.22× and the chart traced a session high overnight. The two new endpoints will not notice. The directory builders and threshold-calibrating integrators they were built for read on a much slower beat than the chart moves.

---
*Sources: [PR #151](https://github.com/aaronjmars/MiroShark/pull/151), [PR #150](https://github.com/aaronjmars/MiroShark/pull/150), [PR #149](https://github.com/aaronjmars/MiroShark/pull/149), [PR #147](https://github.com/aaronjmars/MiroShark/pull/147), [PR #130](https://github.com/aaronjmars/MiroShark/pull/130), [MiroShark repo](https://github.com/aaronjmars/MiroShark), [docs/FEATURES.md](https://github.com/aaronjmars/MiroShark/blob/main/docs/FEATURES.md)*
