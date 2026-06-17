🦈 *MiroShark Shipped Its Agent Loop Untested for Two Months — Then a Dependency Bump Returned Zero Agents*

thesis: for ~2 months CI never ran the real agent loop. camel-ai 0.2.90 silently zeroed it — and `total_actions` was hardcoded to 0, so a dead run read identical to a healthy one. only after that did #183 add the first smoke test (+ #180 a frontend build gate). reactive, narrow, but it's the engine's first tripwire on the wire that snapped.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-article-2026-06-17.md
