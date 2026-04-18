---
name: tweet-allocator
description: Allocate $10/day worth of $MIROSHARK to top tweeters about the project — rewards organic engagement
var: ""
tags: [crypto, social]
---
> **${var}** — Override daily budget (e.g. "20" for $20/day). If empty, defaults to $10/day.

Today is ${today}. Distribute $MIROSHARK rewards to the authors of the best tweets about this project's token.

## Config

- Tracked token: read from `memory/MEMORY.md` (Tracked Token table).
- Tweet source: today's `memory/logs/${today}.md` under `## Fetch Tweets` sections (written earlier today by the `fetch-tweets` skill). **Do not read yesterday's log.**
- Bankr verification: `.bankr-cache/verified-handles.json` (produced by `scripts/prefetch-bankr.sh` before Claude starts — the sandbox blocks `BANKR_API_KEY` in curl headers, so the prefetch is the only path).

### Excluded authors (never allocate to these)

Project-owned accounts. Valuable signal, but self-dealing:

- `aaronjmars`
- `miroshark_`

### API key strategy

- **`BANKR_API_KEY`** (read-only, required) — handle-to-wallet lookups only. Used by `scripts/prefetch-bankr.sh`. Cannot send funds. Safe in CI.
- **`BANKR_SEND_KEY`** (read-write, optional) — only set when you want auto-send enabled. If unset, the skill writes a manual send plan instead.

## Steps

1. **Read today's tweets.** Extract every tweet from `## Fetch Tweets` sections in `memory/logs/${today}.md`. For each capture: `handle`, `tweet_url`, `summary`, `likes`, `retweets`. If the log has no `## Fetch Tweets` sections, log `TWEET_ALLOCATOR_EMPTY — no tweets in today's log`, send a one-line notification via `./notify` (e.g. `Tweet Allocator — ${today}: no tweets in today's log to allocate from.`), and stop.

2. **Exclude project accounts** (`aaronjmars`, `miroshark_`).

3. **Exclude already-paid tweets and authors.** Scan the last 30 days of `memory/logs/` for previous `## Tweet Allocator` entries. Drop any tweet URL that's already been rewarded. Drop any author who already got paid today.

4. **Check Bankr.** Read `.bankr-cache/verified-handles.json` — a `{ "handle": "0xwallet" | null }` map. For each remaining candidate, look up the handle:
   - Value is a `0x...` address → **eligible**, keep for allocation.
   - Value is `null`, or handle missing from the cache → **not eligible**, drop silently.

   **Hard stop if the cache is missing or empty.** Log `TWEET_ALLOCATOR_ERROR — .bankr-cache/verified-handles.json missing; check BANKR_API_KEY secret and prefetch-bankr.sh workflow output`, send an alert notification via `./notify` (e.g. `Tweet Allocator — ${today}: ERROR — Bankr cache missing, check BANKR_API_KEY secret.`), and stop. No "unverified" fallback — no wallet, no payment.

   If zero candidates remain after this step, log `TWEET_ALLOCATOR_EMPTY — no eligible tweets (nobody in today's log has a Bankr wallet)`, send a one-line notification via `./notify` (e.g. `Tweet Allocator — ${today}: no eligible tweeters (none had a verified Bankr wallet today).`), and stop.

5. **Score and rank.** `score = likes + 3 * retweets`. If both are zero/missing, score = 1. Sort descending. Take top 5.

6. **Allocate.** Budget = `${var}` if set, else `10` — **USD-equivalent, paid in $MIROSHARK on Base**. Always phrase amounts as "$X.XX in $MIROSHARK" so the USD-vs-cashtag distinction is unambiguous.
   - Each share = `(score / total_score) * budget`, rounded to 2 decimals.
   - $0.50 minimum per tweet. If the budget can't cover all 5 at $0.50, reduce count until it fits.

7. **Send or queue.**

   **If `BANKR_SEND_KEY` is not set (manual mode — default):** do not send. Write a ready-to-execute allocation plan. For each recipient: `@handle`, amount in $MIROSHARK, tweet URL, verified wallet.

   **If `BANKR_SEND_KEY` is set (auto-send):**
   ```bash
   JOB_ID=$(curl -s -X POST "https://api.bankr.bot/agent/prompt" \
     -H "X-API-Key: ${BANKR_SEND_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"send '"${amount}"' $MIROSHARK to @'"${handle}"' on base"}' \
     | jq -r '.jobId')
   ```
   Poll for completion (max 60s, 8s intervals). Record each result: handle, amount, status, tx hash or error. If curl fails (sandbox), write the request JSON to `.pending-bankr-send/` for a post-run script to process.

8. **Build the report** at `articles/tweet-allocator-${today}.md`:

   ```markdown
   # Tweet Allocation — ${today}

   **Token:** $MIROSHARK | **Budget:** $X.XX in $MIROSHARK | **Chain:** Base

   ## Rewards

   | Rank | Author | Tweet | Score | Reward | Wallet | Status |
   |------|--------|-------|-------|--------|--------|--------|
   | 1 | x.com/handle | [summary](tweet_url) | XX | $X.XX in $MIROSHARK | 0x... | pending |
   | ... | | | | | | |

   **Total allocated:** $X.XX in $MIROSHARK to N authors
   ```

9. **Notify** via `./notify`:
   ```
   *Tweet Rewards — ${today}*

   Budget: $X.XX in $MIROSHARK on Base

   1. x.com/handle — $X.XX in $MIROSHARK (score: XX)
      [brief summary]
      [View tweet](tweet_url)
   ...
   Total: $X.XX in $MIROSHARK allocated to N authors
   ```

   IMPORTANT: Use `x.com/handle` not `@handle` (avoid pinging on Telegram). Always write "$X.XX in $MIROSHARK" (not "$X.XX $MIROSHARK") so the USD-vs-cashtag distinction is unambiguous.

10. **Log** to `memory/logs/${today}.md`:
    ```markdown
    ## Tweet Allocator — ${today}
    - **Status:** TWEET_ALLOCATOR_OK (or _EMPTY / _ERROR)
    - **Budget:** $X.XX in $MIROSHARK
    - **Tweets in log:** N | **With Bankr wallet:** M | **Paid:** K
    - **Paid tweets:**
      - x.com/handle — $X.XX in $MIROSHARK — tweet_url — wallet 0x... — pending (manual send)
      - ...
    - **Total distributed:** $X.XX in $MIROSHARK
    - **Notification sent:** yes
    ```

## Sandbox note

The Bankr Agent API requires `BANKR_API_KEY` in the header — **the sandbox blocks env var expansion in curl**, so direct calls from this skill fail. All wallet verification happens in `scripts/prefetch-bankr.sh` before Claude starts. That script is the authoritative source. If the cache is missing, the skill stops — it does not try to call Bankr from inside the sandbox.

## Environment Variables Required

- `BANKR_API_KEY` — **Read-only** Bankr API key (required for prefetch). Enable Wallet API + Agent API, keep Read Only Mode **on**. Cannot send funds.
- `BANKR_SEND_KEY` — **Read-write** Bankr API key (optional). Only set when enabling auto-send. Enable Wallet API + Agent API, Read Only Mode **off**.

## Status flags

- `TWEET_ALLOCATOR_OK` — allocation plan produced (or auto-send completed).
- `TWEET_ALLOCATOR_EMPTY` — no tweets in today's log, OR no candidates have a Bankr wallet.
- `TWEET_ALLOCATOR_ERROR` — Bankr cache missing (prefetch didn't run or `BANKR_API_KEY` not set).
