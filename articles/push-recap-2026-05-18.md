# Push Recap — 2026-05-18

## Overview

The 24h window opens with the two MiroShark PRs that sat unmerged through yesterday's recap and ends with both of them landed on `main` within four seconds of each other (23:43:19Z and 23:43:22Z on 2026-05-17). PR #85 (trajectory chart SVG, +1,099 / -4) and PR #87 (SMTP completion emails, +1,661 / -29) close two arcs at once: the embed-citation chain now has a stdlib SVG companion to the Jupyter notebook and DKG citation, and the notification quadrant is complete at four platform-agnostic channels (webhook + Discord + Slack + email). On the aeon side, two single-file surgical fixes — PR #40 (project-lens PR-status verification) and PR #41 (skill-freshness `every_Nd` cadence) — also merged, both correcting false-positive bugs caught in the last week of skill logs. Three new PRs were opened today: **PR #89 on MiroShark is the first external-contributor security PR in the project's history** (Neo4j default-password removal, by `teifurin` — same handle that starred and forked the repo today), PR #90 (Farcaster Frame v2 by aeon-feature), and aeon PR #42 (repo-pulse article output by aeon-self-improve).

**Stats:** ~2,800 lines merged to MiroShark `main` (+2,760 / -33 across 25 files in two PRs). ~9 substantive aeon-side commits (+7 / -2 in merged skill edits, plus ~600 lines of new article content). 36+ housekeeping commits on miroshark-aeon. Zero force-pushes, zero reverts.

---

## aaronjmars/MiroShark

### Theme 1: The Two-Merge Night — Embed Citation Chain + Notification Quadrant Close Simultaneously

**Summary:** Yesterday's recap framed PRs #85 (chart SVG) and #87 (SMTP) as "still open" — both opened on 2026-05-17 morning, neither merged at notify time. In the eight hours after that recap fired, both landed on `main`. The simultaneity is unusual (within 4 seconds at 23:43Z, presumably an aaronjmars batch-merge session) and meaningful: it lets the recap frame these as a single closing event rather than two separate days.

**Commits:**

- `1d5ccad` — **feat: SMTP completion-email notifications (4th channel — zero platform dependency) (#87)**
  - **New file `backend/app/services/email_notify.py`** (+796 LoC, pure stdlib `smtplib` + `email.mime` + `ssl`): `notify_if_configured()`, `build_email_message()`, `send_email()`, plus daemon-thread dispatcher and per-process `(sim_id, status)` dedup. Port-keyed transport selection (`465` ⇒ SMTP_SSL / `587` ⇒ STARTTLS / `25` ⇒ plain). Auth-optional — blank `SMTP_USER` / `SMTP_PASSWORD` routes through unauthenticated relays (e.g. `localhost:25` Postfix). On a credentialed STARTTLS-required connection where the server refuses STARTTLS, the dispatcher **refuses to send** rather than fall back to cleartext — same "secret never crosses degraded boundary" posture as the HMAC signing in PR #79.
  - **`backend/app/services/simulation_runner.py`** (+33): three new dispatch sites at terminal-state hooks (exit-code completed, exit-code failed, `simulation_end` action-log event) — stacked after the existing Slack dispatcher, making the runner a five-deep channel fan-out per terminal event.
  - **`backend/app/api/notifications.py`** (+8 / -5): `/api/config/notifications` envelope extended with `email_configured: bool` (boolean-only; recipient lists never returned).
  - **`backend/tests/test_unit_email_notify.py`** (+572 LoC, 34 offline tests): env-var pinning, `is_configured` guards, port resolution, subject/plain/HTML body builders, dedup, transport selection per port, auth-skip, **credential-leak refusal**, exception swallowing.
  - **Body shape:** `multipart/alternative`. Plain text uses the same Unicode block bars (`█████░░░░░ 62.0%`) as the Slack mrkdwn block; HTML uses inline-CSS swatches matching the Discord embed colours and a consensus-coloured "View simulation →" CTA. Subject is `[MiroShark] Bullish: <scenario>` so inbox rules can triage on direction without parsing the body. Custom headers: `X-MiroShark-Sim-Id`, `X-MiroShark-Event`.
  - **`docs/NOTIFICATIONS.md`** (+113 / -16): full SMTP section with transport table, Gmail recipe, test snippet, channel-selection guide. **`docs/FEATURES.md`** + zh-CN twin: extends "Channel-Native Completion Notifications" to four channels. **`frontend/src/components/EmbedDialog.vue`** (+17 / -3): adds the fourth "Email" chip + extends `notifConfig` reactive with `email_configured`.

- `0e5b84d` — **feat: trajectory chart SVG — stdlib-rendered belief curves for `<img>` embeds (#85)**
  - **New file `backend/app/services/chart_svg.py`** (+442 LoC, pure stdlib `xml.etree.ElementTree`): the SVG renderer. Three stance polylines (bullish `#22c55e`, neutral `#6b7280`, bearish `#ef4444`) on a fixed 800×400 viewBox, 5-line y-axis grid, adaptive x-axis labels, three-swatch legend, scenario title. Reuses `trajectory_export.build_rows` so a single schema change to `trajectory.json` flows to both the CSV and SVG surfaces. **Bytewise-deterministic output** — the same simulation always produces byte-identical SVG, which makes the output suitable as its own cache key. Same approach (stdlib XML, no `lxml` / no `matplotlib`) as the sitemap in PR #82.
  - **`backend/app/api/simulation.py`** (+78): new `GET /api/simulation/<id>/chart.svg` route. Publish-gates identically to `trajectory.csv`. Increments the `chart_svg` surface counter. `Cache-Control: public, max-age=300` (matches watch-page poll cadence). Returns 404 when trajectory empty.
  - **`backend/app/services/surface_stats.py`** (+3 / -1): extends `SURFACE_KEYS` with `chart_svg` so the inbound analytics counter recognises it.
  - **`backend/openapi.yaml`** (+50): documents the path under Publish & Embed; adds `chart_svg` to `SimulationSurfaceStats`.
  - **`backend/tests/test_unit_chart_svg.py`** (+384 LoC, 17 offline tests): viewBox lock, polyline count, stance-color preservation, y-axis inversion, 404-on-empty, malformed-input resilience, title truncation, single-round renders, **deterministic byte output** assertion, route decorator + surface_stats increment presence.
  - **`frontend/src/components/EmbedDialog.vue`** (+103): new "Trajectory chart (SVG)" section under the trajectory-CSV row — lazy-loaded preview, Download .svg anchor, copyable chart URL, paste-ready `<img>` embed snippet.

**Impact:** The notification quadrant — four platform-agnostic channels (webhook for automation, Discord for community, Slack for ops, email for universal) — is the explicit completion gate the project has been building toward since PR #57. Email is the channel that requires *zero third-party accounts*: a self-hosted Postfix or a corporate MTA is enough. The credential-leak refusal in `email_notify.py` matches the HMAC signing pattern in PR #79 (webhook secret never crosses a degraded boundary) — the same security primitive applied to a new transport. Meanwhile chart.svg closes the embed citation chain: a Notion page or a Substack post or a LaTeX paper can now `<img src="...chart.svg">` and get the full belief journey with no JavaScript and no library dependency. Where the share card (PR #42) shows the verdict and the replay GIF (PR #50) shows motion, chart.svg shows the *journey* — the missing static surface for written analysis.

**Architecture shift:** `simulation_runner.py` now has a five-deep dispatch stack at each terminal-state hook (webhook → discord → slack → email → DKG action-log branch). The channel-notifier idiom (`is_configured()` + `notify_if_configured()` + per-process `_FIRED` set + daemon-thread dispatch) is now at five instances across five different transports. A 6th channel would justify a registry-based fan-out; five is still cleanly readable as a vertical stack.

---

### Theme 2: First External-Contributor Security PR

**Summary:** PR #89 is the first security-focused PR opened by an external contributor. The author `teifurin` (Furin) also starred the repo and forked it within the same day — a complete external-engagement event captured in a single repo-pulse window. The fix is small (+3 / -3 across two files) and the body is unusually well-written for a first-time external PR: it cites the 2020 Neo4j "Meow" attacks and Shodan-driven sweeps as prior-art motivation, distinguishes intentional breaking change from accidental one, and offers two scoped follow-up PRs.

**Commits:** none yet on `main` — PR #89 is OPEN.

**PR detail:**
- `docker-compose.yml` — `NEO4J_AUTH=neo4j/miroshark` → `NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:?NEO4J_PASSWORD must be set in .env}` (in both the `neo4j` and `miroshark` services, kept in sync). The `:?...` docker-compose syntax fails fast on unset variables with a clear error.
- `.env.example` — `NEO4J_PASSWORD=miroshark` → `NEO4J_PASSWORD=CHANGE_ME_GENERATE_A_RANDOM_PASSWORD`. A naive `cp .env.example .env && docker compose up` user now hits a hard error instead of shipping the public default to the internet.
- **PR status verified:** `gh pr view 89 --json state,mergedAt` → `{state: OPEN, mergedAt: null}` as of recap time.

**Impact:** From the May-16 hyperstition target log: "≥3 publicly-named external integrators citing MiroShark as AI infrastructure by 2026-07-31 (set 2026-05-16) — RevaultDrops is #1". `teifurin` is not an integrator per se, but they are the first external contributor to do focused security review and open a PR with a clear threat model. That's an early signal that the project is reaching the level of attention where security-conscious eyeballs find it. Worth tracking whether `teifurin` follows up on either of the two stated follow-up offers (README port-exposure note, launcher hardening to detect `CHANGE_ME_*` literals). For the same-day star + fork + PR overlap, see today's repo-pulse log.

---

### Theme 3: Farcaster Frame v2 Opened (Base-Chain Audience Reach)

**Summary:** PR #90 (opened today at 12:26Z by aeon-feature) makes MiroShark share pages render as interactive Farcaster Frame v2 cards in Warpcast clients. Until this PR, a `/share/<id>` URL pasted into a Warpcast cast rendered as a blank link card; the PR injects `fc:frame:*` meta tags so the same URL renders as a belief-chart image with a "View Simulation →" link button. The PR pairs naturally with yesterday's (now-merged) chart.svg: the SVG at 2:1 aspect ratio is the natural Frame backing image, with the share-card PNG (1.91:1) as the fallback for pre-trajectory simulations.

**Commits:** none yet on `main` — PR #90 is OPEN.

**PR detail (verified via `gh pr view 90 --json state,additions,deletions,changedFiles`: state=OPEN, +1,140 / -0, 10 files):**
- `backend/app/services/frame_metadata.py` (new, ~210 LoC stdlib) — `build_frame_metadata()` + `warpcast_compose_url()` helpers. Pure stdlib.
- `backend/app/api/simulation.py` — `GET /<id>/frame-metadata` route, publish-gated, 5-min cache, proxy-aware base URL detection.
- `backend/app/api/share.py` — `fc:frame:*` meta tags emitted in the public share-page `<head>`; suppressed for private sims.
- `backend/tests/test_unit_frame_metadata.py` — 13 offline tests.
- `backend/openapi.yaml` — endpoint + `FrameMetadata` + `FrameMetadataButton` schemas under Publish & Embed.
- `frontend/src/api/simulation.js` — `getFrameMetadata()` + `buildWarpcastComposeUrl()` helpers.
- `frontend/src/components/EmbedDialog.vue` — 🟣 Farcaster Frame section, dialog-open + publish-toggle loaders.

**Impact:** $MIROSHARK lives on Base. Base-native social is Farcaster. The Frame is the surface that closes the audience-reach gap for the largest Base-chain social platform — a cast containing a share URL now becomes an interactive card. Zero new dependencies — this advances the zero-dep streak to a candidate 26 PRs (#57 → #87 merged + #90 candidate).

---

## aaronjmars/miroshark-aeon

### Theme 4: Two Self-Correction PRs Land (Both Single-File, Both Surgical)

**Summary:** Aeon's self-improve and project-lens systems both shipped tiny surgical fixes for false-positive bugs observed in the past week's logs. Both PRs were opened earlier in the week and stalled — PR #40 sat for ~32h, PR #41 for ~8h — and both merged within today's window.

**Commits:**

- `6f0e7d6` — **improve: project-lens must verify PR status before notify (#40)** (+3 / -0, single file)
  - The 2026-05-15 project-lens log noted the notification said "merged" while the article body correctly said "opened" for PR #83. The skill had no guidance to verify PR state with `gh` before drafting either surface.
  - Fix: adds a "PR status verification" sub-bullet to writing guidelines (`gh pr view <num> --repo <owner>/<repo> --json state,mergedAt,updatedAt`) and a guardrail to the notify step (notification PR-status verbs MUST match the article body word-for-word).
  - Already exercised: yesterday's project-lens log shows the new step worked (`gh pr view 87 --json state,mergedAt → {state: OPEN, mergedAt: null}` and the article + notification both said "opened today").

- `8e44147` — **improve: skill-freshness handles every-N-day cron cadence (#41)** (+4 / -2, single file)
  - `repo-actions` and `self-improve` run on `*/2` day-of-month, so their articles can legitimately be up to 48h old between runs. The skill's cadence detector only knew daily / weekly / on_demand and defaulted to the 28h daily threshold — firing `FRESHNESS_WARN` every odd day at ~14:00 UTC on three consumers (feature, hyperstitions-ideas, self-improve) even though nothing was actually stale.
  - Fix: adds an `every_Nd` cadence bucket. Cron whose day-of-month field matches `^\*/(\d+)$` gets a `24 × N + 4`h threshold (`*/2` → 52h, `*/3` → 76h, etc.). Also extends the MISSING-eligible cadence set to include `every_Nd` so a never-run every-other-day producer still surfaces.

**Impact:** Both PRs are textbook examples of the aeon self-improve pattern: a log entry observes a false-positive or drift, self-improve emits a single-file SKILL.md edit, the PR sits open briefly, then merges. The aggregate effect is that the skill fleet's signal-to-noise ratio improves week over week — yesterday's skill-freshness log was the second-to-last false-positive surface for this class of bug.

---

### Theme 5: Self-Improve and Feature Skills Both Opened New PRs Today

**Summary:** Today's `self-improve` and `feature` skill runs both produced new PRs. Self-improve targeted yesterday's skill-freshness audit gap; feature targeted the May-16 repo-actions batch idea #2 (Farcaster Frame).

**Commits:**

- `1a44fd7` — `chore(self-improve): auto-commit 2026-05-18` (no `main`-content change; the branch + PR were created elsewhere)
  - **PR opened:** aeon PR #42 (`improve/repo-pulse-article-output`, +33 / -1, single file).
  - **What it does:** `skills/repo-pulse/SKILL.md` now writes `articles/repo-pulse-${today}.md` with canonical fields (`stargazers_count`, `forks_count`, `New stars (24h)`, `New forks (24h)`). Closes the architectural gap explicitly flagged by yesterday's skill-freshness audit: `articles/repo-pulse-*.md` is referenced by 5 consumers (operator-scorecard, thread-formatter, star-momentum-alert, show-hn-draft, skill-freshness) but the producer never wrote the file. Operator-scorecard step 3a already had a parser for this exact shape with a memory/logs fallback noted as "older format" — adding the article makes the primary path the actual primary path.
  - **Backward compat:** memory/logs remains the deltas source-of-truth; existing consumer fallbacks keep working unchanged. Same-day reruns overwrite (idempotent).

- `a9aace5` — `chore(feature): auto-commit 2026-05-18` (no `main`-content change for the same reason)
  - **PR opened:** MiroShark PR #90 (covered in Theme 3 above).

**Impact:** Self-improve PR #42 is interesting structurally: it's a skill-fleet-internal feedback loop. Yesterday's skill-freshness audit flagged "repo-pulse never writes articles/" → today's self-improve writes the fix. The loop is tight enough (24h from observation to PR) that the architectural gap surfaces and the patch lands in adjacent cron windows. Mark as a confirmed instance of the self-improve cadence performing its intended function — the same pattern that produced PR #40 and PR #41 in earlier weeks.

---

### Theme 6: Article-Generating Skill Runs (Housekeeping)

**Summary:** The day's cron loop fired its full daily rotation. Each skill produced an article and a corresponding log entry; nearly all of the 36 housekeeping commits on `main` are paired `feat(<skill>): ...` + `chore(<skill>): auto-commit` + `chore(cron): <skill> success` triples. No skill prompts or aeon Python code changed outside the two merged self-correction PRs.

**Commits (substantive content writes only — the chores and schedulers are elided as routine):**

- `28d420f` — `weekly-shiplog: 2026-05-18 — Four Channels, One Citation Chain, First Hop Off-Host`
  - 1,565-word narrative covering May 11–17. Frames the week around three completed arcs: notification quadrant (PR #83 + #87), citation chain (PR #80 → #84 → #85), discoverability + transport security (PR #79 + #81 + #82). Plus the first operational hotfix (PR #86, Grok→Gemini deprecation swap, same-day open + merge) and eight aeon self-corrections.
- `82e625f` — `feat(ai-framework-watch): cold start — RELEASE WEEK, 6 frameworks, 16 releases (2026-05-18)` (+225 across 3 files including a new `memory/topics/framework-watch-state.json` baseline)
  - First-ever run of this skill. Tracked: 9 / 9 frameworks (langgraph, crewAI, llamaindex, mastra, smolagents, pydantic-ai, autogen, langchain, semantic-kernel). 16 releases in the 7-day window. Notable: pydantic-ai v1.97.0 ships a breaking-ish `GoogleProvider` split + `MCPToolset` replaces `MCPServer*`; mastra 1.34.0 ships ACP coding agents + xAI voice; langgraph 1.2.0 ships a durable error-handler. crewAI 1.x still in alpha (no stable since 2025-09-30); autogen quiet ~33d.
- `dfd97f9` — `feat(repo-pulse): MiroShark daily repo pulse 2026-05-18 — 1172 stars (+7), 236 forks (+1)`
  - Stars: koolkao, mikedemarais, traewang, **teifurin**, LulzimTafaj, EVTKR, quiz42. Forks: teifurin/MiroShark. (Teifurin is the PR #89 author — see Theme 2.)
- `e2acbc4` — `feat(operator-scorecard): weekly scorecard 2026-05-18 — 🟢 OK`
  - 6/7 clean heartbeats, 0 P0/P1 flagged, 1 auto-remediated missing-skill (skill-freshness, May 17), 0 open issues.
- `f3af50b` — `feat(repo-actions): 2026-05-18 action ideas batch`
  - 5 ideas: Trading Signal JSON, Simulation Archive Bundle, Per-Agent Stance Sparklines, Scenario Clone Button, Chinese+Japanese README translations. Three are re-eligible from the May-10 batch.
- Token-report content commit (auto-commit only; no `feat:` standalone): $0.00003323 (+41.25% 24h), NEW ATH $0.0000377 (4th consecutive ATH session), FDV $3.32M crossed $3M.

**Impact:** Two of these are worth flagging as substantive: `ai-framework-watch` first-run establishes a baseline for tracking 9 competing agent frameworks (useful for the "MiroShark vs. other agent frameworks" framing in future repo-articles); `operator-scorecard 🟢 OK` confirms the 7-day fleet health window is clean despite the skill-freshness false-positive incidents. The rest is rhythm.

---

## Developer Notes

- **New dependencies:** zero. The 24-PR zero-new-deps streak (PR #57 → PR #87 merged) is preserved through both merges; PR #90 candidate would push it to 25 if it merges as-is. Both `chart_svg.py` (`xml.etree.ElementTree`) and `email_notify.py` (`smtplib` + `email.mime` + `ssl`) are pure stdlib.
- **Breaking changes:** PR #89 (still OPEN) is an intentional breaking change for any deployment that relied on the hardcoded `miroshark` Neo4j password. Operators need to add `NEO4J_PASSWORD=<their-password>` to `.env`; the error message is actionable. No breaking changes shipped to `main` yet.
- **Architecture shifts:** `simulation_runner.py` is now a five-deep channel fan-out at terminal-state hooks (webhook → discord → slack → email → DKG action-log branch). The vertical stack is still readable; a 6th channel would justify a registry. The notification-channel surface area also extended in two API places: `/api/config/notifications` now returns `email_configured` and the OpenAPI `NotificationsConfig` schema reflects it.
- **Tech debt:** None obviously introduced. `email_notify.py` carries a noteworthy comment-as-spec block around the credential-leak refusal logic — worth preserving across future refactors. The deterministic-byte-output assertion in `test_unit_chart_svg.py` is the kind of test that's easy to break with an innocent reorder; flagging here so a future contributor knows it's intentional.
- **Stalled PRs cleared:** PR #40 (~32h stall) and PR #41 both merged. PRs #85 and #87 (both opened ~12h before yesterday's recap fired, both still open at recap time) also merged. Currently OPEN: MiroShark PR #89 (~12h, external), MiroShark PR #90 (~3h, aeon), aeon PR #42 (~2h, aeon).

## What's Next

- **MiroShark PR #89 (Neo4j password fix)** — first external security PR. Worth watching for: maintainer response time, whether `teifurin` follows up on the two scoped offers (README port-exposure note, launcher hardening), whether the same external contributor becomes a repeat reviewer.
- **MiroShark PR #90 (Farcaster Frame v2)** — pairs naturally with chart.svg (now merged); Frame backing image works at 2:1 from `chart.svg`. Likely fast-merge candidate. If merged before the next push-recap, it caps the embed family at: share card PNG (PR #42) + replay GIF (PR #50) + thread (PR #72) + reproduce.json (PR #75) + lineage (PR #76) + trending (PR #78) + HMAC (PR #79) + notebook (PR #80) + filtered feed (PR #81) + sitemap (PR #82) + Discord/Slack (PR #83) + DKG (PR #84) + chart SVG (PR #85) + email (PR #87) + Farcaster Frame (PR #90) — 15 instances of the "publish-gate + surface-stats + EmbedDialog" pattern.
- **aeon PR #42 (repo-pulse article output)** — should be fast-merge. Closes the architectural gap flagged by yesterday's skill-freshness audit; backward-compat with existing memory/logs consumers; idempotent same-day reruns. Probably this week's clearest single-file self-improve win.
- **Re-eligible May-10 ideas** (Trading Signal JSON, Simulation Archive Bundle, Per-Agent Stance Sparklines) — back on the repo-actions ladder after the 7-day cool-down expired. Trading Signal JSON is the smallest of the three and has the most natural API shape; likely next candidate if `feature` runs again before the next batch refresh.
- **No new branches created and abandoned this window** — all five PRs opened in the last 36h are live and have either landed or are still tracked.

