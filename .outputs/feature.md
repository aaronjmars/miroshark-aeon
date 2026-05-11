*Feature Built — 2026-05-11*

Webhook HMAC Signature Verification
MiroShark's outbound webhook now signs every payload with HMAC-SHA256 when the operator sets a `WEBHOOK_SECRET`. The signature ships as an `X-MiroShark-Signature: sha256=<hex>` header alongside the existing `X-MiroShark-Event` and `X-MiroShark-Sim-Id` headers, so any tool consuming MiroShark webhooks can prove the payload actually came from this MiroShark instance and wasn't spoofed en route. Same scheme Stripe and GitHub use — three lines of stdlib `hmac` on the recipient side.

Why this matters:
Integration demand on MiroShark is no longer hypothetical — recent threads list Revault, CancerHawk, and x402/API as active integrations consuming MiroShark output, with bankrbot and trading screeners on the way. Every operator receiving MiroShark webhooks faces the same unresolved question once more than one tool sees the same stream: did this payload actually come from my instance, or is something spoofing it? Until today, there was no answer — anyone who could guess the webhook URL shape could forge a "simulation.completed" event into a downstream integration. HMAC signing closes that gap with the industry-standard primitive both Stripe and GitHub already ship. Picked from yesterday's repo-actions batch (idea #1, top of the list).

What was built:
- backend/app/services/webhook_service.py: New `compute_signature(payload_bytes, secret=None)` returns `sha256=<hex>` or `None` when the secret is blank, reading `WEBHOOK_SECRET` at call time so a Settings change takes effect immediately. New `verify_signature(payload_bytes, header_value, secret)` uses `hmac.compare_digest` for constant-time recipient-side checks. `_post_json` injects the header only when the signature is non-None — auto-fire, retry, and the "Send test event" button all sign consistently because they share the same dispatch path.
- backend/tests/test_unit_webhook_signature.py: 8 offline tests covering the format guard (`sha256=` + 64 lowercase hex), round-trip verification, tampered-body rejection, tampered-header rejection, empty-secret backward compatibility, on-the-wire header presence/absence (urlopen-mocked integration tests), and retry dispatch carrying its own signature over its own retry body.
- docs/WEBHOOKS.md + WEBHOOKS.zh-CN.md: New "Verifying webhook signatures" section with Python/Node.js/curl verification snippets, header table updated, security notes call out the transport-only nature of the secret.
- frontend/src/components/EmbedDialog.vue: A collapsible "🔐 Verify webhook signatures" hint appears beneath the Retry button once a delivery has succeeded — shows the env var NAME only, never the secret value, and links to the WEBHOOKS.md verification section.
- docs/FEATURES.md + FEATURES.zh-CN.md + backend/openapi.yaml + README.md + .env.example: Parallel documentation updates so the feature is discoverable from every entry point.

How it works:
The signature is computed inside `_post_json` over the raw body bytes that go on the wire — not the parsed JSON — so recipients must verify before parsing (re-serializing JSON can re-order keys or change whitespace and break the digest). When `WEBHOOK_SECRET` is unset or blank, the signature helper returns `None` and the header is omitted entirely, which makes the feature fully backward compatible: every existing Slack / Discord / Zapier / Make / n8n integration keeps working without changes. The retry endpoint adds `retry: true` to the payload before serialization, so the retry body differs from the auto-fire body and gets its own signature — recipients verifying both paths use one canonical check. The published `verify_signature` helper exists so the dispatcher and the receiver share the same implementation; if the algorithm ever needs to evolve, both ends move together. Zero new dependencies (pure stdlib `hmac` + `hashlib`).

What's next:
The remaining four ideas from yesterday's repo-actions batch are still unbuilt: #2 Jupyter notebook export (institutional researcher handoff), #3 trading signal JSON (structured output for bankrbot-class tools), #4 per-agent stance sparklines (the "who moved the needle?" view), #5 simulation archive bundle (one-click ZIP of every artifact). Each is scoped for a future autonomous build. Zero-new-deps streak now stands at 18 consecutive PRs (#57 → #79).

PR: https://github.com/aaronjmars/MiroShark/pull/79
