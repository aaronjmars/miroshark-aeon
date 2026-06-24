*Push Recap — 2026-06-24*
aaronjmars/MiroShark — SHIPPING — wait subcommand and thinking-model robustness ship; automation pipeline complete

Shipped to users:
• `wait` CLI subcommand blocks until a simulation reaches a terminal state (exit 0 completed / 1 failed+stopped / 2 timeout), eliminating hand-rolled poll loops — `wait "$SIM" && report "$SIM"` now just works (cli.py, 4 files, +121/−1)
• Thinking-model engine hardening (dan-and): `llm_client.py` pads `max_tokens` with `THINKING_BUDGET_TOKENS`, strips unclosed `<think>` blocks, returns `None` on empty content so retries fire; `json_repair.py` fixes invalid escape sequences; 6 call sites get `repair_truncated=True`; CAMEL sim runner gets the combined token budget (9 files, +97/−21)
• `cost` CLI subcommand surfaces per-run USD estimate at the terminal so "$1 to simulate anything" is verifiable from automation scripts, not only the embed widget (cli.py, docs, tests, +81/−1)

Under the hood:
• Graph fan-out fix (#211): #209's total-failure fallback narrowed PanoramaSearch to 1 sub-query; restored the 4-way semantic default (participants / causes / development process)

Shape: 5 user-visible · 2 internal · 0 infra · ~40 bot-filtered · 7 merged PRs
Volume: 19 files, +308/−25 lines (MiroShark product commits)

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-24.md
