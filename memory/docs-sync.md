---
type: Reference
---
# Docs Sync config

Config for the `changelog` skill's **push-to** (cross-repo) branch — which product
repo's merged PRs become the changelog, and which marketing-site repo to open the
PR against. (Post-migration: the old `docs-sync` skill is folded into `changelog`
`var: push-to:…`; this file's keys are unchanged.)

- product_repo: aaronjmars/miroshark
- website_repo: aaronjmars/miroshark-website
- min_prs: 1
- lookback_days: 7
- draft: true
- git_user_name: aeonframework
- git_user_email: aeonframework@proton.me
