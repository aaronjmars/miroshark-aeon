# Repo Action Ideas — 2026-04-22

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 770 stars · 147 forks · 0 open issues · 0 open PRs
**Recent activity:** Social Share Card (PR #42) merged today — simulations now unfurl as visual cards on Twitter/X, Discord, and Slack. Yesterday's direct-push wave landed Settings presets (Cheap/Best/Local), LLM URL fetcher, multi-market settings, and chart copy/download. The graph memory stack + 8-tool MCP server shipped Sunday night. 1K-stars-by-Apr-30 target: 230 needed in 8 days (~29/day; current pace ~19/day).

## Ecosystem Context

MiroShark has crossed from "run a simulation" to "research infrastructure." The last five days delivered: a knowledge graph with bi-temporal edges and Leiden clustering, an MCP server exposing 8 research tools, public share permalinks with Open Graph image cards, settings presets, and an LLM-powered URL fetcher. The parts are assembled. What's missing is the connective tissue — the flows that let users discover each other's work, build on prior runs, organize a growing simulation library, and expose the graph memory to the AI tools they already use.

Four signal threads drive this batch:

- **Discovery gap:** `is_public` and `POST .../publish` exist (from PR #41), and share cards now render (PR #42). But there's no `/explore` page. Every public simulation is invisible except to the person who ran it. The infrastructure for a community gallery is complete; only the frontend shell is missing.

- **Iteration friction:** Researchers running multiple variations of the same scenario open a new setup form and fill it in from memory each time. Config Export/Import (suggested Apr 20, not yet shipped) addresses this through files. Fork-in-app addresses it through a single button click — lower friction, higher discoverability, no file system required.

- **Invisible infrastructure:** The MCP server is the most forward-looking capability MiroShark has shipped — 8 tools, bi-temporal graph, Leiden community clusters. But there's no path for a user to connect Claude Desktop or Cursor to it. The feature exists only for the engineer who wrote it.

- **Organization debt:** Power users accumulating 50+ simulations have no search, no tagging, no way to find a specific run. The history view is a chronological scroll. Organization features compound in value as the library grows — building them now, before the pile becomes overwhelming, pays forward.

Previously suggested ideas excluded from this batch (last 7 days): Social Share Card (shipped), Trending Topics (shipped), Round Scrubber (#1, Apr 20), Collaborative Comments (#4, Apr 20), Config Export/Import (#5, Apr 20), Recurring Simulation Watch (Apr 18), PDF Report (Apr 18), Dev Container (Apr 18), Checkpoint & Resume (Apr 15), HuggingFace LLM (Apr 15), RSS Output Feed (Apr 15), Simulation Replay (Apr 16), Multi-Document Comparative Mode (Apr 16), Director Mode (shipped), Embeddable Widget (shipped), Demographic Breakdown (shipped), Scenario Auto-Suggest (shipped), Counterfactual Explorer (shipped), Statistical Batch Runs (Apr 14), Browser Push Notifications (shipped), Jupyter Export (Apr 14), REST API + Webhook (Apr 14), Hall of Fame (Apr 14). All 5 ideas below are net-new.

---

### 1. Public Simulation Gallery

**Type:** Growth
**Effort:** Small (hours)
**Impact:** PR #41 added `is_public` flag + `POST /api/simulation/:id/publish`. PR #42 gave every simulation a 1200×630 share card. The discovery layer — a public `/explore` page — doesn't exist. Without it, every public simulation is a tree falling in an empty forest. A gallery page showing recent public simulations as visual cards (share-card thumbnail, scenario headline, consensus %, quality badge, "Fork this →" button) turns every researcher who presses "Publish" into a referral node. For the 1K-star sprint, this is the highest-leverage distribution lever available: new visitors land on a page of real research results rather than an empty setup form.
**How:**
1. Add `GET /api/simulations/public` — queries `is_public=true` simulations sorted by `created_at` desc, returns 50/page. Payload per item: `sim_id`, `scenario` (120 chars max), `quality_health`, `final_consensus` (bull/bear/neutral %), `agent_count`, `round_count`, `created_at`, share-card URL.
2. Add `/explore` Vue route (no auth). Render a responsive card grid: each card shows the share-card PNG via `<img>`, scenario headline, quality/consensus pills, agent/round metadata, and a "Fork this →" link to `/?fork=:sim_id`. Empty state: "No public simulations yet — yours could be first." Add a compass-icon Explore link to the main nav.
3. Surface a "Submit to Gallery" CTA inside the EmbedDialog alongside the existing share-link section. Add the gallery URL to the README under Sharing and to the `GET /share/:id` landing page footer. Link the explore page from the project's GitHub description to drive organic discovery.

---

### 2. Simulation Clone / One-Click Fork

**Type:** Feature / DX
**Effort:** Small (hours)
**Impact:** Researchers testing variations of a scenario — different framing, agent count, model preset — currently recreate the setup from memory. Config Export/Import (from Apr 20, not yet shipped) solves this through files; in-app forking solves it through a button. A "↩ Re-run" button on the simulation result page and history cards opens the setup form pre-filled with that run's exact parameters: scenario text, agent count, round count, document URLs, model preset, any Director Mode events. The fork-in-app pattern is also the user-facing expression of the public gallery's "Fork this →" action, making ideas #1 and #2 mutually reinforcing.
**How:**
1. Add a `setup_params` JSON column to the simulation record (set at creation from the `POST /api/simulation` request body — scenario, agent_count, round_count, document_urls, model slot values, director events if any). Expose as `GET /api/simulation/:id/params`. No migration needed for historical simulations — return `null` and fall through to a partial hydration.
2. Add a "↩ Re-run" button to the simulation result page header (alongside Share/Embed) and to each history card dropdown. Clicking routes to `/?fork=:sim_id`. The `Home.vue` `onMounted` reads the `fork` query param, fetches `/api/simulation/:id/params`, and hydrates all form fields in a single reactive update. Show a dismissible "Forked from [scenario headline]" banner.
3. Add `forked_from` field to the simulation record. Surface fork lineage on history cards ("Forked from abc123 · 3 derived"). Wire the "Fork this →" button in the public gallery (idea #1) to the same `?fork=` route, making the gallery → fork flow end-to-end without additional plumbing.

---

### 3. Claude Desktop / AI IDE MCP Onboarding

**Type:** DX / Integration
**Effort:** Small (hours)
**Impact:** The graph memory MCP server — 8 tools (`search_memory`, `store_memory`, `browse_clusters`, `analyze_connections`, and four more), bi-temporal edges, Leiden community clusters — is the most technically sophisticated feature MiroShark has shipped. It's also completely invisible: there's no documented path for a user to connect Claude Desktop, Cursor, or Windsurf to it. A Settings "AI Integration" tab with a toggle, a copy-pasteable `claude_desktop_config.json` snippet (auto-populated with the correct port), a "Test connection" button, and a link to `docs/MCP.md` turns invisible infrastructure into a discoverable power-user capability — and positions MiroShark as MCP-native in the ecosystem narrative at a moment when MCP adoption is accelerating.
**How:**
1. Add `GET /api/mcp/status` — returns `{enabled: bool, port: int, tools: [{name, description}]}` from the existing MCP server config. Expose `MCP_SERVER_ENABLED` toggle via the existing `GET/POST /api/settings` endpoints. No new backend services; the server already runs.
2. Add an "AI Integration" tab to the Settings modal. When enabled: (a) copy-pasteable `claude_desktop_config.json` block auto-populated with `command: "npx"`, `args: ["miroshark-mcp"]`, and `url: "http://localhost:{PORT}"`; (b) "Test connection" button calling `/api/mcp/status` with a green/red indicator; (c) list of all 8 tools with one-line descriptions. When disabled: an "Enable MCP Server" toggle and a "What is this?" tooltip.
3. Write `docs/MCP.md`: step-by-step for Claude Desktop (config screenshot), Cursor (`.cursor/mcp.json` snippet), and Windsurf stub. Add a "Connect to Claude" badge to the README Features table. Add the MCP server port to `docker-compose.yml` as a named service for documentation clarity. This is the integration story that separates MiroShark from every other simulation tool that doesn't expose an MCP surface.

---

### 4. Simulation History Search & Tags

**Type:** DX
**Effort:** Small (hours)
**Impact:** Power users accumulating 50+ simulations have no way to find a specific run beyond scrolling chronologically. Tags (set at setup, editable on history cards) and a search bar (filters by scenario text, tags, quality badge, date range) turn the history view from a log into a research library. All data lives on existing records; this requires one new column and frontend filter UI. Tags also open a cross-feature layer: the public gallery can be filtered by tag (`/explore?tag=defi`), and the simulation setup form can suggest tags from the user's prior runs to nudge consistent categorization.
**How:**
1. Add a `tags` column (text array / comma-separated string) to the simulation model. Expose on `POST /api/simulation` (accept `tags: string[]`) and `PATCH /api/simulation/:id`. Add `GET /api/simulations?q=<text>&tags=<csv>&quality=<badge>&since=&until=` — `ILIKE %q%` on scenario text, array contains on tags. Add `GET /api/tags/recent` returning the user's 20 most-used tags for autosuggest.
2. Add a chip-style tag input to the simulation setup form (below scenario text). Press Enter or comma to add; cap at 10 tags, 30 chars each. Autosuggest from `GET /api/tags/recent`. Display tags on history cards as small colored pills (color deterministically derived from tag name hash).
3. Add a search/filter bar to the history page header. Wire to `GET /api/simulations?q=...` with 300ms debounce. Filter chips for quality badge, date range picker, and tag multi-select. Match count label ("12 simulations"). Clear-all button. Surface tags in the public gallery as clickable filter links so `/explore?tag=defi` narrows the gallery to DeFi simulations — the same tagging taxonomy spans personal history and community discovery.

---

### 5. Multi-Scenario Comparison View

**Type:** Feature / Research
**Effort:** Medium (1-2 days)
**Impact:** PR #39 (Scenario Auto-Suggest) generates three Bull/Bear/Neutral variants from a document. Users typically run one, then open a new tab to run another, then compare results manually. A Compare mode lets users select 2-3 simulations from history and view them side-by-side: a unified belief-drift chart (one colored line per simulation), consensus % comparison bar, quality diagnostic alignment, and an "Export comparison PNG" button. This is distinctly different from Multi-Document Comparative Mode (suggested Apr 16) — it compares multiple scenario framings on the same document, not multiple documents. The Scenario Auto-Suggest → Compare pathway specifically turns a "run one" interaction into a "evaluate all three" research workflow.
**How:**
1. Add `GET /api/simulations/compare?ids=a,b,c` — batch-fetches up to 3 simulations, normalizes trajectory data to a common round scale (interpolate to `max(roundCount)` if they differ). Returns the same simulation payload shape but as an array. No new DB schema.
2. Add a "Compare" checkbox to each history card. When 2-3 are checked, a sticky "Compare N →" bar appears at the page bottom. Route to `/compare?ids=a,b,c`. The compare page renders: (a) a unified belief-drift chart with one colored line per scenario (legend: scenario name + quality badge), (b) final consensus comparison row (stacked bars side-by-side), (c) quality diagnostic bar alignment table (participation rate, stance entropy, convergence speed as horizontally grouped bars), (d) agent/round metadata header. Add "Export comparison PNG" using the existing Pillow infrastructure.
3. Add a "Run all 3 & compare →" shortcut to the Scenario Auto-Suggest panel (PR #39 flow). After the user runs one of the three suggested scenarios, show a prompt: "Run the other 2 scenarios and compare →". Clicking queues two background simulation runs with the remaining scenarios and redirects to the compare view when all three complete. This closes the Auto-Suggest → Compare → Export loop into a single research workflow.

---

## Selection Rationale

Today's batch is organized around the transition from individual simulation tool to shared research platform:

- **Public Gallery** (#1) — The `is_public` + share-card infrastructure is complete. The discovery layer is the only missing piece. Every public simulation becomes a distribution node for the 1K-star sprint.
- **Simulation Clone** (#2) — Removes the single highest-friction gap for repeat researchers. Pairs with the gallery as the "Fork this →" action, making both features stronger.
- **MCP Onboarding** (#3) — Makes the most sophisticated infrastructure feature (graph memory + 8 MCP tools) discoverable. Positions MiroShark as MCP-native at the right moment in the ecosystem.
- **History Search & Tags** (#4) — Organization debt that compounds as the user base grows. Tags span personal history and community gallery, making them a foundational data type worth adding now.
- **Multi-Scenario Compare** (#5) — Closes the research workflow that Scenario Auto-Suggest opened: generate three framings, compare all three, export the comparison. Turns a single-simulation interaction into a publishable multi-variant analysis.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, all required data already in the codebase, no ambiguous design decisions, no external approvals needed.
