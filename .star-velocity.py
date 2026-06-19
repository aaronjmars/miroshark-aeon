import json, sys
from datetime import datetime, timedelta, timezone
today = datetime(2026, 6, 19, tzinfo=timezone.utc)
cutoff_7 = today - timedelta(days=7)
cutoff_30 = today - timedelta(days=30)
data = json.load(sys.stdin)
print('entries:', len(data))
v7 = sum(1 for x in data if datetime.fromisoformat(x['starred_at'].replace('Z','+00:00')) >= cutoff_7)
v30 = sum(1 for x in data if datetime.fromisoformat(x['starred_at'].replace('Z','+00:00')) >= cutoff_30)
last_star = max(x['starred_at'] for x in data) if data else None
first_star = min(x['starred_at'] for x in data) if data else None
print('v7:', v7)
print('v30:', v30)
print('last_star:', last_star)
print('first_star:', first_star)
