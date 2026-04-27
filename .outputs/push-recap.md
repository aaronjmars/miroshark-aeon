*Push Recap — 2026-04-27*
MiroShark — 4 commits / miroshark-aeon — 1 commit (24h window)

*Three contracts on main:* PR #45 OpenAPI 3.1 + PR #46 Webhook merged within 9 minutes Apr 26 17:03/17:12 UTC. PR #45's drift-detection regex test caught the missing `/api/settings/test-webhook` entry from PR #46 and absorbed the OpenAPI patch into its squash — second-merge coordination pattern working as intended. Three machine-readable surfaces (MCP stdio inbound / OpenAPI HTTP inbound / Webhook outbound) now all on main.

*Verified Predictions ship (PR #47, +1,194/−21):* New `POST /api/simulation/<id>/outcome` writes `outcome.json` to sim dir; gallery cards surface 📍/⚠/◑ outcome pills + coloured edge accents; new `/verified` route filters Explore to runs with recorded outcomes. `_read_outcome_file` strips non-http URLs as defense-in-depth so a corrupt artifact can't land `javascript:` on a card. EmbedDialog gains "Mark outcome" panel. Pivot from Apr 26 idea #1 — turns Bankr Terminal v2 Aave-sim citation (15M-view quote-tweet) into a permanent product surface.

*Mutation surface locked down (PR #48/#49, +540/−1):* `require_admin_token` decorator on `/publish`, `/resolve`, `/outcome` — `Authorization: Bearer $MIROSHARK_ADMIN_TOKEN` with constant-time `hmac.compare_digest`. Fail-closed: 503 if env unset (so a misconfigured deploy doesn't silently ship an open mutation surface), 401 generic if wrong/missing (so probes can't fingerprint). 17 new unit tests.

*Bankr Agent unblocked (miroshark-aeon PR #25, +4/−2):* Two-line `jq -n` payload fix — adds `maxMode: {enabled: true, model: "claude-sonnet-4.6"}` to the prompt. Bankr started subscription-gating AI prompts ~Apr 25; `verified-handles.json` had been empty 2 days running. Today's tweet-allocator log already shows wallet resolution working again.

Key changes:
- `backend/app/api/simulation.py` — `require_admin_token` decorator + `/outcome` POST+GET + `_read_outcome_file` + verified gallery filter
- `backend/openapi.yaml` — `AdminToken` securityScheme + `SimulationOutcome` schema + `outcome` on `GalleryCard` + `verified` query param
- `scripts/prefetch-bankr.sh` — `maxMode` field added to Bankr Agent prompt payload

Stats: 34 substantive files / +5,764 / −25
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-27.md
