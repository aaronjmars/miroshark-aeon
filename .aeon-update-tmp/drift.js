const { execSync } = require("child_process");
const norm = (f) =>
  `sed -E -e 's/"generated":"[^"]*"/"generated":""/' -e 's/"sha":"[^"]*"/"sha":""/g' -e 's/"updated":"[^"]*"/"updated":""/g' ${f}`;
const cmd = `bash -c '${norm("catalog/skills.json")} > /tmp/a.json; bin/generate-skills-json >/dev/null 2>&1; ${norm("catalog/skills.json")} > /tmp/b.json; git checkout -- catalog/skills.json; diff /tmp/a.json /tmp/b.json | head -40'`;
try { console.log(execSync(cmd, { encoding: "utf8" })); }
catch (e) { console.log(e.stdout || e.message); }
