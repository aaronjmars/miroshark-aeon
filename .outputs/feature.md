*Feature Built — 2026-05-31*

Simulation Clone JSON
MiroShark simulations now expose their *inputs* — the exact configuration each one was built with — as a JSON endpoint. Every other share surface on the platform (the chart, the badge, the signal, peak-round, volatility, Polymarket, the share card) returns *outputs*: numbers the agents produced. Clone JSON is the first one that returns the recipe.

Why this matters:
Before this, forking a published simulation meant either remembering what you typed into the create form or scraping the raw state.json file off disk. There was no machine-readable way to ask 'what was this sim configured with?' That mattered for AntFleet's benchmark workflow, for researchers running variant studies (same scenario, 40 agents instead of 20), and for the still-unbuilt Scenario Clone Button (May-26 idea #3 / May-18 idea #4). This is also the API complement to the existing /api/simulation/compare endpoint — clone the inputs, run, then diff outputs against the original. Identified as net-new in repo-actions May-30 idea #4 after a 60-second grep confirmed no /clone.json route, no clone_payload field, no clone_service module existed on main (POST /api/simulation/fork is a server-side child creation — different shape).

What was built:
- backend/app/services/clone_service.py (new, ~250 LoC stdlib): build_clone_payload reads state.json + simulation_config.json and assembles the envelope; build_example_curl produces a deterministic one-line curl with the canonical 'https://your-host' placeholder. Pure stdlib (json + os). Returns None when state.json is missing/corrupt so the route emits a clean 404.
- backend/app/api/simulation.py: new GET /<sim_id>/clone.json handler reusing _build_embed_summary_payload for publish gate (403 on private, 404 on no-state). 1-hour cache (vs 5-min on analytical surfaces — inputs are structural, not round-to-round). Increments clone_json surface_stats counter per request.
- backend/openapi.yaml: path entry + CloneResponse schema + ClonePayloadBody schema (every field documented).
- backend/tests/test_unit_clone_service.py (new, 24 offline tests): payload shape, manager-default toggles, polymarket count clamping to [1,5], country lowercasing, demographic_filters pass-through, unicode survival, curl format, static wiring guards.
- frontend/src/components/EmbedDialog.vue: new 🔁 Clone configuration section beneath Polymarket — live summary of project/graph/platforms/country/scenario, plus Download / Copy URL / Copy snippet / Copy POST body buttons.
- docs/API.md row + docs/FEATURES.md section (between Polymarket and Badge SVG).

How it works:
The endpoint reads two on-disk artifacts every published sim already has — state.json (the structural fields create() accepts) and simulation_config.json (the scenario text the LLM-generated config stored). It assembles the envelope so that clone_payload is byte-for-byte the request body POST /api/simulation/create would have accepted: same field names, same defaults, same clamps (manager.create_simulation lowercases country, clamps polymarket count to [1,5], coerces empty filter dicts to None — clone_service mirrors all three). simulation_requirement is echoed at envelope level rather than inside clone_payload because the scenario text lives at the project level — /create doesn't accept it as a body field, the project's value is reused. A fork that needs a different scenario updates the project before POSTing. Zero new dependencies (35th straight PR since Nemotron).

What's next:
PR #131 awaits review. Once merged, an AntFleet benchmark fork is one curl call away. The Scenario Clone Button (still on the unbuilt list, May-26 #3) now has the API half wired — the button just needs to call this endpoint. May-30 batch status: #4 done, #3 RSS Feed verified pre-existing (full filter knobs at /api/feed.rss + /api/feed.atom), #1 Private Share Link / #2 French Locale (issue #95) / #5 Compare UI View still unbuilt.

PR: https://github.com/aaronjmars/MiroShark/pull/131
