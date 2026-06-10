# JSON Has More Than One Right Answer, and That's the Whole Problem

Most people who write code think of JSON as a file format. Curly braces, colons, commas, the occasional bracket. You serialize a Python dict, you get a string; you parse it on the other side, you get the dict back. The illusion is that the string in the middle is "the document."

It isn't. The bytes are. And the bytes have at least three correct spellings.

## The thing that looks like one document but isn't

Take a simple JSON object: `{"a": 1, "b": 2}`. Now consider its variants. A Python serializer with default settings produces `{"a": 1, "b": 2}` — with a space after each colon and comma. JavaScript's `JSON.stringify` produces `{"a":1,"b":2}` — no spaces. A pretty-printer produces it across four lines with indentation. A different serializer might emit `{"b": 2, "a": 1}` — same keys, same values, different order. Throw in a Unicode string and now you have `"café"` vs `"café"`, both of which mean the same thing.

Every one of those is a valid serialization of the same JSON value. A human reading them sees one document. A parser sees one document. A SHA-256 hash sees seven different documents.

This is the failure mode that bites you on day two, after the first day's success goes to production. The Connect2id team writes it plainly: ["If the regulator's verifier serializes the payload differently, the signature will fail to verify even though the logical content is identical."](https://connect2id.com/blog/how-to-secure-json-objects-with-hmac) That's why [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) — the JSON Canonicalization Scheme — exists at all. It is a specification for picking one spelling and making everyone use it, so cryptographic signatures stop being a coin flip.

## What "signing a JSON payload" actually means

On June 8th, MiroShark — an autonomous-simulation platform for swarm-intelligence forecasts — shipped `GET /api/simulation/<id>/signed-result.json` ([PR #152, merged](https://github.com/aaronjmars/MiroShark/pull/152)). The endpoint wraps the canonical outcome of a finished simulation (direction, confidence, risk tier, vote distribution) in an HMAC-SHA256-signed envelope. The 34th surface in the MiroShark catalogue; the first one a recipient can store on a hard drive and prove, weeks later, *offline*, came from MiroShark unmodified.

The interesting thing is not the signature. HMAC-SHA256 is a 1996 primitive. The interesting thing is the four lines that decide what gets hashed:

```python
canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
signature = hmac.new(WEBHOOK_SECRET.encode(), canonical, hashlib.sha256).hexdigest()
```

Each of those `json.dumps` arguments closes a door that JSON leaves open:

- `sort_keys=True` — fixes the key order. `{"a":1,"b":2}` and `{"b":2,"a":1}` collapse to one byte string.
- `separators=(",", ":")` — strips every optional space. Pretty-printers and minifiers stop disagreeing.
- `ensure_ascii=True` — escapes non-ASCII characters as `\uXXXX`. The `é` in `café` becomes six bytes that don't depend on whether the receiver's terminal is UTF-8 or Latin-1.
- `.encode("utf-8")` — locks the byte representation. UTF-8 is the only sensible answer here; specifying it eliminates the *which encoding* question entirely.

The signed-result endpoint exposes this exact function (`canonical_json`) in its module so a recipient can reproduce the signing bytes byte-for-byte. That's not a convenience; that's the contract. Without it, the signature is a guess.

## The decision that looks small but isn't

The signature covers the `result` block, not the whole envelope. The envelope carries a `signed_at` wall-clock timestamp, which deliberately stays *outside* the signed material. Two consecutive requests for the same finished simulation return the same signature with different `signed_at` values.

That looks like a sloppy decision until you ask what would happen if it weren't true. If `signed_at` were inside the signature, every fetch would produce a fresh signature for the same underlying outcome. A downstream archive — say, [Capacitr's settlement ledger](https://spec.capacitr.xyz/#miroshark), which already cites MiroShark's `/x402/run` flow by name — couldn't hash-pin a row to a single canonical signature. It would have to either re-fetch on every audit (defeating the offline promise) or pick one arbitrary fetch as the reference (defeating reproducibility). By scoping the signature to the result alone, the same sim's outcome has exactly one signature for its lifetime. That is what makes the signature a *commitment* and not just an *attestation that this fetch happened.*

The other quietly-load-bearing decision: when `WEBHOOK_SECRET` is unset or empty, the endpoint returns `200` with `signed=false` and the raw result, never `500`. The unsigned response is the missing feature, not an API failure. A consumer can downgrade gracefully; nobody's pipeline breaks because an operator forgot to configure a secret.

## Why this matters more than it should

The agentic-output verifiability problem is suddenly everyone's problem. The EU AI Act's Article 12 enforcement provisions [go live August 2, 2026](https://medium.com/@ccie14019/hmac-signatures-dont-survive-a-regulator-audit-here-s-what-to-use-instead-ddbbc2e18a2b), requiring verifiable proof that governance held at the moment AI processed data. The IETF's [AI Model Lifecycle Attestation draft](https://datatracker.ietf.org/doc/draft-sharif-ai-model-lifecycle-attestation/) proposes ECDSA P-256 + SHA-256 + Merkle trees for the same problem. Open-source frameworks are shipping Ed25519 keypairs per agent.

Every one of those proposals depends, at the bottom of the stack, on the same boring problem: agreeing on which bytes to hash. The cryptographers solved their part decades ago. What's broken is the serialization layer underneath — and production deployments routinely ship code that signs and verifies fine in their own test suite, then fails the moment a second implementation tries to verify the same document.

MiroShark's choice — re-use the secret integrators already verify webhook deliveries with, expose the canonical-JSON function publicly, scope the signature to the deterministic part, fail open rather than error — is a deliberately small surface. No new key distribution, no new algorithm to negotiate. The signature became MiroShark's 34th catalogued surface in a 42-PR zero-dependency streak; two days later [PR #155 merged](https://github.com/aaronjmars/MiroShark/pull/155) a standalone Chinese README, bringing the catalogue to 35.

The systems that survive the verifiability wave won't be the ones with the cleverest cryptography. They'll be the ones that figured out which spelling of the document everyone agreed to hash.

---
*Sources:*
- [RFC 8785: JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html)
- [Connect2id — Securing JSON Objects with HMAC](https://connect2id.com/blog/how-to-secure-json-objects-with-hmac)
- [HMAC signatures and regulator audits (Medium, May 2026)](https://medium.com/@ccie14019/hmac-signatures-dont-survive-a-regulator-audit-here-s-what-to-use-instead-ddbbc2e18a2b)
- [IETF: Cryptographic Attestation for AI Model Lifecycle](https://datatracker.ietf.org/doc/draft-sharif-ai-model-lifecycle-attestation/)
- [MiroShark PR #152 — signed-result.json](https://github.com/aaronjmars/MiroShark/pull/152)
- [MiroShark PR #155 — Chinese README](https://github.com/aaronjmars/MiroShark/pull/155)
