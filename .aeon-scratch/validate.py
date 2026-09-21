import subprocess, json, glob, os
# validate-config
r=subprocess.run(["node","scripts/validate-config.js","aeon.yml"],capture_output=True,text=True)
print("validate-config exit", r.returncode)
print(r.stdout.strip()[-1200:])
if r.stderr.strip(): print("ERR", r.stderr.strip()[-800:])

# JSON parse-check regenerated catalogs + lock
print("\n--- JSON parse checks ---")
for p in ["catalog/skills.json","catalog/packs.json","catalog/skill-icons.json","eyebrowlock.json"]:
    try:
        json.load(open(p)); print("OK ", p)
    except Exception as e:
        print("FAIL", p, e)

# YAML parse-check applied workflow yml (+ aeon.yml untouched)
print("\n--- YAML parse checks ---")
try:
    import yaml
    have_yaml=True
except Exception:
    have_yaml=False
    print("pyyaml unavailable; skipping (workflows validated by CI)")
if have_yaml:
    for p in ["catalog","x"]:
        pass
    for p in glob.glob(".github/workflows/*.yml"):
        try:
            yaml.safe_load(open(p)); print("OK ", p)
        except Exception as e:
            print("FAIL", p, e)
