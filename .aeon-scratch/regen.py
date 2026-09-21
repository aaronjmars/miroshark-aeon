import subprocess, os
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    print("$"," ".join(cmd),"-> exit",r.returncode)
    if r.stdout.strip(): print("  out:",r.stdout.strip()[-800:])
    if r.stderr.strip(): print("  err:",r.stderr.strip()[-800:])
    return r.returncode
run(["bash","bin/generate-skills-json"])
run(["bash","bin/generate-packs-json"])
run(["bash","bin/generate-skill-icons"])
if os.path.exists("scripts/gen-agents-md.js"):
    run(["node","scripts/gen-agents-md.js"])
else:
    print("no scripts/gen-agents-md.js")
