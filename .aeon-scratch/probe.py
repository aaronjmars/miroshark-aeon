import subprocess, os
print("cwd", os.getcwd())
with open(".aeon-scratch/pyw.txt","w") as f:
    f.write("py can write\n")
print("wrote ok")
print(subprocess.run(["git","rev-parse","--abbrev-ref","HEAD"],capture_output=True,text=True).stdout.strip())
