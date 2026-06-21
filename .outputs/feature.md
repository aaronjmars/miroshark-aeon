*Feature Built — 2026-06-21 — aaronjmars/MiroShark*

Locale threading for the fallback interview path

MiroShark's interview tool has a backup path that kicks in when the main interview service is down — it asks the simulated agents your questions directly via the LLM. On non-English sessions (Chinese, German, French) that backup was silently answering in English. PR #198 fixes it so the agents stay in your language. Closes issue #195.

Why this matters:
This is the exact same bug class that PR #194 fixed yesterday in the report agent — locale getting dropped when work hops onto a background thread. Aaron filed #195 the same day pointing at the next instance. ~4 of 5 active app locales were affected on this path. The "$1 to simulate anything" promise breaks the moment a German user gets English output — fixing it keeps the localization credible where it actually shows up.

What was built:
- backend/app/services/graph_tools.py — `_fallback_interview` now captures the active locale before spawning its thread pool and re-applies it inside each worker (Python ContextVars don't cross thread boundaries); `_interview_single_agent_llm` swapped its hardcoded-English role-play prompt for a registry lookup.
- backend/app/prompts/locales/{en,zh_CN,de,fr}/graph_tools.py — new `interview_single_agent_roleplay` prompt, translated into all four locales.
- backend/tests/test_unit_graph_tools_locale.py — regression test proving the worker's prompt comes out in zh-CN even though it runs on a pool thread.

How it works:
Two defects compounded: locale was dropped across the ThreadPoolExecutor boundary, AND the worker built its role-play framing in hardcoded English — so even a correct locale couldn't change the output. The fix mirrors #194 exactly (capture + `use_locale` context manager) and moves the prompt into the locale registry, so the threaded-through locale actually selects the language. The new key rides the existing parity tests — any untranslated locale fails CI.

What's next:
This closes the last known instance of the ThreadPoolExecutor locale-drop class flagged during #194 review. Worth a sweep for any other `executor.submit` sites that read locale, but the two filed cases (report_agent, graph_tools) are now both fixed.

PR: https://github.com/aaronjmars/MiroShark/pull/198
