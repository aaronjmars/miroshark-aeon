*Thread Draft — 2026-06-22*
Topic: Thinking-token budget separation — PR #203

1/ MiroShark's reasoning models used one max_tokens value for both thinking trace and response. blow the budget — thinking trace wins, response arrives empty. PR #203 splits them.

2/ reasoning models on OpenRouter use a single max_tokens value. on Anthropic-routed models, max_tokens caps the full payload: thinking trace + response. same token budget that already broke suggest_scenarios (#187) — one pool, two consumers, first one wins.

3/ PR #203: two new env vars. LLM_REASONING_MAX_TOKENS caps the thinking trace (Anthropic's thinking.budget_tokens). LLM_REASONING_EFFORT sets effort level (OpenAI's reasoning_effort). both map to OpenRouter's unified reasoning field. 8 new unit tests.

4/ this is the third truncation-class fix in MiroShark's recent history: suggest_scenarios (#187), locale ContextVar drops (#194/#198), now reasoning token budget. pattern: one shared pool, multiple consumers, no guardrail until it silently fails.

5/ PR #203 — thinking-token budget for reasoning models. https://github.com/aaronjmars/MiroShark/pull/203 🦈

(article: articles/thread-2026-06-22.md)
