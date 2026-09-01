*aeon-update — 2026-09-01 (follow-up)*
**PR #161 was CI-red — fixed. all 15 checks green, ready to merge.**

no new upstream delta (canon still `3b4c5a3`, the open sync PR already covers it) — but the PR was failing both catalog gates. the 01:30 run couldn't execute `bin/generate-*` (permission layer), so it hand-wrote the catalogs, and the bytes drifted from real generator output: a trailing newline in `skills.json` the generator never emits, a missing one in `packs.json`, and a raw em-dash where `json.dump` escapes it. semantically identical — the gates diff bytes.

re-ran the real generators and pushed `070eb9a4` (no semantic change). `mergeStateStatus: CLEAN`, 13 pending conflicts still tracked in the PR body.

merge when ready — baseline advances to `3b4c5a3` on merge:
https://github.com/aaronjmars/miroshark-aeon/pull/161

🔗 https://github.com/aaronjmars/miroshark-aeon/pull/161