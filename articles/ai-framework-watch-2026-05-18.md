# AI Framework Watch — 2026-05-18

**Verdict:** RELEASE WEEK: 6 frameworks shipped — langgraph, crewAI [PRE], llamaindex, mastra, smolagents, pydantic-ai

**Tracked:** 9 of 9 frameworks  ·  **Unreachable:** 0  ·  **Anchor:** aaronjmars/aeon  ·  *(COLD START — first run, no prior deltas)*

---

## Ranked table

*Sorted by 7d Δ desc; anchor pinned top. Cold start: all deltas baseline this run — deltas begin next week.*

| Framework | Stars | 7d Δ | 30d Δ | Releases (7d) | Breaking? | Headline |
|-----------|------:|------|-------|:-------------:|:---------:|---------|
| aaronjmars/aeon | 366 | — | — | 0 | — | Active dev (pushed 2026-05-17); no formal releases |
| microsoft/autogen | 58,137 | — | — | 0 | — | No releases; last push 2026-04-15 (quiet ~33d) |
| crewAIInc/crewAI | 51,633 | — | — | 2 [PRE] | — | 1.14.5 alpha cadence; stable line last shipped 2025-09-30 |
| run-llama/llama_index | 49,480 | — | — | 1 | — | v0.14.22 — dependency sweeps across 55+ integrations |
| stanfordnlp/dspy | 34,496 | — | — | 0 | — | No releases in window; 3.2.1 shipped 2026-05-05 |
| langchain-ai/langgraph | 32,311 | — | — | 5 | — | 1.2.0 — durable error-handler, set_node_defaults(), DeltaChannel beta |
| huggingface/smolagents | 27,366 | — | — | 1 | — | v1.25.0 — registry refactor, MLflow docs |
| mastra-ai/mastra | 23,981 | — | — | 2 | — | @mastra/core@1.34.0 — ACP coding agents, xAI realtime voice, push-PubSub |
| pydantic/pydantic-ai | 17,120 | — | — | 5 | — | v1.97.0 — GoogleProvider split, MCPToolset replaces MCPServer* (provider API changed — review changelog) |

---

## Releases (7-day window: 2026-05-11 → 2026-05-18)

### langchain-ai/langgraph — 5 releases

- **1.2.0** (2026-05-12) — Durable error-handler resume across host crashes; `set_node_defaults()` added to `StateGraph`; DeltaChannel and delta-history APIs marked beta; checkpoint packages promoted to stable alongside.
- **prebuilt==1.1.0** (2026-05-12) — Promoted from alpha; changes since prebuilt==1.1.0a2.
- **langgraph-checkpoint-postgres==3.1.0** (2026-05-12) — Postgres checkpointer stable; changes since 3.1.0a4.
- **langgraph-checkpoint-sqlite==3.1.0** (2026-05-12) — SQLite checkpointer stable; changes since 3.1.0a1.
- **langgraph-cli==0.4.26** (2026-05-12) — CLI patch; changes since 0.4.25.

### crewAIInc/crewAI — 2 releases [PRE]

- **1.14.5a6** (2026-05-15) [PRE] — Alpha release; "What's Changed" (no headline provided).
- **1.14.5a5** (2026-05-12) [PRE] — Alpha release; "What's Changed" (no headline provided).

*Note: crewAI's last stable release was python-v0.7.5 on 2025-09-30 (~7.5 months ago). The repo is actively developed (pushed 2026-05-18), but the 1.x line has been in pre-release cadence throughout that period.*

### run-llama/llama_index — 1 release

- **v0.14.22** (2026-05-14) — Maintenance sweep: dependency upgrades across 55+ integration packages via `uv lock --upgrade`; no headline feature additions in published notes.

### mastra-ai/mastra — 2 releases

- **@mastra/core@1.34.0** (2026-05-15) — ACP Coding Agents as Tools or Subagents (new `@mastra/acp@0.1.0`); xAI realtime voice integration (`@mastra/voice-xai-realtime@0.1.0`); push-capable PubSub + HTTP workflow event ingestion; `ResponseCache` for identical LLM step deduplication.
- **@mastra/core@1.33.0** (2026-05-13) — Push-capable PubSub delivery; `Mastra.handleWorkflowEvent()` unified entry point; `POST /api/workflows/events` for broker push delivery (GCP Pub/Sub, SNS, EventBridge).

### huggingface/smolagents — 1 release

- **v1.25.0** (2026-05-14) — Registry pattern replaces `importlib` for agent/model deserialization; fixes `TokenUsage` import; adds MLflow integration documentation.

### pydantic/pydantic-ai — 5 releases

- **v1.97.0** (2026-05-15) — `GoogleProvider(vertexai=True|False)` split into `GoogleProvider` + `GoogleCloudProvider`; provider ID `google-gla:` → `google:`, `google-vertex:` → `google-cloud:` (old names deprecated); `MCPToolset` using `fastmcp-slim[client]` replaces `MCPServer*` and `FastMCPToolset` (deprecated); `OnlineEvaluator.run_on_errors` for eval-on-failure; `ModelResponse.state=incomplete` during streaming. *(Provider API changed — review changelog before upgrading.)*
- **v1.96.1** (2026-05-14) — Auto-generated; patch release.
- **v1.96.0** (2026-05-13) — Auto-generated; minor release.
- **v1.95.1** (2026-05-13) — Auto-generated; patch release.
- **v1.95.0** (2026-05-12) — Auto-generated; minor release.

---

## Momentum picks

*No momentum picks this run — cold start, all 7d deltas baseline this week. Picks begin next Monday.*

---

## Anchor position

aeon sits at 366 stars and 74 forks — the smallest repo in the cohort by an order of magnitude against the top three (autogen 58k, crewAI 51k, llamaindex 49k). It shipped no releases this week but pushed as recently as 2026-05-17, indicating active development. The cohort logged 16 combined releases this week across 6 frameworks; aeon contributed 0, consistent with its GitHub-Actions-native runtime model where capability ships as skill files rather than versioned packages. The framework comparison that matters most for aeon's operators: the cohort averages 2.6 releases per active framework per week — a pace that creates weekly breaking-change noise. aeon's no-release cadence is a different kind of signal.

---

## Source status

`gh_api: ok · reachable: 9/9 · releases_lookup: 9/9 · breaking_signals_fired: 0 · cold_start: true`
