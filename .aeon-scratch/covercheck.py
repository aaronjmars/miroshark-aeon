import glob, os
lock=open("eyebrowlock.json").read()
missing=[]
for f in glob.glob("skills/*/SKILL.md"):
    slug=os.path.basename(os.path.dirname(f))
    if f'"discoveredFrom": "skills/{slug}/SKILL.md"' not in lock:
        missing.append(slug)
print("total skills:", len(glob.glob("skills/*/SKILL.md")))
print("missing lock entries:", missing if missing else "NONE")
