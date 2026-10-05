const { execSync } = require("child_process");
const fs = require("fs");
const norm = (s) =>
  s.replace(/"generated":"[^"]*"/g, '"generated":""')
   .replace(/"sha":"[^"]*"/g, '"sha":""')
   .replace(/"updated":"[^"]*"/g, '"updated":""');
function regenAndDiff(gen, file) {
  const before = norm(fs.readFileSync(file, "utf8"));
  execSync(gen, { encoding: "utf8", stdio: ["ignore", "ignore", "ignore"] });
  const after = norm(fs.readFileSync(file, "utf8"));
  execSync(`git checkout -- ${file}`);
  if (before === after) return `CLEAN (${file})`;
  // find first differing region
  const a = before.split(/(?<=},)/), b = after.split(/(?<=},)/);
  let diffs = [];
  const max = Math.max(a.length, b.length);
  for (let i = 0; i < max && diffs.length < 6; i++) {
    if (a[i] !== b[i]) diffs.push(`#${i}\n  OLD: ${(a[i]||"").slice(0,160)}\n  NEW: ${(b[i]||"").slice(0,160)}`);
  }
  return `DRIFT (${file}) first diffs:\n` + diffs.join("\n");
}
console.log(regenAndDiff("bin/generate-skills-json", "catalog/skills.json"));
console.log("---");
console.log(regenAndDiff("bin/generate-packs-json", "catalog/packs.json"));
