# What GraphQL, gRPC, and Kubernetes Already Knew: APIs Should List Themselves

A developer hitting an API for the first time has one question: *what can this thing do?* If the API is GraphQL, they send a `__schema` query. If it's gRPC, they call `ServerReflection`. If it's Kubernetes, they type `kubectl api-resources`. In all three cases the server answers — in a structured, machine-readable form — with a list of everything it exposes.

If the API is REST, they read a PDF. Or a Notion page. Or, in good cases, an OpenAPI spec that may or may not match the running code. The New Stack found that of more than 100,000 public REST APIs catalogued, fewer than 5% had good, consistent, up-to-date OpenAPI specs. The discoverability gap isn't theoretical. It's 95,000 APIs that don't know how to describe themselves.

## Three protocols, three commitments

GraphQL introspection shipped with the protocol in 2015. Every server speaks it by default: send a `__schema` query, get back a structured tree of types, queries, mutations, arguments, and return values. The schema *is* the introspection result. There is no separate document to maintain because there is no separate document — the running server is the source.

gRPC reflection, the docs for which were last updated this month, is similar but opt-in. The server author adds a `ServerReflection` service to the binary, and tools like `grpcurl` and Postman can then talk to it without a `.proto` file in hand. The reflected information is mirror-true to the protobuf definitions. The protocol is a bidirectional stream and ensures all related calls land on the same server, which matters when a cluster runs many versions concurrently.

The Kubernetes Discovery API is the most ambitious of the three. The `/api` and `/apis` endpoints don't just list built-in resources — they list every Custom Resource Definition the cluster has accepted, every operator extension, every aggregated API. Run `kubectl api-resources` against any cluster and it returns *that specific cluster's* capability list, not Kubernetes-the-product's catalog. Each deployment is self-describing because the control plane is self-aware.

Three protocols, three answers. All three made "ask the server what it is" a wire-level primitive — the kind of thing you can rely on without coordinating out-of-band.

## A REST service quietly adopting the primitive

PR #130 was opened on the MiroShark repo this week. It adds `GET /api/surfaces.json` — a single endpoint that returns a JSON envelope listing every surface the deployment exposes. Twenty-seven entries: twenty-four publish-gated per-simulation surfaces (the signal JSON, the trajectory CSV, the embed iframe, the BibTeX citation, the consensus badge), two platform-level surfaces (the stats endpoint and its badge), and — recursively — the catalog itself. Each entry carries a `key`, the `endpoint` path, the HTTP `method`, a `type` category from a frozen seven-category set (`analytics` / `visualization` / `export` / `embed` / `integration` / `platform` / `discovery`), a one-line `description`, the `added_in_pr` number that introduced it, and a copy-pasteable `example_curl`.

The endpoint is a meta-surface. It doesn't return data the platform produces; it returns the platform's own contract with consumers.

## The fourth model: hand-curated, drift-guarded

What's interesting about PR #130 is what it *doesn't* do, and the reasoning attached. The catalog is hardcoded — a literal list at module scope in `backend/app/services/surfaces_catalog.py`. It is explicitly *not* auto-derived from the Flask URL map, and it is explicitly *not* auto-derived from the in-process `SURFACE_KEYS` registry that powers per-surface serve counters.

The URL-map approach was rejected because Flask's map includes admin and mutation routes the catalog must not advertise. Full reflection — the GraphQL or gRPC default — would leak the platform's private surface area. The `SURFACE_KEYS` approach was rejected because that registry covers only publish-gated per-simulation surfaces; the catalog also includes platform-level ones and itself.

Instead, the catalog is editorially maintained — a manifest of what the operator chooses to publish — paired with a drift-guard test. `test_unit_surfaces_catalog.py` asserts that the per-simulation subset of the catalog matches `SURFACE_KEYS` exactly. Ship a new publish-gated surface without entering the catalog and CI fails before merge.

That's a fourth model for API self-description. GraphQL and gRPC derive introspection from the schema and accept whatever leakage that entails (which is why production GraphQL servers routinely disable `__schema` in prod). Kubernetes Discovery exposes whatever the API server has accepted, CRDs included. A handwritten catalog with drift guards is the inverse: you say what's public, and a test ensures you didn't forget anything you said you'd publish. It trades expressiveness for editorial control.

## Why REST is starting to need this

The agent wave makes machine-readable discoverability load-bearing again. When the consumer is a person reading docs, drift is a quality-of-life problem. When the consumer is an LLM tool-caller picking endpoints at runtime, drift is a correctness problem — the agent hits paths that don't exist, or misses paths that do. The "95,000 APIs without specs" number stops being a documentation gripe and starts being an integration ceiling.

GraphQL APIs are in a strong position here because introspection is free. gRPC services with reflection enabled are too. REST APIs have been the laggards — partly because the protocol never committed to it, partly because OpenAPI files have always lived alongside the code instead of being generated by it.

The Surface Catalog API is a small move in the opposite direction: a single endpoint, schema-versioned (`schema_version: "1"`), ETag-cacheable (`surfaces-v1-27` short-circuits to 304), that lets any consumer — agent or human — ask the deployment what it can do. It's a 27-entry list today. It's also the surface that the surface-discovery tooling no longer has to grep Markdown to find.

---
*Sources:*
- *[The State of Introspection for REST and GraphQL APIs — The New Stack](https://thenewstack.io/the-state-of-introspection-for-rest-and-graphql-apis/)*
- *[GraphQL Introspection — graphql.org](https://graphql.org/learn/introspection/)*
- *[gRPC Server Reflection — grpc.io](https://grpc.io/docs/guides/reflection/)*
- *[The Kubernetes API — kubernetes.io](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)*
- *[MiroShark PR #130 — Surface Catalog API](https://github.com/aaronjmars/MiroShark/pull/130)*
