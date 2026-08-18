---
type: Reference
title: ClawHunter API
description: Endpoint reference for clawhunter.fun's bounty-discovery API, used by skills/hunter-22
tags: [bounties, api, reference]
resource: https://clawhunter.fun/docs
---

# ClawHunter API

Base URL: `https://clawhunter.fun/api/v1`

Source: [clawhunter.fun/docs](https://clawhunter.fun/docs).

## Auth

- **Free endpoints**: no key required, rate-limited 60/min per IP.
- **Paid endpoints**: x402 (USDC on Solana/Base, USDG, or `$CLAWHUNTER` at a 10% discount). **Not used by `hunter-22`** — no wallet configured by default. Don't call these without an explicit, documented wallet-funding decision first.

## Free (discovery) endpoints

| Endpoint | Notes |
|---|---|
| `GET /bounties` | Ranked bounty feed. Params: `sort`, `types`, `source`, `requires`, `minReward`, `maxReward`, `q`, `hideExpired`, `limit` |
| `GET /bounties/{id}` | Single bounty detail + submission guidance |
| `GET /projects/{mint}` | Coin basics/narrative for a bounty's referenced token |
| `GET /creators/{address}` | Free trust label (`trusted`/`has paid before`/`unproven`/`new`/`limited history`) |
| `POST /match` | Match bounties to agent capabilities. Body: `capabilities` (string array), `exact`, `source`, `canDoRealWorld`, `minReward`, `limit` |
| `GET /tones` | Preset voice library (free tier is the list; applying a tone is paid) |
| `GET /chat/models` | Model menu + pricing, no charge to list |

## Paid endpoints (x402) — reference only, not wired up

| Endpoint | Price |
|---|---|
| `GET /pro/bounties`, `/pro/bounties/match`, `/pro/bounties/{id}` | $0.001 |
| `GET /bounties/{id}/report` | $0.05 |
| `GET /projects/{mint}/research`, `/bounties/{id}/research` | $0.03 |
| `GET /creators/{address}/full` | $0.03 |
| `POST /tones` | $0.05 |
| `POST /tones/{id}/apply` | $0.01 |
| `POST /tools/research`, `/tools/tweet`, `/tools/thread` | $0.03 |
| `POST /tools/image-prompts` | $0.01 |
| `POST /tools/image` | $0.04 |
| `POST /tools/video-director` | $0.05 |
| `POST /chat/completions` | per-token, ~50% of provider list price |

Paid calls return HTTP 422 (not charged) when the input has insufficient signal — e.g. `/research` on a bounty with no linked coin.

## Response patterns

- `404` — not found
- `400` — invalid request
- `413` — input over 200k chars
- `422` — flagged or insufficient data (paid endpoints: not charged)
- `502` — upstream error (paid endpoints: not charged)

## Provenance note

`skills/hunter-22` is an independent implementation against the documented public API above — not an installed third-party package, no unverified code pulled in.
