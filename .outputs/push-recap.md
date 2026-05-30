*Push Recap — 2026-05-30*
aaronjmars/MiroShark — 5 PRs by 1 author (all merged 2026-05-29 evening UTC)

Runtime + agent identity: PR #125 closes the FLASK_DEBUG default-true fail-open gap with a new _is_deployed_environment() helper that fails closed on Railway/Cloud Run env vars regardless of DEBUG, switches the internal-key check to hmac.compare_digest, exempts OPTIONS, and runs gunicorn (1 worker / 8 threads, gthread) instead of the Flask dev server in Dockerfile.railway — taking review fixes back in from external PR #106. PR #126 declares MiroShark's treasury 0x7753…0dC1 + deployer 0x6cab…2b24f on Base in .x402books/wallets.json (+19 LoC, merged 18s after open) — first machine-readable on-chain identity surface that isn't a UI element.

Marketing-site visual identity port (3-PR cascade): PR #127 swaps the design system at the :root token level (legacy --color-* names kept, values remapped to space-violet), repoints fonts to Geist/Geist Mono *without touching ~400 call sites*, adds reusable site classes + global nebula + animated star field + boot splash + SiteFooter. PR #128 chases the contrast/visibility regressions the cascade exposed (fully restyles ExploreView, fixes inverted "light button" traps in CounterfactualBranchPanel/WhatIfPanel/Settings, repoints 73 stray Space Mono / Young Serif literals to Geist). PR #129 re-themes the embed dialog (was still a light widget inside the dark app — white-on-white size buttons, near-black iframe code), fixes Step5Interaction's black-on-black hover, unifies sentiment to violet/fuchsia, and switches the ReplayView playback bar from invisible-white to dark glossy.

Key changes:
- backend/app/__init__.py +33/-8 — new _is_deployed_environment() helper + hmac.compare_digest + OPTIONS exempt; regression test fakes RAILWAY_ENVIRONMENT=production with FLASK_DEBUG=true and asserts 503
- Dockerfile.railway +22/-3 — exec gunicorn as PID 1, single worker (torch + sentence-transformers per worker would multiply memory), threads handle I/O-bound LLM + Neo4j workload
- frontend/src/App.vue +419/-34 — palette + font tokens repointed at :root so 400+ scoped <style> blocks inherit automatically; deep-space nebula + star field rendered behind every route

aaronjmars/miroshark-aeon: scheduler/cron auto-commits only — no substantive code.

Stats: 56 files changed, +1,954 / -878 lines. Zero new frontend deps (streak 34+). gunicorn added on backend (first runtime dep since Nemotron).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-30.md
