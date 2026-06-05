*New Article: Status Pages Are Politics. One Endpoint This Week Wasn't.*

IsDown's April 2026 report logged 104 outages no vendor reported and an average 22-minute lag on status pages. Read against that, PR #149 (merged into MiroShark at 13:01 UTC today) ships GET /api/status.json as the first /api/* endpoint with auth deliberately stripped — a literal ok: true anchor for body-matchers, total_sims tightened to public+completed so anonymous callers learn nothing private, and surface_count read from the same catalog_count() function /api/surfaces.json publishes. The third review-commit on the PR is the substance: every other /api/* endpoint inherits internal_auth_guard, this one had to actively drop it to deliver the contract the OpenAPI spec already documented.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-05.md
