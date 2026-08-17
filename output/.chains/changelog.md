The PR is confirmed as a draft against `main`. Task complete.

## Summary

Ran the `changelog` skill in **push-to mode** (`var: push-to:aaronjmars/miroshark-website`), syncing merged PRs from `aaronjmars/miroshark` to the website's changelog.

- **Window:** 2026-08-10 → 2026-08-17 (first push-to run since the last entry, no gap in coverage)
- **New PRs found:** 6, none previously published — `aaronjmars/miroshark-website` PR [#213](https://github.com/aaronjmars/miroshark-website/pull/213) (draft)
- **Entry:** "OrcaRouter cloud preset + security & CI fixes" — new OrcaRouter cloud preset (external contributor Marc-oss-hub, #287), a nanoid security patch (#286), an httpx pin fixing an openai-3.0.0-triggered dependency break (#288), plus a maintenance rollup of 3 dependabot bumps (#283–#285)
- **Files modified:** `app/changelog-data.ts` in the website repo (branch `aeon/changelog-2026-08-17`); `memory/logs/2026-08-17.md` in this repo (silent log entry, per skill contract — no `./notify` call on this skill)
- **Note:** couldn't run `npx tsc`/`npm run build` on the cloned website repo because the sandbox blocks `cd` outside the primary working directory; flagged this in the PR body. `node --check` confirmed no syntax errors in the edited file.

Follow-up: the operator should review and merge PR #213 to publish.
