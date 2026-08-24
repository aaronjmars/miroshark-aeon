#!/usr/bin/env node
// P4: turn an iron-proxy audit log into a deterministic health signal.
//
// Reads audit.jsonl (path in argv[2]) and emits {flag, hosts} JSON on stdout.
// `egress_blocked` fires when the allowlist REJECTED a host the skill actually
// tried to reach - an allowlist gap (or an exfil attempt) the §7 repair loop can
// act on. Rejects occur only in enforce mode; in audit/warn the log is all
// "allow" and this emits flag:null. Hosts we deny ON PURPOSE are excluded so a
// by-design block never raises a false signal.
import { readFileSync } from "node:fs";

const path = process.argv[2];

// Intentional denies (see the baseline note in iron-config.mjs): Claude Code's
// own telemetry. A reject here is expected, not a misconfiguration.
const EXPECTED_DENY = [/(^|\.)datadoghq\.com$/];

const stripPort = (h) => (h || "").replace(/:\d+$/, "");
const isExpected = (h) => EXPECTED_DENY.some((re) => re.test(h));

let text = "";
try { text = readFileSync(path, "utf8"); } catch { /* no audit log = audit was off */ }

const denied = new Map();
for (const line of text.split("\n")) {
  if (!line.startsWith("{")) continue;          // skip non-JSON startup noise
  let e;
  try { e = JSON.parse(line); } catch { continue; }
  if (e.msg !== "request") continue;
  const a = e.audit || {};
  const rejected =
    a.action === "reject" ||
    Boolean(e.rejected_by) ||
    (e.request_transforms || []).some((t) => t.action === "reject");
  if (!rejected) continue;
  const host = stripPort(a.host);
  if (!host || isExpected(host)) continue;
  denied.set(host, (denied.get(host) || 0) + 1);
}

const hosts = [...denied.entries()].map(([host, count]) => ({ host, count }));
process.stdout.write(JSON.stringify({
  flag: hosts.length ? "egress_blocked" : null,
  hosts,
}));
