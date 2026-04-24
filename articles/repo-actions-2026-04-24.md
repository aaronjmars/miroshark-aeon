# Repo Action Ideas — 2026-04-24

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 799 stars · 149 forks · 0 open issues · 0 open PRs
**Recent activity:** MCP Onboarding panel (PR #44) merged today — the graph memory stack is now discoverable inside Settings. PR #43 (Public Simulation Gallery) merged yesterday. 1K-stars-by-Apr-30 target: 201 more needed in 6 days (~34/day needed; current pace ~10-22/day). Paradigm CTO starred the repo today; OriginTrail founder co-signed for DKG V10; Chinese quants are forking.

## Ecosystem Context

The past week delivered the full research-platform stack: graph memory with bi-temporal edges, an 8-tool MCP server, public share cards, a community gallery, and in-app onboarding for AI IDE integration. The infrastructure is assembled. What's lagging is the *social layer* — the mechanics that make simulation results spread, get discovered as best-in-class, and integrate into the tools researchers already use. With 6 days left on the 1K-star sprint and organic momentum from the Paradigm/OriginTrail co-signs, the highest-leverage ideas are the ones that create shareable moments, reduce friction for community re-sharing, and put MiroShark on surfaces where researchers and developers discover tools.

Four signal threads drive this batch:

- **Social moment creation:** Simulations complete in silence. There's no "watch it happen" experience, no live state to screenshot mid-run, no shareable animation. Real-time streaming turns every run into a showreel.
- **Community gravity:** The gallery is chronological. There's no curated "best of" surface. Researchers landing for the first time need social proof — not just recent activity, but high-quality results ranked by impact.
- **Zero-code integrations:** Power users want simulations to flow into their existing tooling (Slack alerts, Zapier workflows, Discord channels). A webhook and one-click Discord post eliminate the copy-paste step entirely.
- **Developer discovery:** With MCP onboarding live, researchers are now connecting AI IDEs to MiroShark. The next thing they look for is an API spec — OpenAPI/Swagger is the signal of production-quality that gets MiroShark onto API directories and into `openapi-generator` SDKs.

Previously suggested ideas excluded from this batch (last 7 days): Public Gallery (shipped Apr 23), Simulation Clone (shipped via PR #43 fork), MCP Onboarding (shipped Apr 24), History Search & Tags (Apr 22, not yet built), Multi-Scenario Compare (Apr 22, already existed from PR #41), Recurring Simulation Watch (Apr 18), PDF Report (Apr 18), Dev Container (Apr 18), Round Scrubber (Apr 20), Collaborative Comments (Apr 20), Config Export/Import (Apr 20). All 5 ideas below are net-new.

---

### 1. Live Simulation Streaming (Server-Sent Events)

**Type:** Feature
**Effort:** Small (hours)
**Impact:** Simulations currently complete in silence — users submit, wait, then see results. Streaming round-by-round belief updates via SSE creates a "watch the minds change" experience: the belief bar animates, the round counter ticks, agent stances shift in real time. This is the shareable moment the project has been missing — a GIF-able, screenshot-worthy view of collective belief formation. For the 1K-star sprint, it's a distribution mechanic: the live view is compelling to share mid-run in ways a completed result is not. Flask supports SSE natively via `stream_with_context`; no new dependencies.
**How:**
1. Add `GET /api/simulation/:id/stream` — a Flask route using `stream_with_context` and a generator that yields `data: {json}\n\n` events. Emit one event per completed round: `{round, belief_distribution: {bullish, neutral, bearish}, agent_stances: [...], timestamp}`. The generator polls the simulation runner's state every 0.5s (the runner already writes per-round state to disk) and yields each new round exactly once. Terminate with a `data: {"done": true}\n\n` event when `status == "completed"` or `"failed"`.
2. Add a "Watch live" toggle to the simulation submit flow. When active, redirect to `/simulation/:id?stream=1` instead of polling. In `SimulationView.vue`, open an `EventSource` to `/api/simulation/:id/stream`. On each event, animate the belief bars using CSS transitions (update the existing `beliefSplit` reactive variable). Show the round counter ticking. On `done`, mark the run complete and enable the full analytics panel. Falls back to the existing polling path if `EventSource` is unavailable.
3. Add a "📡 Live" badge to the simulation header while streaming. Include a "Copy live link" button that shares the `/simulation/:id?stream=1` URL — so viewers can watch a run in progress. Add a note to the `/explore` gallery cards showing "Live now" for simulations currently streaming. This makes in-progress runs a discovery surface, not just completed results.

---

### 2. Simulation Engagement Leaderboard

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** The `/explore` gallery is sorted chronologically. New visitors see whatever was published most recently — not the most compelling evidence that MiroShark produces high-quality research. A leaderboard showing the top 20 public simulations by engagement (fork count × 3 + quality bonus + share view count) creates a curated "best of all time" surface that acts as social proof. A researcher landing on the site for the first time sees "1,247 people forked this DeepSeek earnings simulation (Excellent quality, 73% bearish consensus)" — not an empty setup form. Backend is a one-field sort extension over the existing public gallery endpoint; frontend reuses `ExploreView.vue` card layout with rank overlays.
**How:**
1. Add a `share_view_count` integer field to the simulation record, incremented (in-memory, no lock needed for approximate count) each time `GET /share/:id` is served. Expose the field in `_build_gallery_card_payload()`. Add `sort=engagement` query param to `GET /api/simulation/public` — when set, rank by `(fork_count * 3) + (1 if quality_health == "excellent" else 0) + (share_view_count // 10)`. Default remains `created_at` desc.
2. Add a `?view=leaderboard` tab to `/explore` (or a `/leaderboard` route reusing the same `ExploreView.vue` component). When active, fetch `GET /api/simulation/public?sort=engagement&limit=20`. Overlay a rank badge (#1, #2, #3) on each card's top-left corner; use gold/silver/bronze colors for the top three. Add a "🏆 Leaderboard" nav link to `Home.vue` alongside the existing "◎ Explore" link.
3. Add a "View on leaderboard" link to the `GET /share/:id` landing page when the simulation ranks in the top 20 (include rank in the `_build_gallery_card_payload` response when `sort=engagement`). This closes the loop: a shared simulation that performs well organically surfaces in the leaderboard, which drives more shares, which raises its rank — a compounding discovery loop that costs nothing to operate.

---

### 3. Webhook Notification on Simulation Complete

**Type:** Integration / DX
**Effort:** Small (hours)
**Impact:** Researchers running long simulations (50+ agents, 20+ rounds) leave the tab and come back later. They miss the moment of completion. A webhook fires a POST to a user-configured URL the instant a simulation finishes, carrying the full result summary including the share permalink. This enables zero-code integrations: Zapier → email, Make → Airtable row, n8n → Slack message (with OG card auto-unfurling from the share URL), or a custom dashboard listener. One setting field, one stdlib POST call, no new dependencies.
**How:**
1. Add `WEBHOOK_URL` to the settings config (stored alongside existing `LLM_API_KEY` etc.). Expose via `GET /api/settings` (masked to domain only, e.g. `https://hooks.slack.com/***`) and `POST /api/settings`. Add a "Webhook URL" input to the Settings modal's existing layout with a "Test webhook" button that fires a sample payload.
2. After the simulation runner writes its final `state.json` (status `"completed"` or `"failed"`), call a `_fire_webhook(sim_id, config)` helper. Build the payload: `{sim_id, scenario (120-char truncated), status, final_consensus: {bullish, bearish, neutral}, quality_health, quality_score, agent_count, round_count, share_url: "https://{host}/share/{sim_id}", created_at}`. POST via `urllib.request` with a 5s timeout and `Content-Type: application/json`. Fire in a daemon thread so a slow webhook endpoint never delays the runner. Log success/failure; never raise.
3. Document the webhook payload shape in `docs/` (one new section in an existing doc, or a new `docs/WEBHOOKS.md`). Add a "Webhook integrations" row to the README's Features table. Include Zapier, Make, and n8n as named integration targets in the doc — these are searchable keywords that drive organic discovery from users who search for "n8n MiroShark integration" or "Zapier simulation webhook".

---

### 4. "Post to Discord / Slack" Share Button

**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** Crypto communities coordinate on Discord; AI researchers coordinate on Slack. The current share flow is: copy link → open Discord/Slack → paste → wait for OG unfurl. A "Post to channel" button in the existing `EmbedDialog` collapses this to one click. Users paste a Discord Incoming Webhook URL or Slack Incoming Webhook URL (stored in settings). Clicking sends a pre-formatted embed: scenario headline, quality badge, consensus split, belief bar (text art), and the share link — which auto-unfurls as the 1200×630 OG card. No bot, no OAuth, no hosted infrastructure — one POST per share action. This is the highest-friction-reduction lever for the crypto-community distribution channel.
**How:**
1. Add `DISCORD_SHARE_WEBHOOK` and `SLACK_SHARE_WEBHOOK` to user settings (two optional URL fields). Validate on save: must match `https://discord.com/api/webhooks/` or `https://hooks.slack.com/`. Add a "Post to channel" subsection to `EmbedDialog.vue` below the existing share-link section: two small inputs (pre-populated from settings), a "Post to Discord" button, and a "Post to Slack" button. Show a ✓ / ✗ confirmation inline without navigating away.
2. Add `POST /api/simulation/:id/share-to-channel` — accepts `{channel: "discord"|"slack", webhook_url}`. Builds the Discord embed payload: `{embeds: [{title: scenario[:80], description: belief bar + consensus line, color: 0x00ff88, fields: [{name: "Quality", value: quality_health}, {name: "Consensus", value: "Bull X% · Neutral Y% · Bear Z%"}], url: share_url, image: {url: share_card_url}}]}`. For Slack: `{blocks: [{type: "section", text: {type: "mrkdwn", text: "..."}}, {type: "image", image_url: share_card_url, alt_text: scenario[:80]}]}`. POST to the user-provided webhook URL via `urllib.request`. Return `{ok: true}` or `{ok: false, error}`. Backend-proxied to avoid browser CORS restrictions.
3. Pre-populate the webhook URL inputs from `GET /api/settings` on `EmbedDialog` mount, so repeat sharers don't re-enter URLs. Add a "Save as default" checkbox. Extend `GET /api/simulation/:id/share-card.png` to accept `?format=discord` — returns a slightly cropped 1200×630 variant with padding adjusted for Discord's preview box — so the card looks native in Discord embeds. Add a one-line mention in the README Sharing section: "Post directly to Discord or Slack — no bot required."

---

### 5. OpenAPI / Swagger Documentation

**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** With MCP onboarding (PR #44) live, researchers connecting Claude Desktop or Cursor to MiroShark will next ask: "What REST endpoints can I call directly?" An `openapi.yaml` served as Swagger UI at `/api/docs` answers that question, and also: (a) lists MiroShark on APIs.guru and RapidAPI, (b) enables `openapi-generator` SDKs so community contributors can build Python/JS/Go clients, (c) shows up in GitHub topic searches for `openapi`, and (d) signals production-quality to the developers and ML researchers who starred from the Paradigm co-sign. Handwritten YAML for the public surface (~15 endpoints) is a few hours of work; Swagger UI is a single CDN script tag.
**How:**
1. Write `backend/openapi.yaml` covering all public endpoints: `POST /api/simulation/start`, `GET /api/simulation/{id}`, `POST /api/simulation/{id}/pause`, `POST /api/simulation/{id}/resume`, `GET /api/simulation/public`, `GET /api/simulation/{id}/share-card.png`, `GET /share/{id}`, `POST /api/simulation/suggest-scenarios`, `GET /api/mcp/status`, `GET /api/settings`, `POST /api/settings`, `GET /api/simulation/trending`, `POST /api/simulation/{id}/share-to-channel` (idea #4). Use OpenAPI 3.0. Include request/response schemas with examples drawn from real payloads. Tag by category: Simulation, Discovery, Settings, Integrations.
2. Add a `GET /api/docs` route in the Flask app (one blueprint, ~10 lines). Serve an HTML page that loads Swagger UI from jsDelivr CDN (`swagger-ui-bundle.js` + `swagger-ui.css`) and points `url` at `/api/openapi.yaml`. Add `GET /api/openapi.yaml` as a static-file serve of `backend/openapi.yaml` with `Content-Type: application/yaml`. No new Python dependencies.
3. Add a "📖 API Reference" link to the README alongside the existing docs links. Submit the `openapi.yaml` URL to APIs.guru via their GitHub-based submission process (one PR to their repo). Add `openapi` to the GitHub repo's topic tags. This is the integration surface that separates "cool demo" from "tool I can build on" — the signal the Paradigm/quant audience will look for when evaluating MiroShark as infrastructure.

---

## Selection Rationale

Today's batch targets the gap between "infrastructure complete" and "infrastructure discoverable and viral":

- **SSE Streaming** (#1) — Creates a shareable moment during runs, not just after. The live view is GIF-able, screenshot-worthy, and link-shareable mid-run. Direct lever on distribution for the 1K-star sprint.
- **Leaderboard** (#2) — Turns the chronological gallery into a curated "best of" surface. Social proof for new visitors. The share-view-count compounding loop costs nothing to operate.
- **Webhook** (#3) — Zero-code integrations for Zapier/Make/n8n. Researchers running long simulations get instant notification with a shareable link. Named integration targets (n8n, Zapier, Make) drive organic search discovery.
- **Discord/Slack Post Button** (#4) — Collapses the copy-link-open-app-paste share flow to one click for the communities where MiroShark's audience lives. No bot, no OAuth, high signal-to-effort ratio.
- **OpenAPI docs** (#5) — The document the Paradigm-adjacent ML/developer audience will look for next. API directory listings + SDK generation + production-quality signal. Natural follow-on to MCP onboarding (PR #44).
