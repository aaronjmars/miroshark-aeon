*Push Recap — 2026-06-12*
MiroShark — SHIPPING: /api/surfaces.json gains a ?type= category filter

Shipped to users:
• `?type=<category>` on GET /api/surfaces.json (#157) — integrators fetch one category server-side instead of pulling the full catalog + jq; unknown value 400s with the valid set, full-catalog path unchanged
• Filtered responses carry the category in their ETag (surfaces-v1-30-analytics) so they never collide with the full catalog in a shared cache
• 8 new tests assert the filtered counts partition the full catalog and the no-filter call stays byte-identical

Under the hood (aeon repo):
• feature skill now clones in-workspace + runs tests before opening PRs (#60); inbound TG/Discord/Slack messaging disabled (outbound notify unaffected)

Shape: 1 user-visible · 1 internal · 1 infra · 32 bot-filtered · 2 merged PRs
Volume: 14 files, +341/-41

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-12.md
