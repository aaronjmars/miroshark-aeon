import json
f = open('/home/runner/.claude/projects/-home-runner-work-miroshark-aeon-miroshark-aeon/a629af8a-4f66-41cd-abaf-27339e5776cc/tool-results/bxt156mrz.txt')
data = json.load(f)
f.close()
trades = data['data']
parsed = []
for t in trades:
    a = t['attributes']
    ts = a['block_timestamp']
    kind = a['kind']
    vol = float(a['volume_in_usd'])
    txhash = a['tx_hash']
    if kind == 'buy':
        token_amount = float(a['to_token_amount'])
    else:
        token_amount = float(a['from_token_amount'])
    parsed.append((vol, kind, ts, txhash, token_amount))
parsed.sort(reverse=True)
for p in parsed[:5]:
    print(p)
