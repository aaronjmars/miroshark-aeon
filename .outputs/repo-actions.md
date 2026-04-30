*Repo Action Ideas — 2026-04-30*
Generated from analysis of aaronjmars/MiroShark (904 stars, 0 open PRs). Five net-new ideas — none overlap with the past 7 days of suggestions.

1. Historical Simulation Mode (Feature, Small)
   Date-anchor picker + historical templates (WWII, 1929 Crash, Cuban Missile Crisis) capitalising on the viral WWII talkie demo; per-slot Wonderwall override already works — UI layer is the missing piece.

2. LLM-as-Judge Audit Panel (Feature, Small)
   `GET /api/simulation/:id/audit` sends transcript.json to a configurable judge model and returns per-agent reasoning/factual/stance-consistency scores; README explicitly says the transcript is for 'LLM-as-judge pipelines' — the entry point just doesn't exist yet.

3. Batch Rerun / Reproducibility Badge (Feature, Medium)
   Run the same scenario N times (cap 5), compute consensus mean ± std, write a 'Reproducible (n=3)' or 'Varies (n=3)' badge to gallery cards — turns a one-off result into a scientific finding; 3× Cheap runs now cost ~$0.50.

4. Belief Trajectory CSV / JSONL Export (Integration, Small)
   `GET /api/simulation/:id/trajectory.csv` — one row per round, per-round belief %s + agent count; stdlib csv, zero new deps; the fifth export surface and the one Pandas/Excel/Tableau users reach for automatically.

5. Spectator Watch Page (Growth, Small)
   `/watch/:id` — minimal fullscreen live viewer with OG meta that auto-unfurls as a share card when tweeted; 'Watch this $AAVE depeg sim in real time →' is a different content format than sharing a finished result; zero new backend.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-04-30.md
