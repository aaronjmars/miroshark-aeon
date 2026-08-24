✅ aeon-update: 43 commits synced -> PR #146

**aeon-update — 2026-08-24** ⭐

synced 43 upstream commits from `aeonfun/aeon` (`b1d9079..b7a909a`) → **[PR #146](https://github.com/aaronjmars/miroshark-aeon/pull/146)**. first real run of the downstream updater.

**85 files applied clean** — 25 added, 45 updated, 11 auto-merged 3-way, 4 deleted. catalogs + AGENTS.md regenerated, validate-config green. your local edits to notify/skill_mode/heartbeat/skill-health survived — merged, not clobbered.

what's landing:
- fx/Vercel as a 7th harness + `harnesses.json` capability manifest
- reactive-trigger + chain `when:` routing, dry-run gate before self-authored auto-merge
- structured audit log, secretcurl argv-hardening, all GH Actions SHA-pinned
- memory-flush deterministic prep

**4 need a hand** (workflows you customized + upstream also touched, overlapping lines):
- `.github/workflows/aeon.yml` — your narrowed env vs upstream's 188-line SHA-pin/harness rewrite
- `ci-tests.yml` — checkout SHA-pin + ~10 new test steps
- `messages.yml` — keep your ALL_SECRETS allowlist, cherry-pick the pins + AI_GATEWAY/VERCEL/HOOK_MAINNET_OK
- `llms.txt` — your MiroShark copy left untouched vs upstream's new generic one

baseline advances to `b7a909a` only when you merge. conflicts tracked in state, they'll resurface until reconciled.

🔗 https://github.com/aaronjmars/miroshark-aeon/pull/146