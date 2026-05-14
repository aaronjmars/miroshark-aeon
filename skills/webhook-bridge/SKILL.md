---
name: webhook-bridge
description: External-event-to-skill bridge — fire any Aeon skill via repository_dispatch from outside GitHub Actions UI
var: ""
tags: [productivity, meta]
---

# Webhook Bridge

A skill in name only — this folder documents the calling convention for the
`repository_dispatch` listener defined in `.github/workflows/webhook.yml`.
Dispatching this skill via `workflow_dispatch` is a no-op; the operator's job
is to invoke other skills *through* the bridge from external systems.

The bridge lets any HTTP-capable caller (Zapier, n8n, IFTTT, another GitHub
Actions workflow, a cron'd curl on a VPS, a DexScreener alert webhook proxy,
the operator's iPhone shortcut) fire an Aeon skill without opening the Actions
UI. Every Aeon skill is reachable as a webhook target.

## Call shape

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/{owner}/{repo}/dispatches \
  -d '{
    "event_type": "aeon-skill",
    "client_payload": {
      "skill": "token-report",
      "var": "AEON",
      "model": "claude-sonnet-4-6"
    }
  }'
```

- `event_type` **must** be the literal string `aeon-skill`. Other event types
  are ignored by the bridge (and may match other workflows, so do not reuse).
- `client_payload.skill` (required) — slug of a skill that exists as a
  directory under `skills/`. Must match `^[a-z0-9][a-z0-9-]{0,63}$`.
  Unknown slugs are rejected before dispatch.
- `client_payload.var` (optional) — free-form parameter passed as the `var`
  workflow input. Max 512 chars, no newlines.
- `client_payload.model` (optional) — model override. Must be one of the
  Aeon-supported model IDs (see `aeon.yml` `model:` comment for the list).

The caller's token needs `Actions: write` on the target repo. A fine-grained
PAT with `Contents: read` + `Metadata: read` + `Actions: write` is the minimum
scope. Classic PATs need `repo` (private) or `public_repo` (public).

## Worked examples

### GitHub Actions cross-repo

A workflow in `owner/upstream` fires `token-report` whenever it pushes:

```yaml
on:
  push:
    branches: [main]

jobs:
  trigger-aeon:
    runs-on: ubuntu-latest
    steps:
      - name: Fire Aeon token-report
        env:
          GH_TOKEN: ${{ secrets.AEON_DISPATCH_PAT }}
        run: |
          gh api \
            -X POST \
            repos/aaronjmars/aeon-agent/dispatches \
            -f event_type=aeon-skill \
            -F client_payload[skill]=token-report \
            -F client_payload[var]=AEON
```

### Zapier (Webhooks by Zapier — POST)

- URL: `https://api.github.com/repos/aaronjmars/aeon-agent/dispatches`
- Payload Type: JSON
- Data: `{ "event_type": "aeon-skill", "client_payload": { "skill": "fetch-tweets", "var": "$AEON" } }`
- Headers:
  - `Authorization: Bearer ghp_…`
  - `Accept: application/vnd.github+json`

Pair with a Zapier "Schedule" trigger to run any disabled skill on a cadence
that isn't easy to express in cron, or with a Slack-message trigger to fire a
skill on a `!aeon token-report` command.

### n8n (HTTP Request node)

- Method: POST
- URL: `https://api.github.com/repos/aaronjmars/aeon-agent/dispatches`
- Authentication: Header Auth → `Authorization: Bearer ghp_…`
- Headers: `Accept: application/vnd.github+json`
- Body Content Type: JSON
- JSON Body: `{ "event_type": "aeon-skill", "client_payload": { "skill": "{{$json.skill}}", "var": "{{$json.var}}" } }`

### DexScreener-style price-alert webhook proxy

Most webhook-producing services (DexScreener, BlockNative, etc.) post a JSON
body and headers you don't control. Use a thin proxy (Cloudflare Worker,
small Vercel function, n8n endpoint) that:

1. Validates the incoming webhook signature (each vendor has its own
   `X-…-Signature` header pattern).
2. Transforms the payload into Aeon's expected shape.
3. Forwards to `/repos/{owner}/{repo}/dispatches` with the PAT.

A 15-line worker is the typical implementation. Treat the PAT as a server-side
secret — never embed it in the vendor's webhook config.

## Validation contract

The bridge rejects a dispatch when:

| Check | Reason output |
|---|---|
| `client_payload.skill` missing | `missing_skill` |
| Skill slug fails regex `^[a-z0-9][a-z0-9-]{0,63}$` | `bad_slug` |
| `skills/<slug>/` directory does not exist | `unknown_skill` |
| `client_payload.var` > 512 chars | `var_too_long` |
| `client_payload.var` contains `\n` or `\r` | `var_bad_chars` |
| `client_payload.model` not in the Aeon-supported set | `bad_model` |

Skills present locally as a directory but missing from `skills.json` are still
dispatched (with a workflow warning) — this preserves the "custom skill in a
fork" pattern. The exit code is captured in the Actions UI; rejections show as
red, dispatches show as green with a `::notice::` line stating skill + var.

## What it does NOT do

- It does not relay the *result* of the dispatched skill back to the caller.
  The dispatched skill runs asynchronously in its own `aeon.yml` workflow run;
  the bridge job completes as soon as the dispatch succeeds. Callers that
  need a callback should pair this with `repository_dispatch` listeners on
  their side that consume Aeon's notify channels.
- It does not authenticate beyond GitHub's repository-level PAT scoping. A
  caller with `Actions: write` can fire any skill — there is no per-skill
  authorization. Restrict the PAT's scope to a single repo if multiple
  consumers share it.
- It does not deduplicate dispatches. Two identical webhooks within one
  minute will run the skill twice. If the upstream system retries on its own,
  add idempotency at the proxy layer.

## Reactive triggers vs. webhook bridge

`aeon.yml` already has a `reactive:` section that fires skills on internal
state transitions (e.g. `skill-repair` when `consecutive_failures >= 3`).
That stays inside the GitHub-Actions universe — driven by `cron-state.json`,
not external events. The webhook bridge is the *outside-in* path: external
systems trigger skills. The two compose — a webhook can fire `skill-repair`
externally, or a reactive trigger can fire after a webhook-dispatched skill
sets a new state value.

## Sandbox note

This skill's body is documentation; the implementation is the workflow file
above. Operators who fork Aeon get the bridge as soon as they pull `main` —
no secret, no enabling, no extra workflow. The endpoint is live on every
fork that has Actions enabled. The first call from outside is the
acceptance test.

If `gh workflow run` fails inside the bridge job (e.g. PAT rotated, repo
archived), the dispatch step exits non-zero and the bridge job goes red.
Check the failed run's logs for the `gh` error message and re-issue the
external POST after fixing the cause.

## Steps (for operators)

There is no per-run skill body. Operator setup is:

1. Pull `main` after this PR merges. The workflow file is auto-installed.
2. Mint a GitHub PAT with `Actions: write` on the target repo (fine-grained
   recommended). Store it wherever the external caller reads its credentials.
3. POST the call-shape body above with a test payload like
   `{ "skill": "repo-pulse" }`. Verify the dispatched skill run appears in
   the Actions tab within ~5 seconds.
4. Wire the production caller (Zapier zap, n8n flow, vendor webhook proxy).

That's the entire skill. The work happens in `webhook.yml`.
