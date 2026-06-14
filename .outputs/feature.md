*Feature Built — 2026-06-14 — aaronjmars/MiroShark* 🦈

Full contributor guide
CONTRIBUTING.md was a stub — it told you how to run pytest and nothing else. Now it's a real onboarding doc: how to set up the project locally, how to submit a PR the way the repo actually merges them, and how to add an API endpoint without breaking CI. Mirrored into Chinese too, so the zh-CN side stays in sync.

Why this matters:
1,270 stars, and a first-time contributor had to reverse-engineer setup from the README, package.json, and the CI workflow in parallel. That friction is the gap between "cool repo" and "I shipped a PR." This was repo-actions' #2 pick — yesterday closed #1 (SECURITY.md). Lower the cost of the first contribution and ecosystem growth follows.

What was built:
- CONTRIBUTING.md: added Development setup (npm run setup:all → Neo4j via docker compose → npm run dev), Submitting a PR (branch prefixes, Conventional Commit titles, run the unit suite first), and Adding an API endpoint (the openapi.yaml drift-test contract). ~30 → ~90 lines.
- CONTRIBUTING.zh-CN.md: every new section mirrored in Chinese — i18n parity held.
- README.md: docs-table label updated to match the broader guide.

How it works:
No code — every instruction is anchored to what's actually in the repo, not invented. Setup commands come straight from the package.json scripts block; the Neo4j step matches docker-compose.yml; the CI line matches tests.yml. The endpoint section documents the real gate: test_unit_openapi.py fails CI if openapi.yaml and the Flask routes drift, so the guide tells you to register the blueprint, document the path, and add an offline unit test — the exact loop maintainers already follow.

What's next:
Two repo-actions ideas still open and autonomously buildable — ISSUE_TEMPLATE (#5) and CODE_OF_CONDUCT (monitor). pip-audit in CI (#3) stays blocked until the token gets workflows scope.

PR: https://github.com/aaronjmars/MiroShark/pull/162
