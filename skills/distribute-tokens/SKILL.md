---
name: Distribute Tokens
description: Send tokens to a list of contributors via Bankr Agent API (supports Twitter handles and EVM addresses)
var: ""
tags: [crypto]
---
> **${var}** — Distribution list label to use. If empty, uses the default list. Pass a label to target a specific group (e.g. "contributors", "team").

## Config

This skill reads distribution lists from `memory/distributions.yml`. If the file doesn't exist, log a warning and exit.

```yaml
# memory/distributions.yml
defaults:
  token: USDC
  amount: "5"          # per recipient
  chain: base

lists:
  contributors:
    description: "Weekly contributor rewards"
    token: USDC        # override default
    amount: "10"       # override default
    recipients:
      - handle: "@alice_dev"      # Twitter/X handle — resolved via Bankr
        amount: "15"              # per-recipient override (optional)
      - handle: "@bob_builder"
      - address: "0x742d...5678"  # direct EVM address
        label: "Charlie"
        amount: "20"

  team:
    description: "Monthly team distribution"
    token: ETH
    amount: "0.01"
    recipients:
      - handle: "@core_dev1"
      - handle: "@core_dev2"
```

### Required secrets

| Secret | Purpose |
|--------|---------|
| `BANKR_API_KEY` | Bankr API key (prefixed `bk_`). Must have **read-write** access and **Agent API** enabled. |

Get a key at [bankr.bot/api](https://bankr.bot/api). Enable read-write mode and Agent API access in key settings.

### How it works

- **Twitter handles** (`@username`): Sent via the Bankr Agent API using natural language. Bankr resolves the handle to the recipient's linked wallet. The recipient must have a Bankr account — if they don't, that transfer fails and is logged.
- **EVM addresses** (`0x...`): Sent via the direct Wallet Transfer API (`POST /wallet/transfer`). Base chain only.

---

Read memory/MEMORY.md and memory/distributions.yml.
Read the last 2 days of memory/logs/ to check for recent distributions (avoid double-sending).

Steps:

1. **Validate config** — parse `memory/distributions.yml`. If `${var}` is set, find the matching list by label. If not set, use the first list. Abort if no lists found or file missing.

2. **Check for duplicates** — scan recent logs for distributions to the same list in the last 24 hours. If found, log "DISTRIBUTE_TOKENS_SKIPPED — already distributed to '${list}' today" and exit. This prevents accidental double-sends from re-runs.

3. **Check BANKR_API_KEY** — if not set, log "DISTRIBUTE_TOKENS_ERROR — BANKR_API_KEY not configured" and exit.

4. **Process each recipient** — for each entry in the list:

   Determine the amount: use recipient-level `amount` if set, otherwise list-level `amount`, otherwise `defaults.amount`.
   Determine the token: use list-level `token`, otherwise `defaults.token`.

   **Path A — Twitter handle** (starts with `@`):

   Use the Bankr Agent API with a natural language transfer command:
   ```bash
   JOB_ID=$(curl -s -X POST "https://api.bankr.bot/agent/prompt" \
     -H "X-API-Key: ${BANKR_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"send '"${amount}"' '"${token}"' to '"${handle}"' on base"}' \
     | jq -r '.jobId')
   ```

   Poll for completion (max 60s, 5s intervals):
   ```bash
   for i in $(seq 1 12); do
     RESULT=$(curl -s "https://api.bankr.bot/agent/job/${JOB_ID}" \
       -H "X-API-Key: ${BANKR_API_KEY}")
     STATUS=$(echo "$RESULT" | jq -r '.status')
     if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then break; fi
     sleep 5
   done
   ```

   Record result: if `completed`, extract tx hash from response. If `failed`, log the error (likely "no linked wallet for this handle").

   **Path B — EVM address** (starts with `0x`):

   For USDC on Base, the token address is `0x833589fcd6edb6e08f4c7c32d4f71b54bda02913`.
   For native ETH, set `isNativeToken: true`.

   Use the Wallet Transfer API:
   ```bash
   RESULT=$(curl -s -X POST "https://api.bankr.bot/wallet/transfer" \
     -H "X-API-Key: ${BANKR_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "recipientAddress": "'"${address}"'",
       "tokenAddress": "'"${token_address}"'",
       "amount": "'"${amount}"'",
       "isNativeToken": '"${is_native}"'
     }')
   ```

   Check `success` field. Extract `txHash` on success.

   Common token addresses on Base:
   - USDC: `0x833589fcd6edb6e08f4c7c32d4f71b54bda02913`
   - BNKR: look up via Bankr Agent API if needed
   - ETH (native): use `isNativeToken: true`, any `tokenAddress`

5. **Build summary** — compile results:
   ```
   *Token Distribution — ${today}*

   List: ${list_label} (${description})
   Token: ${token} on Base
   Total sent: ${total_amount} ${token}

   ✓ @alice_dev — 15 USDC (tx: 0xabc...)
   ✓ @bob_builder — 10 USDC (tx: 0xdef...)
   ✓ Charlie (0x742d...) — 20 USDC (tx: 0x123...)
   ✗ @inactive_user — failed: no linked Bankr wallet

   Success: N/M recipients
   ```

6. **Send** via `./notify`.

7. **Log** results to `memory/logs/${today}.md`:
   - List label, token, chain
   - Each recipient with status (success/fail), amount, tx hash
   - Total distributed vs total attempted

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

If `memory/distributions.yml` doesn't exist, send nothing. Log "DISTRIBUTE_TOKENS_OK — no distribution lists configured" and end.
