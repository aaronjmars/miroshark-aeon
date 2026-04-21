*Feature Built — 2026-04-21*

Trending Topics Auto-Discovery
MiroShark's setup page now has a "What's Trending" panel below the URL Import box. It pulls the 5 most recent items from a curated list of public news feeds (Reuters tech, The Verge, Hacker News, CoinDesk by default) and shows them as one-click cards. Click one and MiroShark grabs the article and instantly drafts three Bull/Bear/Neutral scenarios — going from blank canvas to ready-to-simulate in a single click.

Why this matters:
PR #39 on Saturday solved the blank-page problem for users who already had a document — paste a URL, get scenario cards. But people who arrive at MiroShark wanting to simulate "something about AI" or "something about crypto" without a specific article in mind were still left staring at an empty input. This closes that last onboarding gap and connects MiroShark directly to the live news cycle that prediction-market framing is built around. The Kelp DAO / Aave cascade story over the weekend (Director Mode demo accidentally previewing a real exploit ~24h early) is exactly the kind of moment this turns into a one-click simulation.

What was built:
- backend/app/api/simulation.py: New GET /api/simulation/trending endpoint (~430 lines added). Stdlib-only RSS/Atom parser using xml.etree.ElementTree + urllib.request — zero new Python dependencies. Parallel feed fetch via ThreadPoolExecutor with 5s per-feed timeout and 1MB body cap. Items deduplicated by URL, sorted newest-first. In-memory cache keyed by feed-list hash (15min TTL on success, 60s on empty so recovery is fast). Per-IP sliding-window rate limit (30/min) mirrors the existing suggest-scenarios pattern. Never 5xxes — failure modes return empty items + reason code so the UI just hides the panel.
- frontend/src/components/TrendingTopics.vue: New Vue 3 component, 5-card responsive grid (auto-fit, min 200px). Each card shows source, relative time ("3h ago"), title clamped to 3 lines, "Simulate →" CTA. Manual refresh button bypasses the server cache. Disables clicks while parent is mid-fetch so URL fetches can't stack. Hidden entirely when items array is empty.
- frontend/src/views/Home.vue: Mounts TrendingTopics under URL Import, wires @select to a new handleTrendingSelect that pushes the picked URL into urlInput and calls the existing fetchUrlDoc() — so ScenarioSuggestions auto-fires once the article text lands. Zero coupling between the two features.
- frontend/src/api/simulation.js + .env.example + README.md: API client, TRENDING_FEEDS env var docs, new "What's Trending" section in README under Smart Setup.

How it works:
The backend resolves the feed list (TRENDING_FEEDS env override → curated default), checks the in-memory cache, and on miss spawns up to 8 worker threads that each fetch one feed with timeout. Each response is XML-parsed with stdlib ElementTree; the parser handles both RSS 2.0 (channel/item, RFC 822 pubDate) and Atom (feed/entry, RFC 3339 published/updated, multi-link with rel="alternate" discrimination) plus dc:date fallbacks. Custom User-Agent header so feeds that reject default Python urllib (Reuters, several Atom blogs) still work. Frontend wiring goes through the existing URL input rather than a separate code path — clicking a trending card is identical to typing the URL by hand and hitting Fetch, so URL deduplication, error handling, the ScenarioSuggestions auto-fire, and the file-and-URL combined preview all work without modification.

What's next:
Natural follow-ups: a settings-modal feed picker persisted to a config record, per-source icons, topic-filter chips (AI / crypto / geopolitics) cycling between curated subsets. None needed today — v1 already removes the friction. Repo-actions ideas still on the table: Round Scrubber (#1, temporal explorer across all panels), Social Share Card Generator (#2, OG-image growth lever), Collaborative Comments (#4), Config Export/Import (#5).

PR: https://github.com/aaronjmars/MiroShark/pull/40
