ℹ️ aeon-update: 25 commits → PR #151

**aeon-update — 2026-08-25**

Synced 25 upstream commits → PR #151. 52 files applied, 9 need a manual merge.

Canon `b7a909a..8b8d719`. New skills land: `rightstack` (Web3 stack advisor), `skill-article` (launch article for any skill). Framework: post-run notify dispatcher (tokens out of skill env), egress-audit hardening, fx harness fixes, macOS cron portability. `messages.yml` — a standing conflict — auto-merged clean this time.

Held back the whole eslint lint gate as one bundle — `ci-apps.yml` lint steps + `apps/{dashboard,webhook}` package.json + lockfiles. Dashboard runs `npm ci`; your lockfiles diverge, so shipping the gate would land it CI-red. Merge those five together or none.

Also manual: `aeon.yml` workflow (your narrowed env), `ci-tests.yml`, `docs/skill-packs.md` (fork pack counts), `llms.txt` (MiroShark copy). `aeon.yml` config got one disabled `rightstack` entry upstream — optional.

Baseline advances only when you merge.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/151

🔗 https://github.com/aaronjmars/miroshark-aeon/pull/151