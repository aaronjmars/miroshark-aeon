# MiroShark Spent Its Week Teaching the Swarm to Speak German — Not to Simulate Better

This week MiroShark didn't ship a faster swarm or a smarter agent. It shipped a German one. And a French one. Of the 20 non-bot pull requests merged between June 13 and June 20, seven were about language — adding locales or fixing the paths that break when an agent stops speaking English. The simulation core didn't move at all.

## The claim
> Localization is MiroShark's busiest workstream this week — 7 of 20 non-bot merged PRs (06-13→06-20) added German/French locales or fixed non-English LLM paths, and none touched the swarm core (`simulation_runner`/`simulation_manager`).

## Evidence
The locale build-out is the largest single line of work in the window. [#184](https://github.com/aaronjmars/MiroShark/pull/184) generalized the prompt-locale helpers and laid the German/French foundation. [#185](https://github.com/aaronjmars/MiroShark/pull/185) and [#186](https://github.com/aaronjmars/MiroShark/pull/186) wired French through the language switcher and added a CI coverage gate so a half-translated locale can't merge. Then external contributor Daniel Andersen (`dan-and`) landed the heaviest PR of the week: [#189](https://github.com/aaronjmars/MiroShark/pull/189), +2,888/−1,973 across 48 files, translating not just the frontend but the agent profiles and inter-agent communication into German. The result is two full prompt locales that didn't exist seven days ago — `backend/app/prompts/locales/de/` and `.../fr/`, each carrying nine files from `graph_tools.py` to a 329-line `report_agent.py`.

The other three count toward the seven because going multilingual is what exposed them. `dan-and`'s [#188](https://github.com/aaronjmars/MiroShark/pull/188) raised the `suggest_scenarios` timeout and token limit specifically for non-English and local LLMs, which run longer and verbose. [#192](https://github.com/aaronjmars/MiroShark/pull/192) added `backend/app/utils/json_repair.py` to salvage the truncated JSON those verbose models produce. [#194](https://github.com/aaronjmars/MiroShark/pull/194) — a one-file, +10/−8 surgical fix — routed the report agent through the locale registry after it was found still answering in English while everything else spoke the user's language.

What's missing from the diff is the tell. Across the entire 7-day file-change set, `backend/app/services/simulation_runner.py` and `simulation_manager.py` — the swarm loop — appear zero times. The closest the core got was `backend/wonderwall/social_agent/agent.py`, a +2/−2 signature tweak from the camel-ai bump. The engine that runs the agents was frozen; only the language it puts in their mouths changed.

## Counter-evidence / what would change my mind
The split authorship complicates the "external contributor leads it" reading: `dan-and` owns the German and the non-English-LLM reliability fixes, but `aaronjmars` authored the entire French side (#184/#185/#186) and the JSON salvage. This is a shared push, not a handoff. And the bug-fix PRs (#188, #192, #194) are arguably reliability work that happens to surface in non-English paths, not localization proper — count them out and the number drops to four clean locale PRs, still a plurality but not a majority. The honest read: localization is the dominant *theme*, not a strict 7-of-20 majority of *features*. What it isn't, on any reading, is engine work.

## Why it matters
MiroShark's pitch is "simulate anything, for $1." Anything includes anyone — and most of the people who'd model a market or a population don't run in English. Translating the prompts is the cheap part. The hard part is that LLMs degrade in non-English: LILT's analysis attributes [70–80% of multilingual failure](https://lilt.com/blog/multilingual-llm-performance-gap-analysis) to tokenizer inefficiency and English-centric reasoning, not bad data. That's exactly the failure mode #188, #192 and #194 are patching — agents that time out, blow their token budget, or quietly revert to English mid-run. MiroShark builds its swarm on top of [CAMEL](https://github.com/camel-ai/camel), which inherits the same English bias. So localization here isn't a translation chore. It's the work of making a sim credible for the half of the audience the engine wasn't reliable for. The risk is that a frozen core can't absorb the load forever — every new locale multiplies the surface where a verbose model can break a run, and the fixes so far are reactive, one bug at a time.

---
*Sources*
- [PR #184 — generalize locale helpers + German/French foundation](https://github.com/aaronjmars/MiroShark/pull/184)
- [PR #189 — German frontend + agent profiles/communication (+2,888/−1,973)](https://github.com/aaronjmars/MiroShark/pull/189)
- [PR #188 — raise suggest_scenarios timeout/token for non-English/local LLMs](https://github.com/aaronjmars/MiroShark/pull/188)
- [PR #194 — route report-agent through the locale registry](https://github.com/aaronjmars/MiroShark/pull/194)
- [LILT — why LLM performance drops in non-English languages](https://lilt.com/blog/multilingual-llm-performance-gap-analysis)
- [CAMEL — the multi-agent framework MiroShark's swarm is built on](https://github.com/camel-ai/camel)
