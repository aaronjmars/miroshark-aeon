import subprocess, os, hashlib
HEAD="ba01e9f3e4495c8f761ab483000639cc8d5f5221"

def blob(sha,path):
    r=subprocess.run(["git","show",f"{sha}:{path}"],capture_output=True)
    return r.stdout if r.returncode==0 else None
def local(path):
    return open(path,"rb").read() if os.path.exists(path) else None
def h(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None

# prior pending entries NOT resolved by this window's compare
paths = [
 ".github/workflows/messages.yml",
 "apps/dashboard/package.json",
 "apps/dashboard/package-lock.json",
 "apps/webhook/package.json",
 "apps/webhook/package-lock.json",
 "llms.txt",
 "skills/competitor-monitor/SKILL.md",
]
for p in paths:
    lb=local(p); hb=blob(HEAD,p)
    ls,hs=h(lb),h(hb)
    if lb is None:
        print(f"{p}: local MISSING; head_exists={hb is not None} -> KEEP (divergent)")
    elif ls==hs:
        print(f"{p}: local==HEAD -> RESOLVED (drop)")
    else:
        print(f"{p}: local!=HEAD -> KEEP (still divergent)")

# skill dirs (compute-resell, submit-hook): check if SKILL.md present locally
for d in ["skills/compute-resell","skills/submit-hook"]:
    sk=os.path.join(d,"SKILL.md")
    print(f"{d}: local_SKILL_exists={os.path.exists(sk)} -> {'RESOLVED?' if os.path.exists(sk) else 'KEEP (not present locally)'}")
