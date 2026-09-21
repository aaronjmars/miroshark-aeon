import subprocess
BASE="95142d19705ca379815e7fc9493a497ee0504e8d"
HEAD="ba01e9f3e4495c8f761ab483000639cc8d5f5221"
files=[
 ".github/workflows/aeon.yml",
 ".github/workflows/ci-tests.yml",
 ".github/README.md",
 "docs/skill-packs.md",
 "skills/miroshark-matchday/SKILL.md",
]
for f in files:
    r=subprocess.run(["git","log","--format=%h",f"{BASE}..{HEAD}","--",f],capture_output=True,text=True)
    shas=[s for s in r.stdout.split() if s]
    print(f, shas)
