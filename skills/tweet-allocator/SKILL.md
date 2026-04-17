---
name: tweet-allocator
description: Allocate $10/day worth of $MIROSHARK to top tweeters about the project — rewards organic engagement
var: ""
tags: [crypto, social]
---
> **${var}** — Override daily budget (e.g. "20" for $20/day). If empty, defaults to $10/day.

Today is ${today}. Distribute $MIROSHARK rewards to the authors of the best tweets about this project's token.

## Config

This skill reads the tracked token from `memory/MEMORY.md` (Tracked Token table).
It reads recent tweet data from `memory/logs/` (entries logged by the `fetch-tweets` skill).
It uses the Bankr Agent API to verify Twitter handles have linked wallets.

### Excluded Authors (project accounts — never allocate to these)

These are project-owned accounts. Tweets from them are valuable signal but should not receive allocations (that would be self-dealing):

- `aaronjmars` — project creator
- `miroshark_` — MiroShark project account

### API Key Strategy

This skill uses **two separate Bankr API keys** for safety:

- **`BANKR_API_KEY`** (read-only) — Used for daily automated runs. Can verify handles and look up wallets but **cannot send funds**. Safe to use in CI/cron.
- **`BANKR_SEND_KEY`** (read-write, optional) — Only needed when auto-send is enabled. Has Agent API write access to execute transfers. Not used until the operator explicitly enables auto-send.

---

Read memory/MEMORY.md for the tracked token info.
Read the last 3 days of memory/logs/ for fetch-tweets entries.
Read the last 3 days of memory/logs/ for any previous tweet-allocator entries (to avoid double-paying).

## Steps

1. **Collect tweet data (last 24h only).** Read today's `memory/logs/${today}.md` for `## Fetch Tweets` sections. Extract every tweet that was reported — for each one, capture:
   - `handle` (the x.com/handle, NOT @handle)
   - `tweet_url` (full https://x.com/handle/status/ID link)
   - `summary` (brief content description)
   - `likes`, `retweets` (engagement numbers — use 0 if not logged)
   - `date` (when it was posted or reported)

   Also check `.outputs/fetch-tweets.md` and `.xai-cache/fetch-tweets.json` for any additional tweet data from today.

   If NO tweets found from the last 24h, log "TWEET_ALLOCATOR_EMPTY — no tweets found today" to `memory/logs/${today}.md` and **stop — do NOT send any notification**.

   **Required-token filter (defensive).** Read the `fetch-tweets` entry in `aeon.yml` — its `var` lists the OR-separated tokens that define a valid tweet (e.g. `$MIROSHARK OR @miroshark_ OR github.com/aaronjmars/miroshark`). For each candidate tweet, check whether its `summary` / `text` / URL contains **at least one** of those tokens (case-insensitive substring match). Drop any tweet that contains **none** of them — those are stale pre-filter false positives (e.g. a tweet using the bare word "miroshark" without the $ cashtag). Log the drops in the run entry under `**Dropped (no required token):**`. This mirrors the `scripts/filter-xai-tweets.py` guard that `fetch-tweets` applies to the Grok cache, protecting against older log entries written before the filter existed.

2. **Deduplicate — no double-paying tweets OR authors.** Scan the last 30 days of `memory/logs/` for previous `## Tweet Allocator` entries. Build two lists:
   - `PAID_TWEETS` — tweet URLs that were already rewarded
   - `PAID_AUTHORS` — X handles that have already received a reward in the last 24h (same-day dedup)

   Remove any tweets from step 1 where:
   - The tweet URL appears in `PAID_TWEETS` (never pay the same tweet twice), OR
   - The author handle appears in `PAID_AUTHORS` (max one reward per author per day)

   If all tweets were already paid or all authors already rewarded today, log "TWEET_ALLOCATOR_SKIPPED — all recent tweets/authors already rewarded" and stop.

3. **Score and rank tweets.** For each unpaid tweet, compute an engagement score:
   ```
   score = (likes * 1) + (retweets * 3)
   ```
   If engagement data is missing (zeros), assign a base score of 1 so every tweet gets at least considered.

   Sort by score descending. Take the top 5 tweets (or fewer if less than 5 unpaid tweets exist).

4. **Verify Bankr accounts — always check the pre-fetched cache first.** The workflow runs `scripts/prefetch-bankr.sh` before Claude starts, which queries the Bankr Agent API with full env access (`BANKR_API_KEY` in curl headers is blocked inside the sandbox — the cache is the authoritative source).

   ```bash
   cat .bankr-cache/verified-handles.json 2>/dev/null
   ```

   The cache is a JSON object mapping `{ "handle": "0xwallet" }` — or `null` if the handle has no Bankr wallet. Use it like this:
   - If `.bankr-cache/verified-handles.json` exists: look up each candidate handle in the cache.
     - Value is a `0x...` address → **verified**, include in allocation.
     - Value is `null` or missing → **unverified**, exclude from allocation. List separately in the report with the note: "Sign up at bankr.bot to claim future rewards."
   - If the cache file is missing or empty **and** `BANKR_API_KEY` is set, attempt the direct Agent API call as a fallback (likely to fail inside the sandbox, but worth trying):

   ```bash
   JOB_ID=$(curl -s -X POST "https://api.bankr.bot/agent/prompt" \
     -H "X-API-Key: ${BANKR_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"what is the wallet address for @'"${handle}"' on base? just tell me the address or say they don'\''t have one"}' \
     | jq -r '.jobId')
   ```

   Poll for completion (max 60s, 8s intervals):
   ```bash
   for i in $(seq 1 8); do
     RESULT=$(curl -s "https://api.bankr.bot/agent/job/${JOB_ID}" \
       -H "X-API-Key: ${BANKR_API_KEY}")
     STATUS=$(echo "$RESULT" | jq -r '.status')
     if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then break; fi
     sleep 8
   done
   ```

   - If both the cache and the direct API are unavailable, mark all handles as "unverified (no Bankr data available — check that `BANKR_API_KEY` is set as a GitHub secret and that `scripts/prefetch-bankr.sh` ran successfully in the workflow)".

   Only verified handles proceed to the allocation step.

5. **Allocate the budget.** The daily budget is `${var}` if set, otherwise `10` **USD-equivalent, paid in $MIROSHARK on Base**. Always phrase the amount as "$X in $MIROSHARK" in every output (notification, report, log) so the reader understands the $-sign refers to USD value, not a cashtag for $MIROSHARK.
   - Distribute proportionally by score: each tweet's share = `(tweet_score / total_score) * budget`
   - Round to 2 decimal places ($MIROSHARK has 6 decimals, but keep amounts human-readable)
   - Minimum allocation: $0.50 per tweet. If proportional share is less, set to $0.50 and redistribute remainder.
   - If the budget can't cover all selected tweets at $0.50 minimum, reduce the number of tweets until it fits.

6. **Send or report.** Check if `BANKR_SEND_KEY` is set:

   **If `BANKR_SEND_KEY` is NOT set (default — manual mode):**
   Do NOT send any tokens. Output the allocation plan so the operator can execute transfers manually. For each allocated tweet, list:
   - The X handle (as `@handle` — the format needed for Bankr)
   - The $MIROSHARK amount
   - The tweet URL (for reference)
   - The verified wallet address (from step 4)

   Save as a ready-to-execute list. The operator will use `distribute-tokens` or the Bankr dashboard to send.

   **If `BANKR_SEND_KEY` IS set (auto-send mode):**
   Send $MIROSHARK to each verified handle using the read-write key:
   ```bash
   JOB_ID=$(curl -s -X POST "https://api.bankr.bot/agent/prompt" \
     -H "X-API-Key: ${BANKR_SEND_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"send '"${amount}"' $MIROSHARK to @'"${handle}"' on base"}' \
     | jq -r '.jobId')
   ```
   Poll for completion (max 60s, 8s intervals). Record each result: handle, amount, status, tx hash or error.

7. **Build the allocation report** and save to `articles/tweet-allocator-${today}.md`:

   ```markdown
   # Tweet Allocation — ${today}

   **Token:** $MIROSHARK | **Budget:** $X.XX in $MIROSHARK | **Chain:** Base

   ## Rewards

   | Rank | Author | Tweet | Score | Reward | Status |
   |------|--------|-------|-------|--------|--------|
   | 1 | x.com/handle | [summary](tweet_url) | XX | $X.XX in $MIROSHARK | pending |
   | 2 | x.com/handle | [summary](tweet_url) | XX | $X.XX in $MIROSHARK | pending |
   | ... | | | | | |

   **Total allocated:** $X.XX in $MIROSHARK (manual send required)
   **Recipients:** N authors

   ## Scoring Method
   Score = (likes x 1) + (retweets x 3). Budget split proportionally, $0.50 minimum per tweet.

   ## Source Tweets
   [Full list of all tweets considered, with engagement data]
   ```

8. **Send notification** via `./notify`:
   ```
   *Tweet Rewards — ${today}*

   Budget: $X.XX in $MIROSHARK on Base

   1. x.com/handle — $X.XX in $MIROSHARK (score: XX)
      [brief summary]
      [View tweet](tweet_url)

   2. x.com/handle — $X.XX in $MIROSHARK (score: XX)
      [brief summary]
      [View tweet](tweet_url)

   ...

   Total: $X.XX in $MIROSHARK allocated to N authors (manual send)
   ```

   IMPORTANT: Do NOT use @handle format in the notification — it pings users on Telegram. Use x.com/handle instead. Always write "$X.XX in $MIROSHARK" (not just "$X.XX $MIROSHARK") so the USD-vs-cashtag distinction is unambiguous.

9. **Log** to `memory/logs/${today}.md`:
   ```markdown
   ## Tweet Allocator — ${today}
   - **Status**: TWEET_ALLOCATOR_OK (or _EMPTY / _SKIPPED / _ERROR)
   - **Budget**: $X.XX in $MIROSHARK
   - **Bankr cache**: yes / no (source: `.bankr-cache/verified-handles.json` — if no, note whether BANKR_API_KEY was missing or prefetch failed)
   - **Tweets scored**: N total, M unpaid, K rewarded
   - **Paid tweets**:
     - x.com/handle — $X.XX in $MIROSHARK — tweet_url — PENDING (manual send)
     - x.com/handle — $X.XX in $MIROSHARK — tweet_url — PENDING (manual send)
   - **Total distributed**: $X.XX / $X.XX in $MIROSHARK
   - **Notification sent**: yes / no (reason)
   ```

## Environment Variables Required

- `BANKR_API_KEY` — **Read-only** Bankr API key (required). Used for handle verification only. Enable Wallet API + Agent API, keep Read Only Mode **on**. Safe for automated cron runs — cannot send funds.
- `BANKR_SEND_KEY` — **Read-write** Bankr API key (optional). Only set this when you want auto-send enabled. Enable Wallet API + Agent API, Read Only Mode **off**. If not set, the skill outputs a manual allocation plan instead of sending.

## Sandbox note

The Bankr Agent API requires `BANKR_API_KEY` in the header — **the sandbox blocks env var expansion in curl**, which makes direct calls from this skill fail reliably. The fix is the pre-fetch pattern: `scripts/prefetch-bankr.sh` runs **before** Claude starts with full env access, queries Bankr for each candidate handle, and caches the wallet mappings to `.bankr-cache/verified-handles.json`. Always read that cache first (step 4). If the cache is missing, it means either `BANKR_API_KEY` is not set as a GitHub secret or the prefetch script failed — check the workflow log.

## Logging

Write to `memory/logs/${today}.md` under `## Tweet Allocator`. Use status flags:
- `TWEET_ALLOCATOR_OK` — rewards sent successfully
- `TWEET_ALLOCATOR_PARTIAL` — some sends failed
- `TWEET_ALLOCATOR_EMPTY` — no tweets found to reward
- `TWEET_ALLOCATOR_SKIPPED` — all tweets already rewarded
- `TWEET_ALLOCATOR_ERROR` — API error or missing config
- `TWEET_ALLOCATOR_PENDING` — sandbox blocked sends, queued for postprocess
