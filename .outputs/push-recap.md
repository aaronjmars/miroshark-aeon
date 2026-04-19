*Push Recap — 2026-04-19*
MiroShark + miroshark-aeon — 5 substantive commits, 3 authors, 11 files, +1,207/-81.

*Community perf PR (MiroShark #36, open):* builtbydesigninc parallelized report-section generation with a ThreadPoolExecutor, dropped MAX_REFLECTION_ROUNDS 3→1, and cut previous_sections context — measured 5x speedup (20.8→4 min) and 55% cost reduction on a 5-section report. First real external code contribution to the report engine.

*Next analytics feature in flight (MiroShark #37, open):* Aeon opened the 'What If?' Counterfactual Explorer — new /counterfactual endpoint + WhatIfPanel.vue (+761) that recomputes belief drift with up to 3 selected agents excluded. Pure data transform over trajectory.json, no re-simulation. Turns the network graph's 'dominant hub' finding into a quantifiable counterfactual.

*Infra hardening on miroshark-aeon:* Aaron shipped three tightly scoped workflow fixes — (1) chain-runner jq filter unbreak (chain dispatch was silently failing), (2) scheduler catch-up now compares LAST_DISPATCH_EPOCH vs scheduled fire time so skills don't double-fire, (3) ./notify hashes messages with sha256 and suppresses test/trace probes — stops duplicate notifications at the right layer.

Key changes:
- MiroShark d6afe00: ThreadPoolExecutor in report_agent.py (+87/-60) — 80% fewer input tokens, 50% fewer LLM calls
- MiroShark 347eda6: WhatIfPanel.vue new (+761), split-line SVG chart with dashed original / solid counterfactual curves
- miroshark-aeon 2417bf8: aeon.yml notify dedup (+54/-3) — hashes in .notify-sent-hashes, probes matching test/trace/ping/debug suppressed under 120 chars

Stats: 11 files, +1,207/-81 (excl ~35 automation chores)
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-19.md
