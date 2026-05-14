*Thread Draft — 2026-05-14*
Topic: Search-Engine Sitemap — MiroShark PR #82

1/ PR #82 is the 20th consecutive MiroShark PR with zero new dependencies. It ships /sitemap.xml and robots.txt — every public simulation is now indexable by any search crawler, no config required.

2/ MiroShark already served human browsers through the SPA and aggregators through the filtered RSS/Atom feed from PR #81. The one gap: web crawlers had no structured list of what was public. Every shared simulation was effectively invisible to search.

3/ The sitemap gives /share/<id> priority 0.8 and /watch/<id> priority 0.7. <lastmod> walks updated_at → created_at → state.json mtime. Turn ENABLE_SITEMAP off and both the XML endpoint and the Sitemap: robots.txt line go dark — no way to get a half-configured state.

4/ MiroShark started as a project with a SPA. It now serves three separate audiences at once — browsers hit the app, feed readers subscribe to filtered Atom, crawlers index via sitemap. All three surfaces compose the same public-corpus filter. None needed a new algorithm.

5/ 22 tests, zero new dependencies, and a sitemaps.org 0.9 compliant XML. PR #82 on MiroShark: https://github.com/aaronjmars/MiroShark/pull/82

(article: articles/thread-2026-05-14.md)
