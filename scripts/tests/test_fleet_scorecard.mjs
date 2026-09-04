import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'

test('least-reliable table contains skills only and uses their slug', async () => {
  const originalFetch = globalThis.fetch
  const originalRepo = process.env.GITHUB_REPOSITORY
  const createdAt = new Date().toISOString()
  const run = (name) => ({ name, conclusion: 'failure', created_at: createdAt, head_branch: 'main' })
  const workflowRuns = [
    run('ci-tests'), run('ci-tests'), run('ci-tests'),
    run('skill: digest'), run('skill: digest'), run('skill: digest'),
  ]

  process.env.GITHUB_REPOSITORY = 'operator/aeon'
  globalThis.fetch = async (input) => {
    const url = String(input)
    if (url.includes('/actions/runs?')) {
      return new Response(JSON.stringify({ workflow_runs: workflowRuns }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    }
    if (url.endsWith('/contents/skills')) {
      return new Response(JSON.stringify([{ type: 'dir' }]), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      })
    }
    return new Response('', { status: 404 })
  }

  try {
    await import(new URL(`../fleet-scorecard.mjs?test=${Date.now()}`, import.meta.url))
    const body = readFileSync('/tmp/fleet-scorecard/scorecard-body.md', 'utf8')
    assert.doesNotMatch(body, /\| ci-tests \|/, 'non-skill workflow leaked into the skill table')
    assert.match(body, /\| digest \|/, 'skill slug missing from the skill table')
    assert.doesNotMatch(body, /\| skill: digest \|/, 'workflow prefix leaked into the skill name')
  } finally {
    globalThis.fetch = originalFetch
    if (originalRepo === undefined) delete process.env.GITHUB_REPOSITORY
    else process.env.GITHUB_REPOSITORY = originalRepo
  }
})
