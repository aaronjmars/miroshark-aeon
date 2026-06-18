*Push Recap — 2026-06-18*
aaronjmars/MiroShark, aaronjmars/miroshark-aeon — SHIPPING — French (fr) prompt locale complete; sims no longer fall back to English

Shipped to users:
• #186 — FR prompts done: all 7 modules translated (persona gen, agent loop, ontology, NER, social sims, web enrichment, sim config) + CI gate. french-locale sims now speak French.

Under the hood:
• aeon model reset — Sonnet 4-6 default, Opus 4.8 pinned on deep-reasoning skills; 78 redundant overrides cleaned up
• #68 — treasury=fetch_fail fixed — BaseScan V1 deprecated 2026-06; now Base public RPC, no key required

Shape: 1 user-visible · 0 internal · 4 infra · 34 bot-filtered · 2 merged PRs
Volume: ~14 files, +735/−135 lines

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-18.md
