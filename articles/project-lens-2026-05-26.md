# Before 1935, an Earthquake Was Whatever It Felt Like

For most of human history, the size of an earthquake was a story you told afterward. The ground moved, chimneys fell, people ran into the street, a church bell rang itself. The instrument of record was the witness. The Italian volcanologist Giuseppe Mercalli formalized this in 1902, and the version still in use — the Modified Mercalli Intensity scale — runs from "not felt" up through "fall of chimneys" to "total destruction." It is a genuinely useful scale. It is also, by construction, subjective: the same earthquake reads as a IX near the fault and a IV fifty miles away, and two people standing in the same kitchen can disagree. Intensity is a measure of how the shaking landed on *you*, not of how big the thing actually was.

The problem with running a science on felt effects is that you cannot compare. By the early 1930s, the seismological lab at Caltech was receiving reports of dozens of earthquakes a week from stations across Southern California, and there was no standard way to say that one was larger than another. Charles Richter, a theoretical physicist who had wandered into seismology and never left, had a continuous record to work with — the seismogram, the inked wiggle a Wood-Anderson torsion seismometer drew as the ground moved. The record was complete. What was missing was a number.

## The day shaking became a single number

Richter's move, published in 1935 with his colleague Beno Gutenberg, was almost embarrassingly simple in hindsight. Take the maximum amplitude the needle traced on the seismogram. Take its logarithm, base ten. Correct for how far the station sat from the epicenter, calibrated so that a magnitude-zero quake draws a one-micron line at a hundred kilometers. That's it. The entire roiling, minutes-long record of an earthquake collapses into one figure derived from its single largest swing. Richter borrowed the word "magnitude" from astronomy — he'd been a stargazer as a child — and the borrowing is exact: like a star's brightness, the number says nothing about where you were standing.

The seismogram did not go away. It is still the thing of record, still where you read the aftershocks and the wave arrivals and the fault mechanics. But the seismogram is not what travels. The magnitude is what travels — into the newspaper, the building code, the comparison across decades. The discipline's whole leap was deciding that a rich time series needs a scalar derived from its peak before humans can actually act on it. When the Richter scale was finally superseded for large quakes by the moment magnitude scale (Hanks and Kanamori, 1979), the new method computed something more physically honest — the actual energy of the fault slip — but it was deliberately calibrated to line up with Richter's numbers. The derivation got better. The contract with the record stayed the same.

## A simulation is a record before it's a number

[MiroShark](https://github.com/aaronjmars/MiroShark) is an open-source engine where you stage a multi-agent debate, watch a population of synthetic stakeholders argue across rounds, and end up with a trajectory: three stance lines — bullish, neutral, bearish — rising and falling as agents change their minds. That trajectory is the project's seismogram. It is stored completely, exported as a chart, a CSV, a notebook. And until very recently, that was the only way to read it: you looked at the whole wiggle and described, in your own words, that round four "got contentious" or that opinion "swung hard near the end." Felt intensity. A IX in the kitchen.

[Pull request #108](https://github.com/aaronjmars/MiroShark/pull/108) — merged on May 26 — adds the magnitude reading. The new endpoint, `GET /api/simulation/<id>/peak-round`, walks the full trajectory once and returns, for each stance, the round where it peaked and the percentage it hit; plus `most_volatile_round`, the single round with the largest aggregate swing; `max_swing_pct`, the size of that swing; and `total_rounds`. It is the Richter reduction applied to a debate: from the complete record, the one largest movement and where it happened.

## Why the derivation has to agree with the record

The interesting part is buried in how it computes. The new `peak_round.py` is about 190 lines of pure standard-library Python, an O(n) pass over the same `trajectory.json` the chart and the CSV already read. Crucially, it reuses the project's existing `compute_stance_split` with the same ±0.2 thresholds that the trajectory CSV uses — which means the peak the API reports and the line you see on the chart are derived from one definition, not two. This is exactly the moment-magnitude discipline. You can build a better scalar, but it has to agree with the record it claims to summarize, or you've created a second, quietly contradictory source of truth. Seismology kept Mw consistent with Richter's old numbers; MiroShark builds the same guarantee in by refusing to recompute the stance split a second way. No new dependency was added to ship it.

## What a scalar buys that a chart can't

A chart is for looking. A scalar is for comparing, sorting, querying, and citing — and that is the whole difference between an artifact you admire once and one that survives into other people's systems. With `max_swing_pct` exposed as a number, you can ask which of a thousand simulations was the most volatile, or flag every debate whose decisive round came in the final stretch, without a human ever opening the chart. The same move that let a 1935 seismologist rank an entire week of earthquakes against each other is what lets a downstream tool rank a corpus of debates. The trajectory is still the record. But the magnitude is what gets quoted.

Before 1935, an earthquake was whatever it felt like. Then someone decided the record deserved a number, derived honestly from its largest moment, that meant the same thing to everyone. Most kinds of recorded time eventually get their Richter scale. This week, a debate engine got its own.

---
*Sources:*
- *[Richter scale — Wikipedia](https://en.wikipedia.org/wiki/Richter_scale)*
- *[Documents that Changed the World: Charles Richter's seismic scale, 1935 — University of Washington](https://www.washington.edu/news/2015/08/13/documents-that-changed-the-world-charles-richters-seismic-scale-1935/)*
- *[Moment magnitude scale — Wikipedia](https://en.wikipedia.org/wiki/Moment_magnitude_scale)*
- *[Mercalli Scale vs Richter Scale — Diffen](https://www.diffen.com/difference/Mercalli_Scale_vs_Richter_Scale)*
- *[How Are Earthquakes Measured? — Caltech Science Exchange](https://scienceexchange.caltech.edu/topics/earthquakes/earthquakes-measured)*
- *[MiroShark PR #108 — Peak-Round Belief Analytics](https://github.com/aaronjmars/MiroShark/pull/108)*
