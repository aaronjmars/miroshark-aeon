*Thread Draft — 2026-06-03*
Topic: Ecosystem JSON Registry — /api/ecosystem.json (PR #145)

1/ MiroShark shipped /api/ecosystem.json today. 14 integrators, 5 categories, typed JSON envelope — machine-readable version of the ECOSYSTEM.md table that external contributors have been updating since May 26.

2/ ECOSYSTEM.md has been an open-contribution list since PR #109 (May 26). It's human-readable: Markdown rows with a name, URL, description, and now a logo. The machine equivalent didn't exist. Integrators who wanted to enumerate the registry had to parse Markdown.

3/ The endpoint is static and hardcoded, not auto-derived from Markdown. A drift-guard test cross-checks both sources so neither drifts silently. 52 minutes after PR #145 merged, a new external PR broke sync. The drift guard caught it. PR #146 closed it 5 minutes later.

4/ surfaces.json (PR #130) lists what the API exposes. ecosystem.json (PR #145) lists who is using it. They live on the same blueprint. That's the pairing a new integrator follows before writing any code. There were 10 integrators in the registry 8 days ago.

5/ PR #145 — 14 integrators, 5 categories, 15 offline tests, zero new dependencies (38th consecutive). https://github.com/aaronjmars/MiroShark/pull/145

(article: articles/thread-2026-06-03.md)
