#!/usr/bin/env node

import { spawnSync } from "node:child_process";

const PIN = "rightstack@0.3.2";
const raw = (process.env.SKILL_VAR ?? "").trim();

const childEnv = Object.fromEntries(
  ["PATH", "HOME", "TMPDIR", "TMP", "TEMP", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "TERM", "CI"]
    .flatMap((key) => process.env[key] === undefined ? [] : [[key, process.env[key]]]),
);
Object.assign(childEnv, {
  npm_config_ignore_scripts: "true",
  npm_config_audit: "false",
  npm_config_fund: "false",
  npm_config_update_notifier: "false",
});

function fail(message, code = 2) {
  console.error(message);
  process.exit(code);
}

if (!raw) fail("RIGHTSTACK_EMPTY: provide a build goal or an operation prefix", 2);

let command = "recommend";
let args = [raw, "--json"];
const match = raw.match(/^([a-z-]+)\s*:\s*(.*)$/s);

if (match) {
  const operation = match[1];
  const value = match[2].trim();
  if (!value) fail(`RIGHTSTACK_BAD_INPUT: ${operation} requires a value`);

  switch (operation) {
    case "recommend":
    case "workflow":
    case "explain":
    case "migrate":
      command = operation;
      args = [value, "--json"];
      break;
    case "compare": {
      const tools = value.split("|").map((part) => part.trim()).filter(Boolean);
      if (tools.length !== 2) fail("RIGHTSTACK_BAD_INPUT: compare requires exactly two tools separated by |");
      command = "compare";
      args = [...tools, "--json"];
      break;
    }
    default:
      fail(`RIGHTSTACK_BAD_INPUT: unsupported operation ${operation}`);
  }
}

const result = spawnSync("npx", ["--yes", "--package", PIN, "rightstack", command, ...args], {
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
  env: childEnv,
});

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
if (result.error) fail(`RIGHTSTACK_TOOL_ERROR: ${result.error.message}`, 1);
process.exit(result.status ?? 1);
