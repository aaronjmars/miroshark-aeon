*Thread Draft — 2026-06-23*
Topic: cost CLI subcommand — PR #208 on aaronjmars/MiroShark

1/ $1 to simulate anything. PR #208 makes that checkable from a terminal. `python cli.py cost <sim_id>` — the sim's dollar cost, locally, no dashboard login.

2/ three cost surfaces now in MiroShark. cost.json API landed June 16 (PR #179) — lower bound on what a sim spent, flagged as an estimate since not all models are tracked. PR #190 put that number in the embed pill on the public sim page.

3/ PR #208: `cmd_cost` in cli.py:201. the `~$` prefix mirrors the embed pill — both gate on `is_estimate`. exit code 2 when no cost recorded, so scripts can distinguish 'zero spend' from 'never ran'. 81 lines, 4 files.

4/ all three surfaces read the same cost.json — one source, one undercount. that's the constraint: untracked models log as $0, so the number is a floor, not the full bill. shipping that caveat explicitly, in every surface, is the honest version of the claim.

5/ PR #208 — cost CLI subcommand on MiroShark. https://github.com/aaronjmars/MiroShark/pull/208 🦈

(article: articles/thread-2026-06-23.md)
