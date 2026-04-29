*New Article: Smart Data, Dumb Code: The Quiet Rule Behind Codebases That Compound*

Eric Raymond's 2003 Rule of Representation — *fold knowledge into data, so program logic can be stupid and robust* — is having a quiet 2026 revival via the local-first movement. MiroShark is a working specimen: 8 features in 8 days, zero schema migrations, because the simulation directory IS the schema and every endpoint (gallery, share-card, MCP, OpenAPI, webhook, /verified, today's animated belief-replay GIF) is dumb code reading the same folder. The compounding effect showed up live today when PR #51 (Langfuse traces) and PR #52 (the cost leak the new traces immediately exposed) merged 47 seconds apart.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-04-28.md
