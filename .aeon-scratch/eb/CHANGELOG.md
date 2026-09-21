# Changelog

All notable changes to eyebrow are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Exit codes are part of the CLI contract and are covered by SemVer:
`0` clean · `1` drift/policy violation · `2` usage · `3` internal error.

## [Unreleased]

## [0.4.2] - 2026-08-05

### Added

- **skills-lock discovery**: repos that publish a catalog at
  `skills/<slug>/SKILL.md` and declare it with a root `skills-lock.json`
  (dexter-mcp, solana-foundation/pay) are now discovered as a source. The
  adapter is gated on that marker so a plain `skills/` directory elsewhere is
  never picked up, and it stays inert when `aeon.yml` is also present so no
  skill is reported twice.

### Fixed

- Skill directories reached through a symlink (e.g. `skills/pay ->
  ../.agents/skills/pay`) were silently skipped during discovery; the entry is
  now resolved before it is rejected.

### Internal

- Dashboard web lockfile back to zero `npm audit` advisories; TypeScript
  majors held out of the weekly dependency group (Next 16 does not support
  TS 7).

## [0.4.1] - 2026-08-04

### Added

- **Registry scanning** (opt-in): `--registry <base-url>` adds a remote
  catalog to the scan as a new `registry` scope — off by default because,
  unlike the local scopes, reading it makes network calls. The AgentOS
  Appstore is the first adapter.
- **Listing assessment rules**: a registry exposes what a publisher
  *declared*, never the code that runs, so the rules judge the declaration —
  `REGISTRY-ENTRYPOINT-UNPINNABLE` (no integrity anchor for what executes),
  `REGISTRY-NO-SOURCE`, `REGISTRY-NO-CAPABILITY-DECL` (commands exposed with
  no permissions or secrets declared), `REGISTRY-UNVERIFIED-PUBLISHER`.
- **AEON discovery**: AEON agent repos keep skills at
  `skills/<slug>/SKILL.md` rather than under `.claude/skills`, so a scan of a
  checkout previously saw almost nothing. Gated on the `aeon.yml` marker. A
  skill's declared egress is fingerprinted as a network capability.
- **Policy — `failOnCapabilityExpansion`**: fails an artifact that, relative
  to the lockfile, gains a capability (a new egress host, exec, or filesystem
  path). For prose artifacts whose wording changes constantly, this is the
  security-relevant signal: a rug pull adds reach it was not approved for.
  Off by default. `verify` reports it as `capability_expanded`.
- **Policy — `allowContentDrift`**: stops a bare content-hash change from
  failing the gate, leaving the outcome to policy violations alone
  (capability expansion, findings, frozen/quarantine). For catalogs of prose
  artifacts edited routinely; the lockfile still records the hashes for the
  audit trail. Off by default — the usual contract is that any drift fails.
- **Dashboard**: inline actions on a change row, and the capability delta
  shown alongside it.

### Fixed

- `resolve` keeps a local source ref portable across machines instead of
  recording a machine-specific path.

## [0.4.0] - 2026-07-22

### Added

- **Tool-surface audit**: an MCP server's advertised tools are canonically
  digested from its `tools/list` result, recorded as a `tool_surface` audit
  event, and diffed per server — so a server that quietly grows a new tool
  after approval is flagged. Surfaced in `eyebrow audit` and in the dashboard
  as an advertised-tools drawer section with a change banner.
- **Sleeper alerts**: an artifact that lies dormant and then executes is a
  distinct signal from drift. The verdict is computed from the local audit
  log at snapshot time, carried and aggregated per machine, raised as a
  fleet-critical alert, named in a blast-radius gate failure, and marked in
  the fleet report and heatmap (including which machines it woke on).
- **Discovery**: VS Code MCP servers, Zed context servers, and Kiro MCP
  servers plus steering files.
- **Demo mode**: `EYEBROW_DEMO` serves the dashboard an in-memory demo
  dataset behind the `Deps` seam, with a demo-data badge and chip so it can
  never be mistaken for live data.

### Fixed

- Dashboard display names for VS Code, Zed, Kiro, and Claude Desktop.

### Internal

- `discover`: MCP artifact assembly split from config parsing.
- CI installs shellcheck on the macOS runner; the generated demo recording is
  no longer tracked; dependency bumps clear `npm audit` for the dashboard.

## [0.3.0] - 2026-07-11

### Added

- **`doctor`**: environment health check — required tools, lockfile state,
  quarantined artifacts, frozen pins, sandbox availability, usage-hook
  installation, control-plane reachability, local signing key; `--json` for
  machines and `--strict` to exit non-zero on warnings in CI.
- **SBOM**: `sbom --format` renders the lockfile as CycloneDX or SPDX 2.3.
- **Shell completion**: `completion` for bash, zsh, and fish.
- **Claude Desktop**: MCP-server discovery joins the default tool set.
- **`digest --json`** for machine-readable review summaries; `list --tool`
  and `list --type` filters.
- **Reputation export**: build a hash-only trust corpus from local approvals.
- **Release provenance**: artifacts are attested with GitHub build
  provenance — verify any download with
  `gh attestation verify <archive> -R alexverify/eyebrow`.

### Internal

- CI runs the configured `.golangci.yml` linters on pull requests
  (`only-new-issues`), gating new code without forcing a backlog cleanup.
- Refactors with no behavior change: command errors route through a shared
  `fail` helper; the dashboard backend is split by responsibility
  (`handlers.go`, `security.go`, `view.go`) and its view layer into wire types
  (`dto.go`) and the assembler (`buildscan.go`).

## [0.2.0] - 2026-06-20

### Added

- **Distribution**: install via a Homebrew cask, a checksum-verifying
  `install.sh`, and `go install`.
- **Dashboard** gained a per-finding code view (open a finding's source in a
  modal or full screen, with flagged-line highlighting and prev/next nav), an
  artifact source-file browser in the detail drawer, a plain-language
  capability summary, and the artifact's stated purpose from its frontmatter.
- **Flag-safe**: mark a finding as an accepted false positive — it stays
  visible but passes the CI gate; approvals made from the dashboard are
  auto-signed with the local key.
- **Solo mode**: when no trusted-keys registry exists, the dashboard shows
  Approved / Not approved and hides the signing vocabulary entirely.
- **Account unaccounted**: bulk-approve shadow (installed-but-undeclared)
  artifacts from the UI.
- **`wrap`** now covers Claude Code's per-project `mcpServers` store and
  tolerates a missing `.mcp.json`.
- **Control plane** (opt-in, self-hostable): audit-event ingest, team alerts
  derived from fleet drift and denied tool calls, an org reputation corpus with
  hash-only lookup, and a conformance rollup — all surfaced in the dashboard
  when `--server` is set.
- **SBOM**: export the lockfile as a CycloneDX 1.6 document.

## [0.1.0] - 2026-06-11

Initial release.

### Added

- **Component 1 — supply-chain integrity**: discover every skill, MCP server,
  plugin, hook, and rule across AI coding tools; resolve, canonically hash, and
  statically analyze them; commit an `eyebrowlock.json` lockfile; detect
  post-audit modification (rug pulls) via `verify`; `sign` lockfiles and manage
  trusted keys (ed25519). Tools: Claude Code, Cursor, Gemini, OpenCode, Codex,
  Windsurf, Copilot CLI. Linux, macOS, Windows.
- **Component 2 — runtime MCP firewall**: `wrap`/`unwrap` route stdio MCP
  servers through `eyebrow mcp-shim`, which relays JSON-RPC byte-for-byte,
  enforces per-server tool policy, injects a redacting egress proxy, and
  confines the server with an OS sandbox (Seatbelt/bwrap). Audited to
  `~/.eyebrow/audit/<date>.jsonl`, queryable with `eyebrow audit`.
- **`fleet`**: export/push a machine snapshot and print the team blast-radius
  ("git is the backend").

[Unreleased]: https://github.com/alexverify/eyebrow/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/alexverify/eyebrow/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/alexverify/eyebrow/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/alexverify/eyebrow/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/alexverify/eyebrow/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/alexverify/eyebrow/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alexverify/eyebrow/releases/tag/v0.1.0
