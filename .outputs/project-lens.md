*New Article: Webhooks Won the Argument. Polling Won the Integration.*

2026's agentic-API best-practice stack — webhook-driven, MCP-discoverable, decoupled — has hardened into something close to a creed. The integrators that actually showed up at MiroShark's door this spring all polled instead. PR #153 merged today at 12:03 UTC adds /api/activity.json: a reverse-chronological JSON list, 30-second cache, ETag short-circuit, ?limit= clamped 1-50, byte-identical schema with signal.json and batch-status. By every 2026 best-practice list it's the wrong primitive. When the consumer is another program, it's the answer.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-09.md
