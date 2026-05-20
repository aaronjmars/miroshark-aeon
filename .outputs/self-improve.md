*Agent Self-Improvement — 2026-05-20*

Distinguished Bankr Agent **timed-out** jobs from genuine "no wallet" responses in `scripts/prefetch-bankr.sh`. When a Bankr Agent prompt (Max-Mode `claude-sonnet-4.6`) didn't finish inside the 64-second polling window, the script was silently recording the handle as `null` — same shape as Bankr saying "this handle has no wallet." `tweet-allocator` then treated it as `TWEET_ALLOCATOR_EMPTY` instead of an error worth alerting on.

Why: 3 consecutive empty days (May 18 → May 20). Handles previously verified on May 14/16/17 (100xDarren, cybercelos, btcbabycow) all came back null in the May 20 prefetch, and the only signal `tweet-allocator` saw was "6 candidates, 0 wallets." That's the *exact* signature of an LLM-call timeout, not a real allocation cliff.

What changed:
- `scripts/prefetch-bankr.sh`: poll loop 8→14 iterations (~64s→~112s budget); submit max-time 30s→45s; new `TIMED_OUT` counter; timed-out handles excluded from `verified-handles.json`; new `prefetch-status.json` field `timed_out`; new top-level status `agent-timeout` when most lookups hit the poll-window ceiling.
- `skills/tweet-allocator/SKILL.md`: new step-4 branch for `agent-timeout` → `TWEET_ALLOCATOR_ERROR` with retry/credit hint, instead of silent `_EMPTY`.

Impact: Future Bankr LLM-mode latency surfaces as a real alert (actionable: check api.bankr.bot status / LLM credits), not a silent skip. Doubled polling window should also rescue handles that drift out of the previous 64s budget on slower Bankr days.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/43
