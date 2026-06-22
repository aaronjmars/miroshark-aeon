*Repo Action Ideas — aaronjmars/MiroShark — 2026-06-22*
Five ideas this cycle; top pick closes the one remaining exact-pinned dep and lets the camel smoke test guard every future 0.2.x patch automatically.

Top pick: Loosen `camel-ai==0.2.90` → `>=0.2.90,<0.3.0` (Security/DX, Small, Priority HIGH)
 → Lets Dependabot propose camel-ai patch-release bumps that the smoke test (#196) validates automatically — security updates flow in, regression guard is live.

1. Loosen `camel-ai==0.2.90` to `>=0.2.90,<0.3.0` (HIGH, Security/DX, Small)
2. Add `wait` subcommand to `miroshark-cli` (MED, DX/Feature, Small)
3. Add `CITATION.cff` for GitHub's "Cite this repository" button (MED, Community/Growth, Small)
4. Add `cost` subcommand to `miroshark-cli` (MED, DX/Feature, Small)
5. Add `.github/FUNDING.yml` → Bankr $MIROSHARK page (MED, Growth, Small)

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-06-22.md
