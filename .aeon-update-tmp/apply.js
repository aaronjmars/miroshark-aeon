const { execSync } = require("child_process");
const BASE = "531f575eb2beaf12d71e8d9699ce451887babdb4";
const HEAD = "1a7f07e1b259eb46abb472139bb3284d64beee54";
const TREE = "6516899f7110828b2a90a6b7933c5878517b54f9";
const sh = (c) => execSync(c, { encoding: "utf8" });
const shq = (c) => { try { return { ok: true, out: execSync(c, { encoding: "utf8", stdio: ["ignore","pipe","pipe"] }) }; } catch (e) { return { ok: false, out: (e.stdout||"")+(e.stderr||"") }; } };

// changed paths (baseline..upstream HEAD), name-status
const changed = sh(`git diff --name-status ${BASE} ${HEAD}`).trim().split("\n").map(l => {
  const p = l.split("\t");
  // handle rename: A B status; take last field as the current/new path
  return { status: p[0][0], path: p[p.length - 1], prev: p.length === 3 ? p[1] : null };
});

// conflicts from merge-tree --name-only (lines between tree sha and blank line)
const mt = shq(`git merge-tree --write-tree --name-only --merge-base=${BASE} HEAD upstream/main`).out.split("\n");
const conflicts = new Set();
for (let i = 1; i < mt.length; i++) { const l = mt[i].trim(); if (l === "") break; conflicts.add(l); }

const isOperator = (p) =>
  p === "aeon.yml" || p === "STRATEGY.md" || p === ".mcp.json" || p === "aeon.db" ||
  p === "skills.lock" || p === "eyebrowlock.json" ||
  p.startsWith("memory/") || p.startsWith("output/") || p.startsWith("soul/") ||
  (p.startsWith("catalog/") && p.endsWith(".json")) ||
  p.startsWith(".env") ||
  (p.startsWith(".claude/") && !p.startsWith(".claude/skills/aeon/")) ||
  p.startsWith("apps/dashboard/outputs/");

// generated artifacts: never copy from tree; regenerate after
const GENERATED = new Set(["AGENTS.md", "apps/dashboard/lib/skill-icons.data.ts", "catalog/skills.json", "catalog/packs.json"]);
// new skills (would change count/pack-set → hold to protect held README gate)
const isNewSkillHold = (p) => p.startsWith("skills/feedback-builder/");

const buckets = { apply: [], del: [], heldConflict: [], heldOperator: [], heldNewSkill: [], generated: [] };

for (const { status, path } of changed) {
  if (isOperator(path)) { buckets.heldOperator.push(path); continue; }
  if (GENERATED.has(path)) { buckets.generated.push(path); continue; }
  if (isNewSkillHold(path)) { buckets.heldNewSkill.push(path); continue; }
  if (conflicts.has(path)) { buckets.heldConflict.push(path); continue; }
  // clean OWNED: apply or delete based on presence in merged tree
  const inTree = shq(`git cat-file -e ${TREE}:"${path}"`).ok;
  if (inTree) buckets.apply.push(path);
  else buckets.del.push(path);
}

// EXECUTE apply via a single pathspec checkout (batched)
if (buckets.apply.length) {
  // checkout in chunks to keep arg length sane
  const chunk = 60;
  for (let i = 0; i < buckets.apply.length; i += chunk) {
    const slice = buckets.apply.slice(i, i + chunk).map(p => `"${p}"`).join(" ");
    sh(`git checkout ${TREE} -- ${slice}`);
  }
}
for (const p of buckets.del) shq(`git rm -q --ignore-unmatch "${p}"`);

console.log("APPLY:", buckets.apply.length, "| DELETE:", buckets.del.length,
  "| held-conflict:", buckets.heldConflict.length, "| held-operator:", buckets.heldOperator.length,
  "| held-new-skill:", buckets.heldNewSkill.length, "| generated(regen):", buckets.generated.length);
console.log("\n-- DELETE --\n" + buckets.del.join("\n"));
console.log("\n-- HELD conflict --\n" + buckets.heldConflict.join("\n"));
console.log("\n-- HELD operator --\n" + buckets.heldOperator.join("\n"));
console.log("\n-- HELD new skill --\n" + buckets.heldNewSkill.join("\n"));
console.log("\n-- GENERATED (regen) --\n" + buckets.generated.join("\n"));
// persist buckets for later steps
require("fs").writeFileSync(".aeon-update-tmp/buckets.json", JSON.stringify(buckets, null, 1));
