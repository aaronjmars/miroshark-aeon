# Push Recap — 2026-05-16

## Overview

Three MiroShark PRs landed on `main` in the window (Aaron-authored merges of Aeon-built branches), one new MiroShark PR opened and is still in CI, and one Aeon prompt-level fix opened against `miroshark-aeon`. The headline is **PR #84 (OriginTrail DKG citation)** — the "citation" gap that reproduce.json + share-card + notebook always implied is now closed on-chain. Alongside it, the operational hotfix **PR #86** swapped a deprecated xAI model out of the cloud preset within hours of the breakage, and **PR #85 (trajectory chart SVG)** opened to extend the vector-embed surface set.

**Stats:** ~53 files changed across MiroShark `main` (PR #83 + #84 + #86), +4,301 / -47 lines merged + 1,099 / -4 staged in the open PR #85. Plus 1 single-file aeon PR (+3/-0) and ~40 autonomous housekeeping commits on `miroshark-aeon`.

**Window:** 2026-05-15T15:12Z → 2026-05-16T15:12Z

---

## aaronjmars/MiroShark

### Theme 1: The Citation Gap Closes — On-Chain Provenance

**Summary:** Until PR #84, the reproducibility stack (`reproduce.json` SHA-256 → notebook.ipynb → share card → sitemap) made a simulation *reproducible* and *shareable* but not *un-rewritable*. PR #84 anchors finished public sims as OriginTrail DKG Knowledge Assets — the SHA-256 of `reproduce.json` becomes a blockchain-anchored citation key. The shape is identical to the existing webhook/discord/slack notifier idiom: opt-in via env vars (`DKG_*` empty → no-op), `<sim_dir>/dkg-citation.json` persisted atomically for idempotence, fire-against-local-daemon HTTP via stdlib `urllib.request`, all behind the same publish gate as reproduce.json itself.

**Commits:**

- `6b8e605` — feat: OriginTrail DKG citation — on-chain provenance for finished sims (#84, merged 2026-05-15T19:53Z)
  - New `backend/app/services/dkg_publisher.py` (+709 lines): composes Turtle RDF from the byte-stable reproduce.json blob + the webhook payload (one source of truth across surfaces). Walks the four-step DKG v9/v10 daemon flow — `assertion/create` (WM) → `assertion/{name}/write` (Turtle append) → `assertion/{name}/promote` (WM→SWM) → `shared-memory/publish` (SWM→VM, on-chain). Returns `{ual, merkleRoot, transactionHash, blockNumber, finalized}`. Idempotent — second click reads the persisted citation, never re-spends TRAC + gas. Sub-step timeouts tuned for the daemon's RocksDB-then-network rhythm.
  - `backend/app/api/simulation.py` (+233 lines): two new routes. `GET /<id>/dkg-citation` is a public read of the persisted file (404 when never anchored, 403 when sim not public — same publish gate as reproduce.json / thread / lineage). `POST /<id>/publish-dkg` is admin-token-gated and triggers the pipeline. Daemon failure modes map cleanly to 502 / 503 / 504 with stage info in the body.
  - `backend/app/api/notifications.py` (+13): `/api/config/notifications` now exposes `dkg_configured` + `dkg_network` so the SPA renders the right state without ever seeing the daemon URL. The auth token never leaves the backend.
  - `backend/app/config.py` (+21): four new env vars — `DKG_NODE_URL`, `DKG_AUTH_TOKEN`, `DKG_OPERATIONAL_WALLET`, `DKG_NETWORK` (metadata only — chain choice is daemon-side at `dkg init`).
  - `backend/openapi.yaml` (+257): full path specs for both routes + a `DkgCitation` response schema. Expands the `/api/config/notifications` envelope with the two new fields.
  - `backend/tests/test_unit_notifications_config.py` (+72): five existing tests updated for the new keys, two new tests for the fully-configured and partial-configuration cases (SPA must not surface a publish button when one required var is missing).
  - `frontend/src/api/simulation.js` (+48/-1): `getDkgCitation` + `publishDkg` helpers.
  - `frontend/src/components/EmbedDialog.vue` (+393/-1): new citation card slotted between the Jupyter notebook export and the lineage navigator. Testnet/mainnet chip, UAL + Merkle + tx-hash with copy buttons, explorer link, and a "Publish to DKG" CTA when not yet anchored. Reuses the chip CSS from PR #83's notifications callout.
  - `docs/DKG.md` (+240): setup walkthrough, payload schema, endpoint table, verification recipe (fetch reproduce.json → hash bytes → compare to on-chain Merkle root), and a TRAC + gas cost model.
  - `README.md` (+2): feature row.

**Impact:** A researcher quoting a MiroShark sim in a paper, Substack post, or Discord thread can now cite a UAL that anyone can verify against the un-rewritable on-chain Merkle root. This is the same provenance property a DOI gives a paper or Stripe gives a charge. It's also the first surface where MiroShark hardware-of-record stops being the operator's own machine — a tampered host can be detected by a third-party verifier without trusting the host at all. Caps an 11-surface arc (PRs #57–#84) that turned `sim_dir/` from a runtime artifact into a citable, verifiable, distributable research output.

---

### Theme 2: Operational Hotfix — xAI Deprecation Swap

**Summary:** xAI deprecated `x-ai/grok-4.1-fast` on OpenRouter — every call returned `404 "xAI recommends switching to Grok 4.3"`. That broke three slots in MiroShark's cloud preset (Smart, NER, `WEB_SEARCH` `:online` variant). PR #86 swapped all three to `google/gemini-3-flash-preview` and updated every doc reference. The Default slot (Mimo V2 Flash, the 850-call-per-run cost driver) was untouched, so the per-run cost stays near the advertised $1.

**Commits:**

- `44d1c4e` — fix: swap deprecated grok-4.1-fast → gemini-3-flash-preview (#86, merged 2026-05-16T14:20Z)
  - `backend/app/api/settings.py` (+4/-4): the `cheap` preset's label flips from "Mimo V2 Flash + Grok-4.1 Fast" to "Mimo V2 Flash + Gemini 3 Flash" and all three model-name fields swap.
  - `backend/app/config.py` (+3/-3): docstrings.
  - `backend/app/utils/llm_client.py` (+1/-1): latency comment.
  - `backend/app/utils/run_summary.py` (+1/-1): pricing table entry updated to the actual OpenRouter rate ($0.50/M in, $3.00/M out — 6× more expensive on output than Grok was, but only the Smart slot's ~19 calls per run touch it).
  - `backend/app/utils/url_fetcher.py` (+2/-2): docstring + error message.
  - `.env.example` (+5/-5): three model IDs + the latency comment + header text.
  - `README.md`, `docs/MODELS.{md,zh-CN.md}`, `docs/INSTALL.{md,zh-CN.md}`, `docs/CONFIGURATION.{md,zh-CN.md}` (+30/-30): EN + ZH references everywhere they were named.
  - PR body confirms an end-to-end sim ran clean against the new model — ontology generation (10 entity types + 7 edge types in ~11s), graph build (22 entities + 22 edges, stable JSON), web enrichment (`:online` variant fetched Hacker News at 2144 chars), persona generation untouched.

**Impact:** Same-day open + merge (PR #86 created 14:19 UTC, merged 14:20 UTC). The cloud preset is the lowest-friction onboarding path — a 404 in the Smart slot would have silently bricked new operators' first sim. This is the first MiroShark merge that's pure ops-keepalive against an upstream provider deprecation rather than a feature or refactor. Worth flagging as a precedent: model-provider deprecations on OpenRouter are now part of MiroShark's regular maintenance surface.

---

### Theme 3: Distribution Surface Extends to Vector

**Summary:** PR #85 opens (still in CI as of window close) a `GET /api/simulation/<id>/chart.svg` endpoint that renders the belief trajectory as pure-stdlib SVG via `xml.etree.ElementTree`. Same publish gate, same byte-stable property as reproduce.json + notebook.ipynb, same `Cache-Control: public, max-age=300`. Closes May-14 repo-actions batch idea #3.

**Commits:**

- (branch `feat/chart-svg-trajectory`, PR #85, opened 2026-05-16T11:29Z, OPEN at window close)
  - `backend/app/services/chart_svg.py` (NEW, ~390 LoC stdlib): three polylines — bullish `#22c55e` / neutral `#6b7280` / bearish `#ef4444` — on a fixed `viewBox="0 0 800 400"`. 5-line y-axis grid, adaptive round-number x-axis ticks, right-aligned three-swatch legend, scenario title truncated at 80 chars + ellipsis. Reuses `trajectory_export.build_rows` so trajectory.json schema changes flow through both surfaces.
  - `backend/app/api/simulation.py`: new `get_chart_svg` route handler — same publish gate, surface-stats increment, 5-min cache, 404 on empty trajectory (no blank SVG).
  - `backend/app/services/surface_stats.py` + tests: `SURFACE_KEYS` frozenset extended with `chart_svg` (analytics counter).
  - `backend/tests/test_unit_chart_svg.py` (NEW): 17 offline tests (viewBox lock, 3 polylines, stance-colour preservation, y-axis inversion, 404-on-empty, malformed-input resilience, title truncation, single-round renders, deterministic byte output, route + counter presence).
  - `frontend/src/api/simulation.js`: `getChartSvgUrl` helper.
  - `frontend/src/components/EmbedDialog.vue`: new "📈 Trajectory chart (SVG)" section — lazy-loaded preview + Download .svg + Copy URL + paste-ready `<img>` embed snippet.
  - Docs: `README.md` + `docs/FEATURES.md` + `docs/API.md` + the zh-CN siblings — feature row + `chart_svg` added to the surface-stats counter list.

**Impact:** Bytewise-deterministic vector output makes SVG a cache-key-friendly cousin of reproduce.json + notebook.ipynb. Where the share-card PNG is fixed-resolution and the notebook is runnable, the SVG is the *embed-anywhere* surface — Notion / Substack / Ghost / LaTeX render `<img src=…/chart.svg>` natively, no JS. Twenty-third consecutive zero-new-deps PR (streak from #57). When it merges, it'll close May-14 repo-actions batch idea #3 — leaving only idea #5 (Private Share Link) unbuilt from that batch.

---

### Theme 4: PR #83 (Discord + Slack Notifications) Merges

**Summary:** Opened 2026-05-15 11:41 UTC (covered in yesterday's recap as the OPEN PR with the third instance of the channel-notifier shape), merged 2026-05-15 16:25 UTC inside this window. Inside the merge: the original feat commit plus a fix commit (`map notifications_bp in OpenAPI drift scanner`) — the static drift scanner builds Flask routes from `@<bp>.route(...)` decorators using a `_BLUEPRINT_PREFIXES` map that was missing `notifications_bp`. Aaron caught it pre-merge, single-line fix.

**Commits:**

- `1d6f6ee` — feat: Discord rich-embed + Slack Block Kit completion notifications (#83, merged 2026-05-15T16:25Z, +2269/-1 across 17 files)

**Impact:** First feature whose PR body explicitly names a named external integrator's stack (RevaultDrops Discord, CancerHawk Slack). Closes May-14 repo-actions batch idea #1. Was the most-watched PR of the window — driving today's project-lens article ("Two Is Coincidence. Three Is The Shape You Didn't Plan.") and aeon's PR #40 prompt-level fix (next theme).

---

## aaronjmars/miroshark-aeon

### Theme 5: Prompt-Level Fix for Project-Lens PR-Status Drift

**Summary:** Yesterday's `project-lens` notification said "merged" while the article body correctly said "opened" — PR #83 was still open at notify time (16:10 UTC) and merged ~15 min later (16:25 UTC). Single observed instance but the highest-visibility surface project-lens produces (push to Telegram/Discord/Slack). PR #40 hardens the skill prompt to verify PR state via `gh pr view` before any notification.

**Commits:**

- (branch `improve/project-lens-pr-status-verify`, PR #40, opened 2026-05-16T13:06Z, OPEN at window close)
  - `skills/project-lens/SKILL.md` (+3/-0): one bullet under step 5 requires `gh pr view <num> --repo <owner>/<repo> --json state,mergedAt,updatedAt --jq '{state, mergedAt, updatedAt}'` for any PR referenced by number, with verb caching so step 6 reuses the same word. One assertion at the top of step 6 — the notification's PR-status verb (`opened`/`merged`/`closed`/`draft`) must match the article body word-for-word; on doubt, re-query gh and let JSON win.

**Impact:** ~1 extra `gh pr view` per article (the skill already runs `gh api repos/owner/repo` in step 1, so incremental cost only). Eliminates a class of factual error in the highest-visibility surface this skill emits. Pattern is transferable to `repo-article` and `thread-formatter` if the same drift surfaces there. Diff is single-file, 3 insertions — minimum-invasive prompt-level fix, exactly the shape Aeon's self-improve skill is meant to produce.

---

### Theme 6: Autonomous Skill Cadence (Housekeeping)

**Summary:** ~40 commits on `miroshark-aeon` `main`, all `aeonframework` cron auto-commits and scheduler bookkeeping. Substantive skill outputs are already covered in their own theme above or in standalone log entries.

**Skill firings logged today (in cron order):**
- 06:33 — `token-report` ($0.00001446, +28.6% 24h, new ATH $0.0000162 intraday)
- 07:28 — `fetch-tweets` (10 new tweets, all bullish; CN tweet "米罗莎要来了")
- 08:18 — `tweet-allocator` ($9.99 across 3 authors — tsubixxx $4.44, PoodleFi_ $3.33, btcbabycow $2.22)
- 10:11 — `repo-pulse` (1162⭐, +8 stars 24h, +1 fork)
- 10:12 — `hyperstitions-ideas` (≥3 named external integrators by 2026-07-31)
- 10:44 — `star-momentum-alert` (OUT_OF_WINDOW for 1500⭐, ~60d to target)
- 11:36 — `feature` (PR #85 — Trajectory Chart SVG)
- 13:08 — `self-improve` (PR #40 — project-lens PR-status verify)
- 14:27 — `repo-actions` (5 idea slate: oEmbed, Farcaster Frame, Email Notifications, Peak-Round Belief Analytics, Operator Profile Page)
- 15:11 — current scheduler state update

**Impact:** Substantive skills ran clean. No quiet skills. The repo-actions slate this morning surfaced two net-new ideas (Farcaster Frame, Email Notifications) and three re-eligible May-8 carryovers — feeding the next 2–3 days of `feature` runs.

---

## Developer Notes

- **New dependencies:** Zero. PR #83 / #84 / #85 / #86 are all pure stdlib (urllib.request / json / os / hashlib / xml.etree). 23rd consecutive zero-new-deps MiroShark PR (streak from #57).
- **Breaking changes:** None at the API level. The `/api/config/notifications` response grows two keys (`dkg_configured`, `dkg_network`) — frontend reads them by name, so existing SPA versions ignore the new fields cleanly. The `SimulationSurfaceStats` response grows a `chart_svg` field — same backward-compatible additive shape.
- **Architecture shifts:** Channel-notifier idiom (fire-and-forget daemon dispatch + `(sim_id, status)` dedup + late-bound env reads + shared `build_payload` artifact) now appears in `webhook_service`, `discord_notify`, `slack_notify`, AND `dkg_publisher` — four instances. The DKG publisher swaps "fire HTTP at a webhook URL" for "walk a 4-step daemon pipeline," but the optionality + idempotence + env-var-gate posture matches. First *on-chain* channel.
- **Tech debt:** PR #84's DKG publish path is synchronous (`POST /api/shared-memory/publish` blocks the operator's click). The async `/api/publisher/enqueue` flow exists in DKG but adds polling complexity; v1 chose latency over architectural depth. Worth revisiting if mainnet publishes start regularly exceeding the 90s timeout. PR #86 swap cost-shifts the Smart slot 6× upward on output tokens — the per-run cost note in the PR body claims it stays near $1 because Wonderwall (Mimo V2 Flash) is untouched, but the actual telemetry will need a `run_summary` audit after a week of production sims.

## What's Next

- **PR #85 (Trajectory Chart SVG)** is in CI. Expect merge today or tomorrow, closing May-14 batch idea #3. Once merged the May-14 batch is 4/5 resolved with only #5 (Private Share Link) still unbuilt.
- **PR #40 (project-lens PR-status verify)** is in CI. Single-file prompt fix; merge is procedural. Once merged, the next `project-lens` firing will be the first observed run under the new guard — worth checking whether any PR referenced by number in tomorrow's run triggers the new `gh pr view` block.
- **Today's repo-actions slate** (5 ideas) feeds the next `feature` cycle. Two net-new (Farcaster Frame, Email Notifications) plus three May-8 carryovers (oEmbed, Peak-Round, Operator Profile).
- **Open thread:** the DKG citation is anchored on testnet by default (`DKG_NETWORK=testnet`). Aaron has not yet flipped any sim to mainnet — the first mainnet publish will be the first real-money citation event for MiroShark and is worth watching for both UX friction (TRAC + gas cost surface) and the first verifiable third-party citation cycle.
- **Model deprecation watch:** PR #86 establishes that upstream provider deprecations on OpenRouter are now part of the maintenance surface. Worth setting up a periodic probe against the cloud preset's model IDs so the next 404 is caught by Aeon, not by a new operator's first sim.
