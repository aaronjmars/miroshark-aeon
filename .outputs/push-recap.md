*Push Recap — 2026-04-16*
MiroShark — 6 commits, miroshark-aeon — 28 commits (2 authors)

Director Mode (Event Injection): Users can now inject breaking events into running simulations — agents receive them at the next round boundary, shifting posts, trades, and stances. File-based event queue, REST API (max 3 per sim), full UI panel with timeline banners and belief drift markers. PR #31 merged.

Multi-Model Routing & Cost Optimization: New OASIS_MODEL_NAME decouples the sim loop model from the default LLM. GraphToolsService gains a fast_llm path routing mechanical work to cheap models. Report context capped at 6K chars (was unbounded at 112K tokens). Auto-generated run_summary.md tracks cost/performance per simulation. Gemini empty-message crash fixed.

NER Quality & Integration Fixes: Larger NER chunks (1500/100), nonspeaking-entity filter (rejects dates, concepts, countries from becoming agents), PDF citation artifact stripping, ontology type validation. OpenRouter headers updated from deprecated X-Title to X-OpenRouter-Title.

Aeon Infra Hardening: Heartbeat detects stuck runs (>2h in_progress) and bypasses dedup guard for fresh dispatch (PR #14). Notification system tracks delivery to prevent double-send. project-lens and repo-article promoted to daily schedules.

Key changes:
- backend/scripts/director_events.py: new file-based event queue for mid-sim injection (+187 lines)
- backend/app/utils/run_summary.py: auto-generated cost/perf reports (+335 lines)
- backend/app/services/graph_tools.py: three-tier model routing (fast/default/smart)
- backend/app/services/entity_reader.py: nonspeaking entity filter (+60 lines)
- skills/heartbeat/SKILL.md: stuck-run timeout detection

Stats: ~40 files changed, +1,700/-320 lines
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-16.md
