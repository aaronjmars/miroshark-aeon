---
name: GitHub Releases
description: Track new releases from key AI, crypto, and infra repos
schedule: "0 8 * * *"
commits: false
permissions: []
var: ""
tags: [dev]
---
> **${var}** — Comma-separated list of repos to check (e.g. "anthropics/anthropic-sdk-python,solana-labs/solana"). If empty, uses the default watch list.

Read memory/MEMORY.md for context.
Read the last 2 days of memory/logs/ to avoid repeating releases already reported.

## Steps

1. **Build the repo list.** If `${var}` is set, use those repos. Otherwise use this default watch list:

   **AI / LLM**
   - anthropics/anthropic-sdk-python
   - anthropics/anthropic-sdk-typescript
   - openai/openai-python
   - openai/openai-node
   - BerriAI/litellm
   - langchain-ai/langchain
   - microsoft/promptflow

   **Agent infra**
   - anthropics/claude-code
   - crewAIInc/crewAI
   - run-llama/llama_index

   **Crypto / DeFi**
   - solana-labs/solana
   - ethereum/go-ethereum
   - uniswap/v4-core
   - aave/aave-v3-core

   **Dev infra**
   - vercel/next.js
   - supabase/supabase
   - ggerganov/llama.cpp

2. **Fetch latest release for each repo** using the GitHub API. Use WebFetch:
   ```
   https://api.github.com/repos/{owner}/{repo}/releases/latest
   ```
   Key fields: `tag_name`, `name`, `published_at`, `html_url`, `body` (first 300 chars).

   If the API returns 404 or rate-limit (403/429), skip that repo silently.

   If `GITHUB_TOKEN` is set in the environment, include it as `Authorization: Bearer $GITHUB_TOKEN` header to avoid rate limits.

3. **Filter to recent releases.** Keep only releases published in the last 24 hours (compare `published_at` to today's date). If running weekly (${var} includes "weekly"), expand window to 7 days.

4. **If no new releases found**, log "GITHUB_RELEASES_NONE" and end — do not send a notification.

5. **Send via `./notify`** (under 4000 chars). Group by category. Format:

   ```
   *GitHub Releases — ${today}*

   *AI / LLM*
   • [anthropics/anthropic-sdk-python v0.50.0](url) — one-line summary of key change

   *Agent Infra*
   • [anthropics/claude-code v1.2.0](url) — one-line summary

   *Crypto / DeFi*
   • [solana-labs/solana v2.1.0](url) — one-line summary

   *Dev Infra*
   • [vercel/next.js v15.3.0](url) — one-line summary
   ```

   For the one-line summary: pull from the release title or first sentence of `body`. Strip markdown. Keep it punchy — what actually changed, not the version number.

   Omit categories with no new releases.

6. **Log to memory/logs/${today}.md.** Include repo names and versions reported.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Optional | Personal access token. Increases rate limit from 60 to 5000 req/hr. |
