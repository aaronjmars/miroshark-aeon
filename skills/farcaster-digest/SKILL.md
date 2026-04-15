---
name: Farcaster Digest
description: Trending and relevant Farcaster casts filtered by crypto, prediction markets, and coordination topics
var: ""
tags: [crypto, social]
---
> **${var}** — Topic filter or channel name (e.g. "prediction-markets", "base", "defi"). If empty, uses default interest areas.

If `${var}` is set, focus the search on that topic or channel.

Read memory/MEMORY.md for context on current interests and active topics.
Read the last 2 days of memory/logs/ to avoid repeating casts.

## Steps

1. **Search for relevant casts** using the Neynar cast search API. Run multiple searches across core interest areas. If `${var}` is set, search only that topic.

   Default search topics (customize via var or MEMORY.md interests):
   - `"prediction markets" | "coordination markets" | polymarket | kalshi`
   - `hyperstitions | futarchy | "mechanism design"`
   - `"AI agents" | "autonomous agents" | "agentic"`

   For each search, use WebFetch or curl:
   ```
   GET https://api.neynar.com/v2/farcaster/cast/search/?q=QUERY&sort_type=algorithmic&limit=15
   Headers: x-api-key: $NEYNAR_API_KEY
   ```

   The `sort_type=algorithmic` ensures results are ranked by engagement, not just recency.

2. **Also fetch trending casts** for broader crypto context:
   ```
   GET https://api.neynar.com/v2/farcaster/feed/trending?limit=25&time_window=24h
   Headers: x-api-key: $NEYNAR_API_KEY
   ```

3. **Filter and deduplicate.** From all fetched casts:
   - Remove duplicates (same cast hash)
   - Filter to last 24h only
   - Deduplicate against recent logs — skip any cast already covered
   - Prioritize: casts with high engagement (likes + recasts), casts from known builders/researchers, casts touching prediction markets or coordination themes

4. **Select top 5-8 casts.** For each:
   - Author username and display name
   - Cast text (truncate if over 280 chars)
   - Engagement stats (likes, recasts, replies)
   - Link: `https://warpcast.com/{username}/{cast_hash_short}`
   - One-line editorial note on why it matters

5. **Format the digest** (keep under 4000 chars):
   ```
   farcaster digest — ${today}

   @username — "cast text here"
   ↳ X likes, Y recasts | warpcast.com/user/0xabc123
   why it matters: one-line take

   @username2 — "cast text here"
   ↳ X likes, Y recasts | warpcast.com/user/0xdef456
   why it matters: one-line take

   ...
   ```

6. **Send via `./notify`** with the formatted digest.

7. **Log to memory/logs/${today}.md.** Record which casts were included and search queries used.

If no relevant casts found or the API is unreachable, log "FARCASTER_DIGEST_SKIP — no relevant casts or API error" and notify.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables Required
- `NEYNAR_API_KEY` — Neynar API key for Farcaster data access (get one at neynar.com)
