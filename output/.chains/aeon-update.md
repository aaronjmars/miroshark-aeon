✅ aeon-update: 7 commits synced → PR #174

**aeon-update — 2026-09-07** ⭐

synced 7 upstream commits → PR #174. baseline moves to `21b82db` on merge.

18 files applied clean. no new skills — this window is hardening, not surface area:
- `send-email` — delivery preflight: a 200 only means "accepted", so it now checks prior sends for bounces before composing
- `vuln-scanner` — trufflehog git-history scan is bounded now, no more phantom-success runs
- `pr-review` — machine-readable verdict receipts for the dev-loop chain
- `deploy-uni-hook` — price/skew gates anchor to the pool's own start price, not an implicit 1.0

`eyebrowlock.json` regenerated with the SHA256-verified v0.4.2 binary — 4 fingerprints changed, no new egress hosts.

12 conflicts still yours to merge by hand. 2 moved this window — both `.github/workflows/*` (env-narrowing vs upstream edits), and the PAT can't push workflow files anyway. the other 10 unchanged.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/174

🔗 https://github.com/aaronjmars/miroshark-aeon/pull/174