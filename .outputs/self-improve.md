*Agent Self-Improvement — 2026-06-04*

pre-existing-features registry
A second exclusion registry that records features the watched repo already ships. Sibling to yesterday's blocked-features.md (PR #50). Together they cover both ways an idea can be unbuildable: architecturally blocked (needs a missing field) or already done (lives elsewhere).

Why: across May-20 → Jun-01 repo-actions batches, 8 distinct ideas were re-suggested after the watched repo had already shipped them — Gallery JSON, Gallery Trending, Compare API, Compare UI, RSS Feed, Per-Sim Surface Engagement, Webhook Test Ping, Simulation Search. May-28 batch had 3/5 pre-existing; Jun-01 batch had 3/5. The feature skill caught them via grep and pivoted, but they keep eating idea slots upstream.

What changed:
- memory/topics/pre-existing-features.md: new registry with 8 bootstrapped entries (signature keywords + lives-at path + verifying log per entry). Permanent — features don't unship.
- skills/repo-actions/SKILL.md: step 4 reads both registries, with distinct "Excluded (blocked):" vs "Excluded (pre-existing):" notes in the article's Selection Rationale.
- skills/feature/SKILL.md: step 6 checks the registry before the upstream grep, and writes back new entries when the grep discovers a previously-unknown pre-existing surface. Discovery cost paid once.

Impact: frees ~1-3 idea slots per repo-actions run for net-new suggestions; eliminates "why did the agent suggest something we already have?" operator confusion. Together with yesterday's blocked-features.md, Aeon now has a complete memory layer for "do not suggest" patterns.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/52
