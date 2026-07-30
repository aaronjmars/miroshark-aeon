#!/usr/bin/env python3
"""Check a set of wallets' token holdings via public RPC, price via GeckoTerminal.

Keyless by default: Base uses https://mainnet.base.org, Solana uses
https://api.mainnet-beta.solana.com. Override with BASE_RPC_URL / SOLANA_RPC_URL.
Only Python stdlib is used so it runs under the aeon sandbox with no deps.

Config (memory/holdings.json):
{
  "wallets": [
    {"address": "0x...", "label": "personal", "chain": "base"},
    {"address": "8mjM...", "label": "sol-treasury", "chain": "solana"}
  ],
  "tokens": [
    {"symbol": "aeon", "contract": "0xbf8e...aba3", "chain": "base", "decimals": 18}
  ]
}

A token is checked against every wallet on the SAME chain. Output is JSON on
stdout: per-holding rows plus totals, so the skill can format the notification
and the STATE log line deterministically.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE_RPC = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")
SOL_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
GT = "https://api.geckoterminal.com/api/v2/networks/{net}/tokens/{addr}"
GT_NET = {"base": "base", "solana": "solana"}
TIMEOUT = 20
# Some public RPCs (mainnet.base.org) 403 the default python-urllib User-Agent.
UA = "Mozilla/5.0 (aeon-holdings-skill)"
RETRY_CODES = {429, 500, 502, 503, 504}
MAX_RETRIES = 5
RPC_PACE = 0.15   # public Base RPC tolerates rapid calls
GT_PACE = 2.0     # GeckoTerminal free tier ~30/min — space GET calls to avoid 429 bursts


def _request(req):
    """Send a urllib request with exponential backoff on rate-limit / 5xx.

    On HTTP 429 honor the Retry-After header when present (GeckoTerminal sets it),
    otherwise fall back to exponential backoff.
    """
    delay = 1.0
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in RETRY_CODES and attempt < MAX_RETRIES - 1:
                wait = delay
                ra = e.headers.get("Retry-After") if e.headers else None
                if ra and ra.isdigit():
                    wait = min(float(ra), 30.0)
                time.sleep(wait)
                delay *= 2
                continue
            raise
        except urllib.error.URLError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("exhausted retries")


def _post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
    )
    out = _request(req)
    time.sleep(RPC_PACE)
    return out


def _get(url):
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": UA})
    out = _request(req)
    time.sleep(GT_PACE)
    return out


def erc20_balance(rpc, contract, wallet):
    """balanceOf(address) -> raw integer. selector 0x70a08231."""
    data = "0x70a08231" + wallet.lower().replace("0x", "").rjust(64, "0")
    res = _post(rpc, {
        "jsonrpc": "2.0", "id": 1, "method": "eth_call",
        "params": [{"to": contract, "data": data}, "latest"],
    })
    if "result" not in res or not isinstance(res["result"], str):
        raise RuntimeError(res.get("error", "no result"))
    return int(res["result"], 16)


def spl_balance(rpc, mint, owner):
    """Sum raw token amount across all SPL token accounts owner holds for mint."""
    res = _post(rpc, {
        "jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner",
        "params": [owner, {"mint": mint},
                   {"encoding": "jsonParsed", "commitment": "confirmed"}],
    })
    if "result" not in res:
        raise RuntimeError(res.get("error", "no result"))
    total = 0
    for acct in res["result"]["value"]:
        amt = acct["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"]
        total += int(amt)
    return total


def token_meta(chain, contract):
    """GeckoTerminal token attributes: price_usd + total_supply (in whole tokens).

    On-chain totalSupply() reverts on the DERC20 aeon contract, so GT is the
    authoritative supply source. total_supply is returned raw (base units); the
    caller divides by 10**decimals. Price is used only to value the current
    snapshot — 7d/30d growth is measured in token amount, not dollars, and comes
    from the skill's own prior snapshots, not from any price history here.
    """
    net = GT_NET.get(chain)
    out = {"price_usd": None, "total_supply_raw": None, "meta_error": None}
    if not net:
        out["meta_error"] = "unsupported chain"
        return out
    try:
        a = _get(GT.format(net=net, addr=contract))["data"]["attributes"]
        p = a.get("price_usd")
        out["price_usd"] = float(p) if p is not None else None
        ts = a.get("total_supply")
        out["total_supply_raw"] = float(ts) if ts is not None else None
    except Exception as e:
        out["meta_error"] = str(e)[:120]
    return out


def check(config):
    rows = []
    meta = {}   # (chain, contract) -> token_meta + decimals/supply
    for tok in config["tokens"]:
        chain = tok["chain"]
        contract = tok["contract"]
        decimals = int(tok.get("decimals", 18))
        symbol = tok.get("symbol", contract[:6])
        key = (chain, contract.lower())
        if key not in meta:
            m = token_meta(chain, contract)
            m["decimals"] = decimals
            m["symbol"] = symbol
            ts_raw = m.get("total_supply_raw")
            m["total_supply"] = (ts_raw / (10 ** decimals)) if ts_raw else None
            meta[key] = m
        m = meta[key]
        rpc = BASE_RPC if chain == "base" else SOL_RPC
        for w in config["wallets"]:
            if w["chain"] != chain:
                continue
            row = {"symbol": symbol, "chain": chain, "contract": contract,
                   "wallet": w["address"], "label": w.get("label", "")}
            try:
                if chain == "base":
                    raw = erc20_balance(rpc, contract, w["address"])
                elif chain == "solana":
                    raw = spl_balance(rpc, contract, w["address"])
                else:
                    row["error"] = "unsupported chain"
                    rows.append(row)
                    continue
                row["amount"] = raw / (10 ** decimals)
            except Exception as e:
                row["error"] = str(e)[:120]
            rows.append(row)
    # Totals per symbol + % of supply held. No dollar value is reported. 7d/30d
    # growth is measured in token amount and computed by the skill from prior
    # snapshots (memory/logs) — not here.
    per_symbol = {}
    for r in rows:
        if "amount" not in r:
            continue
        m = meta[(r["chain"], r["contract"].lower())]
        s = per_symbol.setdefault(r["symbol"], {
            "amount": 0.0, "total_supply": m["total_supply"],
            "meta_error": m.get("meta_error"),
        })
        s["amount"] += r["amount"]
    for sym, s in per_symbol.items():
        supply = s["total_supply"]
        s["pct_supply"] = (s["amount"] / supply * 100.0) if supply else None
    return {"rows": rows, "per_symbol": per_symbol}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "memory/holdings.json"
    with open(path) as f:
        config = json.load(f)
    print(json.dumps(check(config), indent=2))


if __name__ == "__main__":
    main()
