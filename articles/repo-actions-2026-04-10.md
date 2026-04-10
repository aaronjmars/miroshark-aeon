# Repo Action Ideas — 2026-04-10

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 639 stars · 115 forks · 3 contributors · 2 open issues · 2 open PRs (history search/filter #20, CLI/TUI #community)
**Recent activity:** Simulation Fork (#17) merged, Simulation History Search & Filter (#20) open (Aeon-built today), community-contributed full CLI/TUI layer (open PR `feature/cli-tui-upstream`), unified observability system landed (LLM tracing, agent decisions, SSE debug panel), performance overhaul (NER 2x, graph build 2x, gzip).

## Ecosystem Context

MiroShark enters its third week at 639 stars with a rich feature core — export, replay, templates, network viz, MCP server, cloud deploy, LLM selector, fork/branch, comparison mode, share permalink, and now an observability system that captures every LLM call and agent decision. The community CLI/TUI PR shows that external contributors are starting to extend the project independently — a sign that the codebase is mature enough to attract real ecosystem development.

The next 361 stars to 1000 require a different growth model. The quick virality wins (share permalink, comparison mode) are shipped. What's left is the stack that earns *durable* interest: research credibility, feedback loops that make simulations more useful over time, and positioning MiroShark as a platform that generates publishable outputs — not just a demo tool.

Key signals driving this batch:

- **Observability data is untapped:** The new LLM tracing system captures every agent decision with its reasoning chain. This data currently lives in a debug panel that only developers open. Surfacing it to non-technical users as "why did this agent change their position?" would make simulations explainable — a hard requirement for research use and for anyone trying to understand a counterintuitive result.
- **Prediction markets never close:** MiroShark generates Polymarket-style prediction markets but never records whether the prediction came true. Without a resolution system, every simulation is a one-way hypothesis — interesting but not verifiable. Closing this loop creates a compounding accuracy record that positions MiroShark as a genuine forecasting tool.
- **Blog post barrier:** The internal ReACT report writer produces analytical breakdowns for simulation owners. But users who want to post about their simulation results on X, Substack, or Medium still have to manually synthesize the results into a shareable narrative. A "Generate Article" button that produces a 400-word publishable brief is the missing bridge between simulation result and social content.
- **Chinese-origin, global audience gap:** MiroShark forked from MiroFish, a Chinese project with existing Chinese-language community interest. The codebase currently assumes English-only document input. Supporting CJK document input natively would unlock a large untapped audience and align with the project's roots.
- **OG image is generic:** Every shared simulation at `/share/:token` currently uses a generic OG image. Social platform previews showing the simulation's actual market price outcome and scenario title as a generated image would significantly increase click-through rates on shared links — the difference between a preview that says "MiroShark" and one that says "EU AI Act Simulation: 78% agents voted AGAINST adoption."

These 5 ideas are distinct from all previously generated ideas (webhooks, A/B testing, embeddable widget, replay ✓, gallery, WebSocket streaming, snapshot sharing, prompt scoring, doc preprocessing, benchmarking, network viz ✓, REST API, multi-document comparison, Discord bot, belief analytics, MCP server ✓, demographic calibration, CLI runner [community PR open], simulation cost estimator, URL ingestion ✓, one-click deploy ✓, template saver, multi-prediction market, influence leaderboard ✓, agent memory inspector, config timeout recovery ✓, LLM selector ✓, agent bulk import, statistical aggregation, simulation comparison ✓, fork/branch ✓, share permalink ✓, history search ✓) and from both open PRs (#20 history search, CLI/TUI community PR).

---

### 1. Prediction Resolution & Accuracy Tracking

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** MiroShark generates prediction market consensus ("78% agents expect the EU AI Act to pass"), but never records whether the real-world outcome matched. Without resolution, every simulation is a one-way artifact — interesting, but not verifiable and not comparable to other forecasting tools. A "Resolve" button on completed simulations lets users record the actual binary outcome (YES/NO) or final price. The system then calculates prediction accuracy: did the agent consensus call the direction correctly? Over time, users accumulate an accuracy track record per scenario domain — "tech policy simulations: 71% accurate, 12 resolutions." This positions MiroShark alongside Metaculus and Polymarket as a legitimate forecasting tool with a verifiable track record, not just a simulation sandbox. Resolved simulations with accurate predictions become powerful testimonials.
**How:**
1. Add a `resolution` object to the simulation model: `{ actual_outcome: "YES"|"NO"|null, resolved_at: ISO8601, resolved_by: "user", accuracy_score: 0.0–1.0 }`. Add a "Resolve Prediction" button on the completed simulation results page that opens a modal with two buttons (YES/NO outcome) and an optional notes field. On submit, `PATCH /api/simulation/:id/resolve` stores the resolution and computes `accuracy_score` = 1.0 if agent consensus matched outcome, 0.5 if split, 0.0 if wrong.
2. Display resolution status in the simulation history card: an unresolved badge ("⏳ Awaiting outcome") and a resolved badge with accuracy indicator ("✓ Correct — 78% confident" or "✗ Incorrect — 72% confident"). Add an "Accuracy" column to the history sort options so users can surface their best-performing simulations.
3. Add a "Track Record" summary card at the top of the history page showing aggregate stats: total resolved simulations, overall accuracy %, most accurate domain, longest correct streak. Surface the same data on the public share page for resolved simulations so viewers can see whether the prediction came true.

---

### 2. One-Click Article Generator from Simulation Results

**Type:** Feature / Content
**Effort:** Small (hours)
**Impact:** The internal ReACT report writer produces analytical deep-dives for simulation owners. But users who want to post about results on X, Substack, or Medium still manually synthesize findings into a shareable narrative — a process that kills the impulse to share. A "Generate Article" button produces a 400-600 word publishable brief: abstract (what was simulated and why), key findings (top agent behaviors, market outcome, sentiment shift), implications, and a caveats paragraph. The output is in clean Markdown, ready to paste anywhere. This turns every simulation into a content asset and removes the last friction point between "cool result" and "tweetable story." Every published article that links back to a MiroShark share page is a backlink and acquisition event.
**How:**
1. Add a "Generate Article" button to the simulation results view (next to the existing "Share" and export controls). On click, call `POST /api/simulation/:id/article` which assembles context — scenario question, top 5 timeline entries, final market price, top 3 influence leaders with their stance trajectory, agent count, round count — and sends it to the LLM with a prompt: "Write a 400-600 word simulation study brief in the style of a Substack post. Include: one-sentence abstract, 3 bullet-point findings with specific agent quotes from the timeline, one paragraph on market dynamics, one paragraph on implications, one 2-sentence caveat on AI simulation limitations. End with a call to action linking to [share_url]."
2. Render the output in a slide-out drawer with a Markdown preview panel, a "Copy to clipboard" button, and a "Download as .md" button. Cache the generated text in `simulation.generated_article` so re-opening the drawer doesn't re-call the LLM.
3. If a share permalink exists for the simulation, automatically append it to the generated article's call-to-action paragraph. If not, show a "Create shareable link first" nudge button that runs the share flow and then resumes article generation.

---

### 3. Agent Decision Trace Viewer

**Type:** DX Improvement
**Effort:** Medium (1–2 days)
**Impact:** The new observability system (landed in `93698f8`) captures full LLM traces and agent decision data in the SSE debug panel. This data is only accessible to developers who know to open the debug panel during a live simulation run. Surfacing it as a click-through from the influence leaderboard would make simulations *explainable* to non-technical users: "Why did Agent #12 flip from bullish to bearish in round 4?" Explainability is a hard requirement for research use — any simulation that could appear in a paper needs an auditable reasoning chain. It also makes simulations more engaging for general users: the leaderboard becomes a launchpad for story-finding, not just a ranking table.
**How:**
1. Add a click handler to each agent row in the influence leaderboard. Clicking opens a slide-out panel showing that agent's round-by-round decision log: round number, platform (Twitter/Reddit/Polymarket), action taken (post/trade/wait), position before/after, and a "Reasoning" excerpt (first 200 chars of the LLM trace for that agent's decision in that round). Highlight rows where the agent's `stance` changed by more than 0.3 (a "flip" event) with an amber indicator.
2. Source the data from the existing observability trace logs stored during simulation. Add a `GET /api/simulation/:id/agents/:agent_id/trace` endpoint that queries the observability store and returns the structured decision log array. If trace data isn't available for older simulations (pre-observability), show a graceful "Trace data not available for this simulation" state.
3. Add a "Position over time" sparkline at the top of the trace panel showing the agent's `stance` value (–1 to +1) across all rounds as a small line chart. Add a "Download trace JSON" button for researchers who want the raw data.

---

### 4. Multi-Language Document Input

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** MiroShark forked from MiroFish, a Chinese AI project with existing Chinese-language community interest. The codebase currently assumes English-only document input — NER prompts, entity descriptions, and persona generation are English-first. Supporting Chinese, Japanese, and Korean document input natively would unlock a large untapped audience that already knows MiroFish but hasn't adopted MiroShark. At 639 stars, the English-speaking AI audience is well-seeded; CJK language support is the highest-leverage geographic expansion available. It also aligns with the "universal" in "Universal Swarm Intelligence Engine" — a simulator that can only process English documents isn't universal.
**How:**
1. Add language detection to the document ingestion pipeline using `langdetect` (pure Python, no API calls). When a document is submitted, detect its primary language and store it as `simulation.document_language` (ISO 639-1 code: `en`, `zh`, `ja`, `ko`). Pass the detected language to all downstream LLM prompts via a `language_instruction` variable: "Generate all output in {language}. Use culturally appropriate names and contexts for that language region."
2. Update the NER extraction prompts in the graph-build phase to include the language hint. Update the persona generation prompts to generate agent names, backgrounds, and social media post styles appropriate to the detected language region (e.g., Chinese agents post on Weibo-style platforms, use Chinese naming conventions). The simulation output (posts, comments, market commentary) is generated in the document's language.
3. Add a language indicator chip to the simulation setup form — "Auto-detected: Chinese (Simplified)" — with a manual override dropdown for edge cases. Add a language badge to history cards and share pages. Update the README with a section on multi-language support, explicitly calling out Chinese/Japanese/Korean support to surface in search results from those communities.

---

### 5. Custom OG Image for Simulation Share Pages

**Type:** Growth
**Effort:** Small (hours)
**Impact:** Every simulation shared via the `/share/:token` public permalink currently generates a social media preview with a generic MiroShark header image. A custom OG image dynamically generated per simulation — showing the scenario title, final market price bar, and a "N agents · M rounds" stat — would dramatically increase click-through rates when shared on X, LinkedIn, and Discord. Social platform previews are the first impression for 80% of link visitors; a preview that shows "EU AI Act: 78% YES" beats one that shows a logo every time. This is zero-cost-per-share growth leverage: every shared link becomes better marketing. The same image can be used as the simulation thumbnail in the history grid.
**How:**
1. Create a `GET /api/simulation/:id/og-image` endpoint that generates a PNG using Python's `Pillow` library. The image template (1200×630px) includes: MiroShark logo (top-left, small), scenario title (large text, max 2 lines), final market price as a horizontal bar (YES% in teal, NO% in coral), agent count and round count in small text (bottom-left), and "miroshark.io" branding (bottom-right). Use a clean sans-serif font bundled with the repo (Inter or similar from Google Fonts, downloaded once to `assets/`). Cache the generated PNG in `backend/static/og/` keyed by simulation ID — regenerate only if the simulation has new data.
2. Update `ShareView.vue` to set the `og:image` meta tag to `/api/simulation/:id/og-image` (using the simulation ID from the share token lookup). Also update the `twitter:card` meta to `summary_large_image` and `twitter:image` to the same endpoint, so both X and LinkedIn previews show the custom image.
3. Add a "Copy image" button to the share page that fetches the OG image and copies it to the clipboard — so users can paste it directly into tweets or Discord messages without needing to screenshot the UI. This makes the image a shareable asset in its own right, not just a link preview.

---

## Selection Rationale

This batch targets MiroShark's maturity phase — the features that convert a strong demo into a durable platform:

- **Feedback loops** (#1) — Prediction resolution is the single feature that makes MiroShark's outputs *verifiable*. Without it, every simulation is an assertion; with it, they're hypotheses with a track record.
- **Content flywheel** (#2) — The article generator removes the last friction point between "good result" and "shared story." Every article that cites a MiroShark simulation is an acquisition event.
- **Explainability** (#3) — Research use requires auditable reasoning chains. The observability system already captures this data; surfacing it in the UI unlocks the academic citation pathway.
- **Geographic expansion** (#4) — CJK language support is the highest-leverage untapped audience for a project with Chinese roots. One README line about Chinese language support could generate significant inbound interest.
- **Social distribution** (#5) — Custom OG images make every shared simulation link look credible and click-worthy. This compounds every growth action taken by share permalink, article generator, and prediction resolution.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, no ambiguous design decisions, no external approvals needed.
