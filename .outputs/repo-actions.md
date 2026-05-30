*Repo Action Ideas — 2026-05-30*
Generated from analysis of the current project — these are ideas that could be autonomously built by the feature skill tomorrow.

1. Private Share Link (Feature, Medium)
   Token-gated /share/<token> URL that exposes a private simulation to specific people without publishing it publicly — the first selective-access pattern the platform has.

2. French Locale (Community, Medium)
   Add lang=fr support following the protocol documented in PR #123; direct response to open issue #95 (the only open issue on the repo).

3. Simulation RSS Feed (Integration, Small)
   GET /api/feed.rss — RSS 2.0 feed of recent public simulations, opening MiroShark to every automation platform and RSS reader that uses feed subscriptions as a native trigger.

4. Simulation Clone JSON (Feature, Small)
   GET /api/simulation/<id>/clone.json — returns the exact input configuration (scenario text, agent count, rounds, locale, model) ready to POST to /run; first surface that returns inputs, not outputs.

5. Simulation Comparison UI View (Feature, Small)
   CompareView.vue at /compare?a=<id>&b=<id> — human-usable frontend for the existing compare API; two sim cards side-by-side with colored belief deltas and consensus agreement chip.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-30.md
