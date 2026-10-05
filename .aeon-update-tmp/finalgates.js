const { execSync } = require("child_process");
const fs = require("fs");
const run = (c, env) => { try { return { ok: true, out: execSync(c, { encoding: "utf8", stdio:["ignore","pipe","pipe"], env: env||process.env }) }; } catch (e) { return { ok: false, out: ((e.stdout||"")+(e.stderr||"")) }; } };
const norm = (s) => s.replace(/"generated":"[^"]*"/g,'"generated":""').replace(/"sha":"[^"]*"/g,'"sha":""').replace(/"updated":"[^"]*"/g,'"updated":""');
const P = (n, pass, extra) => console.log(`${pass ? "PASS" : "FAIL"}  ${n}${extra ? "  — " + extra : ""}`);

// ci-skills-json
{ const b = norm(fs.readFileSync("catalog/skills.json","utf8")); run("bin/generate-skills-json"); const a = norm(fs.readFileSync("catalog/skills.json","utf8")); P("ci-skills-json (regen diff)", b===a); }
// ci-packs-json
{ const b = norm(fs.readFileSync("catalog/packs.json","utf8")); run("bin/generate-packs-json"); const a = norm(fs.readFileSync("catalog/packs.json","utf8")); P("ci-packs-json (regen diff)", b===a); }
// ci-agents-md
{ const b = fs.readFileSync("AGENTS.md","utf8"); run("node scripts/gen-agents-md.js"); const a = fs.readFileSync("AGENTS.md","utf8"); P("ci-agents-md (regen diff)", b===a); }
// validate-readme-catalog (fork lenient)
{ const r = run("node scripts/validate-readme-catalog.mjs"); P("validate-readme-catalog", r.ok, r.out.trim().split("\n").pop()); }
// validate-skill-packs (fork lenient)
{ const r = run("node scripts/validate-skill-packs.mjs"); P("validate-skill-packs", r.ok, r.out.trim().split("\n").pop()); }
// validate-config
{ const r = run("node scripts/validate-config.js aeon.yml"); P("validate-config", r.ok, r.out.trim().split("\n").pop()); }
// ci-skill-category
{ const r = run("bash scripts/check-skill-categories.sh"); P("ci-skill-category", r.ok, r.out.trim().split("\n").pop()); }
// ci-skill-integrity: coverage precheck
{ let missing=[]; for (const d of fs.readdirSync("skills")) { const f=`skills/${d}/SKILL.md`; if(!fs.existsSync(f))continue; const lock=fs.readFileSync("eyebrowlock.json","utf8"); if(!lock.includes(`"discoveredFrom": "skills/${d}/SKILL.md"`)) missing.push(d); } P("ci-skill-integrity coverage", missing.length===0, missing.length?("missing: "+missing.join(",")):"all skills covered"); }
// eyebrow verify
{ const bin=".aeon-update-tmp/eb/eyebrow"; const r = run(`${bin} verify --path . --lockfile eyebrowlock.json 2>&1`, {PATH:process.env.PATH, HOME:process.env.HOME}); P("eyebrow verify", r.ok, r.out.trim().split("\n").slice(-2).join(" | ")); }
