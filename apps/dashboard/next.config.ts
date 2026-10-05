import type { NextConfig } from 'next'
import { resolve } from 'path'

// The Connect modal imports the generated credential manifests
// (harness-adapter/harnesses.json, gateways.json) from the repo root, so the
// bundler's root has to include it. Both roots must match or Next warns.
const repoRoot = resolve(__dirname, '..', '..')

const nextConfig: NextConfig = {
  turbopack: { root: repoRoot },
  outputFileTracingRoot: repoRoot,
  // Next 16.3 writes AGENTS.md and CLAUDE.md into this folder on every
  // `next dev`. The dashboard runs inside the operator's agent repo, where the
  // dashboard's PUSH (lib/sync.ts, `git add -A`) would commit them.
  agentRules: false,
}

export default nextConfig
