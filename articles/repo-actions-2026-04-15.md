# Repo Action Ideas — 2026-04-15

**Repo:** [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Snapshot:** 692 stars · 132 forks · 3 contributors · 0 open issues · 0 open PRs
**Recent activity:** Browser push notifications (PR #30, merged Apr 15), post-simulation trace interview (PR #26, merged), article generator (PR #25), belief drift chart (PR #23), prediction resolution & accuracy tracking (PR #22). Token: new ATH $0.000003815 on Apr 14; cooling to $0.000002666 (-15% 24h) with continued buy-side dominance.

## Ecosystem Context

MiroShark enters its fourth week of sustained development with a feature stack that's now legitimately research-grade: multi-platform cross-pollination engine, observability system, fork/branch, comparison mode, share permalink, history search, prediction resolution, belief drift visualization, one-click article generation, trace-grounded agent interview, and — as of today — browser push notifications for cloud-deploy users. At 692 stars (+14 overnight), the project has settled into a steady 10–15 star/day growth rhythm that isn't driven by any single viral moment — it's compounding reputation.

The gaps that matter now are about **depth over breadth**. The simulation engine produces rich per-round data; the analysis layer (belief drift, leaderboard, article generator) consumes it. But two wedges are still open: **experimental control** (researchers need to perturb running simulations and observe the effect, not just compare two static runs) and **infrastructure resilience** (a crashed 15-minute cloud simulation loses all progress and all API spend). And two growth levers remain untouched: **open-model support** (HuggingFace Inference API would remove API cost as a barrier entirely) and **passive distribution** (an RSS feed turns every completed simulation into a content event that aggregators can pick up without any UI interaction).

Key signals driving this batch:

- **Exogenous shock modeling is the missing research primitive:** Every simulation in MiroShark describes a single-track counterfactual — "what do agents say about document X over N rounds?" But the most interesting research questions involve mid-stream disruptions: "what happens to an EU AI Act debate when the news breaks that three MEPs reversed their vote in round 5?" Director Mode (mid-simulation event injection) is how computational social science answers this. OASIS, SOTOPIA, and Park et al. all include external stimulus injection as a core experimental mechanism. MiroShark's async architecture (asyncio.gather per round) makes this implementable at the round boundary without touching the simulation core — inject into the shared round context after round N commits, before round N+1 dispatches.

- **Cloud simulations die silently:** A 50-agent, 15-round simulation on Railway/Render takes 8–15 minutes. Network hiccups, Railway container restarts, or tab abandonment can kill a run mid-way. Currently the only recovery is restart — losing 50%+ of API spend and all intermediate analysis. A checkpoint file written after each round costs one JSON write; a resume path restarts from round 11 instead of round 1. For users paying $0.10–$0.30 per full run on GPT-4o, this is material. For researchers running 10-round batches, it's essential reliability.

- **API cost is the single biggest adoption barrier:** The LLM selector (PR #12) already lets users choose OpenAI, Anthropic, or Ollama (local). But users who want open-source model performance without local GPU setup are stuck — they can pay $12+ per full 50-agent GPT-4o run or self-host with Ollama. HuggingFace Inference API offers GPU-backed open model inference (Llama 3.3 70B, Mistral 7B, Qwen 2.5 72B) at ~$0.001/1K tokens — roughly 10–15x cheaper than GPT-4o. The Inference API is OpenAI-compatible (same REST interface, different base URL), meaning the entire integration is a new provider branch in the existing switch — no new HTTP client code. Academic users — the fastest-growing segment at 692 stars — disproportionately prefer open-source models for reproducibility and cost.

- **Agent subgroup behavior is invisible:** The belief drift chart shows aggregate stance over time; the leaderboard shows per-agent influence. But neither answers "did the age-35-54 cohort behave differently from the 18-24 cohort?" or "did Reddit agents flip before Twitter agents?" Agent personas carry demographic attributes (age range, region, platform primary, archetype type) — data that's already generated but never cross-tabbed against simulation outcomes. A demographic breakdown panel requires no new data collection; it's a new lens on data that already exists.

- **Cloud instances produce output with no subscribers:** Teams using cloud-deployed MiroShark instances want to be notified when simulations complete without monitoring a browser tab. Browser push (PR #30) solves this for the tab owner. But what about teammates, RSS readers, or automated pipelines that want to consume completed simulation metadata? An RSS/Atom feed at `/feed.xml` turns every completed simulation into a published event — subscribable from Feedly, n8n, Zapier, or a custom cron job. This is the universal no-auth integration layer.

These 5 ideas are distinct from all previously generated ideas in the past 7 days (statistical batch runs, Jupyter export, REST API + webhook, Hall of Fame, Polymarket seeding, community template gallery, polarization index, agent decision trace viewer, multi-language input, custom OG image) and from 0 open PRs.

---

### 1. Mid-Simulation Event Injection (Director Mode)

**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** MiroShark runs single-track simulations — agents respond to the uploaded document over N rounds without any external disruption. But the most research-valuable question is about perturbation: "how does this debate change when breaking news drops in round 5?" Director Mode lets users pause a running simulation at any round boundary, type a one-sentence event ("Central bank unexpectedly raised rates by 100bps"), and inject it into the next round's shared context. All agents receive the event as a new data point before generating their round N+1 actions. The belief drift chart marks the injection round with a vertical line. This is the experimental primitive that transforms MiroShark from "here's what agents say about document X" into "here's what agents say about document X when Y happens at round N" — the most powerful framing for research applications and the clearest differentiator from every other multi-agent simulation tool in the space.
**How:**
1. Add an "Inject Event" button to the simulation UI, visible only during an active run (status = `"running"`). The button is disabled until the current round fully commits. On click, open a compact overlay: a single text field ("Describe the event...") with a submit button. On submit, `POST /api/simulation/:id/inject-event` with `{ round: <current_round>, event_text: "..." }`. The backend writes the event to `<sim_dir>/context/events.json` and sets a `pending_injection: true` flag on the simulation record. The simulation runner reads this flag before dispatching round N+1 — if set, prepends the event text to each agent's round context prompt as "BREAKING: {event_text}" and clears the flag.
2. Display injected events in the simulation feed as a distinct event card (horizontal divider with event text, timestamp, and round number). Add them to the belief drift chart as vertical dashed lines with a hover tooltip showing the event text. Include injected events in the `GET /api/simulation/:id` response as an `events` array so they appear on the share page and in the article generator context.
3. Allow up to 3 event injections per simulation. After 3, grey the button with "Max events reached." Add a "Previous events" expandable list below the inject button showing all events fired in the current run. When the simulation completes, include event injection details in the downloadable artifact list so researchers can fully reproduce the experimental setup.

---

### 2. HuggingFace Inference API as LLM Provider

**Type:** Integration
**Effort:** Small (hours)
**Impact:** The existing LLM selector (PR #12) offers OpenAI, Anthropic, and Ollama (local). Users who want open-source model performance without local GPU setup are stuck — they can pay $12+ per full 50-agent GPT-4o run or self-host with Ollama. HuggingFace Inference API offers GPU-backed open model inference (Llama 3.3 70B, Mistral 7B, Qwen 2.5 72B) at ~$0.001/1K tokens — roughly 10–15x cheaper than GPT-4o. For a 50-agent, 10-round simulation, that's $0.80 vs. $12. The Inference API is OpenAI-compatible (same REST interface, different base URL + token format), meaning the integration is: add a new provider enum, update the base URL, and populate the model dropdown. No new HTTP client code. Academic users — the fastest-growing segment at 692 stars — disproportionately prefer open-source models for reproducibility and cost. This also makes MiroShark accessible to international researchers who can't easily pay for commercial API access.
**How:**
1. Add `"huggingface"` to the provider enum in the backend's LLM client. When `provider == "huggingface"`, set `base_url = "https://api-inference.huggingface.co/v1"`, use the `api_key` field as the `Authorization: Bearer {HF_TOKEN}` header, and use the standard OpenAI-format chat completions endpoint. The model name is passed directly (e.g., `"meta-llama/Llama-3.3-70B-Instruct"`). No new HTTP client needed — just a new branch in the existing provider switch.
2. Update `ProviderSettings.vue` in the LLM selector: add "HuggingFace" to the provider dropdown. When selected, show the API key field labeled "HuggingFace Token" (with a link to hf.co/settings/tokens for new users), and replace the model dropdown options with: `meta-llama/Llama-3.3-70B-Instruct`, `mistralai/Mistral-7B-Instruct-v0.3`, `Qwen/Qwen2.5-72B-Instruct`, `microsoft/Phi-3-mini-4k-instruct`, `google/gemma-2-9b-it`. The "Test Connection" button (already wired in the UI) validates the token by sending a ping prompt.
3. Add a "Cost note" below the HuggingFace provider selector: "HuggingFace serverless inference is ~10x cheaper than GPT-4o for most simulation workloads. Free tier available for lower traffic." Update the README LLM Providers table to add a HuggingFace row with cost comparison.

---

### 3. Simulation Checkpoint & Resume

**Type:** DX Improvement
**Effort:** Medium (1–2 days)
**Impact:** Long-running cloud simulations (50 agents, 15 rounds, GPT-4o) take 8–15 minutes and cost $0.10–$0.30 per full run. Network instability, Railway/Render container restarts, or browser-forced unloads can kill a simulation mid-run. Currently the only recovery is restart — losing all intermediate state, all generated posts, all belief state evolution, and all API spend from completed rounds. A checkpoint file written after each round (one JSON write per round = negligible overhead) enables resume from round N+1 rather than round 1. For users running expensive 200-agent experiments or researchers who deliberately pause to inject an event (Director Mode, idea #1), checkpoint/resume is the reliability primitive that makes long-form simulation trustworthy.
**How:**
1. After each round completes in `simulation_runner.py`, write a checkpoint file to `<sim_dir>/checkpoint.json`: `{ "last_completed_round": N, "agent_belief_states": {...}, "market_state": {...}, "round_memory": {...}, "events_injected": [...] }`. The write is atomic (write to `checkpoint.tmp`, then rename to `checkpoint.json`) to prevent corrupted checkpoints from a mid-write crash. Add a `checkpoint_at` field to the simulation metadata (ISO8601 timestamp of last checkpoint write).
2. Add a `POST /api/simulation/:id/resume` endpoint. It reads `checkpoint.json`, validates the simulation is in `"interrupted"` status (set automatically when the simulation runner detects an unclean exit — SIGTERM or process death without normal completion), restores agent belief states and market state from the checkpoint, and re-queues the simulation runner starting at `last_completed_round + 1`. In the frontend, show a "Resume" button on interrupted simulation cards in the history view alongside the existing "Fork" button.
3. Add `status: "interrupted"` to the simulation state machine (alongside `pending`, `running`, `completed`, `failed`). The simulation runner writes `"interrupted"` on SIGTERM. A startup health check scans for simulations stuck in `"running"` status at startup (unclean shutdown) and transitions them to `"interrupted"`. Add an "Auto-resume" toggle in Settings: when enabled, the backend automatically resumes interrupted simulations at startup.

---

### 4. Agent Demographic Breakdown Panel

**Type:** Feature
**Effort:** Small (hours)
**Impact:** The influence leaderboard ranks agents by interaction volume; the belief drift chart shows aggregate stance over time. Neither answers the subgroup question: "Did institutional actors behave differently from individuals? Did Twitter-primary agents flip before Reddit-primary agents? Were younger archetypes more volatile?" This data already exists — agent personas carry `age_range`, `region`, `platform_primary`, and `archetype_type` (individual vs. institutional) attributes generated during the graph build phase. A Demographic Breakdown panel cross-tabs these dimensions against final stance, stance change magnitude, and trading behavior. Output: "Institutional agents held more stable positions (avg stance delta 0.12) vs. individuals (0.31); Twitter-primary agents reversed consensus 1.4 rounds earlier than Reddit-primary agents." These are the subgroup effects that social science papers report. No new data collection — it's a new analytics lens on existing persona JSON.
**How:**
1. Add a `GET /api/simulation/:id/demographic-breakdown` endpoint that reads all agent persona JSON files for the simulation, extracts the 4 demographic dimensions, and cross-tabs each against: `final_stance` (mean and std), `stance_delta` (|final - initial|, a volatility measure), and `trade_count` (from Polymarket data). Return: `{ by_age_range: { "18-24": { count, final_stance_mean, stance_volatility, ... }, ... }, by_region: {...}, by_platform: {...}, by_type: {...} }`. Store the result in `<sim_dir>/demographics.json` to cache subsequent fetches.
2. Add a "Demographics" tab to the simulation results view (alongside "Belief Drift" and "Influence Leaderboard"). Render 4 horizontal bar chart groups — one per dimension — each showing segments ranked by `final_stance_mean`. Bars are colored by stance (teal = bullish, slate = neutral, coral = bearish) with error bars for std dev. Below each chart, add a plain-text callout for the largest subgroup divergence: "Twitter-primary agents were 0.38 more bullish than Reddit-primary agents on average."
3. Add a "Breakdown" section to the article generator prompt — inject the top 2 demographic divergence findings as "Key subgroup dynamics:" bullet points in the generated article. Include the most notable finding as a `demographic_headline` field in the `GET /api/simulation/:id` response so the share page can surface it as a subtitle.

---

### 5. RSS/Atom Feed for Completed Simulations

**Type:** Integration / Growth
**Effort:** Small (hours)
**Impact:** Browser push notifications (PR #30) alert the simulation owner in-browser. But teams using cloud MiroShark instances want teammates, RSS readers, and downstream automation to consume completed simulations without opening a browser tab. An RSS/Atom feed at `/feed.xml` publishes completed simulations as feed entries: title (scenario text), description (final market price, top agent, agent count, rounds), and link (public share permalink or history URL). Teams subscribe in Slack (via RSS app), Feedly, or n8n and get a new entry every time a simulation completes. Automated pipelines can trigger on new feed entries — "when a simulation completes with >60% YES, post to Discord." This is the universal no-auth integration layer: zero setup for the publisher, zero friction for the subscriber.
**How:**
1. Add a `GET /feed.xml` route that returns a valid Atom feed (RFC 4287) using Python's `feedgen` library (`pip install feedgen`, zero external API calls). Feed title: "MiroShark Simulations" (or the hostname for named instances). Each entry: `<title>` is the scenario text (truncated to 100 chars), `<summary>` is "N agents · M rounds · Final YES: P% · Top agent: {name}", `<link>` is the share permalink (if share token exists) or the instance history URL, `<updated>` is the completion timestamp. Include the last 20 completed simulations. Serve with `Content-Type: application/atom+xml`.
2. Add a "Subscribe" button to the simulation history header that copies the feed URL (`{instance_url}/feed.xml`) to clipboard. Add a small RSS icon in the site header that links to `/feed.xml` directly. Add `<link rel="alternate" type="application/atom+xml" href="/feed.xml">` to the main HTML `<head>` for standard feed autodiscovery.
3. Add a `/feed.xml` entry to the README under a new "Integrations" section: "MiroShark publishes an Atom feed of completed simulations at `/feed.xml`. Subscribe in Feedly, n8n, Zapier, or any RSS reader." Include a sample n8n workflow JSON snippet (in a collapsible `<details>` block) that triggers on new feed entries and posts to a Discord channel — the concrete integration example that turns a footnote into a developer feature.

---

## Selection Rationale

This batch targets MiroShark's maturation from a single-user demo tool to a resilient, multi-integration research platform:

- **Director Mode** (#1) — The experimental control primitive that unlocks MiroShark for serious research. Every computational social science paper needs stimulus injection; now MiroShark can do it without restarting from scratch.
- **HuggingFace provider** (#2) — Removes API cost as the primary adoption barrier. A 10–15x cost reduction on open models opens MiroShark to academic users and batch-heavy workflows that GPT-4o pricing rules out.
- **Checkpoint & resume** (#3) — Reliability infrastructure for long-running cloud simulations. One JSON write per round; resume from round N+1 instead of round 1. Reduces wasted API spend and makes crash recovery a first-class feature.
- **Demographic breakdown** (#4) — A new analytics lens on existing data. No new data collection; subgroup analysis from persona attributes already generated during graph build. Adds a publishable figure to every simulation result.
- **RSS feed** (#5) — The universal no-auth integration layer. Teams subscribe and receive completed simulation events in Slack, Feedly, or n8n without touching the UI. Compounds every share mechanism already built.

Each idea is scoped for autonomous implementation by the `feature` skill — clear inputs/outputs, no ambiguous design decisions, no external approvals needed.
