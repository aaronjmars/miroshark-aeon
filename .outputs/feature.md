*Feature Built — 2026-06-22 — aaronjmars/MiroShark* 🦈

Thinking budget, sized on its own

MiroShark now lets you set how many tokens a reasoning model spends *thinking* — separately from the tokens it spends *answering*. Two new env knobs: `LLM_REASONING_MAX_TOKENS` (a hard token budget) and `LLM_REASONING_EFFORT` (low/medium/high). Set either and the model thinks inside that cap instead of bleeding into the response.

Why this matters:
Right now one `max_tokens` pool covers both the thinking trace and the answer. On a reasoning model a long `<think>` quietly eats the response — the same truncation class that broke suggest_scenarios back in #187/#188. It was an open ask (#193). "$1 to simulate anything" only holds if cost is predictable, and you can't budget a run when thinking and answering share one untracked pool.

What was built:
- backend/app/config.py: `LLM_REASONING_MAX_TOKENS` (int) + `LLM_REASONING_EFFORT` (str) config
- backend/app/utils/llm_client.py: `_resolve_reasoning_directive()` picks the right reasoning directive; `chat()` sends it via `extra_body`
- backend/tests/test_unit_reasoning_config.py: offline tests for every precedence branch
- .env.example + docs/CONFIGURATION.md: both knobs documented

How it works:
Both knobs map to OpenRouter's unified `reasoning` field, so it's one code path across Anthropic, Gemini, and OpenAI o-series — a token budget maps to Anthropic's `thinking.budget_tokens`, effort maps to OpenAI's `reasoning_effort`. It extends the existing `LLM_DISABLE_REASONING` branch: a token count wins over effort, and setting either flips reasoning on even if disable is left at its default. Defaults don't move — unset means exactly today's behavior.

What's next:
Wire it into the cost.json estimate so the thinking budget shows up in the per-sim cost surface — put the spend where strangers actually see it.

PR: https://github.com/aaronjmars/MiroShark/pull/203
