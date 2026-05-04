*Feature Built — 2026-05-04*

Shareable Scenario Links
MiroShark's New Sim form now reads `?scenario=...&url=...&ask=...&template=<slug>` URL parameters — drop a link into a tweet, blog post, or Discord message and the reader lands on the home page with the form already pre-filled, one click away from running their own sim with the exact same setup. A small 🔗 Share-as-link button beneath the Simulation Prompt copies the inverse URL from whatever's currently in the form, and every preset template card gets a 🔗 icon next to Launch that copies a one-click `?template=<slug>` URL.

Why this matters:
Every other share surface MiroShark has shipped — `/share/<id>`, `/watch/<id>`, replay GIF, transcript, RSS, trajectory CSV, the gallery search shipped yesterday — points readers at a *finished* simulation. The *un-run* scenario was the missing direction. When Aaron's "try this sim" tweets pointed at the homepage, the reader saw a blank New Sim form: the friction between "I should try that" and actually running it. PR #67 added the "Fork this scenario" button on `/watch` and `/share` for finished sims; this PR is the same affordance for new ones, completing the share-anywhere loop in both directions.

What was built:
- frontend/src/utils/urlParams.js (new): DOMPurify-backed sanitiser. Strips HTML + javascript: URIs + C0 control chars (preserving \n \r \t so multi-line scenarios survive), caps lengths (scenario 500 / ask 300 / url 2000), restricts `template=` to `[a-z0-9_-]+` so a malicious link can't wedge a path traversal into the template-fetch URL. Read path (`readPrefilledParams`) and write path (`buildScenarioShareUrl` / `buildTemplateShareUrl`) share the same validation.
- frontend/src/views/Home.vue: `onMounted` hook reads the route query, applies pre-fills without overwriting anything the user has already typed, fires a one-shot URL fetch for `?url=`, and hands `?template=<slug>` straight to the existing `setPendingTemplate` + redirect flow. Strips the params via `router.replace` once consumed so refresh / address-bar copy reflects the user's *edited* form, not the original link. Dismissible orange-edged banner above the console signals which fields were populated.
- frontend/src/components/TemplateGallery.vue: every preset card's launch button now has a 🔗 sibling that copies a `?template=<slug>` URL with a brief ✓ flash on success.
- README (en + zh-CN) Features table + docs/FEATURES.md (en + zh-CN) full section with the four-param reference table.

How it works:
The four URL params each sanitise independently — empty / malformed values are no-ops. `?template=<slug>` skips straight to the template launch path (matches the existing card-click flow); the other three pre-fill into the home page's reactive state. URL fetching reuses the same `fetchUrlDoc()` path a manual paste would trigger, so the URL Import list looks identical whether the doc came from a shared link or a hand-typed input. The Share-as-link button reads `formData.simulationRequirement` + the first http(s) doc in `urlDocs` + `askQuestion` and constructs the inverse URL via the same sanitiser; multi-doc setups intentionally only ship the first URL because the rare-and-advanced multi-doc case is better handled by copy-pasting additional URLs separately. Zero backend changes, zero new dependencies (DOMPurify was already pinned for the markdown renderer in `markdown.js`).

What's next:
The remaining ideas from the May 2 repo-actions batch — 1-Click Cloud Deploy (#1, growth), Pre-Run Cost Estimator (#3, the "$1 & under 10 min" tagline at the moment of truth), Per-Agent Stance Sparklines (#4, the per-agent cut on top of yesterday's per-round trajectory CSV) — are all still unbuilt. The cost estimator now has a clean placement: it can sit right next to the Share-as-link button, so the share URL and the run-cost preview show together as the operator hits Launch.

PR: https://github.com/aaronjmars/MiroShark/pull/71
