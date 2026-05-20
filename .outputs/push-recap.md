*Push Recap — 2026-05-20*
MiroShark — 3 PRs merged (largest window of the cycle), aeon — PR #43 opened

*The 12th surface lands the same day as the 11th:* PR #91 (Trading Signal JSON, opened May 19, merged 19:25Z) closed the quant axis; PR #92 (Simulation Archive Bundle, opened 11:27Z May 20 → merged 13:28Z, ~2h cycle) ships the *compositional* surface — `GET /<id>/archive.zip` bundles 9 existing surface renderers + a `manifest.json` (SHA-256 / size / source URL per file) into one ZIP. Yesterday's push-recap explicitly named the 12th as the architectural inflection; it landed ~21h later.

*First external security PR ever merges:* PR #89 (Furin / teifurin) replaces the hardcoded `NEO4J_PASSWORD=miroshark` in `docker-compose.yml` + `.env.example` with a fail-fast `${NEO4J_PASSWORD:?…}` reference + `CHANGE_ME_…` placeholder. Closes 28-day external-merge gap (last was mbs5 April 20). Star→issue#88→PR cycle was 57 min on May 18; merge 35h+ later.

*Aeon self-correction cycle #3 in 4 days:* PR #43 (OPEN) distinguishes Bankr Agent timeouts from "no wallet found" after three consecutive `TWEET_ALLOCATOR_EMPTY` runs (May 18/19/20). Poll loop 8→14 iter (~64s→~112s budget), submit max-time 30→45s, new `agent-timeout` status routes to `TWEET_ALLOCATOR_ERROR` (alert) instead of silent `_EMPTY`.

Key changes:
- `archive_service.py` (+506 LoC, pure stdlib zipfile/hashlib) — `_CANONICAL_ORDER` locks 9-surface set, `_FIXED_ZIP_DATETIME=(1980,1,1,…)` makes per-file portion byte-reproducible, `_safe_call` wraps every surface builder so a missing renderer omits rather than 500s
- `signal_service.py` (+241 LoC, pure stdlib) — confidence formula `(leading_pct - 33.333) / 66.667 * 100` anchored against three-way split; quality_health → risk_tier mapping defaults to high-risk on unknown
- `EmbedDialog.vue` — 📦 Archive section (PR #92, +197) beneath 📡 Trading signal section (PR #91, +245) — both load on open + refetch on publish-flag flip

Stats: 22 files changed, +2,834 / -17 across 4 PRs. 28-PR zero-new-deps streak preserved (PR #57 → … → #92). Stars 1175→1177, forks 237→238.

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-20.md
