# Push Recap — 2026-06-02

## Overview
Seventeen substantive merges to `main` across the 24h window (all on `aaronjmars/MiroShark`; `aaronjmars/miroshark-aeon` saw only cron/auto-commit churn). The window splits into four clusters: (1) two Aeon-built feature PRs shipped paired late on Jun 1 — `#132` Private Share-Link (first tri-state sharing primitive) and `#137` agents.json (the 26th publish-gated per-sim surface, merged at 12:35Z today); (2) a thirteen-commit README + docs visual-and-bilingual rebuild that Aaron ran in a single evening session (18:48Z → 20:06Z on Jun 1), including PR `#134` swapping the README diagrams from PNG to optimized JPG (~92% size cut); (3) PR `#133` UI polish fixing a global border-radius leak and a black-on-dark report-panel palette; (4) three back-to-back ecosystem additions today (`#138` HivemindOS / `#139` Echo Oracle rename / `#141` SyntheticsAI) growing the named-integrator table to 16+, with `#140` Capacitr still open at window close. On the aeon side, `aaronjmars/miroshark-aeon#50` (blocked-features registry self-improve) opened but did not merge.

**Stats:** ~40 distinct files changed, +4,550 / −259 lines across 17 substantive commits. Per-repo: MiroShark = 17 commits, miroshark-aeon = 0 substantive (33 auto-commit / scheduler-state commits excluded as noise per May-31 convention).

---

## aaronjmars/MiroShark

### Theme 1 — Two new surfaces shipped paired: tri-state sharing + agent roster
**Summary:** Two Aeon-authored feature PRs landed inside the window — `#132` Private Share Link merged 2026-06-01T19:46:10Z and `#137` agents.json merged 2026-06-02T12:35:29Z. They're not thematically tied (one is access-control, the other is identity export) but they share a posture: both are net-additive, zero-deletion changes, both add to the publish-gated REST surface family, and together they advance the catalog from 28 surfaces (at start of window) to 29 catalogued (26 publish-gated per-sim + 2 platform-level + 1 self-ref). MiroShark backend now has its 26th publish-gated per-sim surface and its first sharing primitive that isn't binary public-or-private.

**Commits:**

- `f077213` — **feat: private share-link tokens for selective preview without publishing (#132)** (merged 19:46:10Z, Jun 1)
  - New file `backend/app/services/share_link_service.py` (+513) — pure-stdlib token lifecycle. `generate_token` mints a 32-character URL-safe base64 token via `secrets.token_urlsafe(24)` (192 bits of entropy). Storage at `<sim_dir>/share-tokens/<token>.json` co-located with sim data so deleting a sim takes its tokens with it (no orphan flat index). Atomic-write helper mirrors `surface_stats._atomic_write`. Path-traversal guard rejects anything outside `[A-Za-z0-9_-]` before touching the filesystem. Expiry clamp: default 30 days, range `[1, 365]`; non-numeric / negative / oversize all coerce to defaults.
  - Modified `backend/app/api/simulation.py` (+169) — three new admin-gated endpoints alongside `/publish` sharing the `require_admin_token` decorator: `POST /api/simulation/<id>/share-link` (mint, 201 with `preview_url` + `expires_at_iso`), `GET /api/simulation/<id>/share-links` (list active, newest-first, excludes revoked + expired), `DELETE /api/simulation/<id>/share-link/<token>` (idempotent revoke, 204).
  - Modified `backend/app/api/share.py` (+186) — new public `/preview/<token>` route. Resolves the token, renders a separate HTML template from the public `/share/<sim_id>` page with a privacy posture explicitly built for stakeholder-link semantics: `<meta name="robots" content="noindex,nofollow">` + `X-Robots-Tag: noindex,nofollow` + `Referrer-Policy: no-referrer` + `Cache-Control: no-store` (so revocation is instant) + **no** Open Graph / Twitter card / Farcaster Frame / oEmbed tags (so a URL pasted into Discord / Slack / Twitter shows as a bare link, not an auto-unfurl). Unknown / revoked / expired tokens all return the same 404 body so a probe can't distinguish the cases.
  - New file `backend/tests/test_unit_share_link.py` (+396, 18 offline tests) — generate writes record, expiry defaults/clamps math, ISO timestamp present, resolve returns sim_id for valid token, None for unknown/revoked/expired, path-traversal rejected, missing sim_root handled, revoke idempotent, revoke unknown returns False, list excludes revoked/expired and sorts newest-first, two tokens for same sim both resolve, removed sim dir yields None on resolve.
  - Modified `frontend/src/api/simulation.js` (+67) — `createShareLink(simId, expiresInDays)`, `listShareLinks(simId)`, `revokeShareLink(simId, token)`, `getPreviewUrl(token, origin)`.
  - Modified `frontend/src/components/EmbedDialog.vue` (+276) — "🔗 Private share links" panel alongside the public toggle. Expiry presets dropdown (1 / 7 / 30 / 90 / 365 days), Generate button, per-token list with truncated `<code>` URL display, remaining-days countdown, one-click Copy (clipboard API), one-click Revoke. Watcher fires on dialog open + simulation_id change.
  - Modified `docs/API.md` (+4) — four new rows in the Publish/Embed/Export table.
  - Modified `docs/FEATURES.md` (+19) — new "Private Share Links" section between "Publishing for Embed" and "Predictive Accuracy Ledger".
  - Modified `backend/openapi.yaml` (+196) — four path entries (mint / list / revoke / preview) + `ShareLinkRecord` component schema.

  **Privacy boundary made explicit:** the token grants the preview page only — it does **not** unlock per-sim REST surfaces (`signal.json`, `share-card.png`, `chart.svg`, `transcript.md`, `polymarket.json`, `agents/sparklines`, `volatility`, the new `clone.json`, the new `agents.json`, etc.). Those all keep their existing `is_public` gate. This is not a 27th surface — it's the platform's first **third-state** sharing primitive, taking the previously binary `is_public` flag to a tri-state public / token-gated / private model.

- `3d9466c` — **feat: agents.json surface — per-agent identity / persona export (#137)** (merged 12:35:29Z, Jun 2; opened earlier the same day)
  - New file `backend/app/services/agent_export.py` (+420) — roster assembly. Reads `reddit_profiles.json` then `polymarket_profiles.json` for each agent with reddit-wins-on-dupe (matches the transcript renderer's convention). Reuses `agent_sparklines_service.load_agent_trajectories` for the belief layer so the `±0.2` stance threshold is shared — an agent tagged bullish here is bullish in the transcript and the sparkline. Field normalisation: `persona_preview` truncated to 280 chars, `bio` and `scenario` truncations. Sort: most-bullish-first; profile-only agents (no trajectory) sink to the bottom.
  - Modified `backend/app/api/simulation.py` (+94) — `GET /api/simulation/<id>/agents.json` route handler with publish gate, scenario-preview echo, `json.dumps(sort_keys=True)`, 1-hour cache (structural data, like `clone.json`, doesn't change between rounds), increments `agents_json` surface counter.
  - Modified `backend/app/services/surface_stats.py` (+1) — `agents_json` added to `SURFACE_KEYS` frozenset.
  - Modified `backend/app/services/surfaces_catalog.py` (+10) — `agents_json` added to `_CATALOG` and `_PER_SIM_TRACKED_KEYS`. (PR included a follow-up commit `fix(surfaces-catalog): correct agents_json added_in_pr 135 -> 137` after the initial value targeted the wrong PR number — a clean catch from the drift-guard test.)
  - New file `backend/tests/test_unit_agent_export.py` (+497, 24 offline tests) — roster shape, profile lookup order, persona truncation, sort order, stance threshold parity with sparklines, scenario echo, error paths.
  - Modified `backend/tests/test_unit_surface_stats.py` (+1) — `agents_json` added to expected set.
  - Modified `backend/openapi.yaml` (+210) — path entry under Publish & Embed + `AgentsExportResponse` + `AgentExportEntry` schemas.
  - Modified `docs/API.md` (+1) + `docs/FEATURES.md` (+53) — table row and full "Agent Persona Export (Roster)" section.
  - Modified `frontend/src/api/simulation.js` (+45) — `getAgentsJsonUrl` + `getAgentsJson` helpers (mirror sparklines pattern, 403/404 → null).
  - Modified `frontend/src/components/EmbedDialog.vue` (+270) — 🧑‍🤝‍🧑 Agent roster section, capped 12-row preview with name + handle + stance chip + demographic tag row + persona preview, copyable URL + curl. CSS sibling style to the sparklines list.

**Impact:** `agents.json` is the **identity** companion to `agents/sparklines` (May-27 PR #115). Sparklines answers *how each agent's belief evolved*; `agents.json` answers *who was in the debate* — a question that until today required a Markdown regex against `transcript.md` headings. AntFleet's benchmark pipeline (the named #2 integrator, per `ECOSYSTEM.md`) can now cross-reference agent persona composition with outcome quality without parsing transcript prose. The tri-state share-link in #132 is a more structural shift — operators can now hand a stakeholder a recipient-scoped preview URL without flipping the public flag, surfacing the sim on `/explore`, unlocking any REST surface, or generating any social unfurl. Zero new dependencies on either PR — the 36th and 37th consecutive zero-deps PRs since the Nemotron addition.

---

### Theme 2 — README + docs visual-and-bilingual rebuild (Aaron's 70-minute evening session)
**Summary:** Between 18:48Z and 20:06Z on Jun 1, Aaron pushed fourteen commits directly to `main` (eleven Aeon-coauthored direct pushes plus one merged PR, #134, that landed at the end). The session has three threads running in parallel: visual identity refresh (new logo, regenerated diagrams, demo GIF, optimized image sizes), README restructure (trim Features wall to highlights and move the catalog into the deep-dive docs), and Chinese-locale full-sync (FEATURES.zh-CN.md doubled in size, two brand-new Chinese deep-dives, broken-link cleanup). The catalog row count rose from 37 (zh) / 46 (en) to a parity 46-and-46.

**Commits:**

- `b4fe46e` — **docs: refresh README diagrams with regenerated images** (18:48:55Z)
  - +5 / −5 in `README.md` (filename bumps to bust GitHub's camo image cache). Six file swaps in `docs/images/`: `agent-grounding.png`, `cross-platform-dynamics.png`, `graph-memory-pipeline.png`, `simulate-anything-hero.png`, `simulation-phases.png` added; old `diagram1.jpg`, `diagram2.jpg`, `graph-memory.jpg`, `grounding.jpg`, `simulate-anything.jpg` removed.

- `c309deb` — **docs: switch README logo to new chrome shark mark** (18:49:53Z)
  - +1 / −1 in `README.md`; new `docs/images/miroshark-logo.jpg` added, old `docs/images/miroshark.jpg` removed. Cache-busting filename change.

- `fa55ebb` — **docs: fix overview image mapping and drop product screenshots** (18:53:34Z)
  - +3 / −11 in `README.md`. Six product screenshots (`1.jpg`–`6.jpg`) removed; `miroshark-overview.jpg` renamed to `miroshark-overview-diagram.png`; restores the original circular X/Reddit/Polymarket feedback-loop `diagram2.jpg`. "Screenshots" heading renamed to "Diagrams".

- `74246e8` — **docs: slim README Features to highlights, move full list to docs** (19:00:59Z)
  - +13 / −76 in `README.md` (314 → 242 lines). +53 in `docs/FEATURES.md` and +44 in `docs/FEATURES.zh-CN.md` — both deep-dive docs gain an "All features at a glance" / "功能速览" index table at the top so the complete catalog is preserved when the README stops listing it. README now shows an 8-feature Highlights table plus a "40+ more →" link. **Net effect:** no feature content lost, README reads as a teaser instead of an exhaustive enumeration.

- `a117e22` — **docs(zh): full-sync FEATURES.zh-CN.md with English** (19:15:47Z)
  - +590 / −39 across a single file: `docs/FEATURES.zh-CN.md`. The Chinese deep-dive had drifted to 30 sections (37-row catalog) while the English grew to 51 sections (46-row catalog). This rebuild adds the 9 missing catalog rows (Trajectory Export, Trajectory Chart SVG, Trading Signal JSON, Archive Bundle, Farcaster Frame, Live Watch Page, Jupyter Notebook Export, OriginTrail DKG Citation, WaybackClaw Archive) and translates the 21 missing deep-dive sections (Demographic Grounding, Belief Trajectory Export, Farcaster Frame v2, oEmbed, Trajectory Chart SVG, Trading Signal JSON, Peak-Round Analytics, Belief Volatility, Sparklines, Polymarket JSON, Clone JSON, Consensus Badge, Platform Aggregate Stats, Platform Stats Badge, Surface Catalog API, BibTeX, Archive Bundle, Sitemap, Live Watch Page, Jupyter Export, Webhook Event Filtering). The mistitled 转录导出 heading (was 模拟轨迹导出) gets fixed in the same pass. **Result:** both docs now have 52 headings and a 46-row catalog, in the same order. EN 987 lines / ZH 986 lines.

- `eb23a85` — **docs: drop diagram2, distribute remaining diagrams contextually** (19:21:31Z)
  - +11 / −14 in `README.md`. The circular X/Reddit/Polymarket loop (`diagram2.jpg`) is removed and the grouped "Diagrams" table is dissolved. The three remaining diagrams now sit inline next to the text they illustrate: 5-phase pipeline after "What it does", agent-grounding layers after "Use cases", graph-memory pipeline ahead of "Documentation".

- `fb0f197` — **docs(zh): fix broken NOTIFICATIONS.md links in catalog rows** (19:23:34Z)
  - +3 / −3. The Discord / SMTP / Telegram catalog rows in `FEATURES.zh-CN.md` carried over `docs/`-prefixed links from the README. Now that the catalog lives inside `docs/`, those resolved to `docs/docs/NOTIFICATIONS.md`. Changed to bare `NOTIFICATIONS.md`, matching the deep-dive prose links. All sibling-doc links in both FEATURES docs now resolve.

- `290e430` — **docs(zh): add Chinese translations for DEMOGRAPHICS and NOTIFICATIONS** (19:29:58Z)
  - +276 / −5 across five files. New `docs/DEMOGRAPHICS.zh-CN.md` (人口学接地, +79 lines, 6/6 headings parity with English) and new `docs/NOTIFICATIONS.zh-CN.md` (频道通知, +188 lines, 11/11 headings parity). These two docs had no Chinese version before today, so `FEATURES.zh-CN.md` was linking out to English. The English `DEMOGRAPHICS.md` and `NOTIFICATIONS.md` get the standard `<sup>English · [中文](…)</sup>` language switcher (+2 each), and `FEATURES.zh-CN.md` gets its links repointed (+5/−5) — the NOTIFICATIONS translation also points `WEBHOOKS.md` → `WEBHOOKS.zh-CN.md`. Every sibling-doc link in all four files now resolves; each language links to its own siblings.

- `b196460` — **docs: replace demo GIF with new capture** (19:37:09Z)
  - +1 / −1. New filename `miroshark-demo.gif` busts GitHub's camo cache for the updated demo capture.

- `e98308d` — **docs: swap Chinese section image for localized overview diagram** (19:40:23Z)
  - +1 / −1. Uses `miroshark-overview-cn.png` — the 中文 counterpart of `miroshark-overview-diagram.png` — for the Chinese section.

- `d3455f5` — **docs: swap README diagrams for optimized JPGs (#134)** (merged 20:06:56Z) — first merged PR of the cluster.
  - +6 / −6 in `README.md` (filename `-v2` bumps to bust camo cache). Six PNG diagrams swapped to JPG: `agent-grounding-v2.jpg`, `graph-memory-pipeline-v2.jpg`, `miroshark-overview-cn-v2.jpg`, `miroshark-overview-diagram-v2.jpg`, `simulate-anything-hero-v2.jpg`, `simulation-phases-v2.jpg`. **The PR description records ~9.8 MB → ~836 KB (~92% smaller).** PR opened and merged within the session — capped the visual-rebuild thread with a payload-size win.

**Impact:** This is the single largest documentation/visual revision since the original README. It addresses three latent debts simultaneously. (a) The visuals — the diagrams had drifted, the demo GIF was stale, the logo was due, six product screenshots had outlived their relevance, and the diagram set was double-housed (a "Diagrams" table + inline placements). The post-window state: smaller payload (the optimized JPGs ship ~9 MB less of image data), in-context placement, current art. (b) The Chinese locale — `FEATURES.zh-CN.md` had drifted by 21 sections and 9 catalog rows since the English edition, and two of its three peer docs had no Chinese version, so the Chinese deep-dive's sibling-doc links pointed at English content. The post-window state: parity (52 headings each, 46-row catalog each), and `DEMOGRAPHICS` and `NOTIFICATIONS` now both have Chinese versions wired into the locale graph. (c) The README structure — a 46-row feature wall was reading as exhaustive enumeration, not as introduction. The post-window state: 314 → 242 lines, an 8-feature Highlights table, full catalog preserved in `docs/FEATURES.md` and `docs/FEATURES.zh-CN.md`. This is the bilingual reciprocal of the May-31 README rebuild (`#127`–`#129`'s visual identity cascade applied the marketing-site palette across ~60 SPA files) — that rebuild moved color identity, this one moves doc structure and locale fidelity.

---

### Theme 3 — UI polish: button radius leak + report-panel contrast
**Summary:** One PR — `#133`, merged 19:46:06Z (4 seconds before `#132` Private Share Link, as part of the same evening sequence). Two bugs in one diff: a CSS specificity leak that was making list and tab buttons render as pills, and a leftover light-theme palette in the report's right panel that was black-on-dark.

**Commits:**

- `c428a26` — **fix(ui): square off tab/row buttons and raise report-panel contrast (#133)** (merged 19:46:06Z)
  - +107 / −96 across three files.
  - `frontend/src/components/Step4Report.vue` (+99 / −96): the bulk of the diff. The report's right-panel palette had ~85 `rgba(10, 10, 10, ...)` borders/dividers/dots/fills plus several dark-violet text colors (`#5B21B6`, `#6D28D9`, `#7C3AED`, `#8B5CF6`) that sat **black-on-dark** against the `#110a26` panel — including a near-invisible muted timeline dot next to the LLM RESPONSE / TOOL RESULT markers. Migrate everything to light-on-dark `rgba(244, 241, 255, ...)` and brighten the dim violet text to `#a78bfa` / `#c4b5fd`.
  - `frontend/src/components/DemographicBreakdown.vue` (+4 / 0) and `frontend/src/components/PolymarketChart.vue` (+4 / 0): set `border-radius: 0` on `.demo-tab`, `.pm-market-row`, and `.insight-tab`. The PR description identifies the root cause precisely — a global `button { border-radius: 9999px }` default was leaking onto list and tab buttons that never set their own radius, so their background, left accent, and `focus-visible` outline all rendered as a stadium/oval ring. Opting these three classes out matches the flat cards around them.

**Impact:** Two distinct fixes that were independently visible to anyone running the app — the timeline-dot/divider contrast bug masked structural signals in the report's runtime log, and the pill-button bug made list rows look like CTAs. Worth noting the structural-shape fix is precise (three class opt-outs, not a global override) — the global pill default still applies to actual buttons that *want* the radius, which is presumably most of them. Aeon-coauthored, opened and merged inside Aaron's evening session.

---

### Theme 4 — Ecosystem table grew to 16+ named integrators today
**Summary:** Three single-line ecosystem additions merged in the 12-minute window 15:12:36Z → 15:18:02Z today (Jun 2). `#138` HivemindOS (new external builder), `#139` Echo Oracle (rename from "Echo", same maintainer @BuiltByEcho), `#141` SyntheticsAI (new external). `#140` Capacitr (the fourth in the day's batch) is still open at window close. The cluster brings `ECOSYSTEM.md` to ≥16 publicly-named integrators since the registry's bootstrap with NurstarK's `#109` on 2026-05-26.

**Commits:**

- `03a7401` — **docs: add SyntheticsAI to ecosystem (#141)** (merged 15:12:36Z)
  - +1 / 0 in `ECOSYSTEM.md`. Adds `SyntheticsAI · [@SyntheticsAI_](https://x.com/SyntheticsAI_) · [syntheticuser.org](https://syntheticuser.org)`. Inserted alphabetically between Supercompact and Xerg.

- `0c93b51` — **List Echo Oracle in ecosystem (#139)** (merged 15:12:41Z)
  - +1 / −1 in `ECOSYSTEM.md`. Rename of the existing "Echo" row to "Echo Oracle" by @BuiltByEcho. Same maintainer, same `builtbyecho.xyz` link — the name update reflects what the project is now called publicly.

- `f64b900` — **docs: add HivemindOS to ecosystem (#138)** (merged 15:18:02Z)
  - +1 / 0 in `ECOSYSTEM.md`. Adds `HivemindOS · [website](https://hivemindos.liamvisionary.com) · [@thehivemindos](https://x.com/thehivemindos) · [repo](https://github.com/LiamVisionary/hivemindos)`. The PR description notes the row was trimmed to house style: website + X handle + repo, dropping the Bankr token-launch link and the personal dev handle for consistency with the rest of the table.

**Impact:** Three integrator inbound-census additions in 12 minutes — the cleanest external-signal cluster of the window. Tracks against the still-open hyperstition target of "≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31" — that target was already met by RevaultDrops + AntFleet + several others, but the count keeps compounding. PR `#140` Capacitr is still open at window close (`state: open`, no `merged_at`) and presumably lands tomorrow if the housekeeping pattern holds.

---

## aaronjmars/miroshark-aeon

### Theme 5 — Self-improvement opened, not yet merged; no substantive commits to `main`
**Summary:** No substantive commits to `main` in the window. The 33 commits visible on the default branch are all scheduler / skill auto-commit churn (`chore(scheduler): update cron state`, `chore(<skill>): auto-commit YYYY-MM-DD`, `chore(cron): <skill> success`) — pure state-file churn from the cron orchestration layer, excluded as noise per the May-31 recap convention. The substantive Aeon work today opened as PR `#50` but did not merge in window.

**Open at window close:**

- `aaronjmars/miroshark-aeon#50` — `improve(repo-actions): blocked-features registry stops re-suggesting Operator Profile` (state `open`, no `merged_at`)
  - Branch `improve/blocked-features-registry`. Two files: new `memory/topics/blocked-features.md` (the registry with one bootstrap entry — Operator Profile, verified blocked by `platform_stats.py:42-49` which documents `project_id` as the closest stable identifier on `SimulationState`); modified `skills/repo-actions/SKILL.md` step 4 (case-insensitive signature-keyword match against each candidate idea, exclude on hit, append `Excluded (blocked): <title>` line to article's Selection Rationale, 30-second re-verification on each match so the block auto-lifts when upstream lifts the constraint). Triggered by `repo-actions` having suggested **Operator Profile** 13 times across 2026-05-08 → 2026-06-01 — every cycle after the 7-day exclusion window expired. Today's `feature` skill confirmed the block by grep, then pivoted to the #2 candidate (Agent Persona Export → PR #137). The registry frees one idea slot per `repo-actions` run for net-new suggestions and prevents wasted feature-build cycles on perpetually-blocked ideas.

---

## Developer Notes
- **New dependencies:** none. The 36th (PR #132) and 37th (PR #137) consecutive zero-new-deps PRs on MiroShark since the Nemotron addition. The README-and-docs cluster touches no `package.json` or `requirements.txt`. PR #133 is pure CSS/template. The three ecosystem rows touch only `ECOSYSTEM.md`. Aeon's open PR #50 is documentation-only too.
- **Breaking changes:** none observed. PR #132 adds endpoints; PR #137 adds an endpoint and three frozenset entries — both net-additive. PR #133 changes only CSS color values and one `border-radius` rule scoped to three classes; not load-bearing for any JS. The Chinese-doc and image-swap commits don't touch any code path.
- **Architecture shifts:** one — PR #132 takes MiroShark's per-sim sharing model from binary (`is_public` flag, public-or-private) to tri-state (public / token-gated / private). The token-gated state grants the `/preview/<token>` landing page **only**, not the REST surface family. This is the first time the platform has had a sharing primitive whose payload is **strictly more restrictive than the public option** rather than just an alternative. It also exposes a new envelope at `<sim_dir>/share-tokens/` co-located with sim data — worth noting for any future sim-deletion or backup code paths.
- **Tech debt:** none introduced. One subtle "tech credit" worth noting: PR #137's surface-catalog entry initially carried `added_in_pr: 135` (probably from a draft PR that never opened); the drift-guard test caught it pre-merge and a follow-up commit corrected to `added_in_pr: 137`. That's the surface-catalog self-maintaining as designed — the catalog being hardcoded rather than auto-derived means data-entry mistakes show up at PR review, not in production.
- **Catalog count drift:** start of window = 28 catalogued (per May-30 PR #130 + May-31 PR #131 follow-up). End of window = 29 catalogued (26 publish-gated per-sim + 2 platform + 1 self-ref), after `agents_json` added to `_CATALOG` + `_PER_SIM_TRACKED_KEYS`. The Private Share-Link route is **not** a 27th publish-gated per-sim surface — by design, since the token is what's gated, not the sim's `is_public` flag — so it does not appear in the catalog.
- **Surface-stats family invariants held:** `SURFACE_KEYS` grew by exactly one (`agents_json`), `_PER_SIM_TRACKED_KEYS` grew by exactly one, both drift tests passed (the `test_unit_surface_stats` expected set was updated in the same PR).

## What's Next
- **PR #140 Capacitr (ecosystem) is open.** Trivial single-line add; expected to merge in tomorrow's window if Aaron's housekeeping cadence holds.
- **Aeon PR #50 (blocked-features registry) is open.** Validation is end-to-end on the next `repo-actions` run (Jun-3 14:00 UTC). If it lands, the Jun-3 article should excerpt `Excluded (blocked): Operator Profile` from its Selection Rationale.
- **Jun-01 repo-actions batch — only #2 has been built so far** (Agent Persona Export → PR #137 today). #1 Operator Profile (blocked, awaits data-model decision on adding an `operator` field to `SimulationState`), #3 Simulation Search (redundant with `/api/simulation/public` filter set), #4 Gallery Trending (pre-existing as `?sort=trending`), and #5 Per-Sim Surface Engagement (pre-existing as `/surface-stats`) are all addressed but not built. Batch effectively closed except for #1's data-model decision.
- **Jun-02 repo-actions batch generated today**: #1 Ecosystem JSON Registry (re-eligible May-26 #5), #2 Scenario Clone Button (re-eligible May-26 #3), #3 Japanese README & FEATURES (re-eligible May-26 #2 since CN is delivered), #4 Simulation Batch Create API (net-new), #5 Per-Project Stats (net-new). Tomorrow's `feature` run picks from this set.
- **`miroshark-aeon` main has had no substantive merges since PR #49** (2026-06-01 Path B Top Trades fallback). Self-improve, repo-actions, feature, and the housekeeping skills all ran cleanly today; the only open PR is #50, awaiting merge.
- **Surface count target:** the 30-surface threshold is one publish-gated per-sim surface away. Tomorrow's `feature` pick will most likely land it.
- **Aaron's Jun-1 evening session pattern:** thirteen commits in 78 minutes, mixing direct-to-main pushes for image/doc swaps with PRs for code-touching changes. The session pattern suggests the visual-and-bilingual-rebuild thread is done; the next session is likely back to feature pickups from the Jun-02 batch.

---

## Sources
- `gh api repos/aaronjmars/MiroShark/commits?since=2026-06-01T16:04:49Z` (17 commits returned, all read)
- `gh api repos/aaronjmars/MiroShark/events` (PushEvent slice, cross-checked against commits API)
- `gh api repos/aaronjmars/miroshark-aeon/commits?since=2026-06-01T16:04:49Z` (33 commits returned — all scheduler/auto-commit churn, classified as noise; verified by message-prefix grep against `chore(scheduler|cron|<skill>):`)
- `gh api repos/aaronjmars/MiroShark/pulls/140` (verified `state: open`, no `merged_at` → not in window)
- `gh api repos/aaronjmars/miroshark-aeon/pulls/50` (verified `state: open`, no `merged_at` → counted as open, not merged)
- Per-commit detail reads via `gh api repos/aaronjmars/MiroShark/commits/<sha>` (stats + file list) for every substantive commit
- Cross-reference: `memory/MEMORY.md` (catalog count history, batch tracking, surface count), `memory/logs/2026-06-01.md` (yesterday's push-recap, feature-build context for #132), `memory/logs/2026-06-02.md` (today's feature-build context for #137, self-improve context for aeon #50, repo-actions Jun-02 batch generation)
