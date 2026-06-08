*Push Recap — 2026-06-08*
aaronjmars/MiroShark — 3 PRs merged (all Aeon-built, all zero-deps); aaronjmars/miroshark-aeon — 2 PRs merged (skill-prompt self-improvement)

*Jun-06 repo-actions batch ships in full on MiroShark (catalog 31 → 34 in ~21h):* PR #151 `/api/stats/distribution.json` (the shape-companion of /api/stats — bucketed direction/confidence/quality/round-count + two scalar averages, for researchers + Aeon digesters + threshold-tuners), PR #150 `POST /api/simulation/batch-status` (collapses N polling HTTP calls into one for parallel batches; private and unknown sims share a byte-identical `{found:false,…nulls}` envelope so the surface can't be probed for private existence), PR #152 `/api/simulation/<id>/signed-result.json` (HMAC-SHA256 envelope over the canonical signal.json, signed with the existing WEBHOOK_SECRET — recipients verify stored signals with the same code they wrote for the webhook).

*Skill-prompt self-improvement on miroshark-aeon:* PR #53 added a new step 7 to the feature skill forcing the auth posture to be decided upfront (triggered by PR #149's three-commit mid-PR auth rewrite Jun 5) — already paid off on PR #150 the same afternoon, first-commit-correct. PR #54 expanded repo-pulse: every new stargazer + forker now gets a one-line `gh api users/$LOGIN` profile summary (name · @company · location · followers · bio), capped at 25 enriched accounts per run, with a ⚠ low-signal flag for accounts with ≤2 followers AND 0 public repos AND <30d age — a soft fake-star tell that complements star-milestone's burst check.

Key changes:
- MiroShark catalog 31 → 34 (3 entries added: outcome_distribution analytics, batch_status integration, signed_result integration); 42-PR zero-deps streak on MiroShark intact
- New auth-posture wiring point: /api/simulation/batch-status is the second /api/* endpoint deliberately exempt from internal_auth_guard (after PR #149's status probe); /api/simulation/<id>/signed-result.json inherits signal.json's per-sim publish gate
- repo-pulse output will read "Alice Chen · @ Vercel · 2.3k followers" instead of bare "github.com/alice" starting tomorrow

Stats: 34 files changed, +4,638 / -22 lines across 5 PRs
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-08.md
