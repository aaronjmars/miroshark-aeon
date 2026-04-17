*Feature Built — 2026-04-17*

Simulation Quality Diagnostics
MiroShark simulations now get a health report card when they finish. After a simulation completes, the system automatically analyzes the run across four dimensions — how many agents actually participated, how diverse the debate was, how quickly consensus formed, and whether agents interacted across platforms — and assigns an overall health grade: Excellent, Good, or Low. This turns "completed" from a binary status into a meaningful signal about output quality.

Why this matters:
Until now, a 50-agent simulation where 30 agents were silent looked exactly the same as one with rich, multi-platform debate — both just showed "completed." Researchers had no way to tell whether a run produced meaningful agent behavior or a degenerate outcome. This was the #5 idea from repo-actions (Apr 16) and closes the feedback loop between running simulations and configuring better ones. Users now get actionable advice like "Try reducing agent count by 30%" when participation is low, helping them iterate toward higher-quality runs.

What was built:
- backend/app/api/simulation.py: New GET endpoint that computes four quality metrics from trajectory.json and action logs — participation rate (active agents vs. total), stance entropy (Shannon entropy across bullish/neutral/bearish stances, normalized 0–1), convergence speed (first round where one stance exceeds 60%), and cross-platform interaction rate. Results are cached in quality.json for instant subsequent loads. Generates text suggestions per metric.
- frontend/src/api/simulation.js: New getSimulationQuality() API function.
- frontend/src/components/HistoryDatabase.vue: Green/yellow/red quality dot on each simulation card with tooltip breakdown. Modal detail view gets a full "Simulation Quality" section with animated metric bars, health badge, and improvement suggestions.
- frontend/src/components/Step3Simulation.vue: Clickable quality chip appears in the events summary bar when a simulation completes. Clicking expands a diagnostics panel with the same metric bars and suggestions. Auto-fetches when the simulation transitions to completed state.

How it works:
The quality endpoint reads trajectory.json (for belief stance data) and action JSONL logs (for participation and cross-platform metrics). Participation rate counts agents who created at least one content action (post, comment, or trade) divided by total agents. Stance entropy uses Shannon entropy across the three stance buckets at the final round, normalized by log(3) so 1.0 means maximum diversity. Convergence speed finds the first round where any single stance exceeds 60% of agents. Cross-platform rate measures how many active agents interacted on multiple platforms. These four scores determine the health badge using threshold logic — all healthy = Excellent, any critical failure = Low, otherwise Good. Results are cached as quality.json so subsequent loads are instant.

What's next:
Could aggregate quality scores across all simulations to inform default parameter recommendations — "simulations with 30 agents and 8+ rounds produce the best health scores on average." Could also feed quality data into the article generator for richer context.

PR: https://github.com/aaronjmars/MiroShark/pull/32
