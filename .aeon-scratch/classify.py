#!/usr/bin/env python3
import subprocess, os, json, hashlib, fnmatch

HEAD = "ba01e9f3e4495c8f761ab483000639cc8d5f5221"
BASE = "95142d19705ca379815e7fc9493a497ee0504e8d"

FILES = [
 ("modified", ".claude/skills/aeon/SKILL.md"),
 ("modified", ".claude/skills/aeon/references/layout.md"),
 ("modified", ".claude/skills/aeon/references/mcp.md"),
 ("modified", ".claude/skills/aeon/references/skill-anatomy.md"),
 ("modified", ".github/README.md"),
 ("modified", ".github/workflows/aeon.yml"),
 ("modified", ".github/workflows/chain-runner.yml"),
 ("added",    ".github/workflows/ci-gate.yml"),
 ("modified", ".github/workflows/ci-tests.yml"),
 ("modified", "CHANGELOG.md"),
 ("modified", "aeon.yml"),
 ("modified", "apps/dashboard/app/api/mcp-auth/callback/route.ts"),
 ("modified", "apps/dashboard/lib/skill-icons.data.ts"),
 ("modified", "apps/mcp-server/src/skill-executor.ts"),
 ("modified", "catalog/packs.json"),
 ("modified", "catalog/skill-icons.json"),
 ("modified", "catalog/skills.json"),
 ("modified", "docs/ECOSYSTEM.md"),
 ("added",    "docs/assets/skill-icons/miroshark-matchday.svg"),
 ("added",    "docs/assets/skill-icons/sc-audit.svg"),
 ("modified", "docs/skill-packs.md"),
 ("modified", "eyebrowlock.json"),
 ("modified", "harness-adapter/adapters/codex.sh"),
 ("modified", "plugin/skills/aeon/SKILL.md"),
 ("modified", "plugin/skills/aeon/references/layout.md"),
 ("modified", "plugin/skills/aeon/references/mcp.md"),
 ("modified", "plugin/skills/aeon/references/skill-anatomy.md"),
 ("modified", "scripts/dev-loop-pr.sh"),
 ("added",    "scripts/dev-loop-proof.sh"),
 ("added",    "scripts/dev-loop-repair.sh"),
 ("modified", "scripts/dev-loop-review.sh"),
 ("modified", "scripts/install-harness.sh"),
 ("modified", "scripts/resolve-riva-capabilities.sh"),
 ("modified", "scripts/run-grok.sh"),
 ("modified", "scripts/skill_mode.sh"),
 ("added",    "scripts/stage-sc-audit.sh"),
 ("modified", "scripts/telegram-route.sh"),
 ("modified", "scripts/tests/test_chain_runner_no_action.sh"),
 ("modified", "scripts/tests/test_dev_loop_handoff.sh"),
 ("added",    "scripts/tests/test_dev_loop_proof.sh"),
 ("added",    "scripts/tests/test_dev_loop_repair.sh"),
 ("modified", "scripts/tests/test_dev_loop_review.sh"),
 ("added",    "scripts/tests/test_idea_pipeline_dev_loop_offer.sh"),
 ("modified", "scripts/tests/test_run_grok.sh"),
 ("modified", "scripts/tests/test_telegram_route.sh"),
 ("modified", "skills/aeon-update/SKILL.md"),
 ("modified", "skills/changelog/SKILL.md"),
 ("added",    "skills/create-prove/SKILL.md"),
 ("modified", "skills/feature/SKILL.md"),
 ("modified", "skills/idea-pipeline/SKILL.md"),
 ("modified", "skills/miroshark-matchday/SKILL.md"),
 ("added",    "skills/sc-audit/SKILL.md"),
 ("added",    "skills/sc-audit/fixtures/README.md"),
 ("added",    "skills/sc-audit/fixtures/vault/foundry.toml"),
 ("added",    "skills/sc-audit/fixtures/vault/src/Vault.sol"),
 ("added",    "skills/sc-audit/references/hook-checklist.md"),
 ("modified", "skills/vuln-scanner/SKILL.md"),
]

OPERATOR_GLOBS = [
 "aeon.yml","STRATEGY.md","soul/**","memory/**","output/**",".mcp.json",".env*","aeon.db",
 "skills.lock","eyebrowlock.json","catalog/*.json","apps/dashboard/outputs/**",
]

def is_operator(path):
    # .claude/** is operator EXCEPT .claude/skills/aeon/**
    if path.startswith(".claude/"):
        return not path.startswith(".claude/skills/aeon/")
    for g in OPERATOR_GLOBS:
        if fnmatch.fnmatch(path, g):
            return True
        if g.endswith("/**") and path.startswith(g[:-2]):
            return True
    return False

def git_blob(sha, path):
    r = subprocess.run(["git","show",f"{sha}:{path}"], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout

def local_bytes(path):
    if not os.path.exists(path):
        return None
    with open(path,"rb") as f:
        return f.read()

def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None

os.makedirs(".aeon-scratch/merged", exist_ok=True)
os.makedirs(".aeon-scratch/tmp", exist_ok=True)

results = []
for status, path in FILES:
    entry = {"path": path, "status": status}
    if is_operator(path):
        entry["disposition"] = "OPERATOR"
        results.append(entry); continue
    lb = local_bytes(path)
    hb = git_blob(HEAD, path)
    bb = git_blob(BASE, path)
    ls, hs, bs = sha(lb), sha(hb), sha(bb)
    if status == "added":
        if lb is None:
            entry["disposition"] = "CLEAN-ADD"
        elif ls == hs:
            entry["disposition"] = "SKIP"  # already present identical
        else:
            entry["disposition"] = "CONFLICT"; entry["reason"] = "added-collision"
        results.append(entry); continue
    if status == "removed":
        if lb is None:
            entry["disposition"] = "SKIP"
        elif ls == bs:
            entry["disposition"] = "CLEAN-DELETE"
        else:
            entry["disposition"] = "CONFLICT"; entry["reason"] = "removed-locally-diverged"
        results.append(entry); continue
    # modified
    if ls == hs:
        entry["disposition"] = "SKIP"
    elif ls == bs:
        entry["disposition"] = "CLEAN-UPDATE"
    else:
        # 3-way merge
        lp = ".aeon-scratch/tmp/local"; bp=".aeon-scratch/tmp/base"; hp=".aeon-scratch/tmp/head"
        with open(lp,"wb") as f: f.write(lb or b"")
        with open(bp,"wb") as f: f.write(bb or b"")
        with open(hp,"wb") as f: f.write(hb or b"")
        r = subprocess.run(["git","merge-file","-p","--diff3",lp,bp,hp], capture_output=True)
        if r.returncode == 0:
            entry["disposition"] = "CLEAN-MERGE"
            mp = f".aeon-scratch/merged/{path.replace('/','__')}"
            with open(mp,"wb") as f: f.write(r.stdout)
            entry["merged_file"] = mp
        else:
            entry["disposition"] = "CONFLICT"; entry["reason"] = "operator-customized-overlap"
            entry["conflict_hunks"] = r.returncode
    results.append(entry)

with open(".aeon-scratch/classification.json","w") as f:
    json.dump(results, f, indent=1)

from collections import Counter
c = Counter(r["disposition"] for r in results)
print("DISPOSITION COUNTS:", dict(c))
print()
for r in results:
    extra = r.get("reason","")
    print(f"{r['disposition']:14} {r['status']:9} {r['path']}  {extra}")
