# Push Recap — 2026-04-27

## Overview
Five substantive commits across two repos in the last 24 hours. MiroShark merged the back half of the "three protocols in three days" arc to main (PR #45 OpenAPI 3.1, PR #46 Completion Webhook), then shipped Predictive Accuracy Ledger / `/verified` (PR #47) and immediately patched the new mutation surface with operator-secret auth on `/publish`, `/resolve`, and `/outcome` (PR #48/#49). On miroshark-aeon, PR #25 added `maxMode: {enabled: true, model: "claude-sonnet-4.6"}` to every Bankr Agent prompt, ending the two-day-running `TWEET_ALLOCATOR_ERROR` after Bankr started subscription-gating AI prompts on Apr 25.

**Stats:** 34 files changed, +5,764/-25 lines across 5 substantive commits (plus ~25 chore auto-commits from `aeonframework` automation on miroshark-aeon).

**Window:** 2026-04-26 15:11 UTC → 2026-04-27 15:11 UTC.

---

## aaronjmars/MiroShark

### Theme 1: Three formal contracts land on main (PR #45 + PR #46)

**Summary:** The OpenAPI/Swagger PR and the Completion Webhook PR both filed Apr 25/26 squashed into `main` within nine minutes of each other on Apr 26 17:03–17:12 UTC — both authored before this window, but the merges sit at the start of today's recap. The substance was already covered in the Apr 25 and Apr 26 logs; what's new in *this* window is the coordination dance to get them on main together without breaking the drift-detection unit test.

**Commits:**
- `865d341` — feat: completion webhook (Slack / Discord / Zapier / n8n / custom) (#46) — merged 17:03 UTC
  - +1,413/−1 across 10 files. Stdlib-only `urllib.request`, daemon-thread fire-and-forget POST keyed on `(sim_id, status)` dedup so the runner exit-code path AND `simulation_end` event path both call without firing twice. Shared ±0.2 stance threshold across share-card / gallery / webhook so consensus stays consistent across surfaces. URL masked to `scheme://host/***` on `GET /api/settings` so Slack/Discord webhook never echoes through the settings read.
  - 18 offline unit tests in `test_unit_webhook.py` (+441) covering payload full/minimal/corrupt/long/failure, validation+masking, async dispatch, completed+failed dedup, exception swallowing.
  - `docs/WEBHOOKS.md` (+181) full payload schema + Slack/Discord/Zapier/n8n/custom recipes.

- `633f013` — feat: OpenAPI 3.1 spec + Swagger UI at /api/docs (#45) — merged 17:12 UTC
  - +2,613/−2 across 7 files. `backend/openapi.yaml` (+2,002) — 13 tags, ~85 paths, named schemas (`SuccessEnvelope`, `RunStatus`, `BeliefDrift`, `EmbedSummary`, `GalleryCard`, `McpStatus`, `SettingsUpdate`, `PushSubscription`, …). Swagger UI pinned to `swagger-ui-dist@5.17.14` from jsDelivr.
  - Drift-detection test in `test_unit_openapi.py` (+321) statically scans every `app/api/*.py` for `@<bp>_bp.route(...)` decorators, converts Flask `<id>` to OpenAPI `{id}`, asserts the spec's path set equals the registered Flask paths minus an explicit allowlist.
  - **Coordination patch:** the squashed merge commit includes a third commit `docs(openapi): document POST /api/settings/test-webhook` — coordination follow-up flagged in PR #46's footer. PR #46 added a new Flask route (`/api/settings/test-webhook`) that wasn't in the OpenAPI spec; whichever PR merged second had to backfill it, otherwise the drift test would fail on main. PR #45 went second by 9 minutes and absorbed the patch. Same commit also fixed an unquoted backtick-wrapped `Cache-Control: public, max-age=3600` in the share-card description that broke `yaml.safe_load`.

**Impact:** The "three protocols in three days" arc (MCP Apr 24 merged + OpenAPI Apr 25 filed + Webhook Apr 26 filed) is now fully on main. MCP-onboarded developers connecting Claude Desktop / Cursor / Windsurf / Continue can browse the REST surface in their browser at `/api/docs` and pipe the spec through `openapi-generator` to produce typed SDKs. Webhook URL pointed at Zapier/Make/n8n fans out to 5,000+ services. Three machine-readable surfaces (MCP stdio inbound / OpenAPI HTTP inbound / Webhook outbound) over the same engine.

---

### Theme 2: Predictive Accuracy Ledger and the `/verified` gallery hall (PR #47)

**Summary:** Annotation layer for public simulations — any operator can mark a published run with the real-world outcome it called (correct / partial / incorrect, plus optional URL + 280-char summary). The annotation lands on `<sim_dir>/outcome.json` and immediately surfaces on the public gallery as a 📍 Verified pill plus a coloured edge accent on the card. New `/verified` route renders the Explore view pre-filtered to simulations with a recorded outcome — the curated "hall of calls that landed" link to drop into threads about pre-incident simulations. Built autonomously by Aeon as a pivot from repo-actions Apr 26 idea #1 over the rest of the batch — the Bankr Terminal v2 Aave-sim citation is a credibility moment that should live in the product, not on X, and `/verified` is the page that turns it into a permanent surface.

**Commits:**
- `e5c5606` — feat: predictive accuracy ledger + /verified gallery hall (#47) — merged 13:46 UTC
  - +1,194/−21 across 9 files. New `POST /api/simulation/<id>/outcome` (publish-gated) + `GET` (read-only) — open-ended sibling to the binary `/resolve` endpoint. A simulation can have both: `/resolve` writes a YES/NO Polymarket-aligned `accuracy_score`, `/outcome` records the prediction-vs-real-event call.
  - `_read_outcome_file` in `backend/app/api/simulation.py` (+174) — validates label, truncates oversized summaries with `[:277].rstrip() + "…"`, **strips non-http URLs** as defense-in-depth so a corrupt `outcome.json` never lands `javascript:` on a gallery card. Never raises; a corrupt artifact must not blank out the gallery.
  - `_build_gallery_card_payload` surfaces `outcome` on every card. `GET /api/simulation/public?verified=1` filters to verified set + reflects `verified_only` in response. **Filtering happens before pagination** so `total` and `has_more` reflect the filtered set — otherwise the "X remaining" hint would lie.
  - Frontend: `/verified` route → `ExploreView` with `verifiedOnly: true` prop. ExploreView (+252/−16) gains 📍 Verified filter chip (toggles URL between `/explore` and `/verified`, refreshes), 📍/⚠/◑ outcome pills (clickable to outcome URL), coloured left-edge accent per outcome label, verified stat chip, dynamic page title/copy/empty-state for verified-only mode.
  - `EmbedDialog.vue` (+399/−2) gains "Mark outcome" panel — 3-way radio group, URL input, 280-char textarea with live counter, save/update button, success/error inline message, "View on /verified ↗" link once saved; all inputs disabled until publish.
  - openapi.yaml (+110) gets the new path + `SimulationOutcome` schema + `outcome` field on `GalleryCard` + `verified` query param + `verified_only` response field. Drift-detection test passes (new Flask route documented).
  - 8 offline unit tests in `test_unit_outcome.py` (+209) — valid record / unknown label / corrupt JSON / missing file / oversized-summary truncation / non-http URL stripping / gallery-card integration with+without outcome / corrupt-artifact graceful degradation.

**Impact:** Closes the loop on the Bankr Terminal v2 Apr 26 Aave-sim citation (156 likes / 40 RTs, 15M views in the quote-tweet thread). The citation lived on X as a one-off; `/verified` turns every future "we predicted X before it happened" call into a permanent, shareable URL on the product. Two follow-on ideas from the same repo-actions batch — animated GIF Belief Replay (#2) and Share-as-Thread Formatter (#3) — build on top of this once it lands.

---

### Theme 3: Mutation-surface lockdown — admin-token auth on /publish, /resolve, /outcome (PR #48/#49)

**Summary:** Hours after `/outcome` shipped, MiroShark closed a mutation-surface security gap that had been latent on `/publish` and `/resolve` since the public-gallery work landed. Mutation endpoints that write to a simulation's on-disk state now require a shared operator secret via `Authorization: Bearer $MIROSHARK_ADMIN_TOKEN`. Comparison runs through `hmac.compare_digest` so a network attacker can't time-trial the token. **Fail-closed semantics:** if `MIROSHARK_ADMIN_TOKEN` is unset/empty, the gated endpoints return 503 ("admin auth not configured") rather than silently allowing the request — an operator who forgot to set the secret would otherwise ship an open mutation surface and never know.

**Commits:**
- `2e0defe` — feat: admin-token auth on /publish, /resolve, /outcome (#48) (#49) — merged 14:04 UTC
  - +540/−1 across 5 files. New `require_admin_token` Flask decorator in `backend/app/api/simulation.py` (+137/−1) — reads `MIROSHARK_ADMIN_TOKEN` per-request (so tests can monkeypatch and operators can rotate via process restart without code reload), pulls bearer token from `Authorization` header, returns 503 if env unset, 401 if token missing/wrong, constant-time-compares both sides as bytes via `hmac.compare_digest`. Generic "Unauthorized" message — deliberately doesn't distinguish "missing" from "wrong" so a probe can't tell whether it found a valid endpoint.
  - Applied to `publish_simulation` and `resolve_simulation` via decorator. `simulation_outcome` (POST+GET on one view) inlines the same check on the POST branch only, so the public read path the gallery uses stays unaffected.
  - `backend/openapi.yaml` (+73) gains an `AdminToken` securityScheme, `Unauthorized` + `AdminAuthNotConfigured` response components, and `security` / 401 / 503 entries on each gated operation.
  - `.env.example` (+22) + `docs/CONFIGURATION.md` (+33) document the env var and the fail-closed behaviour.
  - 17 new unit tests in `test_unit_admin_auth.py` (+275) pin down header parsing (missing / wrong scheme / empty token / malformed), env loading (unset → 503, empty → 503, set → 401-or-200 by token match), generic 401 response shape, constant-time compare wiring (asserts the call site uses `hmac.compare_digest`, not `==`), and per-view that each gated route actually carries the gate.

**Impact:** A simulation operator running MiroShark behind a reverse proxy or on localhost no longer ships an open `/publish` / `/resolve` / `/outcome` surface. The fail-closed posture matters: the previous behaviour was "the endpoints work without auth", which a careful operator would have caught only by reading the docs — now the deploy yells 503 until the env var is set. The 503-vs-401 distinction also gives ops something useful to alert on (503 = "you forgot to configure" vs 401 = "someone is probing").

---

## aaronjmars/miroshark-aeon

### Theme 4: Bankr Agent API unblocked — maxMode subscription gate (PR #25)

**Summary:** Bankr's `/agent/prompt` endpoint started gating AI prompts behind "Bankr Club membership or Max Mode" around 2026-04-25, returning `subscription_required` on every request. That left `.bankr-cache/verified-handles.json` permanently `{}`, which was tripping the `TWEET_ALLOCATOR_ERROR` hard-stop two days running (Apr 25 + Apr 26 — the same false-alarm pattern that triggered the Apr 26 prefetch-diagnostics PR #24). PR #25 sends `maxMode: {enabled: true, model: "claude-sonnet-4.6"}` in the prompt payload — bills against the Bankr LLM-credits pool (separate top-up at https://bankr.bot/llm?tab=credits). Stacks on top of PR #24: that change gave better visibility into the failure mode (sidecar status file with `lookups-failed` / `completed-no-wallets` / etc.); this change actually unblocks the API call.

**Commits:**
- `56fdb59` — fix(bankr): send maxMode with prefetch + improve failure-mode diagnostics (#25) — merged 17:50 UTC
  - +4/−2 across 3 files (one-liner fix; rest is the diagnostics work in the same branch). The substantive change is two new lines in `scripts/prefetch-bankr.sh` adding `maxMode: {enabled: true, model: "claude-sonnet-4.6"}` to the existing `prompt` JSON payload built via `jq -n`.
  - Verified end-to-end on the sister repo `aeon-agent` PR #20: handle resolves to a real wallet that matches `memory/logs/2026-04-24.md`. Same maxMode field shape Bankr documented in the late-Apr docs update.
  - One-line tweak to `skills/tweet-allocator/SKILL.md` references the new behaviour.

**Impact:** Tweet allocator returns to `TWEET_ALLOCATOR_OK` from this morning's run forward — today's allocator log already shows `100xDarren` resolved + paid. The two-day-running false-alarm noise stops. The Apr 26 prefetch diagnostics work (PR #24) was the reconnaissance pass; PR #25 is the actual fix. Same emergent pattern as the other prefetch hardening work this week — the sidecar truth file lets the skill react accurately to upstream API changes instead of silently producing wrong allocations.

---

### Theme 5: Routine automation chore commits

**Summary:** ~25 `aeonframework` automation commits on `main` over the window — scheduler state, cron success markers, per-skill log+article auto-commits across token-report, fetch-tweets, tweet-allocator, repo-pulse, weekly-shiplog, heartbeat, memory-flush, skill-leaderboard, feature. No code changes; pure data output.

**Notable in the chore stream:**
- `c156e78 chore(cron): feature success` + `31a10a1 chore(feature): auto-commit 2026-04-27` (11:43 UTC) — the auto-commit that wrote `articles/feature-2026-04-27.md` for Predictive Accuracy Ledger / Verified, the same feature that landed as PR #47 on MiroShark two hours later.
- `891d568 chore(heartbeat): auto-commit 2026-04-26` (19:24 UTC) — heartbeat confirmed PR #45 + PR #46 + PR #24 + PR #25 all merged on Apr 26 17:03–17:50, four PRs in 47 minutes.
- `48a5177 chore(memory-flush): auto-commit 2026-04-26` (18:15 UTC) — full flush trimmed Recent Articles 12→8 rows, replaced 6 digests with Apr 24/25/26 entries.

---

## Developer Notes

- **New dependencies:** zero (PR #46 uses stdlib `urllib.request`; PR #45 pins `swagger-ui-dist@5.17.14` via jsDelivr CDN, no npm install; PR #48 uses stdlib `hmac`).
- **Breaking changes:** PR #48 is breaking for any operator who scripts `/publish`, `/resolve`, or `/outcome` via curl — they must now set `MIROSHARK_ADMIN_TOKEN` and pass `Authorization: Bearer $MIROSHARK_ADMIN_TOKEN`. The fail-closed 503 surfaces this loudly. Public read paths (`GET /outcome`, public gallery, embed) are unaffected.
- **Architecture shifts:** Three new architectural through-lines this window:
  1. **Drift-detection tests as the source-of-truth contract** — PR #45's regex scan of `@<bp>_bp.route(...)` decorators is now the third "registered Flask route ↔ external contract" drift test in the codebase (joining MCP tool catalog drift in PR #44 and the `_TOOLS` array drift). The coordination patch in PR #45 (documenting `POST /api/settings/test-webhook` from PR #46) shows the test working as intended — *it caught the missing entry*.
  2. **Outcome record on disk as gallery projection** — PR #47 adds `outcome.json` as a sim-dir artifact, then `_build_gallery_card_payload` projects it onto every card. Same architectural beat as PR #43 (Public Gallery) and PR #42 (Share Card): sim dir IS the schema, new views are cheap projections, no DB schema, no new deps.
  3. **Fail-closed mutation gate** — PR #48 establishes `require_admin_token` as a reusable decorator for any future mutation endpoint. Posture: 503 on misconfigured deploy, 401 on bad/missing token, generic message so probes can't fingerprint. Reusable beyond the three current sites.
- **Tech debt:** PR #46 introduced `POST /api/settings/test-webhook` without backfilling OpenAPI; PR #45's drift test caught it on merge — one example of the "second merge eats the coordination patch" pattern when two contract-spanning PRs land same-day. Likely to recur until the team either (a) requires OpenAPI updates in the same PR as the Flask route or (b) lets the drift test fail in CI on the second PR and patches in a follow-up.

## What's Next

- **Predictive Accuracy Ledger seeding.** PR #47 ships the surface, but `/verified` is empty until someone POSTs an outcome. The Bankr Terminal v2 Aave-sim citation (Apr 26) is the obvious first record — operator just needs to flip the published sim and POST `{label: "correct", outcome_url: "https://x.com/bankrbot/status/2048026489707442360", outcome_summary: "..."}`. Until that lands, the page reads empty-state.
- **Animated GIF / Belief Replay (repo-actions Apr 26 #2)** and **Share-as-Thread Formatter (#3)** are the queued follow-ons — both designed to compound on `/verified` (a verified prediction + a GIF replay + a 5-tweet thread = portable proof artifact). Either is a reasonable next-feature pick.
- **`MIROSHARK_ADMIN_TOKEN` rollout.** Anyone running MiroShark from the Apr 27 main forward needs to set this env var or `/publish` / `/resolve` / `/outcome` will return 503. README + `.env.example` + `docs/CONFIGURATION.md` cover it; worth a tweet/release note callout.
- **1K-stars-by-Apr-30 sprint.** Repo at 837 stars after today's repo-pulse (+9 in 24h vs the ~33/day pace target with 3 days left). PR #47 `/verified` plus admin-auth lockdown plus three-protocols-on-main ship the substrate; the remaining gap is closer to distribution than features.
- **Sister repo aeon-agent.** PR #25's commit message references "Verified end-to-end on the sister repo (aeon-agent PR #20)" — a separate work stream where the same Bankr maxMode patch was tested first. Worth tracking what else lands there as it tends to surface fixes before they hit miroshark-aeon.
