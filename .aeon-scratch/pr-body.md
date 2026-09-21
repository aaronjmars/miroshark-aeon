## Upstream sync: `aeonfun/aeon` `95142d1..ba01e9f`

**19 commits** (2026-09-14 → 2026-09-18) · **47 applied** · **5 manual (this window)** · **14 conflicts carried forward** · baseline → `ba01e9f`.

The headline of this window is upstream's **dev-loop hardening stack** (live behavioral proof + one verified repair pass + a Telegram `[dev-loop::ship]` route) and two new skills: **`sc-audit`** (deep smart-contract audit) and **`create-prove`**. Both new skills landed clean — the `eyebrow` v0.4.2 binary (the version `ci-skill-integrity.yml` actually verifies with) was fetched, checksum-verified, and run in-run, so `eyebrowlock.json` covers them and CI's coverage + drift gates pass.

### Applied cleanly
- **New skills:** `sc-audit` (+ fixtures/vault + references/hook-checklist), `create-prove`  _(regenerated `catalog/skills.json`, `catalog/packs.json` → 82 skills, `eyebrowlock.json` via eyebrow v0.4.2, `AGENTS.md`)_
- **Modified skills:** `aeon-update`, `changelog`, `feature`, `idea-pipeline`, `vuln-scanner`
- **Scripts / harness:** new `scripts/dev-loop-proof.sh`, `scripts/dev-loop-repair.sh`, `scripts/stage-sc-audit.sh`; updated `dev-loop-pr.sh`, `dev-loop-review.sh`, `install-harness.sh`, `resolve-riva-capabilities.sh`, `run-grok.sh`, `skill_mode.sh`, `telegram-route.sh`, `harness-adapter/adapters/codex.sh`; + 8 test scripts (`test_dev_loop_proof.sh`, `test_dev_loop_repair.sh`, `test_idea_pipeline_dev_loop_offer.sh`, and updates)
- **Workflows:** new `.github/workflows/ci-gate.yml` (always-on aggregate gate); updated `chain-runner.yml`
- **Apps:** `apps/dashboard/app/api/mcp-auth/callback/route.ts` (XSS fix), `apps/mcp-server/src/skill-executor.ts` (Riva shadow-mode isolation)
- **Auto-merged (3-way):** `apps/dashboard/lib/skill-icons.data.ts` — your local rows kept; upstream's `sc-audit` + `miroshark-matchday` icon rows applied
- **Docs / other:** `.claude/skills/aeon/**` (4), `plugin/skills/aeon/**` (4), `docs/ECOSYSTEM.md`, `CHANGELOG.md`

### Needs manual review (conflicts — your local copy diverges from upstream)
These 5 files changed both locally (fork customization) and upstream on overlapping lines, so they weren't auto-merged. Review with `git diff 95142d1..ba01e9f -- <file>` against your local copy.

- **`.github/workflows/aeon.yml`** — you narrowed the run `env:`; upstream touched it in `1dbbfd9`, `1d183dc`, `ba01e9f` (dev-loop proof-guard). Merge upstream's disjoint changes, keep your env narrowing.
- **`.github/workflows/ci-tests.yml`** — fork test list vs upstream's new dev-loop-proof test steps (`094c10d`, `1d183dc`, `73f660e`). Add the new test steps you want.
- **`.github/README.md`** — fork (MiroShark) copy vs upstream rewrite (`1d183dc`, `1dbbfd9`). **Note:** I applied a *surgical* fix here — bumped the "all 80 skills by pack" caption to **82** so `ci-readme-catalog` stays green after the catalog regen. The upstream README rewrite itself is still unmerged; reconcile by hand.
- **`docs/skill-packs.md`** — fork pack-count table vs upstream skill-table rewrite (`030f646`, `c2624e1`, `1dbbfd9`, `1d183dc`), 3 regions. (Fork counts here already read "79/80" — stale vs the 82-skill catalog; reconcile when you merge.)
- **`skills/miroshark-matchday/SKILL.md`** — MiroShark-relevant. Upstream added a **vertical 9:16 render path** (`2e9efdb`) — a clean +2 addition you likely want:
  ```diff
  + - **Vertical cut (local run, after the 16:9 batch):** also render each sim to a 9:16 MP4 (`<out>-9x16.mp4`) for Shorts/TikTok/Reels ...
  + - Vertical: <local 9x16 mp4 path, or "failed: <reason>", or "n/a (CI)">
  ```
  It's a CONFLICT only because your fork copy diverges nearby. Graft these two lines in.

### Operator config changed upstream (not auto-applied — reconcile by hand)
- **`aeon.yml`** (+2/-1) — upstream added a default `sc-audit` skill entry and bumped the `dev-loop` chain `max_dispatches` 2→5:
  ```diff
  +  sc-audit: { enabled: false, schedule: "workflow_dispatch", model: "claude-opus-4-8", var: "" } # deep smart-contract audit ...
  -    max_dispatches: 2
  +    max_dispatches: 5
  ```
  The new `sc-audit` **skill files are already installed** by this PR; add the `aeon.yml` entry only if you want it schedulable from the dashboard.
- **`catalog/skill-icons.json`** (+2/-0) — upstream added `sc-audit` + `miroshark-matchday` glyphs. Left as-is (operator-owned; regenerated, never copied). `bin/generate-skill-icons` currently fails on missing glyphs for `cortx-reliability` (pre-existing fork skill), `create-prove`, and `sc-audit`. The subsystem is **not CI-gated**, so this is cosmetic — to unblock the generator, add glyph rows for those three (the `sc-audit`/`miroshark-matchday` ones are in upstream's diff above) and re-run `node bin/generate-skill-icons`.

### Conflicts carried forward (pre-existing, outside this compare window)
Unchanged this window; still divergent, surfaced each run until reconciled:
- `.github/workflows/messages.yml` (env-narrowed)
- `apps/dashboard/package.json` + `package-lock.json`, `apps/webhook/package.json` + `package-lock.json` (eslint-lint-gate coupled lockfile conflicts)
- `llms.txt` (fork copy)
- `skills/competitor-monitor/SKILL.md` (upstream adds an example egress host — needs a lock rescan; coupled with `scripts/competitor-monitor.mjs`)
- `skills/compute-resell`, `skills/submit-hook` — new upstream skills (#1036/#1040) never installed locally; they predate the baseline so are no longer in the compare window. The `eyebrow` binary is now proven runnable in-run, so a future run (or a manual `eyebrow scan`) can pick them up.

### Upstream commits
| SHA | Summary |
|-----|---------|
| ba01e9f | fix(dev-loop): close proof-guard gaps from the dev-loop PR stack (#1078) |
| 73f660e | feat(idea-pipeline): offer: entry point for dev-loop targets (#1077) |
| 8fa449a | feat(telegram): route a [dev-loop::ship] reply into chain-runner.yml (#1076) |
| 1d183dc | feat(dev-loop): require live behavioral proof, not just review (#1075) |
| c2624e1 | docs: sync PRs #1062-#1073 to aeon docs (#1074) |
| 554097c | feat(vuln-scanner): harden disclosure routing (A5.0/A5b.0) (#1073) |
| 1dbbfd9 | feat(sc-audit): add smart-contract audit skill (#1072) |
| c5eaf63 | fix(ecosystem): refresh HivemindOS avatar, drop dead Spoon row (#1071) |
| 094c10d | feat(dev-loop): add one verified repair pass (#1070) |
| 7a7b98a | fix(feature): scope Aeon watermark to dev-loop test runs only (#1069) |
| bdc2532 | fix(vuln-scanner): rephrase curl-pipe-to-shell to clear eyebrow RCE gate (#1068) |
| f6546e9 | fix(mcp-server): close Riva shadow-mode isolation gap (#1067) |
| 5b08c24 | fix(dashboard): escape MCP OAuth callback HTML (reflected XSS) (#1066) |
| 172ae1c | ci: add always-on CI Gate to aggregate path-filtered checks (#1065) |
| 2e9efdb | feat(miroshark-matchday): vertical 9:16 render path (#1062) |
| 09dd581 | docs: add #1060 to changelog and correct skill-lead count (#1064) |
| 030f646 | docs: sync PRs #1042-#1061 to aeon docs (#1063) |
| 7e53f56 | fix(grok): don't claim auth staged after a failed oauth refresh (#1060) |
| 38f0f88 | fix: close two aeon-update/changelog gaps that land sync PRs CI-red (#1061) |

---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
