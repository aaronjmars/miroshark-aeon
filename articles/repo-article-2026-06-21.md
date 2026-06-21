# MiroShark Has Fixed the Same Concurrency Bug Four Times — and Still Won't Fix It Once

Four times now, MiroShark has shipped the identical three-line patch to keep a user's language from vanishing mid-simulation. The latest, [PR #198](https://github.com/aaronjmars/MiroShark/pull/198), landed June 21 and closed [issue #195](https://github.com/aaronjmars/MiroShark/issues/195) — itself filed because reviewers of last week's [#194](https://github.com/aaronjmars/MiroShark/pull/194) noticed the bug had a twin. Each fix is correct. None of them is *the* fix. A reusable solution to this exact problem already sits in the codebase, used for a different purpose.

## The claim
> MiroShark re-fixes one bug by hand: locale, a ContextVar, drops across its ThreadPoolExecutor pools — #198 patched the fourth call-site this week, no shared fix.

## Evidence
The bug is a known Python edge. MiroShark stores the active UI language in a `contextvars.ContextVar` (`backend/app/utils/i18n.py:25`), read via `get_active_locale()`. ContextVars do not cross into `ThreadPoolExecutor` worker threads, so any code that fans simulation work out to a pool and builds prompts inside the workers silently reverts to English.

The repo has hit this in four places, each patched with the same hand-rolled wrapper: capture the locale on the parent thread, re-apply it inside the worker with `use_locale(...)`. `simulation_config_generator.py:345` carries the comment "capture before ThreadPoolExecutor; ContextVars don't cross threads." `wonderwall_profile_generator.py:1124` does the same. PR #194 (commit `3e054f4`, contributor dan-and) added it to `report_agent`. PR #198 (commit `165118d`) added it to `graph_tools._fallback_interview` this week — its diff literally annotates the line `# ThreadPoolExecutor doesn't inherit ContextVar`. Issue #195 names graph_tools as "the remaining known site of the same pattern."

The tell is that MiroShark already solved this generically — for a different context. `backend/app/utils/trace_context.py` ships `TraceContext.wrap_fn`, whose docstring reads: "Snapshot the caller's context; restore it in the wrapped fn ... Use this when submitting to a ThreadPoolExecutor." It exists so Langfuse trace IDs survive the pool boundary. Locale has the same lifetime and the same failure mode, but rides a separate mechanism and gets re-patched site by site. `wonderwall_profile_generator.py` even does both by hand inside one function — locale via `use_locale`, trace context via a manual snapshot (line 1167) — two propagation problems, zero shared abstraction.

The wider Python ecosystem settled this years ago. The standard library's own [contextvars docs](https://docs.python.org/3/library/contextvars.html) point to `copy_context()` plus `Context.run()` to carry context into worker callables; LangChain ships a [`ContextThreadPoolExecutor`](https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.config.ContextThreadPoolExecutor.html) subclass that copies contextvars into every submitted task so callers never think about it. MiroShark's four-site pattern is the manual version of one such wrapper, copy-pasted.

## Counter-evidence / what would change my mind
The per-site fixes are not wrong, and the explicit form is arguably clearer than a magic executor — at each call you can *see* that locale is being carried, which a subclass hides. The number of pooled sites is small and bounded, so the debt is contained; issue #195 calls graph_tools the *last* known one, meaning the team is tracking the full set rather than finding them ad hoc. And a single shared `LocaleThreadPoolExecutor` would couple `i18n` to every service that spawns a pool — a coupling a two-person team can reasonably defer. If the next pooled prompt-builder lands already wrapped, or wrapped through a shared helper rather than another inline copy, the "won't fix it once" half of this thesis is wrong.

## Why it matters
This is what engine-frozen looks like from the inside. MiroShark's simulation core (`simulation_runner`, `simulation_manager`) hasn't moved in weeks; the work is happening at the edges, where non-English self-hosters actually run it. A swarm that fans out to hundreds of agents lives or dies on its concurrency primitives, and "request-scoped state silently lost across a thread boundary" is the most expensive class of bug a simulator can carry — it doesn't crash, it quietly produces the wrong run. The team caught it four times because someone read the diff each time. The fifth pooled site that nobody reviews is the one that hands a German user an English simulation and reports success. A shared wrapper is cheaper than that audit, every single time.

---
*Sources*
- [PR #198 — thread locale through graph_tools fallback interview (aaronjmars/MiroShark)](https://github.com/aaronjmars/MiroShark/pull/198)
- [Issue #195 — graph_tools._fallback_interview drops locale across ThreadPoolExecutor](https://github.com/aaronjmars/MiroShark/issues/195)
- [PR #194 — wire report-agent prompts through locale registry](https://github.com/aaronjmars/MiroShark/pull/194)
- [backend/app/utils/trace_context.py — TraceContext.wrap_fn (the generic fix that already exists)](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/utils/trace_context.py)
- [backend/app/utils/i18n.py — locale ContextVar definition](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/utils/i18n.py)
- [Python docs — contextvars (copy_context / Context.run)](https://docs.python.org/3/library/contextvars.html)
- [LangChain — ContextThreadPoolExecutor (reusable context-propagating pool)](https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.config.ContextThreadPoolExecutor.html)
