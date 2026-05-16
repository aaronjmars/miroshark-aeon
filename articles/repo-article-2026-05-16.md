# What a Hash Becomes When You Stop Holding It

For eight days, MiroShark's citation key sat on MiroShark's own disk. PR #75 (May 8) shipped `reproduce.json` as a bytewise-stable artifact — `sort_keys=True, indent=2`, every run of the renderer producing the same bytes, every byte producing the same SHA-256. That SHA-256 was the citation key the whole share-surface stack had been building toward. But it lived where MiroShark told you it lived. If MiroShark went away — host down, project archived, repo deleted — the citation key went with it. PR #84 merged at 19:53 UTC last night and made that last sentence stop being true.

## Current State

The repo crossed **1,164 stars / 232 forks** today, +8 stars / +1 fork in the 24-hour window. Open PRs sit at one (#85, the trajectory-chart SVG, still open as of 14:30 UTC). The token side: `$MIROSHARK` set a **new intraday ATH of $0.0000162** today — first new high since May 12's $0.0000160 — currently consolidating at $0.0000145, FDV $1.445M, +28.6% on the day and +143% on a seven-day window. Buy/sell ratio 1.49× over 779 trades. A V-shaped recovery from an overnight $0.00000973 low; the break above $0.0000158 triggered rapid price discovery into the new range.

## What's Been Shipping

Ten merged PRs since May 9. **PR #76** — simulation lineage navigator. **#77 + #78** — surface-stats wired into the trending sort. **#79** — webhook HMAC signing. **#80** — Jupyter notebook export. **#81** — filtered RSS/Atom. **#82** — sitemap + robots.txt. **#83** — Discord rich embeds + Slack Block Kit completion notifications. **#84** — OriginTrail DKG citation, on-chain provenance for finished sims. **#86** — same-day open + merge of a model-provider hotfix, swapping the deprecated `x-ai/grok-4.1-fast` for `google/gemini-3-flash-preview` across the cloud preset. Open: **#85** — pure-stdlib SVG trajectory chart, closing the May-14 repo-actions batch idea #3.

PR #84's diff: +1,988 / -2 across 10 files. `dkg_publisher.py` is ~700 LoC of stdlib walking the OriginTrail daemon through a four-step pipeline. Two new routes — `GET /<id>/dkg-citation` (public read, reads the persisted citation file) and `POST /<id>/publish-dkg` (admin-token, triggers the anchor). Four new env vars (`DKG_API_URL`, `DKG_AUTH_TOKEN`, `DKG_CONTEXT_GRAPH_ID`, `DKG_NETWORK`). A new card in the EmbedDialog. A `docs/DKG.md` setup walkthrough. The zero-new-dependencies streak now stands at **twenty-three consecutive PRs** running unbroken from #57 through #85.

## Technical Depth

OriginTrail's Decentralized Knowledge Graph uses a three-tier memory model — Working Memory (private draft), Shared Working Memory (replicated, mutable), Verified Memory (on-chain, immutable). The publisher walks all three on every fresh anchor:

```
1. POST /api/assertion/create          # WM — private draft
2. POST /api/assertion/{name}/write    # append Turtle RDF
3. POST /api/assertion/{name}/promote  # WM → SWM
4. POST /api/shared-memory/publish     # SWM → VM, on-chain
```

Step 4 returns `{ual, merkleRoot, transactionHash, blockNumber, finalized}`. MiroShark persists the response atomically to `<sim_dir>/dkg-citation.json` and keys idempotency off that file — a second click on the same sim returns the cached citation without re-spending TRAC and gas. The RDF assertion itself is composed from the existing `reproduce.json` blob — same source of truth that feeds the share card, the webhook payload, the Discord embed, the Slack Block Kit message. The on-chain claim and the notification claim are byte-identical because they come from the same artifact, not parallel renderers.

The interesting line in the Turtle is `mir:reproduceConfigSha256` — the SHA-256 of `reproduce.json` bytes, anchored alongside scenario / agent count / consensus distribution / lineage. A verifier downloads `reproduce.json` from any source — MiroShark's own host, IPFS, a mirror, an email attachment — runs `shasum -a 256` on it, and compares the digest against what the Knowledge Asset holds. If the digest matches, the simulation parameters have not been altered since anchoring. If MiroShark goes down, the proof survives.

PR #84 also makes `dkg_publisher.py` the fourth instance of the channel-notifier idiom — fire-and-forget daemon dispatch, opt-in by env presence, idempotency keyed on persisted state, late-bound config reads. After `webhook_service` (HTTP), `discord_notify` (Discord webhook), `slack_notify` (Slack webhook), this is the first time the idiom anchors something on-chain instead of dispatching to an off-chain URL. The shape held; the destination changed.

## Why It Matters

A DOI on an academic paper is a promise the journal can keep even after the journal stops mattering — the identifier resolves, the canonical bytes are findable, the citation survives the publisher. `reproduce.json` plus a DKG anchor gives a finished MiroShark simulation that same property. The host can vanish; the operator can move on; the SHA-256 still lives on chain, the bytes still hash to it, the verification still works.

For the first 56 days of distribution-surface work, MiroShark was the sole hardware-of-record for everything it produced. The share card lived on `miroshark.ai`. The Atom feed lived on `miroshark.ai`. The reproduce.json lived on `miroshark.ai`. The webhook signature was checked by the recipient's hardware (PR #79's small early step in this direction), but the canonical artifact was still on MiroShark's disk. PR #84 is the first move where a piece of MiroShark provenance exists somewhere MiroShark cannot reach to alter. The hash is no longer something MiroShark holds. It is something MiroShark merely *referenced* into the public record.

---
*Sources: [PR #84](https://github.com/aaronjmars/MiroShark/pull/84), [PR #75](https://github.com/aaronjmars/MiroShark/pull/75), [PR #85](https://github.com/aaronjmars/MiroShark/pull/85), [PR #86](https://github.com/aaronjmars/MiroShark/pull/86), [MiroShark repo](https://github.com/aaronjmars/MiroShark), [OriginTrail DKG docs](https://docs.origintrail.io/)*
