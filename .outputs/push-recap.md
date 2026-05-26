*Push Recap — 2026-05-26*
aaronjmars/MiroShark + miroshark-aeon — 3 substantive commits by 3 authors (last 24h)

*Ecosystem registry (#109, external):* Community contributor NurstarK added ECOSYSTEM.md — the first curated index of 10 named projects built on MiroShark (AntFleet, Blue Agent, Crucible Sim, Echo, Monitor, Nookplot, RootAI, Signa, Supercompact, Xerg) plus a "no stock forks" PR guideline. Latest in the run of external merges.

*New analytics surface (#108):* GET /api/simulation/<id>/peak-round collapses a full belief trajectory into one machine-readable summary — which round each stance peaked, the most volatile round, max swing, total rounds. Pure O(n) derivation reusing trajectory.csv's stance-split (peaks match byte-for-byte); 22nd surface, zero deps.

*Agent self-fix (#46):* Patched bankr-prefetch crashing on tweetless days — a no-match grep under set -euo pipefail exited 1 and stamped a false "crashed" status, which broke today's tweet-allocator (TWEET_ALLOCATOR_EMPTY). Now falls through to a clean no-candidates path.

Key changes:
- New peak_round.py service (187 LoC, stdlib) + publish-gated route + 19 offline tests + 📊 EmbedDialog section
- ECOSYSTEM.md: 10-project integrator table with contribution rules, merged from an external fork-owner
- prefetch-bankr.sh: |+|| true guards on 3 grep pipelines (complements PR #45 which detected the crash)

Stats: 12 files changed, +893/-4. All 3 merges zero-deps.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-26.md
