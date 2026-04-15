*Repo Action Ideas — 2026-04-15*
Generated from analysis of aaronjmars/MiroShark (692 stars, 0 open PRs). Fresh ideas for autonomous feature build:

1. Mid-Simulation Event Injection — Director Mode (Feature, Medium)
   Inject a breaking event mid-run; agents incorporate it next round. Unlocks exogenous shock modeling and makes MiroShark's experimental design credible for research.

2. HuggingFace Inference API as LLM Provider (Integration, Small)
   Add HuggingFace as a 4th provider option in the existing LLM selector — Llama 3.3 70B, Mistral, Qwen at ~10x lower cost than GPT-4o. Removes API spend as the adoption barrier for academic users.

3. Simulation Checkpoint & Resume (DX, Medium)
   Write a checkpoint JSON after each round; resume from round N+1 after crashes or container restarts. Prevents losing 8–15 min of API spend on interrupted cloud simulations.

4. Agent Demographic Breakdown Panel (Feature, Small)
   Cross-tab agent stance vs. demographics (age, region, platform, archetype type). Data already exists in persona JSON — no new collection. Adds a publishable subgroup figure to every simulation result.

5. RSS/Atom Feed for Completed Simulations (Integration/Growth, Small)
   /feed.xml publishes completed simulations for Feedly, n8n, Slack RSS, and Zapier. Universal no-auth integration layer; teams subscribe and get notified without opening a browser tab.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-04-15.md
