*New Article: Fourteen Workloads, One Question — A Day in the Life of a Pre-Trade Scenario Sweep*

Google added webhooks to Gemini in May to kill polling for long-running AI jobs. But when your "fleet" is fourteen long-running sims on someone else's server, you still have to poll — the question is how. PR #150 (opened today on MiroShark) introduces `POST /api/simulation/batch-status`: one call, list semantics, byte-identical envelopes for private vs unknown IDs (a dedicated test enforces it). The user-story angle: a five-person desk's pre-trade scenario sweep that drops from 420 hourly polls to 30 without exposing whether someone else's private sim exists.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-06.md
