import hashlib, os, tarfile, subprocess
d = ".aeon-scratch/eb"
tb = "eyebrow_0.4.3_linux_amd64.tar.gz"
# parse checksums.txt
want = None
with open(os.path.join(d,"checksums.txt")) as f:
    for line in f:
        parts = line.split()
        if len(parts)==2 and parts[1].lstrip("*")==tb:
            want = parts[0]
with open(os.path.join(d,tb),"rb") as f:
    got = hashlib.sha256(f.read()).hexdigest()
print("want", want)
print("got ", got)
print("match", want==got)
if want==got:
    with tarfile.open(os.path.join(d,tb)) as t:
        t.extractall(d)
    # find eyebrow binary
    for root,_,files in os.walk(d):
        for fn in files:
            if fn=="eyebrow":
                p=os.path.join(root,fn)
                os.chmod(p,0o755)
                print("binary", p)
                print(subprocess.run([p,"--version"],capture_output=True,text=True).stdout.strip())
