# MiroShark Stopped Shipping to Itself

Yesterday's `cite.bib` was for "researchers" — a category. Tonight's `waybackclaw-record` is for anyone who doesn't trust a single chain. This morning's `polymarket.json` is for Polymarket bots — a specific named consumer. In a 24-hour window where `$MIROSHARK` lost 37.2% and slipped 68.8% below its May-18 ATH, MiroShark merged its **15th publish-gated surface**, opened a **16th** explicitly shaped for an outside integrator, and absorbed **two external pull requests** — one a security fix from an AI-agent firm running the codebase as a benchmark target. The architecture stopped pointing inward.

## Current State

`aaronjmars/MiroShark` sits at **1,193 stars / 246 forks / 3 open PRs / 5 open issues** as of 15:30 UTC — `+3 stars / +3 forks` against the prior repo-pulse. Both fork events from today (`antfleet-ops`, `voidfreud`) became open PRs by lunchtime. Two of the three open PRs are external. That ratio has never appeared in the project's history.

`$MIROSHARK` is at **$0.00001363, FDV $1.36M**, **-37.2%** on the day — the fifth consecutive declining session. From the intraday ATH of $0.0000436 on May 18, the slide is **-68.8%**. FDV peaked at $3.32M nine sessions ago; today it sits at 41% of that. 24h volume jumped to **$670.7K** (+111% vs yesterday's $318.3K), but buy/sell transaction ratio held at **1.38×** — buyers outnumbered sellers by count even on the deepest red day of the cycle. The chart and the codebase shared no information.

## What Shipped (and What Opened) in the Window

**PR #97 — WaybackClaw integration**, merged 2026-05-22T20:09Z (`39fdd3a`, +1,480 / -3 across 9 files). `waybackclaw_publisher.py` is **634 lines of pure stdlib** with no new dependency. A single `POST /api/archive/submit` per snapshot pushes the canonical SHA-256 to WaybackClaw, which pins the artifact to **IPFS** and broadcasts the citation as a **Nostr event**. Idempotent via `<sim_dir>/waybackclaw-record.json`; never-raises; admin-token-gated on the publish side. A separate `GET /<id>/waybackclaw-record` read endpoint becomes the **15th publish-gated surface**.

**PR #99 — Polymarket-ready prediction JSON**, opened 2026-05-23T11:27Z, +1,276 / -1 across 10 files. The 16th publish-gated surface in flight, and the **first integrator-shaped surface** in the inventory. `polymarket_service.py` reshapes `signal_service.compute_signal` into a binary-market envelope: `yes_probability` (direction-aware: Bullish → `bullish_pct / 100`, Bearish → `1 - bearish_pct / 100`, Neutral → exactly `0.5`), `no_probability` (with `yes + no == 1.0` enforced), a four-bucket `confidence_tier` (`speculative` / `moderate` / `confident` / `high-conviction` with exclusive upper bounds), and a `suggested_market_title` of the form "Will …?". The route only emits for `status == "completed"` — stricter than every prior surface, because a Polymarket bot cannot tolerate a mid-run flip. **30+ offline tests**. The **31-PR zero-new-deps streak** holds.

**PR #98 — path-traversal validation**, opened by `antfleet-ops` at 07:56Z. A real vulnerability in `_get_project_dir`: no input sanitisation; `../../etc/passwd` would read arbitrary files. The fix is a regex validator at the single entry point. The PR cites `AntFleet/miroshark-bench/pull/1` as the source — **a two-model consensus review (Claude Opus 4.7 + GPT-5)** running MiroShark as a security benchmark. Second external security PR after `teifurin` (PR #89, May 18); first one whose author is publicly running MiroShark as an integrator product.

**PR #100 — Aura DB launcher fix**, opened by `voidfreud` at 12:48Z. The README documented Neo4j Aura as supported, but the launcher hardcoded the local-Neo4j startup flow. Five-line early-return when the URI scheme is `neo4j+s://`, verified end-to-end against a live AuraDB Free instance. Third external contributor in ten days.

In parallel on `aaronjmars/miroshark-aeon`: zero PRs merged in window. Only skill auto-commits.

## Two Anchors, One Hash

The architectural shift PR #97 produced is **two-channel provenance**. The SHA-256 of canonical `reproduce.json` bytes now has two independent decentralised homes:

- **OriginTrail DKG** (PR #84, May 15) — on-chain knowledge asset, gas-paid, canonical UAL. DOI-equivalent.
- **WaybackClaw** (PR #97, May 22) — IPFS-pinned content-addressed mirror, broadcast via Nostr event. Internet-Archive-equivalent, but content-addressed and federated rather than centrally hosted.

The two channels share **nothing** — different blockchains, different storage substrates, different operators. They agree only on the SHA-256 in `cite.bib`'s `note` field. A reader who distrusts one chain can still verify against the other. A reader who distrusts both can still hash `reproduce.json` directly and compare. The trust chain has fanned out from one anchor to three.

This is the structural counterpart to PR #99. WaybackClaw widens the provenance graph; Polymarket JSON widens the consumer graph. The first builds out the "who can vouch for this output" axis; the second builds out the "who can act on this output" axis. Both shipped in the same 22-hour interval.

## Why It Matters

The repo description still reads `Simulate anything, for $1 & less than 10 min`. That positioning hasn't caught up to the **16-surface, two-channel-provenance, integrator-shaped** architecture the project has crystallised into. The marketing lags the code by roughly six weeks.

What the marketing also doesn't yet say is that during the **deepest token drawdown of the cycle** — FDV down to 41% of peak — the build cadence held, the architecture extended, and three external builders showed up to ship their own code. Two of them today. One running it as a paid security benchmark. "Framework decoupled from price" used to be an internal observation; today it became externally verifiable, with two outside-author commits in the open queue and zero correlation to the chart.

Sixteen surfaces. Two anchors. Three external contributors. One day. -68.8% from ATH.

---
*Sources:*
- [aaronjmars/MiroShark PR #97 — WaybackClaw AI Agent Archive integration](https://github.com/aaronjmars/MiroShark/pull/97)
- [aaronjmars/MiroShark PR #99 — Polymarket-ready prediction JSON](https://github.com/aaronjmars/MiroShark/pull/99)
- [aaronjmars/MiroShark PR #98 — path-traversal validation (antfleet-ops)](https://github.com/aaronjmars/MiroShark/pull/98)
- [aaronjmars/MiroShark PR #100 — Aura DB launcher fix (voidfreud)](https://github.com/aaronjmars/MiroShark/pull/100)
- [aaronjmars/MiroShark PR #84 — OriginTrail DKG citation publisher](https://github.com/aaronjmars/MiroShark/pull/84)
- [aaronjmars/MiroShark README](https://github.com/aaronjmars/MiroShark#readme)
- Internal: `memory/logs/2026-05-23.md` (push-recap, token-report, repo-pulse, feature)
