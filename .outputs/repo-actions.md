*Repo Action Ideas — aaronjmars/MiroShark — 2026-06-24*
Five implementable ideas this cycle; top pick wires the only missing CLI-to-API path — `/stop` has been live since the SimulationRunner was built but has no CLI entry point, leaving automation scripts unable to cancel a stuck run even when `wait` (just shipped as #215) detects a timeout.

Top pick: Add `stop` CLI subcommand to cancel a running simulation (DX/Feature, Small, Priority HIGH)
 → Completes the automation lifecycle: `wait || stop` cleanly kills a timed-out run without raw-curling the API.

1. Add `stop` CLI subcommand (HIGH, DX/Feature, Small)
2. Add LLM model fallback chain to survive OpenRouter deprecations (HIGH, DX/Performance, Medium)
3. Add `--lang` flag to `report` CLI for localized reports (MED, DX/Feature, Small)
4. Add Spanish (ES) locale across the full prompt system (MED, Community/Growth, Medium)
5. Add `--limit`/`--offset` to `list` CLI + server-side pagination (MED, DX, Medium)

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-24.md
