✅ aeon-update: synced 22 commits → PR #169

*aeon-update — 2026-09-04* ⭐

synced 22 upstream commits `3b4c5a3..bf33365` → **PR #169**, all green, mergeable clean.

34 files applied clean (12 new, 19 updated, 3 auto-merged). headline: vuln-scanner PoC gate (foundry-fork verifies high/critical findings), dev-loop feature→pr-review chain, skill-health incident-recovery, notify per-channel delivery, scheduler reads block-style model:.

one gotcha worth flagging: upstream bumped the eyebrow gate to **v0.4.2** — its `verify` is now a strict content-drift / rug-pull gate. any skill whose SKILL.md changed fails it, not just new egress hosts. first push went red; regenerated `eyebrowlock.json` with the sha256-verified v0.4.2 binary (scrubbed env), 83 artifacts before/after, no new hosts. green now. the skill's "modified skills don't need a rescan" note is stale for 0.4.2.

12 conflicts still need a human: 3 env-narrowed workflows + the dashboard/webhook eslint dep bundle + 5 fork-only files (README, llms.txt, skill-packs, skill-icons glyphs). all tracked, resurface each run til reconciled.

`aeon.yml` gained a `dev-loop` chain upstream — surfaced, not written.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/169

🔗 https://github.com/aaronjmars/miroshark-aeon/pull/169