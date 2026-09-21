import subprocess, os
def run(cmd, cwd=None):
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=cwd)
    print(f"$ {' '.join(cmd)} (cwd={cwd or '.'}) -> exit {r.returncode}")
    o=(r.stdout or '').strip(); e=(r.stderr or '').strip()
    if o: print("  out:", o[-1000:])
    if e: print("  err:", e[-1000:])
    print()
    return r.returncode

for f in ["scripts/validate-skill-packs.mjs","scripts/validate-readme-catalog.mjs",
          "scripts/validate-skill-category.mjs","scripts/validate-skills-json.mjs"]:
    if os.path.exists(f):
        run(["node",f])
    else:
        print("(absent)", f)
