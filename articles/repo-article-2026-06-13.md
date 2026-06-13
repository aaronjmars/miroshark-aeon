# MiroShark spent its heaviest week teaching you to trust its sims without trusting its server

Seven PRs merged into `aaronjmars/MiroShark` in seven days. Five add or shape JSON endpoints — easy to read as "more API." But the two biggest by code volume aren't about *getting* a result. They're about *proving* one. `signed-result.json` (#152) and `distribution.json` (#151) move the question from "can I fetch the answer" to "can I check the answer without taking the server's word for it."

## The claim
> MiroShark's week added a verification layer, not just endpoints: #152 signs each result with HMAC-SHA256 for offline proof, and #151 exposes the platform-wide outcome distribution so a skeptic can audit bias.

## Evidence

**#152 makes a stored result self-proving.** Commit `7b79e7b` added `backend/app/services/signed_result.py` — 215 new lines — behind `GET /api/simulation/<id>/signed-result.json`. It wraps the canonical signal payload (direction, confidence, risk tier, belief percentages) in an HMAC-SHA256 envelope: `hmac.new(WEBHOOK_SECRET, canonical, sha256)` over the sorted-key JSON of the inner `result` block. The point, per the PR body: once an integrator stores a payload — "Capacitr's settlement ledger, a research archive, an ML pipeline's provenance row" — HTTPS no longer helps, because the bytes are sitting on *their* disk. The signature lets them prove later, with no live call back, that those bytes are what MiroShark emitted. The change shipped with `test_unit_signed_result.py` at 499 lines — more test than implementation.

**#151 exposes the shape of the corpus, not its size.** Commit `7075897` added `backend/app/services/outcome_distribution.py` — 533 lines — behind `GET /api/stats/distribution.json`. It returns the breakdown across 247 analyzed sims: `by_direction` (41.3% bullish / 28.7% neutral / 30.0% bearish), `by_confidence`, `by_quality` (32% excellent, 3.2% poor), and `avg_confidence_pct` 58.4. That's a calibration surface. A stranger deciding whether to trust a single bullish call can first check whether the engine calls *everything* bullish. It doesn't — and now you can see that from one endpoint, backed by 810 lines of tests.

**The weight is in the trust work.** Stack the diffs: #152 and #151 are 215+499 and 533+810 new lines. The week's access endpoints — #150 batch-status, #153 `activity.json`, #157 the `?type=` filter on `surfaces.json` — are thinner convenience surfaces over data that already existed. By volume, the engine spent the week on verifiability, not plumbing. That lands MiroShark inside a live 2026 thread: [EigenAI](https://arxiv.org/html/2602.00182)'s re-executable inference and [HMAC-signed agent receipts](https://phemex.com/academy/what-is-verifiable-ai-cryptographic-proofs-blockchain) are chasing the same property — make the model's output checkable by someone who doesn't trust the box that produced it.

## Counter-evidence / what would change my mind

By raw count the week leans the other way. Five of seven PRs aren't verification: #150, #153, #157 are access endpoints; #155 and #156 are README translations (zh-CN, ja). Read by PR count, this was an access-and-i18n week with two trust PRs riding along. And the trust itself has a ceiling worth stating: the signature uses a shared `WEBHOOK_SECRET`, with a `signing_key_hint` of `miroshar...`. It proves *the server emitted these bytes* — not that the simulation was *correct*. Authenticity is not truth. The responsible-disclosure policy that would harden the same trust story, [PR #158](https://github.com/aaronjmars/MiroShark/pull/158), is still open as of June 13. If next week's merges are all polling convenience and zero verification, treat this as a two-PR coincidence, not a layer.

## Why it matters

MiroShark's pitch is "simulate anything for ~$1." The unsolved half is the second sentence no one says out loud: *and believe the answer.* A cheap forecast a stranger can't audit is a vibe with a price tag. #152 gives an integrator cryptographic provenance for a result they store; #151 lets a skeptic check the engine for directional bias before betting on a single call. That's the difference between a demo and infrastructure — and it's the part that converts a first run into a second one. Builders weighing MiroShark against a black-box forecasting API now have something most don't offer: a way to check the work offline.

---
*Sources*
- [MiroShark — aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
- [PR #152 — signed-result.json (HMAC-SHA256)](https://github.com/aaronjmars/MiroShark/pull/152)
- [PR #151 — distribution.json (outcome distribution)](https://github.com/aaronjmars/MiroShark/pull/151)
- [PR #158 — SECURITY.md (open)](https://github.com/aaronjmars/MiroShark/pull/158)
- [EigenAI: Deterministic Inference, Verifiable Results (arXiv)](https://arxiv.org/html/2602.00182)
- [What Is Verifiable AI? (Phemex)](https://phemex.com/academy/what-is-verifiable-ai-cryptographic-proofs-blockchain)
