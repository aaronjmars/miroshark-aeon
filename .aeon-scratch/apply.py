import subprocess, os, json
HEAD="ba01e9f3e4495c8f761ab483000639cc8d5f5221"

cls = json.load(open(".aeon-scratch/classification.json"))
def blob(sha,path):
    r=subprocess.run(["git","show",f"{sha}:{path}"],capture_output=True)
    return r.stdout if r.returncode==0 else None

applied={"CLEAN-ADD":[],"CLEAN-UPDATE":[],"CLEAN-MERGE":[],"CLEAN-DELETE":[]}
for e in cls:
    d=e["disposition"]; p=e["path"]
    if d in ("CLEAN-ADD","CLEAN-UPDATE"):
        b=blob(HEAD,p)
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        with open(p,"wb") as f: f.write(b)
        applied[d].append(p)
    elif d=="CLEAN-MERGE":
        with open(e["merged_file"],"rb") as f: data=f.read()
        with open(p,"wb") as f: f.write(data)
        applied[d].append(p)
    elif d=="CLEAN-DELETE":
        applied[d].append(p)
for k,v in applied.items():
    print(k, len(v))
    for p in v: print("   ", p)
