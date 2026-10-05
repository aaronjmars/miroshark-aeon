# Changelog

All notable changes to eyebrow are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Exit codes are part of the CLI contract and are covered by SemVer:
`0` clean · `1` drift/policy violation · `2` usage · `3` internal error.

## [Unreleased]

### Fixed

- `SENSITIVE-PATH-READ` no longer matches `process.env`, `import.meta.env`,
  `this.env` or a `...env` spread. The rule matched `.env` anywhere inside a
  word, so it put a high finding on nearly every JavaScript skill and plugin,
  and `eyebrow check` blocked them at the default threshold. `.env` now counts
  only as a file name: the character before the dot must not be a letter,
  digit, `_` or `.`. `cat .env`, `~/.env`, `"/app/.env"` and `.env.local`
  still match. Content hashes do not change; only these findings go away.

## [0.5.5] - 2026-09-28

### Added

- OpenClaw discovery (tool id `openclaw`). eyebrow reads the OpenClaw state
  dir (`$OPENCLAW_STATE_DIR`, default `~/.openclaw`): MCP servers from
  `mcp.servers` in `openclaw.json`, skills from `skills/` and every
  `skills.load.extraDirs` entry, and plugins from `extensions/` (each folder
  with an `openclaw.plugin.json`). A project counts as OpenClaw's only when it
  holds `.openclaw/` or `.clawhub/`; then its `skills/` and
  `.openclaw/extensions/` are read too. `openclaw.json` is JSON5, read by a new
  dependency-free JSON5 reader.
- ClawHub pins. A skill installed from ClawHub carries the `fingerprint` from
  its `.clawhub/origin.json` as its integrity anchor. When the folder no longer
  hashes to it under ClawHub's own algorithm, the skill gets a
  `CLAWHUB-FINGERPRINT-MISMATCH` finding (high). A skill with a `.gitignore` or
  `.clawhubignore` stays unpinned, because eyebrow does not evaluate ignore
  patterns.
- `eyebrow check <dir> [--json] [--fail-on high]` scans one folder as an
  untrusted skill or plugin, for install gates. It writes nothing, resolves
  nothing outside the folder, and makes no network calls. It analyzes vendor
  folders and `.git` too. A file it cannot analyze (binary, larger than
  32 MiB, unreadable) yields `CHECK-UNSCANNED-FILE` (medium); a symlink that
  leaves the folder, a symlink that does not resolve, or a named pipe or
  device yields `CHECK-UNSAFE-ENTRY` (high) and is never opened. The report
  lists at most 20 unscanned files and counts the rest in `unscannedOmitted`.
  Exit `1` when any finding reaches `--fail-on`. The JSON carries rule id,
  severity, OWASP id, file, line and whether each finding blocks; it never
  carries file content.
- `--tool <id>` on `scan` and `verify` limits discovery to one tool, for
  example `--tool openclaw`. `verify --tool` compares only that tool's locked
  entries. `scan --tool` refuses (exit `2`) a lockfile that holds other tools'
  artifacts, so it never shrinks a shared lockfile; give it its own
  `--lockfile`.

### Changed

- `verify --json` prints `"changes": []` when nothing changed. It printed
  `null` before.
- `list --tool` with an unknown tool id exits `2` and names the valid ids, as
  `scan` and `verify` do. It printed an empty list before.
- The hasher streams each file into the digest instead of reading it whole.
  Digests do not change.

## [0.5.4] - 2026-09-27

### Added

- `skills-lock.json` pins. The Vercel skills CLI (`npx skills add`) writes
  a `skills-lock.json` at the project root with a `computedHash` for each
  installed skill: a sha256 over the whole installed folder. eyebrow now
  reads those entries. A skill the lock names, under `.claude/skills/`
  (Claude Code adapter) or `skills/` (skills-lock adapter), carries the
  recorded hash as its integrity anchor in `source.integrity`. When the
  folder no longer hashes to that value under the CLI's own algorithm, the
  skill gets a `SKILLS-LOCK-MISMATCH` finding (high, file
  `skills-lock.json`), so `verify --ci` fails under the default policy. A
  lock whose recorded value changes later shows as `integrity_changed`
  drift. The hash reproduces the CLI byte for byte: files sorted by
  relative path with JavaScript `localeCompare` (punctuation before
  digits before letters, letters compared without case, lowercase first
  on a tie), then sha256 over each path followed by its bytes, with
  `.git` and `node_modules` pruned and symlinks ignored. Checked against
  a real lock: the `agent-browser` skill vendored in `elie222/inbox-zero`
  reproduces its recorded hash exactly, and a one-byte edit fails the
  gate. File names outside ASCII fall back to code-point order, which can
  differ from the CLI. A missing or malformed lock pins nothing and does
  not stop discovery.

## [0.5.3] - 2026-09-21

### Security

- `engine.Options.ConfineToRoot` for embedders that scan untrusted trees.
  Before this release, an MCP entry whose `command` was an absolute path,
  such as `/etc/passwd` or another tenant's directory, made the engine
  hash and analyze that host path. Its lines then showed up in finding
  snippets. With `ConfineToRoot` set, the engine does not read a local
  source whose path resolves outside the scan root (symlinks followed),
  or a local source that is missing from it. It reports a
  `LOCAL-OUTSIDE-ROOT` finding (high) instead, so the scan finishes and
  the verdict fails. The engine hashes and analyzes the exact path it
  checked. The option also works with `Offline`. `Scan` and `Verify`
  return an error if `ConfineToRoot` and `Global` are both set, because
  global discovery reads the host's own configuration. Discovery still
  opens fixed-name config files inside the root, so embedders must also
  remove symlinks, hard links and special files from the tree before a
  scan. The CLI does not change: scanning an absolute command path on
  your own machine is still allowed. Hosted and multi-tenant embedders
  should set the option.

### Changed

- `engine.Version().RuleCount` now counts every built-in rule id,
  including rules the pipeline raises without a pattern match, such as
  `LOCAL-OUTSIDE-ROOT`. `engine.Rules()` lists them too.

## [0.5.2] - 2026-09-21

### Added

- `engine.Options.DialContext`. An embedder of `pkg/engine` can supply the
  dialer for every TCP connection the engine opens itself: the url resolver's
  TLS pinning probe and the registry resolver's fetch. A hosted worker uses it
  to refuse private, link-local, and metadata destinations at connect time,
  after DNS resolves, which also closes DNS rebinding. Child processes such as
  git, npm, and cosign are not affected. `Offline` keeps priority and skips
  all network resolution regardless of the hook.

## [0.5.1] - 2026-09-21

### Added

- AI17Z agent packages. A `*.ai17z-agent` file under a project root is
  discovered as a `subagent` artifact of tool `ai17z`, hashed, scanned by the
  native rules, and locked like any other artifact. Hidden and vendored
  directories are skipped. The package's own checksum field is not verified
  yet.

### Changed

- The npm resolver accepts registry package specs only: an optional scope, a
  name, and an optional version or range. Git specs, tarball URLs, `file:`
  paths, and `npm:` aliases are refused with a resolution finding instead of
  being handed to `npm view` and `npm pack`, which would clone, download, or
  read a local path and, for git specs, run the package's lifecycle scripts.
  Every npm invocation now passes `--ignore-scripts`.

## [0.5.0] - 2026-09-19

### Added

- Public Go package `pkg/engine`, the first supported way to embed eyebrow in
  another Go program. `New` wires the same discoverers, resolvers, hasher, and
  analyzers the CLI uses. `Scan` returns the lockfile bytes exactly as
  `eyebrow scan` writes them, plus typed artifacts, findings, policy
  violations, and a pass or fail verdict. `Verify` compares a directory with a
  lockfile held in memory and reports drift the same way `verify --ci` does.
  `Rules` lists the native rule table and `Version` describes the build, the
  source kinds, and the tools discovery covers. Extra analyzers and
  discoverers plug in through the `Analyzer` and `Discoverer` interfaces; the
  engine owns artifact IDs and rejects unknown types and severities. An
  `Offline` option resolves local and inline sources only. A missing root is
  an error, and a fresh scan ignores approval and freeze rules, since there is
  no approved state to compare with. Artifact IDs and local refs derive from
  the root path, so callers that need results comparable across machines run
  with the working directory set to the project and `Root: "."`, as the CLI
  does.

### Changed

- The git resolver refuses a repository URL or ref that starts with a dash
  before it runs `git ls-remote`, so a declared source cannot pass options to
  git. No other CLI behaviour changes; the internal refactors behind the new
  package (`lockstore.Marshal`, `verify.Check`, `analyze.RuleTable`,
  `discover.Tools`) keep `verify` output and exit codes identical.

## [0.4.7] - 2026-09-14

### Added

- Declared layout discovery. A repo that publishes skills in a layout eyebrow
  does not know can commit an `eyebrow.discover.json` at its root: `name`
  becomes the tool id on every declared skill, `skills` lists globs relative to
  the repo root (a match counts when it is a directory holding `SKILL.md`, and
  `"."` declares the whole repo as one skill), and `harvest` lists globs
  relative to each skill directory whose URL hosts join the skill's network
  capability. Globs cannot escape the repo root, duplicate skill names across
  globs fail the scan, and a manifest that fails to parse or validate exits 3
  and names the bad field instead of reading as an empty catalog. When the
  manifest is present it owns the root and the AEON and skills-lock adapters
  stay inert there; reusing `aeon` or `skills-lock` as `name` keeps existing
  lockfile IDs.

### Changed

- Skill frontmatter parsing reads any top-level key, not only `name` and
  `description`.
- The hasher skips eyebrow's own state at the walk root only: the `.eyebrow`
  directory and the lockfile directly under the root are left out of a
  root-level skill's digest, so a rescan no longer changes the digest it just
  recorded. A nested `.eyebrow` or lockfile is hashed as ordinary content. A
  lockfile that recorded a root-level skill with those files present will show
  a one-time content change on the next scan.

## [0.4.6] - 2026-09-06

### Fixed

- A skill directory that is itself a symlink was listed in the lockfile with
  the empty digest and no file list, so an edit behind the link passed
  `verify`. The hasher now resolves a symlinked root before walking it;
  symlinks inside a tree are still skipped. Lockfiles that recorded a
  symlinked skill will show a one-time content change on the next scan.

## [0.4.5] - 2026-09-05

### Added

- **Discovery — OpenClaude skill registries**: repos that publish a
  `registry.json` in the OpenClaude registry shape (one entry per skill with
  a `SKILL.md` path and a sha256 pin) are scanned as a catalog. Each listed
  skill folder is hashed whole, its egress hosts are fingerprinted, and the
  registry's own pin is recorded beside the tree hash. Per-tool coverage is
  now fifteen.

### Changed

- **OpenClaude skills** now carry an egress fingerprint, the same way AEON
  and skills-lock skills do, so a post-install edit that adds a call to a new
  host reads as a capability change and trips `failOnCapabilityExpansion`
  under a policy that tolerates wording drift. Existing lockfiles that record
  OpenClaude skills with call lines will report a one-time capability change
  on the next scan.

## [0.4.4] - 2026-09-05

### Added

- **Discovery — OpenClaude**: the scanner reads OpenClaude skills from
  `.openclaude/skills` (project) and `~/.openclaude/skills` (global), one
  artifact per skill directory. The whole directory is hashed, including the
  `skill.json` sidecar that registry installs write next to `SKILL.md`, so a
  skill edited after OpenClaude's install-time hash check shows up as drift in
  `verify`. Per-tool coverage is now fourteen.

## [0.4.3] - 2026-08-31

### Added

- **Discovery — qwen-code, Kimi, Droid**: the scanner reads the MCP server
  configs of three more tools, bringing per-tool coverage to thirteen.
- **Shim — server identity audit**: the shim records the name and version a
  server declares in its `initialize` result, so the audit log shows which
  server actually answered, and `eyebrow audit` can report it.

### Fixed

- The shim applied policy only to request-form `tools/call` frames. A server
  call sent as a JSON-RPC *notification* (no `id`) skipped the policy check;
  the shim now enforces policy on notification-form calls too.
- Requests wrapped in a JSON-RPC *batch* array passed through the shim without
  policy or audit. The shim now unpacks batch frames and applies both to every
  call inside.

### Internal

- CI: `actions/attest-build-provenance` bumped from 4.1.1 to 4.2.2.

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

[Unreleased]: https://github.com/alexverify/eyebrow/compare/v0.5.5...HEAD
[0.5.5]: https://github.com/alexverify/eyebrow/compare/v0.5.4...v0.5.5
[0.5.4]: https://github.com/alexverify/eyebrow/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/alexverify/eyebrow/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/alexverify/eyebrow/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/alexverify/eyebrow/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/alexverify/eyebrow/compare/v0.4.7...v0.5.0
[0.4.7]: https://github.com/alexverify/eyebrow/compare/v0.4.6...v0.4.7
[0.4.6]: https://github.com/alexverify/eyebrow/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/alexverify/eyebrow/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/alexverify/eyebrow/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/alexverify/eyebrow/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/alexverify/eyebrow/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/alexverify/eyebrow/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/alexverify/eyebrow/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/alexverify/eyebrow/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/alexverify/eyebrow/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alexverify/eyebrow/releases/tag/v0.1.0
