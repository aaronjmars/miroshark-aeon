# The Poll That Can't Be Checked

In the 1990s, more than three in ten people picked up the phone when a pollster called. [Today fewer than one in twenty do.](https://www.resultsense.com/news/2026-05-01-ai-polling-naratis-uk-elections) That collapse has quietly broken the economics of survey research: providers now charge tens of thousands of dollars to put a ten-minute questionnaire in front of a thousand real humans, and the humans are harder to find every year. So the industry did what every industry does when its labor cost climbs and its supply dries up — it started manufacturing a substitute.

The substitute is the *synthetic respondent*: a large language model prompted to answer as if it were a 34-year-old nurse in Ohio, or a thousand of them at once. The category has pulled in [more than $1.5 billion in venture funding](https://skimle.com/blog/synthetic-respondents-in-research-promise-pitfalls-and-when-to-use-in-2026) and customers including CVS Health, BlackRock, EY, and Microsoft. Qualtrics, the most widely used survey platform on earth, now offers synthetic respondents as a feature. A French startup, Naratis, runs one-on-one political interviews with AI agents. The pitch is irresistible: zero recruitment, answers in hours instead of weeks, and vendor benchmarks claiming up to 90% alignment with human survey data.

## The whole fight is about a number

Read the 2026 literature and you find both sides arguing over the same axis: how close does the machine get to the human?

The critics are winning that argument on the merits. A study by Paglieri and colleagues found that even when an LLM is explicitly told to generate "diverse personas," the output collapses toward a narrow cluster of stereotypical responses — the model has a default voice and keeps drifting back to it. Survey simulations show severe homogenization and a measurable positivity bias; respondents that are too agreeable, too sanded-down, too online. One [arXiv analysis](https://arxiv.org/pdf/2507.02919) put the bias introduced by pure synthesis at 24–86% depending on the task. Ambuj Tewari, a statistics professor at the University of Michigan, offered the cleanest dismissal: a synthetic poll is [a faulty thermometer](https://theconversation.com/ai-is-replacing-humans-in-responding-to-some-surveys-but-simulated-opinions-are-not-the-same-as-public-opinion-280988). "You would not trust one that estimated your temperature by consulting an AI model," he wrote. The chief executive of the French pollster OpinionWay was blunter still: his firm would never publish an opinion poll built on AI-generated data.

But notice what every one of these objections assumes. They assume the product is a *measurement* — a stand-in for a number you could otherwise have gotten from people. On that framing the synthetic respondent is doomed, because it will always be an approximation of a thing you could measure directly, and approximations of measurements are just errors with better marketing.

There is a different way to build the same machine, and it changes what the output even *is*.

## A simulation you can audit, not a number you must trust

One open-source project in this space spawns hundreds of agents that react to a scenario hour by hour — posting, arguing, trading on an internal prediction market, changing their minds — and hands back a report. So far that sounds like every other silicon-sampling vendor. The difference is in what the report contains and what surrounds it.

Each agent is grounded in five distinct layers before it says anything: a demographic seed, web enrichment, semantic search, an explicit relationship graph, and attributes pulled from a Neo4j knowledge graph the system builds for the scenario. That is a direct structural answer to the homogenization problem — the personas are pinned to different points in a constructed world rather than sampled from one model's default voice. And the final report doesn't just state an outcome; it cites the actual posts and trades that produced it. You can read the argument the simulated population had, not just its summary statistic.

Then there is the move that gives this article its reason to exist. In early June the project shipped `signed-result.json` — an HMAC-SHA256, offline-verifiable payload of a simulation's result. Around it sit machine-readable companions: a platform-wide [outcome distribution](https://github.com/aaronjmars/MiroShark) at `/api/stats/distribution.json`, an `/api/activity.json` feed of what just completed, batch status lookups. The output is being deliberately turned into a *signed artifact* rather than a figure on a slide.

Set that against Tewari's actual fear. His sharpest warning wasn't that synthetic numbers are inaccurate — it was that "pollsters may present results from synthetic respondents to the public as if they came from surveys of people." The danger is fabrication and laundering, not approximation. A cryptographic signature plus post-level citations doesn't make a simulation true. It makes it *checkable*: you can prove which run produced a result, that it wasn't edited afterward, and trace the synthetic conversation that led there. The category's critics keep auditing accuracy. This architecture is built to be audited for provenance.

## What survives 2027

The honest counter-argument is that provenance is beside the point — that if the underlying personas homogenize, a beautifully signed result is just a tamper-proof record of a wrong answer. That critique is real, and a signature alone never refutes it.

But it predicts the wrong failures. The self-driving-car industry runs on synthetic data precisely because every synthetic mile is eventually checked against a real one; nobody ships a model that was never validated against ground truth. Synthetic polling has no such loop yet — and you cannot build one on outputs you can't verify weren't fabricated. Provenance is the precondition for the accuracy check, not a substitute for it.

So here is a claim specific enough to be wrong by late 2027: the synthetic-respondent companies that survive will not be the ones topping the alignment leaderboard. They will be the ones whose results a skeptic can re-derive and a regulator can trace. Expect at least one of the well-funded pure-play platforms to fail not because its numbers were off, but because — when it mattered — no one could prove they weren't invented. The teams treating a simulation as a signed, sourced artifact today are hedging against exactly that, and they look slightly paranoid for it. In eighteen months they'll look early.

---
*Sources:*
- [AI is replacing humans in responding to some surveys — The Conversation](https://theconversation.com/ai-is-replacing-humans-in-responding-to-some-surveys-but-simulated-opinions-are-not-the-same-as-public-opinion-280988) — Tewari's thermometer analogy, survey cost economics, trust/laundering concern
- [Synthetic respondents in research: promise, pitfalls, when to use in 2026 — Skimle](https://skimle.com/blog/synthetic-respondents-in-research-promise-pitfalls-and-when-to-use-in-2026) — VC funding, enterprise customers, Qualtrics, Paglieri persona-collapse finding, alignment claims
- [Representativeness and structural consistency of silicon samples — arXiv](https://arxiv.org/pdf/2507.02919) — homogenization, positivity bias, 24–86% synthesis bias
- [AI-run focus groups arrive in political polling — Resultsense](https://www.resultsense.com/news/2026-05-01-ai-polling-naratis-uk-elections) — response-rate collapse, Naratis, OpinionWay refusal, checked-against-reality analogy
- [MiroShark repository](https://github.com/aaronjmars/MiroShark) — five-layer grounding, `signed-result.json` (HMAC-SHA256), distribution/activity APIs, post-citing reports
