# Push Recap — 2026-06-22

## Verdict
> SHIPPING — docs-sync: agent now auto-publishes merged PRs as website changelog

**Shape:** 0 user-visible · 36 internal · 1 infra · 4 bot-filtered
**Volume:** 9 files changed, +204/−10 lines across 3 significant PRs; 34 operational chore commits by aeonframework
**Merged PRs:** 7 total (3 significant: #71 #72 #73 on miroshark-aeon; 4 bot-filtered: #199 #200 #201 #202 on MiroShark)

---

## aaronjmars/miroshark-aeon

### docs-sync — automated changelog from merged PRs to the marketing website

**What this is:** A new agent skill reads the product repo's recently merged PRs each day, composes a changelog entry, and opens a draft PR on the marketing website. No hand-authored release notes; config-driven via `memory/docs-sync.md` so the same skill file works for any product/website pair.

**Under the hood**
- `95523b2` (PR #71) — feat(skill): add docs-sync
  - `skills/docs-sync/SKILL.md`: 179-line skill definition. Steps: fetch merged PRs from the product repo within a lookback window, dedup by PR number (the idempotency key), classify PRs into highlights vs maintenance noise, compose one `ChangelogEntry` (date, title, summary, highlights, prs array), clone the website repo, prepend the entry to `app/changelog-data.ts`, branch + commit + open a draft PR. On a bootstrap run (no `changelog-data.ts` yet) it creates the file, a `/changelog` page mirroring the site's existing chrome, a "Recent changes" section in `/docs`, and a nav link.
  - `memory/docs-sync.md`: configures `product_repo: aaronjmars/miroshark`, `website_repo: aaronjmars/miroshark-website`, `lookback_days: 7`, `draft: true`.
  - `aeon.yml`: adds `docs-sync: { enabled: true, schedule: "0 8 * * *" }` — daily 08:00 UTC.
- `170f4db` (PR #72) — docs-sync: hide PR link from notification output
  - `skills/docs-sync/SKILL.md`: removes the `PR: <url>` line from the step-6 notify template so the website draft-PR URL stays out of the outbound channel notification. Internal `memory/logs/` records keep it for traceability.

### git attribution hardening — cross-repo commits now link to @aeonframework

**What this is:** When any skill clones an external repo (e.g. the website repo during docs-sync), the fresh clone does not inherit the workflow's git identity. Past docs-sync runs produced commits attributed to `aeon@miroshark-aeon.bot` — an email that links to no GitHub account. Switching to `--global` makes every repo cloned during a run inherit the correct identity before any commits are made.

**Infra**
- `e7a416c` (PR #73) — fix(attribution): always commit cross-repo work as aeonframework@proton.me
  - `.github/workflows/aeon.yml`: `git config user.name/email` → `git config --global user.name/email`. Covers `external-feature`, `repo-revive`, `smithery-manifest`, and any future skill that clones a repo.
  - `.github/workflows/chain-runner.yml`: same change — covers chain-based skills.
  - `skills/docs-sync/SKILL.md`: adds explicit `git config user.name/email` inside the clone block as a per-clone guard with an inline comment on why the fallback is unsafe.

### Internal: operational chore volume

34 commits by aeonframework tracking: scheduler state (`chore(scheduler): update cron state` ×5), cron success markers for shiplog, repo-pulse, star-momentum, docs-sync, token-report, heartbeat, tweet-digest, memory-flush, thread-formatter, self-improve, feature, repo-actions. Each auto-commit updates `memory/logs/`, `memory/skill-health/`, `.outputs/`, `apps/dashboard/outputs/`, and `memory/token-usage.csv`. No product path changes.

---

## aaronjmars/MiroShark

### Internal: dependabot CI/Actions wave (all bot-filtered)

4 PRs merged, all by `dependabot[bot]`, all touching only `.github/` or frontend package/lock files:
- `c3c1965` (#201) — actions/setup-node 5→6 (major CI action upgrade, no config changes)
- `89ee2a6` (#200) — docker/metadata-action 5→6 (Docker build CI)
- `d7fce95` (#199) — docker/setup-qemu-action 3→4 (Docker multi-arch CI)
- `c6c973a` (#202) — dompurify 3.4.10→3.4.11 (security patch: fixed leaky config via `setConfig` hooks; frontend only, `npm audit` clean post-bump)

Bot-filtered per rule: all authored by `dependabot[bot]` and touching only `.github/` or package/lock files. Dropped count: 4.

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none
- **New public surface:** `docs-sync` skill (daily 08:00 UTC in `aeon.yml`); `memory/docs-sync.md` config entry
- **Tech debt added:** none

## Open threads
- PR #203 (MiroShark) — `feat(llm): separate thinking-token budget from response budget for reasoning models` — **CLOSED without merge**. Built by the feature skill today: adds `LLM_REASONING_MAX_TOKENS` (int) + `LLM_REASONING_EFFORT` (str) to `config.py`; new `_resolve_reasoning_directive()` staticmethod in `llm_client.py` maps both to OpenRouter's `reasoning` field; 8 offline unit tests. State: CLOSED — not merged. Carried to tomorrow if maintainer re-opens.

## Sources
- aaronjmars/MiroShark: ok — 4 commits (all bot-filtered); 4 bot PRs merged; 0 significant
- aaronjmars/miroshark-aeon: ok — 37 commits (3 significant PR merges + 34 chore); 3 PRs merged
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 4
- diff-truncated: 0
