*Thread Draft — 2026-06-11*
Topic: MiroShark API-surface pivot — 5 JSON endpoint PRs + signed payload

1/ 5 of 8 PRs merged in MiroShark this week ship zero UI. They add JSON endpoints. The web app is not the product anymore — the contract is.

2/ A year ago MiroShark was a browser demo. Three external teams — RevaultDrops, AntFleet, Capacitr — are now building on it as AI infrastructure. A browser tab can't be a dependency. So it became an API.

3/ PR #152 shipped signed-result.json: HMAC-SHA256, offline-verifiable. You don't sign a response for a browser tab. You sign it so a third party can consume a prediction, verify it wasn't tampered with, and trust it without calling back.

4/ The OpenAPI spec grew 1,195 lines this week. The docs now tell integrators to run openapi-generator to get a Python, TypeScript, or Go SDK in one command. This is not a web app adding features. It is a platform deciding it wants to be depended on.

5/ Five API PRs, one signed payload, three named integrators. The full breakdown of what shipped and where this is going: https://github.com/aaronjmars/MiroShark

(article: articles/thread-2026-06-11.md)
