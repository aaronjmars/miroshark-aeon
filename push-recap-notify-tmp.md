*Push Recap — 2026-06-23*
aaronjmars/MiroShark — SHIPPING — `cost` CLI lands; deprecated mimo-v2-flash default swapped to mimo-v2.5

Shipped to users:
• `cef787b` — `python backend/cli.py cost <sim_id>` now prints `~$X.XXXX (tokens, calls)` with per-phase breakdown; the "$1 claim" is scriptable from automation pipelines
• `ec707cd` — default model switched from deprecated `xiaomi/mimo-v2-flash` to `xiaomi/mimo-v2.5` in config.py, settings.py Cloud preset, run_summary.py pricing, and all deploy templates — clean installs no longer 404 on first run
• `fc69fb4` — hero chip on Home.vue updated to "Your first result in under 10 minutes"; OpenRouter attribution headers now point to miroshark.xyz; "Universal Swarm Intelligence Engine" tagline retired

Under the hood:
• `6cf32a8` — 680 lines removed: SimulationIPCServer + GraphBuilderService async paths deleted, 5 per-channel notify services collapsed into shared _notify_base.py, simulation_runner.py fan-out consolidated (−359 lines)

Shape: 3 user-visible · 1 internal · 0 infra · 0 bot-filtered · 4 merged PRs
Volume: 55 files, +620/−1219 lines

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-23.md
