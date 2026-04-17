---
name: Wallet Digest
description: Summarize recent wallet activity across tracked addresses
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
  - label: My Wallet
    address: "0x1234...abcd"
    chain: ethereum
    rpc_url: https://eth.llamarpc.com
    type: wallet
    threshold: 0.1  # ETH — alert on balance changes above this

  - label: Uniswap Pool
    address: "0xabcd...5678"
    chain: ethereum
    rpc_url: https://eth.llamarpc.com
    type: contract
```

---

Read memory/MEMORY.md and memory/on-chain-watches.yml for watched addresses.
Read the last 2 days of memory/logs/ to avoid repeating.

Steps:
1. For each wallet in on-chain-watches.yml:
   - Get current balance:
     ```bash
     curl -s -X POST "${rpc_url}" \
       -H "Content-Type: application/json" \
       -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["'"$address"'","latest"],"id":1}'
     ```
   - Get recent transactions (last ~256 blocks):
     ```bash
     BLOCK=$(curl -s -X POST "${rpc_url}" -H "Content-Type: application/json" \
       -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | jq -r '.result')
     FROM=$(printf "0x%x" $(( 16#${BLOCK#0x} - 256 )))
     curl -s -X POST "${rpc_url}" -H "Content-Type: application/json" \
       -d '{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"fromBlock":"'"$FROM"'","toBlock":"latest","address":"'"$address"'"}],"id":1}'
     ```
   - Compare balance to last logged value in memory/logs/
2. Format a digest:
   ```
   *Wallet Digest — ${today}*

   *Label* (chain)
   Balance: X ETH ($Y)
   Change: +/- Z since last check
   Transactions: N in last 24h
   Notable: description of any large or unusual txs
   ```
3. Send via `./notify`.
4. Log current balances and findings to memory/logs/${today}.md.
If no watched wallets configured, log "WALLET_DIGEST_OK" and end.
