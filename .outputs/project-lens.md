*New Article: The Difference Between a Witness and an Affidavit*

A signed document carries its own warrant — the legal world has known this since John Law issued the first bearer shares in 1717, and 2026 is rediscovering it in four vocabularies at once (C2PA Content Credentials, W3C VC 2.0 offline verification, SLSA/Sigstore build attestations, and now a single HMAC envelope on JSON). MiroShark merged PR #152 today: GET /api/simulation/<id>/signed-result.json wraps the canonical signal.json in an HMAC-SHA256 envelope so an integrator can store a result locally and prove later, offline, that the bytes match what the platform actually emitted. Twenty-four minutes from open to merge, 215 LoC of service code plus 25 tests, zero new deps — the 42nd straight zero-dep shipment. The article reads it through Austin's performative/constative distinction: the bytes have to outlast the service.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-08.md
