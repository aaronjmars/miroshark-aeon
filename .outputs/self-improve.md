*Agent Self-Improvement — 2026-04-22*

Migrated token-report's Social Pulse X/Grok call from inline sandbox-blocked curl to the existing prefetch pattern. The skill was silently failing and falsely reporting "XAI_API_KEY not set" for 3 days straight despite the secret being configured.

Why: `articles/token-report-2026-04-20.md`, `-21.md`, and `-22.md` all carry "XAI_API_KEY not set — social data unavailable" in Social Pulse, but fetch-tweets' prefetch consumes the same key without issue every day. Root cause: step 5 was running `curl -H "Authorization: Bearer $XAI_API_KEY"` inline inside Claude's sandbox, which blocks env var expansion in headers. Flagged in PR #21 body as "separate scope" — self-improve picked it up today.

What changed:
- `scripts/prefetch-xai.sh`: new `token-report)` case. Reads the tracked token symbol from `memory/MEMORY.md` (regex over the `## Tracked Token` table), drops any stale cache + sidecar, runs one `xai_search` with a `$SYMBOL` cashtag query, writes the symbol verbatim to `.xai-cache/token-report-social.symbol` for the skill to verify against.
- `skills/token-report/SKILL.md` step 5: replaced the inline curl with Path A (cache hit + sidecar match → parse `output_text`, cite handles/permalinks) / Path B (no cache or symbol mismatch or empty → accurate one-line "X/Grok data unavailable this run" note instead of falsely blaming a missing secret).

Impact: Restores real Social Pulse content to the daily token report (3 days of silent fall-through fixed). Inherits the same self-heal property as fetch-tweets' PR #19 — changing the tracked token in MEMORY.md invalidates the old cache on the next prefetch. Zero new deps.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/22
