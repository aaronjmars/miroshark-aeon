*Push Recap — 2026-05-28*
aaronjmars/MiroShark — 4 commits by 2 authors (@aaronjmars + ext noelclaw) | aaronjmars/miroshark-aeon — 1 substantive commit (Aeon self-improve)

*Integrator-side surface (PR #120):* WEBHOOK_EVENTS — opt-in allow-list filtering outbound webhooks by direction (bullish/neutral/bearish), confidence (high ≥75% / medium 50–75%), and quality (excellent/good). OR within category, AND across; failed sims always fire; unknown tokens silently ignored; late-bound env so flips take effect without restart. Direct response to PR #109's 10+ integrator list — each integrator now subscribes to its own slice instead of writing request-side filters. 24th surface, +769 LoC, zero deps, Aeon-built.

*README pivot (PRs #118 + #119):* Use cases section moved above the feature wall (so "is this for me?" hits before "what does it have?"); 25-row feature table condensed from multi-sentence rows to scannable one-liners; "Simulate anything" hero banner + grounding & graph-memory diagrams added. 2-minute documentation reordering with outsized funnel effect.

*Ecosystem self-recruitment (PR #117):* External integrator noelclaw added themselves to ECOSYSTEM.md — 11th named integrator. Brings X handle, .com domain, AND a MiroShark-facing MCP server repo (`noelclaw/mcp`). Second external self-submission since the list shipped 2 days ago — the inbound census is starting to function as a passive recruitment surface.

*Self-improving aeon skill (PR #48):* token-report Grok query rewritten with three explicit pre-filters — drop zero-likes-AND-zero-RT tweets, drop contract-drop/vote-for templates + named clone domains, drop duplicate-template spam. Complements PR #47 (which disabled fetch-tweets + tweet-allocator entirely): token-report keeps running but its Social Pulse section degrades cleanly when only spam exists, instead of citing scam contract drops as sentiment.

Key changes:
- `backend/app/services/webhook_service.py` +237 LoC — token frozensets, `_resolve_event_filter`, `_payload_direction/_confidence_pct/_quality_key`, `payload_passes_event_filter(payload, events) → (bool, trace)` wired between dedup and dispatch
- `backend/tests/test_unit_webhook_events.py` new +454 LoC — 25 tests covering OR/AND semantics, failed-sim bypass, unknown-token tolerance, end-to-end fire_webhook behaviour
- `scripts/prefetch-xai.sh` 1-line prompt rewrite — moves spam-filter logic into Grok's picking step rather than post-process

Stats: ~10 files changed, +1,037 / -49 lines across 5 substantive PRs (excluding ~14 scheduler auto-commits)
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-28.md
