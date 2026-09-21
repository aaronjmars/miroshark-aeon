import subprocess, os, json
HEAD="ba01e9f3e4495c8f761ab483000639cc8d5f5221"
cls=json.load(open(".aeon-scratch/classification.json"))
paths=[e["path"] for e in cls if e["disposition"] in ("CLEAN-ADD","CLEAN-UPDATE","CLEAN-MERGE")]
for p in paths:
    r=subprocess.run(["git","ls-tree",HEAD,"--",p],capture_output=True,text=True)
    if not r.stdout.strip(): continue
    mode=r.stdout.split()[0]  # e.g. 100755
    if mode=="100755" and os.path.exists(p):
        os.chmod(p,0o755)
        print("chmod 755", p)
