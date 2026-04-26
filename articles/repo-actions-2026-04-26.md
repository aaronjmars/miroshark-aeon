# Repo Action Ideas — 2026-04-26

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 829 stars · 153 forks · 2 open issues · 2 open PRs (#45 OpenAPI/Swagger filed Apr 25, #46 Completion Webhook filed Apr 26)
**Recent activity:** Two PRs queued to merge: #46 Completion Webhook (fired on simulation completion, Zapier/n8n/Slack-ready, filed today) and #45 OpenAPI 3.1 spec + Swagger UI (`/api/docs`, filed yesterday). PR #44 (MCP Onboarding) merged Apr 24. 1K-stars-by-Apr-30 sprint: 171 needed in 4 days (~43/day needed; +6 stars yesterday — well below pace).

## Ecosystem Context

The past week assembled MiroShark's formal infrastructure layer: graph memory, MCP server, public gallery, social share card, OpenAPI spec, and an outbound webhook. The substrate is documented and machine-readable. Two PRs are queued. The sprint has four days left.

Bankr Terminal v2 cited MiroShark's Aave vulnerability simulation in a 15M-view thread — the strongest external signal in the project's history. It frames MiroShark not as a simulation demo but as an early warning system for protocol risk. That framing lives in a tweet. It doesn't live in the product. There's no badge, no filter, no page that surfaces "simulations that called it" — the credibility moment evaporates when the thread goes cold.

Meanwhile, every completed simulation outputs a static share card. No motion, no thread format, nothing that lands natively on X without a click-through. Animated exports and thread formatters extend the shareable surface from one image to multiple formats — both of which drive higher engagement on the platforms where MiroShark's audience lives.

Four signal threads drive this batch:

- **Credibility surface:** The Bankr citation is a moment that should become a product feature. A "Verified Prediction" annotation layer turns post-hoc external citations into a permanent community gallery surface — every researcher who calls an event early can mark it, and new visitors land on proof that the simulations work.
- **Distribution formats:** The share card is static. A GIF export and a thread formatter extend the distribution surface to formats with higher organic engagement: motion on X/Discord and native multi-tweet posts that require zero blank-page effort.
- **SDK completeness:** PR #45 ships a 1.9K-line OpenAPI spec. The natural downstream is a typed Python client — `pip install miroshark-client` — auto-generated in CI from the spec and published to PyPI on release. Closes the MCP → OpenAPI → Python SDK arc.
- **Causal interpretability:** Director Mode lets operators inject breaking news mid-simulation. The belief chart shows what happened; it doesn't show why. An event overlay connects injected causes to observed belief shifts and gives academic/quant researchers the evidence layer they need to publish about results.

Previously suggested ideas excluded from this batch (last 7 days): SSE Streaming (#1, Apr 24), Simulation Engagement Leaderboard (#2, Apr 24), Completion Webhook (#3, Apr 24 — shipped as PR #46), Discord/Slack Post Button (#4, Apr 24), OpenAPI Docs (#5, Apr 24 — shipped as PR #45), History Search & Tags (#4, Apr 22), Round Scrubber (#1, Apr 20), Collaborative Comments (#4, Apr 20), Config Export/Import (#5, Apr 20). All 5 ideas below are net-new.

---

### 1. Predictive Accuracy Ledger

**Type:** Growth / Feature
**Effort:** Small (hours)
**Impact:** Bankr Terminal v2 cited MiroShark's Aave vulnerability simulation in a 15M-view thread. That citation lives on X and nowhere in the product. A "Verified Prediction" annotation layer lets any user mark a public simulation as having predicted a real event — outcome URL, outcome summary, call/miss/partial label. The gallery shows a "📍 Verified" badge on annotated sims; a `/explore?verified=1` filter narrows to the "hall of accurate calls." For the 1K-star sprint, a `/verified` page full of real-event predictions is the single most compelling link to include in a thread about protocol risk simulation — researchers evaluating the project want to see that it actually works, not just that it can run. Every analyst who publishes early and gets validated is incentivized to keep simulating and marking their calls — a compounding credibility loop that costs nothing to operate.
**How:**
1. Add `POST /api/simulation/:id/outcome` — accepts `{label: "correct" | "incorrect" | "partial", outcome_url, outcome_summary (280 chars max)}`, gated on `is_public=true`. Write to `<sim_dir>/outcome.json`. Add `GET /api/simulation/:id/outcome`. Expose `outcome` field in `_build_gallery_card_payload()` — `null` when absent, full outcome object when set. Add a `?verified=1` filter to `GET /api/simulation/public` that server-side filters to `outcome != null`.
2. In `ExploreView.vue`: render a "📍 Verified" badge on cards where `outcome.label == "correct"`, "⚠️ Called Wrong" for `"incorrect"`, "◑ Partial" for `"partial"`. Add a `Verified` filter chip to the explore page header alongside quality/date chips. In `EmbedDialog.vue` add a "Mark outcome →" section below the gallery block: outcome URL input, 280-char summary textarea, call/miss/partial radio group, Submit button. Show inline confirmation "Outcome saved — your simulation is visible in the Verified filter."
3. Add `GET /verified` route (or `/explore?verified=1` redirect) as a dedicated URL. Include this URL in the README Sharing section and in the `GET /share/:id` landing page footer. This is the link to include in threads about pre-incident simulations; it's the social proof anchor the project has been missing.

---

### 2. Animated GIF Export (Belief Replay)

**Type:** Feature / Growth
**Effort:** Small (hours)
**Impact:** Every completed simulation produces a 1200×630 static share card. There's no animated format. A per-round animated GIF — belief bars shifting across rounds, round counter ticking, scenario header fixed — is a distribution asset that performs differently on X and Discord than a static image: it auto-plays in embed previews, shows the *process* of belief formation, and conveys the story in a format that can't be reduced to a screenshot. Pillow is already pinned (≥12.0, used for share cards); `PIL.Image.save(..., save_all=True, append_images=frames, loop=0, duration=600)` generates animated GIFs natively. Zero new dependencies.
**How:**
1. Add `GET /api/simulation/:id/replay.gif` — reads `trajectory.json` (same source as the belief-evolution chart), extracts `{round, belief_distribution}` per step, generates one 1200×630 Pillow frame per round. Each frame: dark background, scenario title (top, same font/auto-shrink as share card), round label (top-right), three stacked color-fill rectangles (same bullish/neutral/bearish palette, width proportional to distribution), round-progress bar at bottom. Final frame holds for 3× duration. Save via `PIL.Image.save(..., save_all=True, loop=0, duration=600)`. Cache as `<sim_dir>/replay.gif`; regenerate only if `trajectory.json` is newer. Same `is_public` gate as the share-card endpoint.
2. Add "Download as animation" to `EmbedDialog.vue` below the existing "Download PNG" button. Add `downloadReplay()` helper that fetches `/api/simulation/:id/replay.gif` and triggers a browser download (`<a href=blob download="replay.gif">`). Show a loading spinner (GIF generation is 1-3s for a 20-round run). Add a copyable `replay.gif` URL to the share-link section — Discord and Slack auto-play animated GIFs from direct file URLs.
3. On the `GET /share/:id` landing page: add the replay GIF as a lazy-loaded `<img>` below the static card with a "▶ Replay" overlay that removes the lazy guard on click. Add `twitter:image` meta pointing at the GIF URL — X renders animated GIFs as native video in the timeline, which outperforms static images for engagement. This makes every shared simulation a motion asset on X without any extra user action.

---

### 3. "Share as Thread" Formatter

**Type:** Feature / Growth
**Effort:** Small (hours)
**Impact:** The EmbedDialog has a share card, an embed link, and a gallery entry. None of them produce a native X thread. A "Share as thread" formatter auto-writes a 5-tweet copy block from simulation data — no API keys, no OAuth, pure clipboard text. Tweet 1: scenario + hook + final consensus split. Tweet 2: belief journey (start → peak → settle with net shift). Tweet 3: most influential agent name + stance + one-line thesis excerpt. Tweet 4: one key diagnostic insight (e.g. "High echo-chamber risk: 3 influencers drove 78% of belief formation"). Tweet 5: share link + "Fork this →" CTA. For the sprint, this is a distribution multiplier: researchers who run a simulation on a real protocol risk or token event want to post about it immediately — the formatter removes the blank-page problem and guarantees the share card unfurls on tweet 5. Five posts per published simulation at zero marginal effort.
**How:**
1. Add `GET /api/simulation/:id/thread-text` — reads `simulation_config.json` (scenario), `quality.json` (quality health, engagement rate), `trajectory.json` (final belief distribution, per-round array for trend, top agent by delta from final round). Builds `{tweets: string[5], share_url, scenario_excerpt}`. Tweet 1: scenario headline (≤180 chars) + hook + "🔵 Bullish X% | ⚪ Neutral Y% | 🔴 Bearish Z%". Tweet 2: "Started 33/33/33 → peaked at [bull]% bullish in round N → settled [bull]/[neutral]/[bear] — [net]% net belief shift." Tweet 3: top agent (highest |delta_final_bullish| from trajectory last-round agent list), name + stance + first 120 chars of their last post. Tweet 4: one diagnostic insight from `quality.json` (echo-chamber index if high, low participation if notable, or quality health + score). Tweet 5: share link + "Fork this →". No new deps.
2. In `EmbedDialog.vue` add a "📝 Share as thread" section. On expand: five numbered `<pre>` blocks (same dark style as the MCP snippet block). "Copy all 5 tweets" copies the full thread as a newline-separated string. Per-tweet "Copy" micro-buttons for users who prefer to paste tweet-by-tweet. Small spinner on first fetch; cache in component state so re-opens don't re-fetch.
3. Add a "📝 Thread it →" button to the `GET /share/:id` landing page that toggles the 5-tweet block visible — accessible to users who receive a share link without opening the app. Log thread copy events (increment `thread_copy_count` in `<sim_dir>/state.json`) so the copy count is available for future leaderboard scoring.

---

### 4. Python Client SDK via openapi-generator CI

**Type:** Integration / Community
**Effort:** Small (hours)
**Impact:** PR #45 ships a 1.9K-line OpenAPI 3.1 spec over ~85 endpoints. The downstream deliverable for any published spec is a typed client library: `pip install miroshark-client`, then `from miroshark_client import SimulationApi`. `openapi-generator-cli` (Docker image, no install needed) produces a full Python client from `openapi.yaml` in one command. A CI job that re-generates `sdk/python/` whenever the spec changes keeps the SDK in sync automatically. Publishing to PyPI on release creates a new discovery channel: researchers searching for "simulation API" or "swarm intelligence client" on PyPI and in Jupyter ecosystem listings. Closes the MCP → OpenAPI → Python SDK arc: AI IDE clients connect via MCP, direct REST users browse Swagger UI, Python researchers `pip install`. Each surface catches a different audience.
**How:**
1. Add `.github/workflows/sdk-gen.yml` — triggers on `push` to main when `backend/openapi.yaml` changed (path filter). Single job: pull `openapitools/openapi-generator-cli:v7.6.0`, run `generate -i backend/openapi.yaml -g python -o sdk/python --additional-properties=packageName=miroshark_client,packageVersion=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.1.0"),projectName=miroshark-client`. Commit `sdk/python/` back to main only when files changed (`git diff --quiet sdk/python/ || git commit -m "chore(sdk): regenerate Python client"`). Add `sdk/python/` to `.gitignore` on non-main branches so only main carries the committed tree.
2. Customize the generated `sdk/python/README.md` with a MiroShark-branded header and a Jupyter usage block: `import miroshark_client; cfg = miroshark_client.Configuration(host="http://localhost:5001"); api = miroshark_client.SimulationApi(miroshark_client.ApiClient(cfg)); resp = api.start_simulation(...)`. Add `sdk/python/pyproject.toml` with `name = "miroshark-client"`, a placeholder version, and `pip publish` metadata. Add `.github/workflows/publish-sdk.yml` triggering on release tags (`v*`): bumps version from tag and runs `pip publish` using stored PyPI token secret.
3. Add a "Python SDK" row to the README Documentation table: `| [Python SDK](sdk/python/) | \`pip install miroshark-client\` — generated from the OpenAPI spec |`. Add a PyPI badge once the first release publishes. Submit `miroshark-client` as an entry in the `openapi-generator` community showcase (one markdown PR to their repo). The package name `miroshark-client` is available on PyPI; reserving it signals production intent.

---

### 5. Director Event Overlay on Belief Chart

**Type:** Feature / DX
**Effort:** Small (hours)
**Impact:** Director Mode lets operators inject breaking news mid-simulation — one of MiroShark's most distinctive capabilities. The belief-evolution chart doesn't show the injections: a researcher sees belief shifts without knowing which were triggered by a director event and which were organic. Vertical dashed lines at injection rounds with hover-tooltip labels close this interpretability gap. The data already exists (`trajectory.json` stores director events with round numbers and labels); this is a frontend overlay on the existing chart. It transforms Director Mode from a runtime tool into an analytics tool — researchers can argue causally: "the 23-point bearish shift in round 12 was triggered by the Fed rate announcement." This is the evidence layer the academic/quant audience scans for when evaluating MiroShark's model validity.
**How:**
1. Add `GET /api/simulation/:id/events` — reads `trajectory.json` (or `state.json`) and returns `{events: [{round: int, label: string, type: "director" | "counterfactual"}]}` sorted by round. Returns empty array (not 404) when no events. Read-only, no new state required — events are already in the trajectory.
2. In `SimulationView.vue`: after trajectory data loads, fetch `/api/simulation/:id/events`. For each event, inject a vertical annotation into the existing belief-evolution chart at the corresponding round: dashed amber line (`borderColor: "#f59e0b"`, `borderDash: [4,4]`) with a label at the top showing the event headline (truncated to 40 chars + "…"). Use Chart.js `annotation` plugin (if already bundled) or a CSS `position: absolute` overlay positioned by the chart's x-axis scale. On hover: tooltip showing full event label + round number + approximate belief delta (`avg(belief[round+1..round+3]) − belief[round-1]` expressed as "⬆ +12% bullish").
3. Add an "Events" panel below the belief chart (collapsed by default, toggled by "▾ N director events" link). Timeline list: round number, event label, computed belief attribution (e.g. "⬆ +19% bullish in rounds 8–11"). Export this panel's content as an additional section in the existing article generation prompt — events with their attributed belief changes are the strongest causal evidence to include in a written analysis. Wire to the PDF report flow when that ships (Apr 18 idea, still unbuilt).

---

## Selection Rationale

Today's batch addresses the gap between "infrastructure complete" and "infrastructure that tells its own story":

- **Predictive Accuracy Ledger** (#1) — The Bankr citation is a live signal with no product home. A `/verified` gallery turns one tweet into a permanent credibility surface. For the sprint, it's the most compelling page to link from X threads about protocol risk.
- **Animated GIF Export** (#2) — Zero new dependencies (Pillow already in stack). Motion outperforms static on X/Discord. Every share becomes a 40-round animation instead of a frozen card.
- **Thread Formatter** (#3) — Removes the blank-page problem for every researcher who wants to post about their simulation results. Five tweets per published sim at zero marginal effort. Share card unfurls on tweet 5 automatically.
- **Python SDK** (#4) — Closes the MCP → OpenAPI → Python SDK arc that PR #45 opened. New discovery channel (PyPI, Jupyter ecosystem). `pip install miroshark-client` in a notebook is the path the quant audience prefers over a browser.
- **Director Event Overlay** (#5) — Makes Director Mode's causal story visible on the chart. The evidence layer academic/quant researchers need to publish about simulation results. Purely additive frontend change over existing trajectory data.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, all required data already in the codebase, no ambiguous design decisions, no external approvals needed.
