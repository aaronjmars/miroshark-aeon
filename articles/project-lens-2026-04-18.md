# The 72-Hour Message Test: What Replaces the Focus Group

Three days before a policy brief drops, the communications director at a mid-sized think tank has a decision to make. The traditional playbook says: book a focus group. Find twelve participants. Run a 90-minute session, record it, have a researcher code it, pull the themes. Do it again with a different demographic if you want to know whether the argument lands differently for women under 35 than for retirees in the Midwest. Total cost: around $10,000 to $30,000 for a multi-city read. Turnaround: two to four weeks (Drive Research).

She has three days.

## The Research Industry Is Bleeding Out in Slow Motion

2024 was the worst year on record for election polling. In Nate Silver's post-mortem, overall call accuracy dropped to 70% — the lowest since 1998 — and presidential race calls landed correct only 63% of the time. For the third consecutive cycle, polls underestimated Republicans, with an average D+2.9 bias (AAPOR; Baltas 2025 in *Presidential Studies Quarterly*). Response rates have been collapsing for a decade, and in 2024 the crisis crossed a line nobody in the industry pretends they have fully diagnosed.

Focus groups have a parallel problem. A standard commercial session costs $10K to $30K, takes weeks to recruit, and typically pulls only eight to twelve people per segment. Incentives run $75 to $150 per B2C participant, $100 to $500 for B2B. The Qualtrics 2025 Market Research Trends Report — which surveyed over 3,000 researchers across fourteen countries — found that 71% expect synthetic respondents to account for more than half of research data collection within three years. 87% of the researchers already using them report being satisfied. Qualtrics itself launched Edge Audiences, a synthetic-respondent product, at its X4 conference in March 2025.

Meanwhile, the audience has fractured. Pew's 2025 social-media tracking shows X flipped from a Democratic-majority to a Republican-majority user base between 2023 and 2025. Facebook and Instagram skew heavily female; X and Reddit skew male. TikTok and Snapchat cluster under-30; YouTube and Facebook skew over-45. The NBC/SurveyMonkey Decision Desk documented the widest Gen Z gender gap in US political history on Trump approval, marriage, and definitions of success. An identical announcement in 2026 does not land in one room anymore. It lands in eight, and eight of them are talking past each other.

This is the market a message-tester has to survive in. Three days, no focus group budget, and a demographic landscape where the variance *is* the signal.

## What the Day Actually Looks Like

The communications director opens MiroShark — an open-source simulation engine at 720 GitHub stars and 138 forks, 25 days after launch — and pastes the executive summary of the housing affordability brief into the upload field. She picks 300 agents. She selects three platforms: Twitter, Reddit, Polymarket. She hits run.

Over the next thirty minutes, 300 LLM-driven agents — each with a distinct persona drawn from a profile pool containing age, gender, country, occupation, and primary platform — post reactions, reply to each other, shift stances, and trade prediction markets on whether the brief will be adopted. A belief drift chart tracks bullish / neutral / bearish percentages per round. When the run completes, a quality diagnostics badge (Excellent / Good / Low) tells her whether the population behaved like a healthy simulation or collapsed into an echo chamber.

Then she opens the Demographics tab.

## The Cross-Tab That Replaces a Stack of Focus Groups

The Agent Demographic Breakdown panel, which shipped as PR #35 to MiroShark on April 18, 2026, cross-tabulates five persona dimensions — age range, gender, country, actor type (individual vs. institutional), and primary platform — against three metrics: final stance, stance volatility (how far each agent moved from its initial position), and influence score.

At a glance she can see that agents in the 25–34 bucket ended net-bullish on the reform, while agents in the 55+ bucket ended net-bearish. That is not surprising. The surprising finding is in the volatility column: men on X show near-zero stance volatility — they picked a side in round one and held it — while women on Reddit show the highest volatility of any subgroup, which means the argument is actually being engaged with there, and small changes in framing could move the needle. Institutional actors (think-tank accounts, policy orgs) align with the brief's thesis early; individual actors split by age and platform.

A "KEY SUBGROUP DYNAMIC" callout at the top of the panel names the largest cross-segment stance gap — in this run, a 47-point spread between 18–24 men on X and 45–54 women on Facebook — and surfaces it as a headline before she has to go hunting for it.

By 4 PM Monday she knows the brief lands sideways with over-45 women. By Tuesday she has a revised framing. By Wednesday she has rerun the simulation with the new framing and compared the belief drift charts side by side. Thursday the brief drops with an informed bet about where it will land, priced against 300 simulated readers per scenario instead of twelve real ones in a back room in Cincinnati.

## Why the Cross-Tab Is the Product, Not the Simulation

Most LLM-based agent tools stop at the simulation. MiroShark stopped there in March 2026; the analytics layer only arrived in April — Quality Diagnostics (PR #32, Apr 17), Agent Interaction Network (PR #33, Apr 17), Demographic Breakdown (PR #35, Apr 18). Three weeks of shipping into a category nobody else was filling: not the raw simulation, but the reading of it.

Qualtrics Edge Audiences can give you synthetic survey respondents. Artificial Societies can tell you whether a LinkedIn post will perform. Ditto's 2026 synthetic-research market map lists eight vendors — Simile, Aaru, Evidenza, Synthetic Users, SYMAR, Lakmoos, Artificial Societies, Ditto — none of which expose, on a public API, a demographic cross-tab against stance volatility. The question MiroShark's Demographics tab answers — *which subgroup moved, and by how much* — is the question a communications director is going to have to answer every week from now on. Not because AI agents are fashionable, but because the legacy mechanisms for getting that answer are all breaking at the same time.

Whether synthetic readers are more accurate than real ones in any absolute sense is an open academic question. Saucery, one of the vendors, claims 95% correlation with human samples on benchmark tasks; critics point out the benchmarks are self-selected. What is not an open question is that the legacy workflow — two weeks, $30K, eight people in a room — does not fit a news cycle where crisis-comms teams are now expected to deploy initial messaging within two hours of an incident (O'Dwyer's PR News, July 2025).

The communications director closes her laptop at 5 PM Monday, two days before the brief drops. The focus group is booked for early May, to validate what she has already decided.

---

*Sources: [Nate Silver — "So How Did the Polls Do in 2024?"](https://www.natesilver.net/p/so-how-did-the-polls-do-in-2024-its); [Baltas 2025, Presidential Studies Quarterly](https://onlinelibrary.wiley.com/doi/10.1111/psq.70002); [Drive Research — focus group costs](https://www.driveresearch.com/market-research-company-blog/how-much-does-a-focus-group-cost-focus-groups-syracuse-ny/); [Qualtrics 2025 Market Research Trends Report](https://www.qualtrics.com/articles/news/ai-to-drive-massive-changes-to-market-research-in-2025-qualtrics-report-says/); [Ditto — 2026 synthetic research market map](https://askditto.io/news/synthetic-research-platforms-the-2026-market-map); [Saucery AI persona research](https://www.saucery.ai/the-science-behind-ai-personas-research-accuracy/); [Pew Research — 2025 social-media partisan shifts](https://www.pewresearch.org/); [NBC/SurveyMonkey Decision Desk — Gen Z gender gap](https://www.nbcnews.com/politics/politics-news/poll-gen-zs-gender-divide-reaches-politics-views-marriage-children-suc-rcna229255); [O'Dwyer's PR News — 2025 crisis-comms playbook](https://www.odwyerpr.com/story/public/23376/2025-07-31/crisis-pr-done-well-2025-playbook-for-trust-transparency-transformation.html); [MiroShark PR #35](https://github.com/aaronjmars/MiroShark/pull/35).*
