*Push Recap — 2026-04-29*
MiroShark — 6 substantive commits · miroshark-aeon — 1 substantive commit · all by aaronjmars

*Cost-compression continuation (PR #54, PR #55):* Yesterday's PR #51 Langfuse metadata was being silently dropped at OpenRouter's broadcast boundary (only `user`/`session_id`/`trace` keys forwarded) — verified against a 1,783-event Langfuse export: 0/1783 had tags. PR #54 moves per-call context into the spec-compliant `trace` block + adds missing `session_id`. PR #55 ports the agent-env wire compaction from miroshark-api PR #30: −57% input tokens, −55% per-agent simulate cost, −27% simulate stage cost, −24% simulate wall time, no rounds dropped.

*Three quote-friendly share formats now complete (PR #57):* Markdown + JSON transcript download from EmbedDialog. Pure-stdlib renderer, ±0.2 stance threshold matches every other surface, YAML front matter so Notion/Obsidian/Bear/Substack pick it up as page metadata. 18 offline tests, openapi drift test passes. Closes the screenshot-only gap for prose quoting; complements share card (preview) and replay GIF (motion).

*Hardening + CI repair (PR #53, PR #56, PR #58):* PR #53 5× NoneType guards on Reddit/Twitter post handlers (closed a tool-retry-loop cost leak), Polymarket on 4 more templates (5/6 default), default round count capped to [30,40], clickable history files. PR #56 `request.args.get(..., type=int)` so `?from_line=abc` no longer 500s on observability. PR #58 finally green-mained CI on the third iteration: moved compaction helpers to `backend/lib/env_compact.py` (sibling of `wonderwall/`) to dodge the camel/numpy/torch chain that `wonderwall/__init__.py` eagerly imports.

*Aeon (PR #26):* skill-leaderboard now reads every entry in `memory/watched-repos.md` (was reading only first, missed the actual aeon-instance repo at position 2) — application repos contribute zero and fall out naturally.

Key changes:
- `backend/app/services/transcript.py` (new, 615 lines) — pure-stdlib transcript renderer; YAML front matter + ±0.2 stance + 80-round Markdown cap with first-20+last-20 preservation
- `backend/wonderwall/social_agent/agent_environment.py` — compact env wire format (no `indent=4`, relative timestamps, top-3 comments by score with `comments_total` hint, drop-zero-counts) → −57% input tokens
- `backend/app/utils/llm_client.py` — Langfuse pass-through moved into the spec-compliant `trace` block + `session_id` so dashboard filters actually work

Stats: 32 files changed, +2,419/−258 across 7 substantive commits
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-29.md
