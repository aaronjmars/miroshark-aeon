*Feature Built — 2026-06-18 — aaronjmars/MiroShark* 🦈

French prompt locale — now a real end-to-end language, not a label

MiroShark already showed "Français" in the language switcher, shipped a French README, and listed `fr` as supported in the backend. But the actual simulation prompts for French were empty stubs — so picking French silently gave you an English-prompted sim. This PR translates every prompt the engine uses into French, so a French user now gets a genuinely French simulation: French agents, French personas, French interviews.

Why this matters:
French was the most-requested missing locale — two issues (#95, open #161) asked for it directly. The Chinese locale precedent already proved localization pulls in new ecosystem reach. The gap here was the worst kind: the product advertised French everywhere, then quietly degraded to English where it actually counts — inside the sim. Closing that makes the promise real.

What was built:
- 7 prompt modules translated under `locales/fr/`: web enrichment, NER/relation extraction, ontology design, persona generation, simulation config (timing/events/markets/agent behavior), the interview pipeline, and the Twitter/Reddit/Polymarket agent prompts
- A CI coverage gate (`test_fr_has_no_missing_keys_relative_to_en`) that fails the build if any future English prompt ships without a French sibling — same guard zh-CN already has

How it works:
The prompt registry keys on the exact locale code and falls back to English per-key, so the fix was pure data: mirror every English key 1:1 in French. JSON keys, type-name conventions, and `{placeholder}` tokens stay verbatim — only the human-language text changes — so nothing at the call sites moves. No English string was touched, so existing behavior is unchanged for everyone else.

What's next:
German (`de`) prompts are still stubs — same treatment would finish that locale too. And the new coverage gate could be extended to `de` once those land.

PR: https://github.com/aaronjmars/MiroShark/pull/186
