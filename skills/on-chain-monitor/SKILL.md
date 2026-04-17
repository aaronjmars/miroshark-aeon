---
name: On-Chain Monitor
description: Monitor blockchain addresses and contracts for notable activity
var: ""
tags: [crypto]
---
> **${var}** — Address label or chain to check. If empty, checks all watched addresses.

If `${var}` is set, only monitor the address with that label or on that chain.


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

Read memory/MEMORY.md and memory/on-chain-watches.yml for context.
Read the last 2 days of memory/logs/ to avoid duplicate alerts.

For each entry in on-chain-watches.yml:
1. Query the RPC endpoint for recent activity:
   ```bash
   # Get latest block number
   BLOCK=$(curl -s -X POST "${rpc_url}" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' | jq -r '.result')

   # Get logs for watched address (last ~256 blocks)
   FROM_BLOCK=$(printf "0x%x" $(( 16#${BLOCK#0x} - 256 )))
   curl -s -X POST "${rpc_url}" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"fromBlock":"'"$FROM_BLOCK"'","toBlock":"latest","address":"'"$address"'"}],"id":1}'
   ```
2. For wallet watches, check recent transactions:
   ```bash
   curl -s -X POST "${rpc_url}" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["'"$address"'","latest"],"id":1}'
   ```
3. Compare balances/events against previously logged values in memory/logs/

Flag as notable:
- Balance changes > threshold defined in on-chain-watches.yml
- Any event emission from watched contracts
- New token transfers to/from watched wallets

If anything notable is found:
- Send a concise alert via `./notify`:
  ```
  *On-Chain Alert*
  [chain] address: event description
  ```
- Log the finding with current values to memory/logs/${today}.md

If nothing notable, log "ON_CHAIN_OK" and end.
