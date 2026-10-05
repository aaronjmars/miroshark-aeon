const { execSync } = require("child_process");
const fs = require("fs");
const run = (c) => { try { return { ok: true, out: execSync(c, { encoding: "utf8", stdio:["ignore","pipe","pipe"] }) }; } catch (e) { return { ok: false, out: ((e.stdout||"")+(e.stderr||"")) }; } };
const P = (n, ok, x) => console.log(`${ok?"PASS":"FAIL"}  ${n}${x?"  — "+x:""}`);

// ci-harnesses-json: regenerate harness-adapter/harnesses.json and diff
if (fs.existsSync("harness-adapter/bin/generate-harnesses-json")) {
  const f = "harness-adapter/harnesses.json";
  const b = fs.existsSync(f) ? fs.readFileSync(f,"utf8") : "";
  const r = run("harness-adapter/bin/generate-harnesses-json");
  const a = fs.existsSync(f) ? fs.readFileSync(f,"utf8") : "";
  P("ci-harnesses-json (regen diff)", r.ok && b===a, r.ok? (b===a?"":"DRIFT"):r.out.slice(-200));
}
// ci-capabilities-parity: find its script
const capWf = fs.readFileSync(".github/workflows/ci-capabilities-parity.yml","utf8");
console.log("\n-- ci-capabilities-parity run block --");
console.log(capWf.split("\n").filter(l=>/run:|node |bash |\.sh|\.mjs|\.js/.test(l)).slice(0,8).join("\n"));
// ci-aeon-skill-sync
const syncWf = fs.readFileSync(".github/workflows/ci-aeon-skill-sync.yml","utf8");
console.log("\n-- ci-aeon-skill-sync run block --");
console.log(syncWf.split("\n").filter(l=>/run:|node |bash |\.sh|\.mjs|\.js|diff|check-/.test(l)).slice(0,10).join("\n"));
