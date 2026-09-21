import subprocess
r=subprocess.run(["node","bin/generate-skill-icons"],capture_output=True,text=True)
print("exit",r.returncode)
print("out:",r.stdout.strip()[-1500:])
print("err:",r.stderr.strip()[-1500:])
