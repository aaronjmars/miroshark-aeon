import base64
import json
import subprocess
import sys

# Read the new changelog-data.ts content
with open("/home/runner/work/miroshark-aeon/miroshark-aeon/output/changelog-data-2026-07-12.ts", "rb") as f:
    raw = f.read()

encoded = base64.b64encode(raw).decode("utf-8")

payload = {
    "message": "docs(changelog): sync 1 merged PR from aaronjmars/miroshark",
    "content": encoded,
    "sha": "b7e2dc502919f3ef1aa13413e9fb363515640c7e",
    "branch": "aeon/changelog-2026-07-12",
    "committer": {
        "name": "aeonframework",
        "email": "aeonframework@proton.me"
    }
}

payload_path = "/home/runner/work/miroshark-aeon/miroshark-aeon/output/changelog-payload.json"
with open(payload_path, "w") as f:
    json.dump(payload, f)

result = subprocess.run(
    ["gh", "api", "repos/aaronjmars/miroshark-website/contents/app/changelog-data.ts",
     "-X", "PUT", "--input", payload_path],
    capture_output=True, text=True
)

print("STDOUT:", result.stdout[:500])
print("STDERR:", result.stderr[:500])
print("Return code:", result.returncode)
