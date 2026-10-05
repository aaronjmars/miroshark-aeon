## Upstream sync: `aeonfun/aeon` `531f575..1a7f07e`

**71 commits** (2026-09-24 → 2026-10-04) · **312 applied** · **26 held for manual review** · baseline → `1a7f07e`.

Every clean framework change from canon is applied via a real 3-way merge (operator customizations preserved); the derived catalogs, `AGENTS.md`, `harness-adapter/harnesses.json`/`gateways.json` and `eyebrowlock.json` were **regenerated from the synced tree** (not copied). All CI gates this diff triggers were run locally and pass: `ci-skills-json`, `ci-packs-json`, `ci-agents-md`, `ci-harnesses-json`, `ci-skill-category`, `ci-skill-integrity` (coverage + `eyebrow verify` v0.5.6, 0 critical), `ci-capabilities-parity`, `ci-aeon-skill-sync`, `validate-readme-catalog`, `validate-config`.

### Applied cleanly (81 added · 231 updated · 5 deleted)
- **Modified skills (~52):** prose/logic refreshes across most `skills/*/SKILL.md` (xai/grok call paths, read-only notes, egress hosts) + `skills/security/trusted-sources.txt`. Catalogs regenerated; `eyebrowlock.json` rescanned with the CI-pinned `eyebrow v0.5.6` so content drift and capability additions are re-locked (0 critical findings).
- **apps/cli:** `aeon init` + credential manifest, grok auth, manifest module, new `init-sandbox.sh` / `fake-gh` tests (#1158).
- **apps/dashboard:** Aeon Connect onboarding (ConnectModal, OnboardingChecklist, MobileBar, TelegramLinkCard, RunDiagnosis), connect/onboarding/openrouter/telegram API routes + libs & tests; removed the old `AuthModal`/`GrokAuthModal`/`HarnessAuthModal` (#1154–#1160). _(package.json/lock held — see below.)_
- **apps/mcp-server, apps/webhook:** skill-executor + worker otel-redact test + stub refresh.
- **scripts / harness:** new `gateway-failover.sh`, `parse-aeon-config.sh`, `run-context-summary.sh`, `commit-run-results.sh`, `feature-open-pr.sh`, `ccr-aeon-gateway.mjs`, `check-aeon-skill-sync.sh` + ~20 new `scripts/tests/*`; harness-adapter `gateways.json` + adapter refreshes (grok/codex/pi/…).
- **Workflows:** `chain-runner`, `scheduler`, `ci-gate`, `ci-harness-cli` (new), `ci-aeon-skill-sync` (new), `ci-capabilities-parity`, `ci-harnesses-json`, `ci-shellcheck`, `ci-skill-category`, `ci-skill-integrity`, `ci-skills-json`, `ci-packs-json`, `setup-commands` (ubuntu-24.04 runner pin, etc.).
- **Docs / core:** `CLAUDE.md` (+regenerated `AGENTS.md`), `CHANGELOG.md`, `docs/{CONFIGURATION,CORE,ADK,SHOWCASE,attestation,harnesses,langfuse,mcp-oauth}`, `.claude/skills/aeon/**`, `plugin/**`, `bin/{onboard,install-skill-pack,new-from-template}`, `.gitattributes`, `.gitignore`.
- **Deleted upstream:** `bin/install-from-atrium`, `apps/dashboard/components/{AuthModal,GrokAuthModal,HarnessAuthModal}.tsx`, `apps/dashboard/next-env.d.ts`.

### ⚠️ Needs manual review — the skill-count validator cluster
Upstream tightened `validate-readme-catalog.mjs` / `validate-skill-packs.mjs` to enforce **exact** catalog counts across more files. This fork's README/docs carry a **stale, divergent skill count** (hero/README say `85`, `docs/skill-packs.md` says `79`, actual catalog = `82`) that the fork's older lenient validators tolerated. Adopting the stricter validators now would turn CI red. **Held together so the fork stays green:** `scripts/validate-readme-catalog.mjs`, `scripts/validate-skill-packs.mjs`, `.github/workflows/ci-readme-catalog.yml`, `.github/workflows/ci-skill-packs.yml`, and the count-bearing docs `docs/aeon-setup.md`, `docs/examples/README.md`, `docs/assets/hero-animated.svg`, `docs/community-skill-packs.md`, `docs/skill-packs.md`, `.github/README.md`.
**To adopt:** reconcile the fork's README/docs to the real catalog total (`82`) — exact counts + full-catalog table — then apply upstream's validators. (Separately, `validate-skill-packs` already fails on fork `main` on 1 pre-existing community-registry row; its gate isn't triggered by this PR.)

### New skills — not adopted
- `feedback-builder` — new upstream skill. Adopting it changes the skill count/pack set, which the held README/docs tables would mismatch. To adopt: add `skills/feedback-builder/`, update README/docs counts + full-catalog table, run `eyebrow scan --path . --lockfile eyebrowlock.json` + `bin/generate-skills-json && bin/generate-packs-json`.
- `compute-resell` — modify/delete: the fork previously removed it; upstream modified it. Held (respects the removal).

### Needs manual review — content conflicts (your copy diverges from upstream)
- `.github/workflows/{aeon,ci-apps,ci-tests,messages}.yml` — fork-narrowed workflows vs upstream runner/gateway/test changes (overlapping hunks).
- `apps/dashboard/{package.json,package-lock.json,eslint.config.mjs}` + `apps/webhook/{package.json,package-lock.json}` — dep version bumps (eslint 9→10 + espree, next/react patch, wrangler) coupled to their locks; the fork pins these. The applied dashboard/webhook **source** builds against the fork's current deps (bumps only, no new runtime dep), so this is safe to defer.
- `skills/fetch-tweets/SKILL.md`, `skills/shiplog/SKILL.md` — fork-customized; upstream prose refresh overlaps your edits.
- `llms.txt`, `docs/assets/proof-aeon.jpg` — fork copy / binary asset vs upstream refresh.

### Operator config changed upstream (not auto-applied)
- `aeon.yml`, `STRATEGY.md` — upstream touched canon's versions; your instance config is kept as-is. Merge any new defaults you want by hand.
- `catalog/skill-icons.json`, `catalog/skill-packs.json` — operator-owned source catalogs; left untouched (the generated `skills.json`/`packs.json` were regenerated).
- Memory/state files are instance-owned and untouched.

### Note
`bin/generate-skill-icons` reports pre-existing missing glyphs for fork skills `cortx-reliability`, `create-prove`, `sc-audit` (not introduced here) — `apps/dashboard/lib/skill-icons.data.ts` was left at the fork version rather than regenerated.
