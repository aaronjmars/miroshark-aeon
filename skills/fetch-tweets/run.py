import subprocess, json, os, sys

from_date = subprocess.check_output(["date", "-u", "-d", "7 days ago", "+%Y-%m-%d"]).decode().strip()
to_date = subprocess.check_output(["date", "-u", "+%Y-%m-%d"]).decode().strip()
print(f"Date range: {from_date} to {to_date}", flush=True)

prompt = (
    "Search for tweets about the MIROSHARK crypto token on Base chain "
    "(contract address 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3). "
    "Only return tweets specifically about this cryptocurrency, not unrelated uses of the word. "
    "Date range: " + from_date + " to " + to_date + ". "
    "Return 10 tweets, prioritize the most interesting, insightful, or highly-engaged posts. "
    "For each tweet include: handle, the full text, date posted, engagement (likes/retweets if available), "
    "and the direct link (https://x.com/handle/status/ID). Return as a numbered list."
)

payload = json.dumps({
    "model": "grok-4-1-fast",
    "input": [{"role": "user", "content": prompt}],
    "tools": [{"type": "x_search"}]
})

api_key = os.environ.get("XAI_API_KEY", "")
if not api_key:
    print("ERROR: XAI_API_KEY not set")
    sys.exit(1)

result = subprocess.run(
    ["curl", "-s", "-X", "POST", "https://api.x.ai/v1/responses",
     "-H", "Content-Type: application/json",
     "-H", "Authorization: Bearer " + api_key,
     "-d", payload],
    capture_output=True, text=True, timeout=55
)

try:
    data = json.loads(result.stdout)
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    print(c["text"])
except Exception as e:
    print("RAW:", result.stdout[:3000])
    print("ERR:", str(e))
