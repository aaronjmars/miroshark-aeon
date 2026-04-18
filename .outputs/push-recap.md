*Push Recap — 2026-04-18*
MiroShark — 2 open PRs (+2,345 lines, author: Aeon) + license flip/revert on main (net zero); miroshark-aeon — 2 self-improve PRs (+15 lines) triggered by today's own duplicate-run incidents, plus 35 routine chore auto-commits from daily skill runs.

Feature drop: PR #34 Embeddable Simulation Widget — read-only /embed/:simulationId route + embed-summary API + history-modal Embed dialog with iframe/Markdown/URL snippets, Compact/Standard/Wide presets, light/dark themes. Purpose-built for distributing simulations on Substack, Notion, READMEs.

Feature drop: PR #35 Agent Demographic Breakdown — /<sim_id>/demographics cross-tabs age/gender/country/actor type/platform against final stance, volatility, influence; 'KEY SUBGROUP DYNAMIC' headline picks largest divergence. Slots alongside Quality + Network as the population-level explainer.

Self-healing: PR #17 hyperstitions-ideas dedup (+6 lines) — skill fired twice today (stars target, then X-followers target); PR #18 repo-pulse idempotency (+9 lines) — stars=717/forks=137 notified twice. Both converge on the 'scan today's log before acting' idiom now used across 3 skills.

License note: AGPL-3.0 → MIT at 21:00 UTC Apr 17, reverted 2 minutes later. MiroShark remains AGPL-3.0.

Key changes:
- frontend/src/views/EmbedView.vue NEW (+539 lines): iframe-safe embed page with stacked drift sparkline, consensus marker, quality badge
- frontend/src/components/DemographicBreakdown.vue NEW (+582 lines): five-tab overlay with per-segment stance bars + metric columns
- backend/app/api/simulation.py (+169 / +429): two new GET endpoints, OasisProfileGenerator-style archetype classifier

Stats: ~18 files, +2,360 / -5 lines across 6 substantive commits
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-18.md
