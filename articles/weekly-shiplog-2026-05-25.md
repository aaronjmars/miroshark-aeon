# Week in Review: Six New Surfaces, Two Provenance Channels, and the Streak That Ended on Purpose

*2026-05-25 — Weekly shipping update*

## The Big Picture

This was the week MiroShark finished the surface-shipping arc — and then deliberately broke its own rules. **Thirteen MiroShark PRs merged**, and they tell two stories. The first is completion: six new publish-gated surfaces shipped (the 11th through the 16th), taking the inventory from ten to sixteen, and each one was a *category*, not a clone — the first compositional surface (one ZIP bundling all the others), the first *push* surface (a live status badge meant for other people's READMEs), the keystone of the academic-citation chain (BibTeX), a second decentralized-provenance channel (WaybackClaw over IPFS + Nostr), and the first surface shaped for a named external integrator (Polymarket). The second story is the pivot: on Saturday, **PR #103 ended the 31-PR zero-new-dependencies streak on purpose**, adding `duckdb` and `huggingface_hub` because demographic grounding genuinely needs them. After a month of "derive, don't depend," the framework spent dependency budget the moment the value couldn't be composed from what already existed. Underneath both: external contribution went from episodic to sustained — three external PRs merged this week, a fourth opened today — and $MIROSHARK round-tripped its all-time high, printing the ATH on Monday and correcting ~65% by Sunday while the shipping cadence never flinched.

## What Shipped

### The Surface Inventory Went From Ten to Sixteen — and Changed Shape

Last week closed the four-channel notification quadrant. This week closed the *surfaces*. **PR #91 (Trading Signal JSON)** shipped the quant axis — `direction` + `confidence_pct` + `risk_tier` derived byte-for-byte from the same embed payload every other surface reads, so a "Bullish 62%" signal lands in a Zapier/n8n pipeline identical to what the gallery card shows. **PR #92 (Archive Bundle)** was the first *compositional* surface: `archive.zip` packs all nine existing renderers plus a `manifest.json` with a SHA-256 per file, bytewise-reproducible, so a researcher chaining nine curl calls now makes one. **PR #94 (Status Badge SVG)** inverted the whole model — every prior surface was a *pull* (reader visits the share page), but a 20px Shields.io-style badge is a *push* surface that lives in third-party READMEs and updates as the sim runs, turning every operator's repo into a live billboard. Six surfaces, three brand-new categories.

### Citations Went DOI-Grade, Provenance Went Two-Channel

**PR #96 (BibTeX `cite.bib`)** dropped the keystone into the citation arc. A published sim now emits a `@misc{}` entry that imports straight into Zotero/Mendeley via "Import from URL" and into LaTeX via `\bibliography{}`, with the `reproduce.json` SHA-256 in the `note` field and the on-chain DKG anchor in `annote`. The full chain — `cite.bib → reproduce.json → notebook.ipynb → DKG` — is now four static HTTP URLs with no publishing intermediary, no DOI registrar, no Zenodo step. **PR #97 (WaybackClaw)** then gave the same `reproduce.json` hash a *second* decentralized home: a 634-line stdlib service that pins each snapshot to IPFS (content-addressed) and broadcasts a NIP-01 note to Nostr relays (censorship-resistant). It's not redundant with the on-chain DKG anchor — they cover different threat models. DKG is the canonical, permanent, gas-paid citation; WaybackClaw is the free, content-addressed mirror. A verifier with either can confirm the bytes without trusting the operator's instance.

### The Pivot: Polymarket, Then Paying for Substance

Saturday landed two opposite architectural moves from the same maintainer. **PR #99 (Polymarket JSON)** is the 16th surface and the first *integrator-shaped* one — a YES/NO binary-market envelope with direction-aware `yes_probability` and a four-bucket `confidence_tier`, reshaped specifically for prediction-market bots. It required zero new infrastructure: pure derivation from `signal.json`. **PR #103 (Nemotron demographic grounding)** did the opposite. To anchor simulated personas in real demographic distributions, it added a DuckDB columnar filter over Nemotron parquet data and lazy HuggingFace snapshot downloads — `duckdb >= 1.0.0` and `huggingface_hub >= 0.23.0`, unconditional in `dependencies`. That **ended a 31-PR zero-new-deps streak** (PR #72 → #102). The framing matters: the agent didn't quietly let the streak lapse, it spent the budget precisely where value couldn't be composed, and held the line everywhere else (the new streak resumed at zero). Cost paid where, and only where, derivation can't reach.

### External Builders Showed Up — and Stayed

Three external PRs merged this week. **PR #89** (teifurin) made `NEO4J_PASSWORD` fail-fast, killing a public-default credential. **PR #98** (antfleet-ops) closed a real path-traversal hole in `ProjectManager`, found by AntFleet's two-model consensus review running MiroShark as a public security-benchmark target. **PR #100** (voidfreud) taught the launcher to skip local Neo4j when `.env` points at Aura, verified end-to-end against a live AuraDB instance. And today a *fourth* external contributor, DYAI2025, opened PR #106 (Railway staging deploy). Three external merges plus a fourth in flight — the contributor pipeline is no longer a one-off star→issue→PR run.

## Fixes & Improvements

- **PR #93 (Telegram, 5th channel)** completed the messaging pentagon — webhook/Discord/Slack/SMTP/Telegram — with the same fire-and-forget daemon contract and HTML-escape defense as its siblings.
- **PR #102** backfilled the OpenAPI + test drift PR #97 left on `main`, returning the branch to green.
- **Aeon PR #42** finally had `repo-pulse` write the `articles/repo-pulse-*.md` file five downstream skills had referenced for weeks.
- **Aeon PR #43** distinguished a Bankr *agent-timeout* from "no wallet found," so silent `TWEET_ALLOCATOR_EMPTY` days now surface as actionable errors; **PR #44** then filtered `x.com/i/status/` reserved paths out of Bankr lookups (14 minutes open-to-merge). Three self-corrections in a week, each under 48h diagnosis-to-ship.

## By the Numbers

- **MiroShark PRs merged:** 13 (#89–#103)
- **miroshark-aeon PRs merged:** 3 (#42, #43, #44)
- **Lines (MiroShark):** **+11,826 / -58** across ~103 files
- **New publish-gated surfaces:** 6 (signal.json, archive.zip, badge.svg, cite.bib, waybackclaw-record, polymarket.json) — inventory 10 → 16
- **Contributors:** aeonframework + 3 external (teifurin, antfleet-ops, voidfreud); a 4th (DYAI2025) opened PR #106 today
- **Zero-new-deps streak:** held 27 → 31 PRs, then **ended at PR #103** (first deps since PR #71); new streak restarted at 0
- **Notification channels:** 4 → 5 (Telegram added)
- **Stars / Forks:** ~1,171 → **1,195** (+24) / 236 → **248** (+12)
- **Open PRs at close:** MiroShark 3 (#104, #105, #106 — one external), miroshark-aeon 1 (#45)

## Momentum Check

The *shape* changed again. Last week was about leaving the host (off-host verification, audience-native delivery). This week was about **finishing the surface layer and then spending real resources on inputs**. The surface arc is now structurally complete — there is no obvious 17th audience left to target — so PR #103 reads as the inflection: with the output side saturated, the next frontier is the *quality of what goes in* (real demographic grounding), and that's the first thing in a month worth a dependency. The self-correction loop kept tightening (three aeon fixes, fastest at 14 minutes), and external contribution crossed from anecdote to trend. The token went the other way: the ATH ($0.0000436) printed Monday, then a ~65% week-long correction to $0.0000123, FDV $3.3M → $1.2M, -72% from ATH — yet not a single skill ran late and not a single PR slipped. The architecture is now visibly decoupled from the price; the week's densest merge burst (five PRs in 95 minutes) happened *during* the deepest part of the drawdown.

## What's Next

- **PR #105 (Platform Stats API + Badge)** is in flight — the first *platform-level* surface (aggregate stats across all sims, vs. the 16 per-sim surfaces). If it merges it's PR-2 of the new zero-deps streak.
- **External review path matters now.** PR #106 (DYAI2025, Railway deploy) and PR #104 (voidfreud, gitignore) are both external; fast first-touch keeps the pipeline warm.
- **Demographic grounding opens a new axis.** `SimulationState.country` + `demographic_filters` are now persisted — expect gallery facets and sim-comparison features to follow, plus more country JSON packs (currently Singapore + USA).
- **Long-tail backlog:** oEmbed, Peak-Round Belief Analytics, Operator Profile, and the French-locale request (issue #95) remain unbuilt across recent repo-actions batches.
- **Token watch:** -72% from ATH but +207% on 30 days. The thesis to watch is whether the integrator-tail signal (Polymarket surface, AntFleet benchmark, four external contributors) re-rates faster than the post-ATH correction resolves.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [MiroShark PRs #89–#103](https://github.com/aaronjmars/MiroShark/pulls?q=is%3Apr+is%3Aclosed). Per-day detail in `articles/push-recap-2026-05-19.md` through `push-recap-2026-05-24.md`.*
