#!/usr/bin/env python3
import json, sys, datetime, subprocess

today = datetime.date(2026, 6, 11)
cutoff7 = today - datetime.timedelta(days=7)
cutoff30 = today - datetime.timedelta(days=30)

v7, v30 = 0, 0
latest = None
all_items = []

# Fetch page 13 (last page, stars 1201-1255)
r13 = subprocess.run(
    ["gh", "api", "-H", "Accept: application/vnd.github.star+json",
     "repos/aaronjmars/MiroShark/stargazers?per_page=100&page=13"],
    capture_output=True, text=True
)
if r13.returncode == 0:
    all_items.extend(json.loads(r13.stdout))

# Fetch page 12 (stars 1101-1200)
r12 = subprocess.run(
    ["gh", "api", "-H", "Accept: application/vnd.github.star+json",
     "repos/aaronjmars/MiroShark/stargazers?per_page=100&page=12"],
    capture_output=True, text=True
)
if r12.returncode == 0:
    all_items.extend(json.loads(r12.stdout))

# Also fetch page 11 for better 30d baseline
r11 = subprocess.run(
    ["gh", "api", "-H", "Accept: application/vnd.github.star+json",
     "repos/aaronjmars/MiroShark/stargazers?per_page=100&page=11"],
    capture_output=True, text=True
)
if r11.returncode == 0:
    all_items.extend(json.loads(r11.stdout))

for item in all_items:
    ts = item['starred_at'][:10]
    d = datetime.date.fromisoformat(ts)
    if d >= cutoff7:
        v7 += 1
    if d >= cutoff30:
        v30 += 1
    if latest is None or d > latest:
        latest = d

print(f"total_items={len(all_items)}")
print(f"v7={v7}")
print(f"v30={v30}")
print(f"latest={latest}")
if latest:
    days_since = (today - latest).days
    print(f"days_since_last_star={days_since}")

baseline = v30 / 30.0
print(f"baseline_per_day={baseline:.2f}")

# Show the timestamp distribution for the last 30 items
print("\nLast 20 starred_at dates:")
dates = sorted([item['starred_at'][:10] for item in all_items], reverse=True)
for d in dates[:20]:
    print(f"  {d}")
