import subprocess, os, hashlib
EB=".aeon-scratch/eb/eyebrow"
before = hashlib.sha256(open("eyebrowlock.json","rb").read()).hexdigest()
scrub = {"PATH": os.environ.get("PATH",""), "HOME": os.environ.get("HOME","")}
r = subprocess.run([os.path.abspath(EB),"scan","--path",".","--lockfile","eyebrowlock.json"],
                   capture_output=True, text=True, env=scrub)
print("exit", r.returncode)
print("out:", r.stdout.strip()[-2000:])
print("err:", r.stderr.strip()[-2000:])
after = hashlib.sha256(open("eyebrowlock.json","rb").read()).hexdigest()
print("lock changed:", before!=after)
# check new skills covered
import json
lock=json.load(open("eyebrowlock.json"))
txt=json.dumps(lock)
for s in ["skills/create-prove/SKILL.md","skills/sc-audit/SKILL.md"]:
    print(s, "covered:", s in txt)
