# Week in Review: Four Channels, One Citation Chain, and the First Hop Off-Host

*2026-05-18 — Weekly shipping update*

## The Big Picture

Last week's headline was *surfaces talking to each other*. This week's headline is *surfaces leaving the host*. Nine MiroShark PRs merged Mon–Sun, and they cluster into two finished quadrants. The **notification quadrant** — Webhook + Discord + Slack + Email — went from one instance to four with **PR #83 (Discord/Slack rich notifications)** and **PR #87 (SMTP completion emails)**. The **citation chain** — `reproduce.json` (last week) → `notebook.ipynb` → on-chain DKG anchor → embeddable SVG — completed with **PR #80 (Jupyter notebook export)**, **PR #84 (OriginTrail DKG citation)**, and **PR #85 (trajectory chart SVG)**. In between, **PR #81 (filtered RSS/Atom)** and **PR #82 (sitemap.xml)** made the corpus discoverable, **PR #79 (webhook HMAC)** made transport verifiable, and **PR #86** swapped a deprecated xAI model out of the cloud preset in the first ops-keepalive merge in MiroShark's history. The zero-new-deps streak reached **24 consecutive PRs (#57 → #87)**. On the agent side, **eight miroshark-aeon PRs merged** — two self-improve fixes, the largest skill catalog refresh in this repo's history (29 skills via #36 + #37), and four more self-corrections. MiroShark crossed **1,171 stars / 236 forks** (+~37 stars, +10 forks), and $MIROSHARK printed **four consecutive ATH sessions** — the latest at $0.0000377 with FDV crossing $3.32M, **+447% on the week, +1,397% on the month**.

## What Shipped

### The Notification Quadrant Closes (Webhook → Discord → Slack → DKG → Email)

The channel-notifier idiom — `is_configured()` env-var guard, per-process `(sim_id, status)` dedup, daemon-thread fire-and-forget dispatch — went from one instance at week-start to five at week-end. **PR #83** (merged Friday) added `discord_notify.py` and `slack_notify.py`: Discord rich embeds with consensus-coloured borders pulled straight from the SPA's palette, Slack Block Kit messages with Unicode block-bar belief percentages (`█████░░░░░ 52.0%`) that render natively in mobile push notifications. 57 offline tests. First MiroShark feature whose PR body explicitly named confirmed external integrators' stacks — RevaultDrops on Discord, CancerHawk on Slack.

**PR #87** (merged Sunday late-night) shipped SMTP as the fourth channel. Port-keyed transport — `465` → `SMTP_SSL`, `587` → `STARTTLS`, `25` → plain — auth-optional so `localhost:25` to a self-hosted relay works without credentials. The load-bearing detail is the credential-leak refusal: when `SMTP_USER`/`SMTP_PASSWORD` are set and STARTTLS is refused, the dispatcher refuses to send rather than fall back to cleartext. `multipart/alternative` body uses the same block-bar glyphs as Slack in plaintext and the Discord colour swatches as inline-CSS in HTML, so a recipient seeing both surfaces reads the same signal. With email shipped, no operator needs a Discord server or a Slack workspace to be paged on completion — every research team already has an inbox.

### The Citation Chain Completes — and Takes Its First Hop Off-Host

**PR #80 (Monday)** shipped `GET /api/simulation/<id>/notebook.ipynb` — pre-populated nbformat 4 Jupyter notebooks with the trajectory CSV embedded as a Python string literal and seven analysis cells already scaffolded around it. Standalone-runnable: hit *Run All* in air-gapped JupyterLab and the analysis builds itself. Bytewise-stable: two exports of a finished sim produce identical bytes, so the SHA-256 is a stable citation key for paper appendices.

**PR #84 (Friday)** takes the citation chain off-host. `dkg_publisher.py` anchors a finished sim's `reproduce.json` SHA-256 as an OriginTrail DKG Knowledge Asset, walking the four-step daemon flow — `assertion/create` → `write` → `promote` → `shared-memory/publish`. Returns a UAL + Merkle root + transaction hash + block number. A third-party verifier can fetch reproduce.json, hash it, and compare against the on-chain Merkle root *without trusting Aaron's instance*. Same provenance property a DOI gives a paper or Stripe gives a charge — the first MiroShark artifact whose hardware-of-record is not the operator's own machine.

**PR #85 (Sunday)** closes the embed leg. `GET /api/simulation/<id>/chart.svg` renders the belief trajectory as pure-stdlib SVG via `xml.etree.ElementTree` — three coloured polylines on a fixed `viewBox`, adaptive x-ticks, byte-deterministic. Notion / Substack / Ghost / LaTeX render `<img src=…/chart.svg>` natively, no JS. The PNG share card is fixed-resolution; the SVG is the embed-anywhere cousin.

### Discoverability, Transport Security, and the First Operational Hotfix

**PR #79 (Monday)** shipped `X-MiroShark-Signature: sha256=<hex>` HMAC signing — Stripe/GitHub's standard scheme. Pair with PR #84 and the pattern crystallizes: anywhere a byte stream leaves MiroShark, the receiver can prove its provenance without re-fetching. **PR #81 + #82 (Thursday)** merged 11 minutes apart. The first grafts the gallery's six filter knobs onto `/api/feed.atom` + `.rss`, turning syndication from a firehose into a structured signal source. The second adds `/sitemap.xml` + `/robots.txt` — one Search Console submission, every published sim becomes a Google entry point.

**PR #86 (Saturday)** is unlike any prior MiroShark merge: xAI deprecated `x-ai/grok-4.1-fast` on OpenRouter and every cloud-preset call started 404'ing. PR #86 swapped three slots (Smart, NER, `:online`) to `google/gemini-3-flash-preview` and updated every EN+zh-CN doc reference. Same-day open and merge (14:19 UTC open → 14:20 UTC merge). The Default slot — Mimo V2 Flash, the 850-call cost driver — was untouched. Establishes a precedent: upstream provider deprecations are now part of MiroShark's regular maintenance surface.

## Fixes & Improvements

- **Aeon PR #34** removed three scratch verifier scripts the feature skill had leaked to repo root; added `.gitignore` patterns + a "repo root is OFF-LIMITS" prompt rule.
- **Aeon PR #35** added a grep step to the feature skill: check existing routes / OpenAPI / docs *before* building, with a `FEATURE_SKIP` exit when every idea is redundant. First field-test passed silently in the PR #83 build cycle.
- **Aeon PR #36 + #37** synced 29 skills from upstream (7 from aeon-agent, 22 from aeon), all landing `enabled: false`. Catalog size went from ~55 to 84.
- **Aeon PR #38 + #39** enabled six skills for launch-comms + weekly-visibility, then immediately reverted `contributor-spotlight` when its `fork-cohort` dependency was caught still disabled — pre-flight check pattern working as designed.
- **Aeon PR #40** hardened `project-lens` with a mandatory `gh pr view` PR-status check before any notification — fixes the May 15 drift where the notification said "merged" while the article body correctly said "opened."
- **Aeon PR #41** taught `skill-freshness` to handle every-N-day cron cadences (was over-flagging weekly skills as stale).

## By the Numbers

- **MiroShark merged:** 9 PRs (#79 → #87)
- **MiroShark in flight at week close:** 1 open PR (#89, security: `NEO4J_PASSWORD` hardening from external contributor @teifurin, opened ~3h before window close)
- **miroshark-aeon merged:** 8 PRs (#34–#41)
- **Lines (MiroShark):** +11,627 / -128 across ~120 files
- **Stars:** ~1,134 → 1,171 (+~37)
- **Forks:** 226 → 236 (+10)
- **Notification channels:** 1 → 4 (Webhook + Discord + Slack + Email; DKG is a 5th channel-notifier-shaped surface but on-chain)
- **Channel-notifier idiom instances:** 1 → 5
- **Zero-new-deps streak:** **24 consecutive substantive MiroShark PRs (#57 → #87)**
- **First-of-its-kind merges:** 3 (PR #84 first on-chain artifact; PR #86 first provider-deprecation hotfix; PR #87 universal-fallback channel)
- **External contributors active:** 1 (@teifurin opened PR #89 in the final hours)

## Momentum Check

The shape of the work changed again. Last week shipped 8 PRs around the *graph between surfaces*. This week shipped 9 around **off-host verification, audience-native delivery, and provider-resilience** — the substrate now reaches *beyond* the operator's machine. PR #84 is the load-bearing structural shift: for the first time, the integrity check for a MiroShark artifact runs on hardware the operator does not own. PR #87 closes a different loop — the four-channel notification quadrant is now structurally complete, and the channel-notifier idiom is the most-copied pattern in the codebase (five instances, three landed this week). The agent caught and fixed *eight* of its own behavioral patterns in seven days — scratch-file leaks, redundant idea generation, skill catalog drift, dependency cycles, PR-status drift, cron-cadence mismatch — without any human-filed bug, suggesting the self-improve loop is chewing failure modes faster than they accumulate. Token momentum tracked the structural progress: four consecutive ATH sessions (May 12 → 16 → 17 → 18), FDV crossed $3M today, first Japanese-language coverage (@m000_crypto, May 17), first founder-side VC call-out tweet (May 18), Chinese-language $MIROSHARK mentions on five separate days.

## What's Next

- **PR #89** from external contributor @teifurin is the first PR of the new week and the first external-contributor PR in some time — worth prioritizing the review path so the first-touch experience is fast.
- **Notification-quadrant work is structurally done.** Next notification-tier work is more likely **observability** (extending webhook-log #73 / surface-stats #74 to the new channels) than another channel.
- **Open `feature` candidates from the May-16 batch (4 remaining):** oEmbed, Farcaster Frame, Peak-Round Belief Analytics, Operator Profile page. Plus three older unbuilt from May-10 (Trading Signal JSON, Per-Agent Sparklines, Archive Bundle) and three from May-08 (oEmbed appears in both lists — likely the next pick).
- **Issue #70 on MiroShark** (Cyril Private Impact mode + MiroResult collaboration) — still untouched after two weeks.
- **Hyperstition targets** — Chinese-language coverage by 2026-06-15 is now over-realized (CN mentions 5 of 7 days + JP coverage two days running); external Aeon operator by 2026-06-30 still has no movement; ≥3 named integrators by 2026-07-31 still at 1 (RevaultDrops).
- **$MIROSHARK at $0.0000332, FDV $3.32M, +447% 7d** — four-consecutive-ATH structure suggests the market is repricing on the integration-tail signal. Watch for a cool-off retest of the prior $0.0000162 ATH vs. continuation toward FDV $5M.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [PRs #79–#87 on MiroShark](https://github.com/aaronjmars/MiroShark/pulls?q=is%3Apr+is%3Aclosed), [PRs #34–#41 on miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon/pulls?q=is%3Apr+is%3Aclosed). Per-day detail in `articles/push-recap-2026-05-11.md` through `push-recap-2026-05-17.md`.*
