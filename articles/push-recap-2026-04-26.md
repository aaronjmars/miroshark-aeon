# Push Recap — 2026-04-26

## Overview
Two substantive PRs landed on open branches in the 24h window: MiroShark PR #46 (Completion Webhook) — a 1,413-line feature ship that wires Slack/Discord/Zapier/n8n to the simulator's terminal-state path, and miroshark-aeon PR #24 (Bankr Diagnostics) — a 93-line fix that turns two days of misleading "BANKR_API_KEY not set" alerts into accurate failure-mode signals. Both PRs are still **open** at window close. miroshark-aeon's main branch saw only chore auto-commits (cron success markers, scheduler state, per-skill log/article auto-commits) plus one auto-generated repo-actions article.

**Stats:** 14 substantive files changed, +1,497 / −10 across 2 substantive commits (1 per repo, both on PR branches). +30 chore/automation commits on miroshark-aeon main.

---

## aaronjmars/MiroShark

### Theme 1: Completion Webhook — the simulator gains an outbound contract (PR #46, open)

**Summary:** Every simulation that reaches a terminal state now POSTs a JSON summary to a user-configured URL. One env var (or a Settings save) wires up Slack Incoming Webhooks, Discord webhooks, Zapier/Make/n8n/IFTTT receivers, or a plain custom listener — no bot, no OAuth, no hosted infrastructure. Stdlib-only (`urllib.request`), zero new dependencies.

**Commits:**
- `edc7198` — *feat: completion webhook (Slack / Discord / Zapier / n8n / custom)* (10 files, +1,413/−1)
  - **New `backend/app/services/webhook_service.py`** (+457): the whole feature in one self-contained module.
    - `build_payload(simulation_id, status, sim_dir, *, state, base_url, completed_at, error)` reads `simulation_config.json`, `quality.json`, `trajectory.json`, `resolution.json`, `state.json` from the sim directory — every artifact is optional, missing files degrade gracefully into `null` instead of raising.
    - `_final_consensus_from_trajectory()` walks snapshots in reverse, picks the last one with computable belief positions, and buckets stances into bullish/neutral/bearish using **the same ±0.2 threshold as the gallery and share-card helpers** — so the consensus the webhook reports matches what users see in the share-card PNG (the Apr-22 PR #42 surface).
    - `fire_webhook_for_simulation()` runs on a daemon thread (`fire-and-forget`) so a slow webhook endpoint never delays the runner. Per-process dedup keyed on `(sim_id, status)` — bounded to 4,096 entries — so the runner's exit-code path AND the per-platform `simulation_end` event path can both call this without firing twice.
    - `validate_url()` accepts http(s) only, max 2,048 chars, empty string = "disabled". `mask_url()` extracts scheme + host (`https://hooks.slack.com/***`) so the saved URL secret never echoes back through `GET /api/settings`.
    - `send_test_webhook()` is the synchronous variant — fires `simulation.test`, returns `{ok, status, latency_ms, message}` for the Settings test button.
    - 5-second timeout, `MiroShark-Webhook/1.0` user agent, scenario truncated to 280 chars (X-post-length, intentional), error truncated to 1,000 chars.
  - **`backend/app/services/simulation_runner.py`** (+42, −0): hooks the webhook into **both** terminal paths the runner already knows about — the exit-code path in `_monitor_simulation` (line ~619, "completed" + "failed") and the `simulation_end` event path in `_read_action_log` (line ~754, "completed"). Each call sits next to the existing `send_push_notification` and is wrapped in `try/except` so a failing webhook never takes the runner down. The `(sim_id, status)` dedup in the service makes it safe that **both** completion paths fire for a healthy run.
  - **`backend/app/api/settings.py`** (+76, −0): new `Config.WEBHOOK_URL` + `Config.PUBLIC_BASE_URL` config keys; `GET /api/settings` exposes `integrations.webhook = {configured, url_masked, public_base_url}` — never the raw URL. `POST /api/settings` accepts `integrations.webhook.{url,public_base_url}` with URL validation. New `POST /api/settings/test-webhook` endpoint always returns HTTP 200 with `{success, message, latency_ms, url_masked}` so the frontend can render success/failure uniformly.
  - **`backend/app/config.py`** (+17): `WEBHOOK_URL` and `PUBLIC_BASE_URL` env-var-backed config fields.
  - **`frontend/src/components/SettingsPanel.vue`** (+168, −1): new `<section class="settings-section ai-section">` titled "Integrations · Webhook" placed **above** the MCP block. Status badge ("Configured" / "Not configured"), URL input with masked saved value as placeholder, optional public_base_url input, "Send test event" button that surfaces `✓ Delivered (Nms)` or `✗ <error>` inline. Wired through new `testWebhook()` helper in `frontend/src/api/settings.js` (+16).
  - **`docs/WEBHOOKS.md`** (+181): full payload schema, headers, delivery semantics (fire-and-forget, dedup, no retries, no auth), Slack/Discord/Zapier/n8n/custom-listener recipes.
  - **`backend/tests/test_unit_webhook.py`** (+441): **18 offline tests** covering payload shape (full / minimal / corrupt artifact files / long scenario truncation / failure-with-error), URL validation + masking, fire no-op when URL unconfigured, async dispatch (caller returns before slow POST completes), per-`(sim_id, status)` dedup including the `completed` + `failed` both-firing case, exception swallowing, unknown-status guard, `send_test_webhook` end-to-end. Mocks `_post_json` so no real HTTP fires in CI.
  - **`README.md`** (+2): Features + Documentation table rows for the new webhook surface.
  - **`.env.example`** (+13): `WEBHOOK_URL` + `PUBLIC_BASE_URL` blocks.

**Impact:** This is the production-quality checklist item the Paradigm-adjacent ML/dev audience scans for — "does it call my webhook when the job is done?" — and it's a **strict superset of the Apr-24 repo-actions idea #4** ("Post to Discord/Slack" share button), since pointing the webhook URL at Zapier or n8n collapses to the same outcome with infinitely more flexibility. Pivoted from idea #1 (SSE Streaming) and #2 (Engagement Leaderboard) precisely because (a) the cleanest hook into the existing `send_push_notification` call site already existed, (b) it's fully backend-shaped so lower regression risk, (c) it ships on the same "no new deps" rail the project has held on every PR this month. Every published sim now becomes a notification node — Slack/Discord auto-unfurl with the share-card PNG (the Apr-22 PR #42 surface) thanks to `share_card_url` in the payload + the existing OG meta tags on `/share/<id>`. **Open follow-up:** when this and PR #45 (OpenAPI) both merge, the second-merger needs `POST /api/settings/test-webhook` either added to `openapi.yaml` or to PR #45's drift-detection allowlist — otherwise PR #45's regex-scan unit test will fail on the next push.

---

## aaronjmars/miroshark-aeon

### Theme 2: Tweet Allocator stops false-alarming — Bankr prefetch grows a status sidecar (PR #24, open)

**Summary:** The `tweet-allocator` skill emitted `TWEET_ALLOCATOR_ERROR` two days running (Apr 25, Apr 26) with the same misleading text — "BANKR_API_KEY secret is likely not set". The secret has been set continuously since Apr 22 (5 wallets verified daily Apr 22–24). The real cause was silent Bankr Agent API failures, but the skill couldn't tell that from an empty `verified-handles.json`. Fix: prefetch now writes a `prefetch-status.json` sidecar at every exit point, and the skill branches on it instead of guessing.

**Commits:**
- `058f2e1` — *improve: distinguish bankr prefetch failure modes so tweet-allocator stops false-alarming* (4 files, +84/−9)
  - **`scripts/prefetch-bankr.sh`** (+56, −3): `mkdir -p .bankr-cache` moved up before the `BANKR_API_KEY` check so the sidecar is always writable. New `write_status()` helper builds `.bankr-cache/prefetch-status.json` via `jq -n` with `{status, note, timestamp, candidate_count, lookup_attempted, curl_failed, verified_count, null_count}`. Per-handle counters (`LOOKUP_ATTEMPTED`, `CURL_FAILED`) increment inside `bankr_lookup()` so the script can distinguish "all curl calls failed" from "API answered but returned null for everyone". Five terminal states surfaced:
    - `no-api-key` → secret unset, written *and* `verified-handles.json` zeroed.
    - `no-candidates` → no handles in `.xai-cache/` or today's log.
    - `lookups-failed` → `CURL_FAILED == LOOKUP_ATTEMPTED` (real API outage).
    - `completed-no-wallets` → API answered cleanly but `VERIFIED == 0`.
    - `completed` → at least one wallet verified.
  - **`skills/tweet-allocator/SKILL.md`** (+15, −6): step 4 rewritten to read `.bankr-cache/prefetch-status.json` first and branch on `status` rather than guessing from an empty cache file:
    - `no-api-key` → new **`TWEET_ALLOCATOR_DISABLED`** flag, log only, **silent (no notification)** — there's no recipient who can fix this from the bot side and a daily alert is just noise.
    - `no-candidates` / `completed-no-wallets` → `TWEET_ALLOCATOR_EMPTY`, brief one-line notification.
    - `lookups-failed` → `TWEET_ALLOCATOR_ERROR` with **accurate** message: `"Bankr Agent API unreachable (X/N curl failures). Check api.bankr.bot status / BANKR_API_KEY validity."`
    - sidecar entirely missing → `TWEET_ALLOCATOR_ERROR` with "prefetch-bankr.sh did not run; check workflow prefetch step".
    - `completed` → fall through to the existing wallet-eligible filter.
  - Status flags table at end of SKILL.md updated to four-state model: `OK` / `EMPTY` / `DISABLED` (silent) / `ERROR` (alert).
  - **`memory/MEMORY.md`** (+1): note line.
  - **`memory/logs/2026-04-26.md`** (+12): self-improve log entry.

**Impact:** Removes a class of false positives that would have kept escalating as `BANKR_API_KEY` operational reality drifted from `verified-handles.json` shape. Critical because the *real* failure modes (API down, key invalid, rate-limited) now produce alerts that *can be acted on* — and the *non-actionable* "secret literally absent" case is silent rather than crying wolf. Same architectural move as the Apr-22 XAI Cache Query Validation (PR #19/#20/#21 on miroshark-aeon) and Apr-24 Fetch-Tweets ID-Based Dedup: the prefetch + skill contract gets a **sidecar truth file** so the skill stops inferring state from an empty cache. Pattern is consolidating: `prefetch-*.sh` writes a sidecar, the consuming skill validates against it, the skill stays accurate when sandbox or upstream API conditions change.

### Theme 3: Routine automation commits on main (chore)

**Summary:** ~30 chore commits on main from `aeonframework` automation — daily skill runs leaving their tracks. Not surfaced in detail; they are the heartbeat of the daily skill cron, not feature work.

**Commits:** scheduler state updates, cron success markers (`token-report`, `fetch-tweets`, `tweet-allocator`, `repo-pulse`, `feature`, `repo-article`, `project-lens`, `heartbeat`, `self-improve`, `repo-actions`), and per-skill auto-commits of logs+articles. Notable single auto-commit: `8e11506` — `feat(repo-actions): generate 5 action ideas for 2026-04-26` adds `articles/repo-actions-2026-04-26.md` (96 lines: Predictive Accuracy Ledger, Animated GIF Export, Share-as-Thread Formatter, Python SDK via openapi-generator, Director Event Overlay) plus a 15-line log entry. Pure data output, zero code change. The "feat:" prefix on this commit is the auto-commit harness's labeling, not a substantive code feature.

---

## Developer Notes

- **New dependencies:** none. Both PRs hold the project's "stdlib only / pin already-present libs" rail — webhook uses `urllib.request`; the bankr fix uses `jq` and `curl` which are already in the workflow.
- **Breaking changes:** none. `tweet-allocator` adds `TWEET_ALLOCATOR_DISABLED` as a fourth status flag; old `OK/EMPTY/ERROR` semantics preserved (with `EMPTY` now also covering the previous "all-null" case formerly bucketed under `ERROR`).
- **Architecture shifts:**
  - PR #46 establishes the **outbound webhook** as MiroShark's third machine-readable contract over the same engine, after the Apr-24 PR #44 MCP (incoming, stdio) and the Apr-25 PR #45 OpenAPI (incoming, HTTP). Three formal surfaces in three days.
  - The **share-card consistency rail** continues: `_final_consensus_from_trajectory()` reuses the same ±0.2 stance threshold as `_build_gallery_card_payload()` and the share-card renderer, so a sim's "62% bullish / 13% neutral / 25% bearish" stays the same string in the OG image, the gallery card, and the webhook payload — three different surfaces, one source of truth.
  - The **prefetch sidecar** pattern is now in three skills (XAI tweets, fetch-tweets ID dedup, bankr handle verification). Each prefetch script writes a small JSON contract; the consuming skill validates against it. This is the project's emergent answer to the sandbox env-var-expansion limitation.
- **Tech debt:** PR #45 + PR #46 both still open at window close. Whichever merges second needs the other's endpoint reflected in `openapi.yaml` (or in the drift-detection allowlist) — flagged in PR #46's commit footer ("Note for follow-up").

## What's Next

- **PR #45 (OpenAPI/Swagger)** untouched in 24h — likely waits for review feedback or is being held to merge alongside #46.
- **PR #46 (Webhook)** filed 11:25 UTC today, ~3.5h old at window close — fits the rhythm where Apr-23 PR #43, Apr-24 PR #44, Apr-25 PR #45 all merged within ~2h of filing. Most likely merges in the next overnight or tomorrow morning window.
- **PR #24 on miroshark-aeon** (Bankr diagnostics) opened ~13:40 UTC — should clear quickly, behavior is silent on the disabled path so even if review takes time the false alarms will subside.
- The `repo-actions` ideas published today (Predictive Accuracy Ledger, GIF Export, Share-as-Thread, Python SDK, Director Event Overlay) line up the next 3–5 feature picks. Predictive Accuracy Ledger is the natural next ship after PR #46 (it productizes the Bankr Terminal v2 / Aave-vulnerability-sim citation that landed in a 15M-view thread today — see today's `fetch-tweets` log).
- **1K-stars-by-Apr-30 sprint:** 829 stars / 4 days left → ~43/day required vs. today's 6 stars/day pace. The sprint is now structurally unlikely to hit on calendar; the ship cadence (one substantive feature per day) is unchanged.
