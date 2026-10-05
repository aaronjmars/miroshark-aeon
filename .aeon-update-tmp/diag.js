const { execSync } = require("child_process");
function run(cmd) {
  try {
    const out = execSync(cmd, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    return { ok: true, out: out.slice(-1500) };
  } catch (e) {
    return { ok: false, out: ((e.stdout || "") + "\n" + (e.stderr || "")).slice(-1500) };
  }
}
// 1. skills.json drift (mirror ci-skills-json)
const norm = (f) =>
  `sed -E -e 's/"generated":"[^"]*"/"generated":""/' -e 's/"sha":"[^"]*"/"sha":""/g' -e 's/"updated":"[^"]*"/"updated":""/g' ${f}`;
console.log("### ls skills count (dirs w/ SKILL.md)");
console.log(run("bash -c 'ls -d skills/*/SKILL.md 2>/dev/null | wc -l'").out.trim());
console.log("### current catalog total");
console.log(run("bash -c \"grep -oE '\\\"total\\\":[0-9]+' catalog/skills.json | head -1\"").out.trim());
console.log("### ci-skills-json (regen + diff, current tree)");
let r = run(`bash -c '${norm("catalog/skills.json")} > /tmp/a.json; bin/generate-skills-json >/dev/null 2>&1; ${norm("catalog/skills.json")} > /tmp/b.json; git checkout -- catalog/skills.json; diff /tmp/a.json /tmp/b.json && echo SKILLS_JSON_CLEAN || echo SKILLS_JSON_DRIFT'`);
console.log(r.out);
console.log("### validate-readme-catalog (current)");
console.log(run("node scripts/validate-readme-catalog.mjs").out);
console.log("### validate-config (current)");
console.log(run("node scripts/validate-config.js aeon.yml").out);
