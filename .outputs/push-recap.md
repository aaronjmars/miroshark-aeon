*Push Recap — 2026-04-22*
MiroShark — 23 substantive commits + miroshark-aeon — 1 (PR #22), 2 authors

Heavy 21:07–22:52 UTC cluster yesterday + PR #42 today: project-grade tightening pass, not a single feature drop. Settings/onboarding rebuilt model-list-down + simulation runner finally hardened end-to-end + 8-branch cleanup sweep merges into main on the same day docs split into docs/ reference.

Themes:
• Social Share Card lands (PR #42, +1,392/-139): 1200×630 OG card + /share/<id> landing + EmbedDialog preview/download. Zero new deps, 11 unit tests. Direct lever on 1K-stars target.
• Onboarding rebuild: Cheap preset → Qwen3.5-flash/DeepSeek-v3.2/Grok-4.1-fast (CoT-off → ~3× lower latency, ~$0.50/run measured); Settings modal preset dropdown + per-slot overrides; LLM-based URL fetcher replaces brittle HTML parser; prediction-market titles routed through Smart slot.
• Simulation runner hardened: counterfactual injection finally wired into all 4 loops (was imported nowhere, branches silently ran as plain forks); per-round error isolation + 600s ROUND_TIMEOUT watchdog; BeliefTracker persists state across pause/resume; What If? agent_id=0 falsy-trap + display-name vs handle namespace mismatch fixed in /counterfactual + /demographics.
• README & docs rewrite (12 commits): 698→243-line slim landing + 9 docs/ files split + OpenAI/Anthropic install paths + native Neo4j default + Windows path + "$1 & under 10 min" tagline.
• OASIS → Wonderwall rename across 35 files; neo4j added to CI test deps.
• 7 cleanup-branch merges (DRY/defensive/weak-types/types/AI-slop/legacy/unused) in a 39-second window 15:38 UTC + 8 CLEANUP_ASSESSMENT_*.md artifacts deleted (-911 lines).
• Simulation page UI/UX overhaul (+2,364/-344): new inline PolymarketChart, one toggleOverlay() dispatcher, design-system color alignment, chartExport.js with HiDPI Copy/Download + MiroShark footer on every chart, multi-market settings 1–5.
• miroshark-aeon PR #22: token-report XAI prefetch migration closes 3-day silent-fail on daily Social Pulse.

Key changes:
- 6fb30bd UI overhaul (12 files, 985-line new PolymarketChart + 280-line chartExport.js with font preload + sim-id'd footer)
- 9d71291 Social Share Card (Pillow renderer + share blueprint + EmbedDialog dialog + 11 tests)
- 2fd2532 simulation runner hardening (counterfactual_loader actually called for the first time + persisted belief state across pause/resume)
- ea1e799 + cbbf155 README compressed 698→243 lines, split into 9 docs/ files

Stats: ~150 files / +8,645 / -3,726 across 24 substantive commits
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-22.md
