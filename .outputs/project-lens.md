*New Article: The YAML That Matches the Code: API Documentation Stopped Being Allowed to Lie*

Today MiroShark merged PR #45: a 1,966-line OpenAPI 3.1 spec, Swagger UI at /api/docs, and a 321-line test file with a regex-based drift detector. The article zooms out to why "75% of APIs don't conform to their specs" stopped being a documentation hygiene problem in 2026 and became a load-bearing one — once SDK generators, LLM tool callers, and MCP servers all consume the spec as ground truth, a wrong YAML pushes broken type signatures into production code other people are pip-installing. The deep dive: the 30-line static scan that fails CI when openapi.yaml stops matching the Flask routes, and what that earns downstream — typed SDKs, APIs.guru listings, agent tool calling.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-04-25.md
