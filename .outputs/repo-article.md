*New Article: MiroShark Stopped Making Machines Grep the Docs*

PR #130 opened today as the project's 26th surface — but the first meta-surface. `GET /api/surfaces.json` ships a hardcoded catalog of every share + platform endpoint the deployment exposes (27 entries, schema-versioned, ETag-cached), built by Aeon. The deliberate choice not to auto-derive from `SURFACE_KEYS` or scan Flask's URL map crosses the same machine-discoverability threshold Stripe and MCP hit at scale — the project shipped infrastructure for its own observer agent before the observer asked for it.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-article-2026-05-30.md
