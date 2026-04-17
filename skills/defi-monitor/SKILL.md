---
name: DeFi Monitor
description: Check pool health, positions, and yield rates for tracked protocols
var: ""
tags: [crypto]
---
> **${var}** — Position label to check. If empty, checks all watched positions.

If `${var}` is set, only check the position with that label.


## Config

This skill reads watched contracts and positions from `memory/on-chain-watches.yml`. If the file doesn't exist yet, create it or skip this skill.

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

Read memory/MEMORY.md and memory/on-chain-watches.yml for watched contracts and positions.
Read the last 2 days of memory/logs/ to track changes over time.

Steps:
1. For each DeFi position in on-chain-watches.yml (type: pool or position):
   - Query the contract for current state using eth_call:
     ```bash
     # Example: read slot0 from a Uniswap-style pool
     curl -s -X POST "${rpc_url}" \
       -H "Content-Type: application/json" \
       -d '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"'"$address"'","data":"'"$calldata"'"},"latest"],"id":1}'
     ```
   - For known protocols, query standard view functions:
     - Liquidity pools: totalSupply, reserves, current tick/price
     - Lending: supplyRate, borrowRate, utilization
     - Staking: earned rewards, APR
2. Compare current values against last logged values.
3. Flag anything noteworthy:
   - Yield rate change > 20%
   - Pool TVL drop > 10%
   - Position approaching liquidation
   - Impermanent loss exceeding threshold
4. Format and send via `./notify`:
   ```
   *DeFi Monitor — ${today}*

   *Pool/Protocol Label* (chain)
   TVL: $X | APR: Y%
   Your position: details
   Change since last check: summary
   ```
5. Log findings to memory/logs/${today}.md.
If no DeFi positions configured, log "DEFI_MONITOR_OK" and end.
