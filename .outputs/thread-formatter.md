*Thread Draft — 2026-06-08*
Topic: Signed Simulation Result — GET /api/simulation/:id/signed-result.json (PR #152)

1/ PR #152 ships GET /api/simulation/:id/signed-result.json. Every finished sim now carries an HMAC-SHA256 signature over its canonical signal payload. You can verify the output offline, without re-fetching, without staying authenticated, without trusting the connection.

2/ Before today, trust in a MiroShark sim output was connection-level. signal.json is auth-gated — the credentials that got you in were also your proof the data was authentic. Cache the payload and go offline: no verification path existed.

3/ HMAC-SHA256 over canonical JSON: sorted keys, ASCII-only, comma-colon separators. The signed_at timestamp is outside the signed block — two calls on the same finished sim return identical signatures, different timestamps. 25 tests, one pinning the exact canonical form.

4/ Capacitr and AntFleet are named in the PR as the immediate consumers. Both run operations on simulation outputs — settlement ledgers and leaderboard entries — where they need to prove the data came from MiroShark unchanged. The trust anchor is now the artifact, not the session.

5/ 34th catalogued surface on MiroShark. 42nd consecutive zero-dependency PR. schema_version and algorithm fields are the swap-seam for a future Ed25519 upgrade. https://github.com/aaronjmars/MiroShark/pull/152

(article: articles/thread-2026-06-08.md)
