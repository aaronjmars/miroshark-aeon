#!/usr/bin/env node

import process from "node:process";

function fail(message) {
  process.stderr.write(`HUNTER22_GATE_ERROR: ${message}\n`);
  process.exit(2);
}

function parseNow(argv) {
  const index = argv.indexOf("--now");
  if (index === -1) return Date.now();
  if (index + 1 >= argv.length) fail("--now requires an ISO 8601 timestamp");

  const timestamp = Date.parse(argv[index + 1]);
  if (!Number.isFinite(timestamp)) fail("--now must be a valid ISO 8601 timestamp");
  return timestamp;
}

let input = "";
for await (const chunk of process.stdin) input += chunk;

let payload;
try {
  payload = JSON.parse(input);
} catch {
  fail("input is not valid JSON");
}

if (payload === null || typeof payload !== "object" || Array.isArray(payload)) {
  fail("input must be a JSON object");
}
if (!Array.isArray(payload.matches)) fail("input.matches must be an array");

const now = parseNow(process.argv.slice(2));
const matches = [];
const rejected = [];
const seen = [];

for (const candidate of payload.matches) {
  if (candidate === null || typeof candidate !== "object" || Array.isArray(candidate)) {
    fail("every match must be a JSON object");
  }

  const id = typeof candidate.id === "string" ? candidate.id : null;
  if (!id) fail("every match must have a non-empty string id");

  seen.push({
    id,
    title: typeof candidate.title === "string" ? candidate.title : null,
    reward: candidate.rewardUsd ?? candidate.reward ?? null,
  });

  if (candidate.expiresAt === null || candidate.expiresAt === undefined) {
    matches.push(candidate);
    continue;
  }
  if (typeof candidate.expiresAt !== "string") {
    rejected.push({ id, reason: "invalid-expiration" });
    continue;
  }

  const expiresAt = Date.parse(candidate.expiresAt);
  if (!Number.isFinite(expiresAt)) {
    rejected.push({ id, reason: "invalid-expiration" });
    continue;
  }
  if (expiresAt <= now) {
    rejected.push({ id, reason: "expired", expiresAt: candidate.expiresAt });
    continue;
  }

  matches.push(candidate);
}

process.stdout.write(`${JSON.stringify({
  ...payload,
  count: matches.length,
  matches,
  gate: {
    inputCount: payload.matches.length,
    keptCount: matches.length,
    rejectedCount: rejected.length,
    rejected,
    seen,
  },
})}\n`);
