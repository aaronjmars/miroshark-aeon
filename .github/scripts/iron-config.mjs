#!/usr/bin/env node
// Generate an iron-proxy config (JSON, a valid YAML subset) for one skill run.
//
// Phase 2 = WARN mode: nothing is blocked, every request is logged for audit.
// The allowlist is sourced from eyebrowlock.json (the CI-maintained per-skill
// egress-host map) plus a baseline plus every gateway host whose secret is set,
// so the `warn` annotations in the audit log flag only genuine surprises. In
// warn mode the domain list is advisory - the audit still logs ALL hosts either
// way - but priming it now makes the log readable and sets up phase 3 (enforce).
import { readFileSync } from "node:fs";

const skill = process.argv[2] ?? "unknown";
const tmp = process.env.RUNNER_TEMP ?? "/tmp";

// audit (default) = warn:true, nothing blocked, everything logged.
// enforce = warn:false, default-deny anything not on the list below.
const mode = (process.env.EGRESS_MODE ?? "audit").toLowerCase();
const warn = mode !== "enforce";

// Always-needed infra: the harness, the model endpoint, package registries.
// Observed live on every run and NOT declared in any skill's eyebrowlock, so it
// must be hardcoded here or enforce mode would break the harness itself.
const baseline = [
  "api.anthropic.com", "*.anthropic.com",       // model API (from inside bwrap)
  "github.com", "api.github.com", "*.githubusercontent.com",  // gh / git / raw
  "registry.npmjs.org",                          // npm (Claude Code install lives outside the run, but stay safe)
];

// NOTE deliberately absent: http-intake.logs.us5.datadoghq.com. That is Claude
// Code's OWN usage/error telemetry, not skill egress - no skill needs it, so in
// enforce mode it is denied on purpose (a real hardening win, and the sandbox has
// no business phoning home). If a future Claude Code build treats a blocked
// telemetry POST as fatal, add "*.datadoghq.com" here.

// gateway: auto resolves the model host at run time from any provider secret
// (claude -> anthropic -> openrouter -> bankr -> ...), and Langfuse tracing is
// injected on every run. Allowlist all of these UNCONDITIONALLY: the config is
// generated in a composite step that does NOT carry the secrets, so gating on
// process.env presence silently drops them (this rejected Langfuse in the first
// enforce test). Allowing an unused provider host costs ~nothing and covers the
// whole failover cascade; the credential-blocking job is P5's secrets transform.
const gatewayHosts = [
  "openrouter.ai",
  "llm.bankr.bot",
  "api.x.ai",
  "ai-gateway.vercel.sh",
  "*.cloud.langfuse.com", "cloud.langfuse.com",  // observability, absent from eyebrowlock
];

// Per-skill declared egress hosts, as extracted by eyebrow and gated in CI.
let lockHosts = [];
try {
  const lock = JSON.parse(readFileSync("eyebrowlock.json", "utf8"));
  const art = (lock.artifacts ?? []).find((a) => a.name === skill);
  lockHosts = art?.capabilities?.network ?? [];
} catch { /* missing/unreadable lock is non-fatal: the audit still logs everything */ }

const domains = [...new Set([...baseline, ...gatewayHosts, ...lockHosts])];

const config = {
  // Explicit HTTP(S)_PROXY is used, not DNS interception - disable the DNS
  // server so proxy_ip is not required.
  dns: { enabled: false },
  proxy: {
    // Explicit-proxy (CONNECT/SOCKS5) listener. Clients point HTTPS_PROXY here.
    tunnel_listen: "127.0.0.1:8080",
    // The transparent listeners hard-default to :80/:443, which a non-root runner
    // cannot bind - the resulting fatal kills the proxy right after it binds the
    // tunnel. Empty string does NOT disable them (it falls back to the default),
    // so point them at inert high loopback ports instead: they bind harmlessly
    // and nothing routes there (explicit-proxy traffic uses the tunnel listener).
    http_listen: "127.0.0.1:8081",
    https_listen: "127.0.0.1:8082",
    // The 30s default 502s slow LLM responses; a skill's model call can take
    // longer to first byte. Give upstream headers room so warn mode never
    // breaks a real run on a timeout.
    upstream_response_header_timeout: "5m",
  },
  tls: {
    mode: "mitm",
    ca_cert: `${tmp}/iron/certs/ca.crt`,
    ca_key: `${tmp}/iron/certs/ca.key`,
  },
  transforms: [
    { name: "allowlist", config: { warn, domains } },
  ],
  log: { level: "info" },
};

process.stdout.write(JSON.stringify(config, null, 2));
