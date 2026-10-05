const { execSync } = require("child_process");
const fs = require("fs");
const crypto = require("crypto");
const dir = ".aeon-update-tmp/eb";
const tb = "eyebrow_0.5.6_linux_amd64.tar.gz";

// verify checksum against checksums.txt
const sums = fs.readFileSync(`${dir}/checksums.txt`, "utf8");
const want = (sums.split("\n").find(l => l.includes(tb)) || "").trim().split(/\s+/)[0];
const got = crypto.createHash("sha256").update(fs.readFileSync(`${dir}/${tb}`)).digest("hex");
console.log("checksum want:", want);
console.log("checksum got :", got);
if (!want || want !== got) { console.log("CHECKSUM MISMATCH — aborting eyebrow"); process.exit(2); }

// extract
execSync(`tar xzf ${dir}/${tb} -C ${dir}`);
const bin = execSync(`find ${dir} -type f -name eyebrow`, { encoding: "utf8" }).trim().split("\n")[0];
execSync(`chmod +x ${bin}`);
console.log("eyebrow bin:", bin);
console.log("version:", execSync(`${bin} --version 2>&1 || true`, { encoding: "utf8" }).trim());

// scan with scrubbed env (local file hasher; no secrets/network needed)
const scrubbed = { PATH: process.env.PATH, HOME: process.env.HOME };
try {
  const out = execSync(`${bin} scan --path . --lockfile eyebrowlock.json`, { encoding: "utf8", env: scrubbed });
  console.log("SCAN OK:\n" + out.slice(-800));
} catch (e) {
  console.log("SCAN FAIL:\n" + ((e.stdout||"")+(e.stderr||"")).slice(-800));
  process.exit(3);
}
// show lock delta vs HEAD
console.log("\n=== eyebrowlock.json diff stat vs HEAD ===");
console.log(execSync("git diff --stat HEAD -- eyebrowlock.json", { encoding: "utf8" }));
