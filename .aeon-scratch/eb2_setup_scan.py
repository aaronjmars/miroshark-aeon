import hashlib, os, tarfile, subprocess, json
d=".aeon-scratch/eb2"; tb="eyebrow_0.4.2_linux_amd64.tar.gz"
want=None
for line in open(os.path.join(d,"checksums.txt")):
    p=line.split()
    if len(p)==2 and p[1].lstrip("*")==tb: want=p[0]
got=hashlib.sha256(open(os.path.join(d,tb),"rb").read()).hexdigest()
print("checksum match:", want==got)
assert want==got
with tarfile.open(os.path.join(d,tb)) as t: t.extractall(d)
EB=None
for root,_,files in os.walk(d):
    for fn in files:
        if fn=="eyebrow": EB=os.path.join(root,fn)
os.chmod(EB,0o755)
print("version:", subprocess.run([EB,"--version"],capture_output=True,text=True).stdout.strip())
scrub={"PATH":os.environ.get("PATH",""),"HOME":os.environ.get("HOME","")}
r=subprocess.run([os.path.abspath(EB),"scan","--path",".","--lockfile","eyebrowlock.json"],capture_output=True,text=True,env=scrub)
print("scan exit", r.returncode)
print(r.stdout.strip()[-500:])
print("ERR", r.stderr.strip()[-500:])
# verify
v=subprocess.run([os.path.abspath(EB),"verify","--path",".","--lockfile","eyebrowlock.json"],capture_output=True,text=True,env=scrub)
print("verify exit", v.returncode)
print(v.stdout.strip()[-1500:])
print("VERR", v.stderr.strip()[-800:])
