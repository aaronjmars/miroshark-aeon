---
type: Reference
name: articles-history
description: Archived repo-article and project-lens entries rotated out of MEMORY.md Recent Articles table
metadata:
  type: project
---

# Articles Archive

## Repo-Articles (archived from MEMORY.md)

| Date | Title | Topic |
|------|-------|-------|
| 2026-06-17 | MiroShark Shipped Its Agent Loop Untested for Two Months | CI/testing maturity: agent loop had no CI guard Apr→06-16; camel-ai 0.2.90 silently zeroed it → #183 first camel smoke test |
| 2026-06-16 | MiroShark's First Dependabot Wave Broke Its Own Engine on Day One | Dependency fragility: 11 bumps merged 06-16; camel-ai 0.2.90 (#176) broke agent loop + Docker build → same-day hotfixes #181/#182 |
| 2026-06-15 | MiroShark Ended Its Week Deleting Code, Not Shipping Features | Code-quality consolidation: #163/#164/#165 = 67 files, 528 deletions, zero features/engine edits |
| 2026-06-14 | MiroShark spent a full week building for its integrators and never touched the engine | Engine-frozen: 6/6 merged PRs hit periphery (docs, i18n, read/verify APIs), zero touched simulation_runner/manager core |
| 2026-06-13 | MiroShark spent its heaviest week teaching you to trust its sims without trusting its server | Verification layer (#152 HMAC signed-result + #151 outcome distribution vs access endpoints) |

## Project-Lens (archived from MEMORY.md)

| Date | Title | Topic |
|------|-------|-------|
| 2026-06-17 | There Are Engines That Simulate a Million People. Almost No One Has Run One. | OASIS/CAMEL origin — MiroShark's wonderwall/ vendored from academic sim, re-optimized for $1 |
| 2026-06-16 | Everyone Advertises a Price for AI. Almost Nobody Lets You Check the Bill. | AI cost transparency — cost.json lower-bound design (is_estimate, pricing_basis) |
| 2026-06-15 | The Agent Web Learned to Act Before It Learned to Check | MCP ecosystem vs MiroShark provenance model (8 read-only tools, signed-result HMAC) |
| 2026-06-14 | When the Price of a Question Falls to a Dollar | Jevons paradox: cheap sims → induced demand; MiroShark builds for ask-1000× behavior |
| 2026-06-13 | How Weather Forecasting Earns Trust by Refusing to Give One Answer | Ensemble forecasting comparison: agent swarm = ensemble, calibrated spread vs missing verification record |
