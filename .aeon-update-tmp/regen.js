const { execSync } = require("child_process");
const fs = require("fs");
const run = (c) => { try { return { ok: true, out: execSync(c, { encoding: "utf8", stdio:["ignore","pipe","pipe"] }) }; } catch (e) { return { ok: false, out: ((e.stdout||"")+(e.stderr||"")) }; } };
const norm = (s) => s.replace(/"generated":"[^"]*"/g,'"generated":""').replace(/"sha":"[^"]*"/g,'"sha":""').replace(/"updated":"[^"]*"/g,'"updated":""');

console.log("## REGENERATE");
for (const g of ["bin/generate-skills-json", "bin/generate-packs-json"]) {
  const r = run(g); console.log(g, "=>", r.ok ? "ok" : "FAIL", r.ok ? "" : r.out.slice(-400));
}
const si = run("bin/generate-skill-icons"); console.log("generate-skill-icons =>", si.ok ? "ok" : "FAIL " + si.out.slice(-400));
const am = run("node scripts/gen-agents-md.js"); console.log("gen-agents-md =>", am.ok ? "ok" : "FAIL " + am.out.slice(-400));

console.log("\n## GATE: ci-skills-json (regen+diff)");
{
  const before = norm(fs.readFileSync("catalog/skills.json","utf8"));
  run("bin/generate-skills-json");
  const after = norm(fs.readFileSync("catalog/skills.json","utf8"));
  console.log(before === after ? "CLEAN" : "DRIFT");
}
console.log("\n## GATE: ci-packs-json (regen+diff)");
{
  const before = norm(fs.readFileSync("catalog/packs.json","utf8"));
  run("bin/generate-packs-json");
  const after = norm(fs.readFileSync("catalog/packs.json","utf8"));
  console.log(before === after ? "CLEAN" : "DRIFT");
}
console.log("\n## GATE: ci-agents-md (regen+diff)");
{
  const before = fs.readFileSync("AGENTS.md","utf8");
  run("node scripts/gen-agents-md.js");
  const after = fs.readFileSync("AGENTS.md","utf8");
  console.log(before === after ? "CLEAN" : "DRIFT (regen changed AGENTS.md — committing the regen)");
}
console.log("\n## GATE: validate-readme-catalog");
console.log(run("node scripts/validate-readme-catalog.mjs").out.trim());
console.log("\n## GATE: validate-config");
console.log(run("node scripts/validate-config.js aeon.yml").out.trim());
console.log("\n## GATE: ci-readme-catalog validate-skill-packs (community)");
console.log(run("node scripts/validate-skill-packs.mjs 2>&1 || true").out.trim().slice(-600));
