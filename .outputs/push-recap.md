*Push Recap — 2026-04-25*
MiroShark: 1 substantive commit (PR #45, still open). miroshark-aeon: 0 substantive commits (~31 chore/automation).

REST surface gets its own spec: PR #45 lands a handwritten 1.9K-line OpenAPI 3.1 covering ~85 paths under 13 tags, plus a Flask blueprint serving Swagger UI at `/api/docs`, raw YAML at `/api/openapi.yaml`, and a JSON form for `openapi-generator` consumers. The natural follow-on to yesterday's PR #44 MCP onboarding — same developer audience, REST instead of MCP-over-stdio.

Drift test is the load-bearing piece: a regex-based unit test statically scans every `app/api/*.py` for `@<bp>_bp.route(...)` decorators, fully qualifies via blueprint `url_prefix`, and fails CI the moment the spec falls behind the implementation. Same shape as PR #44's mcp_server.py drift check — handwritten source of truth + static-scan tripwire.

Key changes:
- `backend/openapi.yaml` (+1,966): 13 tags, named schemas (`SuccessEnvelope`, `RunStatus`, `BeliefDrift`, `EmbedSummary`, `GalleryCard`, `McpStatus`, …), reusable params/responses.
- `backend/app/api/docs.py` (+268): Swagger UI pinned to `swagger-ui-dist@5.17.14` from jsDelivr, plus YAML + JSON endpoints, pyyaml soft-optional.
- `backend/tests/test_unit_openapi.py` (+321): 8 offline tests, drift detection centerpiece.

Stats: 7 files / +2,577 / −2 across 1 commit. PR #45 open at window close (filed 11:17 UTC).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-25.md
