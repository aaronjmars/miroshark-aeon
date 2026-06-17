*Push Recap — 2026-06-17*
MiroShark — SHIPPING: German/French i18n foundation + French README live; run-end logs stop reporting 0 actions.

shipped to users:
• #184 — i18n goes from hardcoded en/zh to N locales. German + French land. t()/tr() rewritten to keyword overrides, English fallback, old two-arg calls untouched. (22 files, +230/−49)
• #185 — French README + the nav switcher becomes a real 4-locale selector (EN/中/DE/FR). closes the FR entry-point gap #184 left.
• #183 — the runner stopped lying. end-of-run log hardcoded total_actions=0 on every platform — even healthy runs. now logs real per-platform counts, with a camel smoke test gating it in CI so the next bad bump fails loud.

shape: 3 user-visible · 0 internal · 0 infra · 5 bot-filtered · 3 merged PRs
volume: 29 files, +507/−56
engine note: simulation_runner/manager untouched — 4th straight frozen window.

full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-17.md
