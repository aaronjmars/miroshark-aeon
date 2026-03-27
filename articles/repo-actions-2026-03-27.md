# Repo Action Ideas — 2026-03-27

Generated from analysis of **aaronjmars/MiroShark** (288 stars, 47 forks, Python/TypeScript) and the broader multi-agent simulation ecosystem.

**Current state:** MiroShark has had an intense two weeks of development — cross-platform simulation engine (Twitter + Reddit + Polymarket running simultaneously), round memory with sliding-window compaction, belief state tracking, web enrichment for personas, batched Neo4j writes for 10x performance, and Claude Code as an LLM provider option. The project is a fully English, local-first fork of MiroFish (33k stars) that replaces Zep Cloud with Neo4j + Ollama. There's one open PR (simulation data export to JSON/CSV) and zero open issues.

**Ecosystem context:** MiroFish topped GitHub's global trending list in March 2026 and secured $4M in 24 hours. Competitors include AgentSociety (academic, 10k agents), OASIS/CAMEL-AI (the underlying framework MiroFish uses), and MiroFish-Offline. The multi-agent simulation space is white-hot — Gartner reports a 1,445% surge in multi-agent system inquiries. MiroShark's differentiators are: English-first, local-first (no Zep Cloud dependency), three-platform simultaneous simulation, Polymarket integration, and flexible LLM provider support.

---

### 1. Simulation Replay & Timeline Viewer
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Makes simulations shareable and reviewable — users can scrub through rounds, see how opinions shifted, which posts went viral, and how market prices moved. This is the "killer demo" feature that turns a one-time run into a persistent artifact people share on social media. MiroFish has no equivalent.
**How:**
- Add a backend endpoint that stores each round's state (posts, votes, trades, belief snapshots) as a structured JSON timeline
- Build a frontend timeline component with a round slider — clicking a round shows that round's activity feed, market chart position, and belief state heatmap
- Add a "Share Simulation" button that generates a static HTML export of the timeline (no backend needed to view)

### 2. Preset Simulation Templates
**Type:** DX Improvement
**Effort:** Small (hours)
**Impact:** Dramatically lowers the barrier to first run. New users currently need to find or write a document, craft a simulation requirement, and configure settings. Templates let them click "Try it" and see results in minutes. This is critical for conversion — most GitHub visitors bounce if setup takes more than 5 minutes.
**How:**
- Create a `templates/` directory with 5-8 curated simulation configs: a political debate (e.g., "US 2028 Primary: What happens if candidate X drops out?"), a crypto launch, a corporate crisis, a product announcement, and a historical what-if
- Each template includes the seed document, simulation requirement, and recommended settings (agent count, rounds, platforms)
- Add a "Templates" tab to the frontend that lists them with one-click launch

### 3. Webhook & API Integration for Simulation Results
**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** Enables MiroShark to be used as a prediction service by other tools — feed in a document via API, get back structured simulation results. This opens the door to integrations with trading bots, news dashboards, CI/CD pipelines (test PR announcements before publishing), and the growing ecosystem of AI agent orchestration tools.
**How:**
- Add REST API endpoints: `POST /api/simulations` (start a simulation with a document + config), `GET /api/simulations/{id}/status`, `GET /api/simulations/{id}/results` (structured JSON with per-round data, final belief states, market outcomes)
- Add optional webhook URL in simulation config — POST results to the webhook when simulation completes
- Document the API with OpenAPI/Swagger spec auto-generated from FastAPI

### 4. Comparative Simulation Mode (A/B Testing)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Run the same scenario with one variable changed (e.g., "What if the CEO apologizes vs. doubles down?") and see side-by-side results. This is the most requested feature in the MiroFish ecosystem (multiple Medium articles mention it as a wishlist item) and no fork has built it yet. It directly addresses MiroShark's core value proposition of prediction — you can't predict well without comparing alternatives.
**How:**
- Add a "Compare" mode in the frontend that lets users duplicate a simulation config and modify one variable (the seed document, a specific agent's stance, or an injected event)
- Run both simulations (can be sequential or parallel if resources allow) and store results linked by a comparison ID
- Build a comparison view showing side-by-side sentiment trajectories, market price divergence, and a diff of the top posts/trades between the two runs

### 5. Contributor Quick-Start & Example Gallery
**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** MiroShark has 47 forks but only 3 contributors. The gap between "starred" and "contributed" is a classic open-source growth bottleneck. A contributor guide with good-first-issues and an example gallery of interesting simulations creates a flywheel: contributors submit examples, examples attract users, users become contributors.
**How:**
- Create `CONTRIBUTING.md` with: local dev setup (already partially in README), architecture overview (which files handle what), how to add a new platform (the pattern from Twitter/Reddit/Polymarket), and how to submit simulation examples
- Label 5-8 issues as "good first issue" covering concrete tasks: add a new social action type, improve a prompt template, add a frontend visualization, write a simulation template
- Create `examples/` directory with 3-4 curated simulation runs (input document + config + output summary + screenshots) that showcase different use cases

---

## Analysis Notes

**Why these 5:** MiroShark's biggest bottleneck is not technical capability — the engine is already impressive. The bottleneck is *accessibility* (templates, contributor guide), *demonstrability* (replay viewer, comparison mode), and *extensibility* (API). These five ideas target exactly those gaps.

**What was considered but not included:**
- **Security audit** — The codebase is young enough that hardening should wait until the API surface stabilizes
- **Performance** — The recent 10x Neo4j optimization and parallel platform execution already addressed the main bottlenecks
- **Content/blog** — Already being handled by the miroshark-aeon automated skills (repo-article, push-recap)
- **Polymarket real-money integration** — Too much regulatory complexity for autonomous implementation
