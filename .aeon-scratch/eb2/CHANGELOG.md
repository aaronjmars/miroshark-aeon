# Changelog

All notable changes to eyebrow are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Exit codes are part of the CLI contract and are covered by SemVer:
`0` clean · `1` drift/policy violation · `2` usage · `3` internal error.

## [Unreleased]

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

[Unreleased]: https://github.com/alexverify/eyebrow/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/alexverify/eyebrow/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/alexverify/eyebrow/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alexverify/eyebrow/releases/tag/v0.1.0
