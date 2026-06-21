🦈 *MiroShark Has Fixed the Same Concurrency Bug Four Times — and Still Won't Fix It Once*

thesis: locale is a ContextVar. ContextVars don't cross a ThreadPoolExecutor boundary — so a user's language silently drops to English mid-sim. #198 patched the fourth call-site by hand this week. the reusable fix already exists in the repo (trace_context.wrap_fn) — it's just wired for trace IDs, not locale. four hand-rolled copies of one wrapper. engine core still frozen.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-article-2026-06-21.md
