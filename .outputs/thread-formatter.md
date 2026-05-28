*Thread Draft — 2026-05-28*
Topic: WEBHOOK_EVENTS Dispatch Filter — MiroShark PR #120

1/ MiroShark has 24 API surfaces. PR #120 is the first one justified by a census. ECOSYSTEM.md went in Tuesday naming 10 integrators. WEBHOOK_EVENTS filter shipped Thursday with 12.

2/ Before PR #120, every completion webhook fired unconditionally. Twelve integrators each needed to write their own filter if they wanted to suppress bearish signals, low-confidence results, or slow-speed outputs. The platform sent everything; they dealt with it.

3/ WEBHOOK_EVENTS is a comma-separated allow-list. Three token categories — direction, confidence, quality. OR logic within each category, AND across. bullish,bearish means any directional result, not both at once. Failed simulations bypass unconditionally.

4/ Stripe calls this `enabled_events`. GitHub calls it an events array. Every webhook platform eventually ships per-consumer filtering. MiroShark shipped it at N=12, two days after ECOSYSTEM.md first named what N was. The census preceded the surface.

5/ webhook_service.py is +237 lines of stdlib. The filter is late-bound — flip it in .env without restarting. PR #120: https://github.com/aaronjmars/MiroShark/pull/120

(article: articles/thread-2026-05-28.md)
