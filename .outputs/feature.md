*Feature Built — 2026-05-23*

Polymarket-Ready Prediction JSON
MiroShark now ships a one-call adapter that turns any completed simulation into the YES/NO probability shape a Polymarket trading bot expects. A bot author can go from "simulation result" to "actionable market signal" with a single curl — no parsing of the underlying belief distribution required. This is the 15th machine-readable share surface and the first one shaped for a specific external integrator audience.

Why this matters:
The use case has precedent — MiroFish's viral 2026 breakout was driven by one documented Polymarket bot case study (2,847 simulations before trades, $4,266 profit over 338 trades). MiroShark already had `signal.json` (PR #91), but its generic `direction + confidence_pct + risk_tier` shape required every bot author to write their own adapter. This PR ships the exact format Polymarket consumes, naming the audience and removing the integration friction. Continues the explicit-audience pattern PR #83 (Discord/Slack → `@revaultdrops`) started — naming integrators turns generic surfaces into invitations.

What was built:
- `backend/app/services/polymarket_service.py` (new, ~250 LoC stdlib): `compute_polymarket` calls `signal_service.compute_signal` and reshapes its output into the 15-field Polymarket envelope. Includes `_yes_probability` (direction-aware), `_confidence_tier` (4-bucket with exclusive upper bounds), and `_suggested_market_title` (Polymarket's "Will …?" shape with truncation + redundant-prefix dedup).
- `backend/app/api/simulation.py`: `GET /<id>/polymarket.json` route — publish gate, 5-minute Cache-Control, surface_stats hook, bilingual EN/zh-CN error messaging.
- `backend/tests/test_unit_polymarket_service.py` (new): 30+ offline tests covering payload shape, direction-aware probabilities, sum-to-1.0 invariant, four-bucket confidence_tier with exclusive boundaries, market-title shaping, non-completed/missing-belief returns None, ISO-8601 UTC timestamp regex.
- `frontend/src/components/EmbedDialog.vue`: new 🎯 Polymarket prediction (JSON) section with live YES/NO preview, confidence-tier chip, suggested-title rail, copyable URL, and paste-ready `curl | jq` snippet.
- `backend/openapi.yaml` + `docs/API.md` + `docs/FEATURES.md`: full spec entry, `PolymarketPrediction` schema (15 required fields), bot-quickstart curl + Python snippet, feature documentation.

How it works:
`compute_polymarket` is a pure adapter — it calls `signal_service.compute_signal` (PR #91) and reshapes the output into Polymarket's expected envelope. `yes_probability` is direction-aware: Bullish → `bullish_pct/100`, Bearish → `1 - bearish_pct/100`, Neutral → exactly 0.5. The pair sums to 1.0 within float tolerance — the invariant a Polymarket order-book consumer expects. `confidence_tier` is a 4-bucket discrete scale (speculative/moderate/confident/high-conviction) bots use for position-sizing logic. Stricter publish gate than `signal.json`: only `status == "completed"` sims emit a payload — mid-run sims return 404 because a bot sizing positions against a still-flipping signal would chase phantom numbers. Zero new dependencies (streak: 31 PRs).

What's next:
The May-22 repo-actions batch has four other ideas unbuilt — Private Share Link (#1), French Locale closing open issue #95 (#2), Platform Stats API (#4), and Platform Stats Badge SVG (#5). The Platform Stats Badge would reuse `badge_service.py` (PR #94) exactly, and the French Locale closes a community-opened issue from the same day — both natural next picks. Adoption side: the hyperstition target for an external integrator citing one of MiroShark's now-15 publish-gated surfaces by 2026-07-04 just got a much more pointed surface to target.

PR: https://github.com/aaronjmars/MiroShark/pull/99
