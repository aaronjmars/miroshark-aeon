---
name: Treasury Info
description: Show holdings overview for a wallet using Bankr API with block explorer fallback
var: ""
tags: [crypto]
---
> **${var}** — Wallet label to check. If empty, checks all watched wallets.

If `${var}` is set, only check the wallet with that label.


## Config

This skill reads watched addresses from `memory/on-chain-watches.yml`. If the file doesn't exist yet, create it or skip this skill.

```yaml
# memory/on-chain-watches.yml
watches:
  - label: Treasury
    address: "0x1234...abcd"
    chain: base
    rpc_url: https://base.llamarpc.com
    type: wallet
```

### Bankr API (preferred)

Set the `BANKR_API_KEY` secret (prefixed `bk_`). The Bankr portfolio endpoint returns token balances, USD values, PnL, and NFTs across chains — one call covers everything.

If `BANKR_API_KEY` is not set, the skill falls back to direct RPC + CoinGecko.

---

Read memory/MEMORY.md and memory/on-chain-watches.yml for watched addresses.
Read the last 2 days of memory/logs/ to compare against previous snapshots.

Steps:

1. **Load watches** — parse `memory/on-chain-watches.yml`. Filter to `type: wallet` entries. If `${var}` is set, match by label.

2. **Fetch holdings** — for each wallet, try Bankr first, then fall back:

   **Path A — Bankr API** (if `BANKR_API_KEY` is set):
   ```bash
   curl -s "https://api.bankr.bot/wallet/portfolio?include=pnl&showLowValueTokens=false" \
     -H "X-API-Key: ${BANKR_API_KEY}"
   ```
   This returns balances grouped by chain with token symbols, amounts, USD values, and PnL.

   If the Bankr wallet address matches a watched address, use the response directly.
   If querying a different wallet, use the Agent API:
   ```bash
   # Submit prompt
   JOB=$(curl -s -X POST "https://api.bankr.bot/agent/prompt" \
     -H "X-API-Key: ${BANKR_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Show full token balances for wallet '"${address}"' on '"${chain}"'"}' \
     | jq -r '.jobId')

   # Poll for result (max 30s, 3s intervals)
   for i in $(seq 1 10); do
     RESULT=$(curl -s "https://api.bankr.bot/agent/job/${JOB}" \
       -H "X-API-Key: ${BANKR_API_KEY}")
     STATUS=$(echo "$RESULT" | jq -r '.status')
     if [ "$STATUS" = "completed" ]; then break; fi
     sleep 3
   done
   ```

   **Path B — RPC + CoinGecko fallback** (no Bankr key):
   - Get native balance via `eth_getBalance` (EVM) or equivalent RPC call.
   - For ERC-20 tokens, query known token contracts with `balanceOf(address)` via `eth_call`.
   - Look up USD prices from CoinGecko:
     ```bash
     curl -s "https://api.coingecko.com/api/v3/simple/price?ids=${coin_ids}&vs_currencies=usd&include_24hr_change=true"
     ```
   - For Solana wallets, use the Solana RPC `getBalance` and `getTokenAccountsByOwner` methods.

3. **Format treasury overview**:
   ```
   *Treasury Overview — ${today}*

   *Label* (chain)
   Total Value: $X,XXX.XX

   Holdings:
   - TOKEN1: amount ($value) [+/-% 24h]
   - TOKEN2: amount ($value) [+/-% 24h]
   - ...

   Top 5 by value shown. N tokens below $1 hidden.

   Change since last check: +/- $X.XX
   ```
   Include PnL data if available from Bankr. Compare total value against the last logged snapshot.

4. **Send** via `./notify`.

5. **Log** current totals and per-token balances to `memory/logs/${today}.md` so future runs can track changes over time.

If no watched wallets configured, send nothing. Log "TREASURY_INFO_OK — no wallets configured" and end.

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).
