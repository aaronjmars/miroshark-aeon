const { execSync } = require("child_process");
try {
  const out = execSync("bash -c 'echo exec-ok; awk \"BEGIN{print 42}\"'", { encoding: "utf8" });
  console.log("RESULT:", out.trim());
} catch (e) {
  console.log("ERR:", e.message.slice(0, 200));
}
