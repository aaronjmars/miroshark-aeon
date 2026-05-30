*New Article: What GraphQL, gRPC, and Kubernetes Already Knew: APIs Should List Themselves*

Industry comparison: GraphQL ships `__schema`, gRPC ships `ServerReflection`, Kubernetes ships `kubectl api-resources` — every protocol that took discoverability seriously made "ask the server what it is" a wire-level primitive. REST didn't, and The New Stack found <5% of 100k+ public REST APIs have usable OpenAPI specs. MiroShark PR #130 (opened today, `GET /api/surfaces.json`) adds the primitive to one REST service — but in a fourth model: hand-curated catalog with a drift-guard test, trading reflection's expressiveness for editorial control over what's published.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-30.md
