# AI Framework Watch — 2026-05-25

**Verdict:** RELEASE WEEK: 4 frameworks shipped — langgraph, crewai, mastra, pydantic-ai

**Tracked:** 9 of 9 frameworks  ·  **Unreachable:** 0  ·  **Anchor:** aaronjmars/aeon

---

## Ranked table

(Sorted by 7d Δ desc; anchor pinned to top. 30d Δ unavailable — state is 7 days old, ≥21-day threshold not yet met.)

| Framework | Stars | 7d Δ | 30d Δ | Releases (7d) | Breaking? | Headline |
|-----------|-------|------|-------|---------------|-----------|----------|
| aaronjmars/aeon | 442 | +76 | — | 0 | — | — |
| langchain-ai/langgraph | 32,885 | +574 | — | 3 | — | langgraph 1.2.1 + sdk 0.3.15 + checkpoint 4.1.1 patch sweep |
| crewAIInc/crewAI | 52,142 | +509 | — | 2 | — | 1.14.5 stable; 1.14.6a1 [PRE] in progress |
| mastra-ai/mastra | 24,280 | +299 | — | 1 | — | @mastra/core@1.35.0 weekly cadence |
| microsoft/autogen | 58,375 | +238 | — | 0 | — | — |
| run-llama/llama_index | 49,644 | +164 | — | 0 | — | — |
| pydantic/pydantic-ai | 17,276 | +156 | — | 5 | — | v1.102.0 stable + v2.0.0b1/b2/b3 [PRE] (major version beta — review changelog) |
| huggingface/smolagents | 27,500 | +134 | — | 0 | — | — |
| stanfordnlp/dspy | 34,626 | +130 | — | 0 | — | — |

---

## Releases (7-day window: 2026-05-18 → 2026-05-25)

### pydantic/pydantic-ai

The headline story this week: Pydantic AI launched v2 beta in three rapid iterations while continuing to ship the v1 stable track in parallel.

- **v2.0.0b3** (2026-05-23) [PRE] — Third beta iteration; dual-track cadence
- **v1.102.0** (2026-05-23) — Weekly stable; v1 track maintained alongside v2 development
- **v2.0.0b2** (2026-05-22) [PRE] — Second beta iteration
- **v1.101.0** (2026-05-22) — Weekly stable
- **v2.0.0b1** (2026-05-21) [PRE] — 🚀 Pydantic AI V2 Beta 1 launch (major version beta — review changelog)

No `[BREAKING]` flag fires (betas are tagged [PRE]; tag pattern `v2.0.0b*` does not match `v\d+\.0\.0`). Operators building on pydantic-ai should review the V2 beta changelog before the stable v2.0.0 release to plan migration timing.

### langchain-ai/langgraph

- **langgraph-sdk==0.3.15** (2026-05-22) — Changes since sdk==0.3.14
- **langgraph-checkpoint==4.1.1** (2026-05-22) — Changes since checkpoint==4.1.0
- **langgraph==1.2.1** (2026-05-21) — Changes since 1.2.0; patch release one week after the 1.2.0 stable

Three packages shipped within one day — standard langgraph release discipline (core + SDK + checkpoint versioned together).

### crewAIInc/crewAI

- **1.14.6a1** (2026-05-21) [PRE] — Pre-release development build
- **1.14.5** (2026-05-18) — Stable minor release

### mastra-ai/mastra

- **@mastra/core@1.35.0** (2026-05-18) — Weekly highlights bundle; TypeScript agent framework continuing weekly cadence

---

## Anchor position

aeon added 76 stars this week (366 → 442), the smallest absolute delta in the cohort — but the largest percentage gain at 20.8%. Every other framework grew between 0.4% (autogen) and 1.8% (langgraph) by comparison. Fork count jumped from 74 to 116 (+42, +57%), and open issues moved from 1 to 6 (+5). No releases shipped from the anchor this week. By absolute 7d delta, aeon sits last in the cohort; by percentage growth rate, it leads the table. The gap between aeon's absolute numbers and its growth rate is the signature of a smaller repo compounding faster than the established frameworks — that signal is worth watching as the 30d baseline builds up over the next few runs.

---

## Source status

`gh_api: ok · reachable: 9/9 · releases_lookup: 9/9 · breaking_signals_fired: 0`
