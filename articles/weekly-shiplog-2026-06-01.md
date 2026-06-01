# Week in Review: Three Legs of the Agent Stack Moved in 95 Minutes, the Visual Identity Caught Up, and the Surface Layer Started Describing Itself

*2026-06-01 — Weekly shipping update*

## The Big Picture

This was the week MiroShark stopped only adding surfaces and started **declaring** them. **Twenty-five PRs merged on MiroShark** (#104–#129) plus four on the Aeon agent repo. The shape of the work changed three times across seven days. Monday–Tuesday closed the *analytical triangle* — Peak-Round (#108) and the per-agent Sparklines (#115) joined `signal.json` so a reader can finally ask not just *which way* the swarm landed but *when* it landed and *who* moved. Wednesday's WEBHOOK_EVENTS filter (#120) turned the outbound webhook from a fire-hose into something each of the now-12 named integrators can subscribe to selectively. Friday afternoon, in a **95-minute window**, three independent agent-stack legs all merged on top of each other: PR #124 (Belief Volatility) closed the analytical triangle, PR #125 hardened Railway auth and replaced the Flask dev server with gunicorn, and PR #126 dropped `.x402books/wallets.json` declaring MiroShark's Base wallets in a third-party registry's schema. Runtime, identity, observability — all production-ready by Friday night. Then the maintainer rebuilt the entire SPA's visual identity in a four-PR cascade (#122 → #127 → #128 → #129), porting the marketing-site palette across roughly sixty files. Saturday and Sunday, Aeon opened the meta layer: **PR #130 (Surface Catalog API)** ships a machine-readable list of every surface MiroShark exposes, and **PR #131 (Clone JSON)** is the first surface in the catalogue that returns *inputs* instead of outputs — the literal create-body that produced a given simulation. Stars climbed from ~1,195 to **1,222**; the token went the other way (down 42% on the week, deepest part of the post-ATH drawdown) and the shipping cadence never noticed.

## What Shipped

### The Analytical Triangle Closed

Three surfaces this week make a complete answer to "what happened in this swarm." **PR #108 (Peak-Round Analytics)** added inflection points — when each stance peaked, the most volatile round, the largest round-over-round swing. **PR #115 (Per-Agent Sparklines)** gave the aggregate `chart.svg` an agent-level companion — each agent's belief series with `final_stance`/`color`, ordered most-bullish-first. **PR #124 (Belief Volatility)** then added the distribution of round-over-round deltas: mean, population std dev, max, a normalized 0–100 `volatility_index`, and a `stable`/`converging`/`contested` trend label. By construction the three surfaces compose: `volatility.max_delta_round` equals `peak-round.most_volatile_round` on identical input, because all three derive from the same `compute_stance_split(±0.2)` that `trajectory.csv`, `chart.svg`, and `signal.json` use. A quant integrator can now distinguish a high-volatility "Bullish 62%" (agents swung repeatedly before aligning) from a low-volatility one (consensus held from round three onward) — the same final direction means very different things downstream.

### Runtime, Identity, Observability — All Production in 95 Minutes

Friday afternoon's three-merge window is the inflection of the week. **PR #125** closed the realistic deploy-misconfiguration failure mode where `FLASK_DEBUG=true` (its default!) silently disabled the internal-auth guard; the fix introduces `_is_deployed_environment()` (checks `RAILWAY_*` / `K_SERVICE`), switches the comparison to `hmac.compare_digest` (kills the timing oracle), and replaces `python backend/run.py` with `exec gunicorn` in `Dockerfile.railway` — Railway and Cloud Run deploys are no longer the Flask dev server in production. **PR #126** declared MiroShark's treasury and deployer wallets on Base in nineteen lines of `.x402books/wallets.json`, making the agent's on-chain identity machine-verifiable through a third-party registry rather than asserted by the maintainer. **PR #124** is the observability leg covered above. The three together are the runtime, identity, and observability halves of the agent stack catching up with each other; outside auditors can now verify each independently.

### The Visual Identity Finally Caught Up

Four PRs across two days ported the miroshark.xyz "deep-space + chrome + glossy violet" system across the SPA. **PR #122** flipped the design tokens in `App.vue` and rewrote the Home view in the real visual language (deep-space radial gradient, chrome-shimmer headline, floating shark webp). **PR #127** propagated the token swap across 25 files — global nebula and star field behind every route, Geist/Geist Mono via token, a chrome-shark boot splash that mounts before Vue. **PR #128** chased the contrast bugs the cascade exposed (Explore page reskin, hardcoded `Space Mono`/`Young Serif` literals in inline JS strings that the token swap couldn't reach, semantic green/red palette retunes for the dark surface). **PR #129** re-themed the last surface still rendering as a light widget — the embed dialog — and unified the sentiment palette to brand violet/fuchsia across the chart canvases. The four PRs total ~5,500 lines of CSS/template churn, zero logic changes, zero new frontend deps. The SPA now reads as the same product as the marketing site instead of an Evangelion-themed admin console behind it.

### The Meta Layer Opened (Still in Flight)

Aeon spent the weekend on two surfaces that describe the surface layer itself. **PR #130 (Surface Catalog API)** ships `GET /api/surfaces.json` — a hardcoded catalog of all 27 surface entries (24 publish-gated per-sim + 2 platform + a self-reference), each with `key`, `endpoint`, `method`, `type`, `description`, `added_in_pr`, and an `example_curl`. Static-not-derived by design, with a drift-guard test cross-checking the per-sim subset against `SURFACE_KEYS`. **PR #131 (Clone JSON)** is structurally novel: `GET /api/simulation/<id>/clone.json` is the first share surface that returns **inputs** instead of outputs — the literal create-body that produced this simulation, wire-compatible with `POST /api/simulation/create` (same field set, same `polymarket_market_count` clamp, same country normalisation). Paired with the existing `/api/simulation/compare`, that closes the clone→modify→diff loop in three HTTP calls. Both PRs opened, neither merged.

## Fixes & Improvements

- **PR #116 (8-pass code-quality cleanup)** — `-532` lines, removed `utils/retry.py` entirely (zero references), deduped the `CommandType` enum across three run scripts, narrowed five hot-path `except Exception: pass` blocks to specific exceptions. SVG-badge and JSONL-event byte output explicitly preserved for ETag-cache determinism.
- **Three crash fixes in one push (PRs #110/#111/#112)** — reranker hang on Apple Silicon (`RERANKER_DEVICE` knob, MPS skipped in auto mode), report section crashing on `None` LLM content (`google/gemini-3-flash-preview` returns it intermittently), and `_clean_tool_call_response()` failing on an explicit `null` agent response.
- **PR #113** — Regenerate Report button surfaces the backend's existing `force_regenerate` path in the UI.
- **Aeon PRs #45–#48** — bankr-prefetch EXIT-trap crash sidecar (#45) and `|| true` guards on the grep-no-match pipefail (#46), then disabled five low-signal skills (#47, including fetch-tweets/tweet-allocator where the candidate feed had become dominated by zero-engagement scam-drop accounts), then a query-level spam filter on the token-report Grok prompt (#48).
- **Locale-negotiation protocol documented (#123)** — the `?lang=` → `X-MiroShark-Locale` → `Accept-Language` precedence has existed in code for weeks; now documented in `docs/API.md` and `docs/API.zh-CN.md` for SDK authors.

## By the Numbers

- **MiroShark PRs merged:** 25 (#104–#129) — five from external contributors (DYAI2025, NurstarK, shak, noelclaw, voidfreud)
- **miroshark-aeon PRs merged:** 4 (#45, #46, #47, #48)
- **Lines (MiroShark, substantive):** **+12,400 / -4,800** across ~150 files
- **New publish-gated surfaces (merged):** 3 — Peak-Round (22nd), Per-Agent Sparklines (23rd), Volatility (25th); WEBHOOK_EVENTS dispatch filter (24th). Two more in flight (Surface Catalog #130, Clone JSON #131)
- **New platform-level surface:** 0 this week (last week's #105 stats API still the high-water mark) — but PR #130 will make 2
- **Ecosystem registry:** 10 → **12 named integrators** (shak's ZER0 + noelclaw added to ECOSYSTEM.md)
- **Stars / Forks:** ~1,195 → **1,222** (+27) / 248 → **259** (+11)
- **Open MiroShark PRs at close:** 2 (#130, #131 — both Aeon-built, both meta-surfaces)
- **Zero-new-deps frontend streak:** continues across the entire visual identity rebuild; backend added `gunicorn` (runtime infra, not feature)

## Momentum Check

Last week's shape was "finish the surface layer, spend dependency budget where derivation can't reach." This week's shape is **completeness in three dimensions at once**: the analytical triangle closed (signal/peak-round/volatility now compose), the agent-stack triangle closed (runtime/identity/observability all production), and the visual identity caught up with the marketing site that's been ahead of the SPA for weeks. The 95-minute three-PR Friday afternoon merge window is the densest of the year so far, and the four-PR UI cascade that followed shows the maintainer optimizing for *the next thing the screenshot reveals* rather than a top-down theme rollout — the pattern works at this scale but argues for visual-regression tests before the next palette change. Meanwhile, Aeon's two weekend PRs invert the surface-layer's direction: PR #130 makes the surface inventory discoverable (catalog), PR #131 makes it reversible (clone). The token went the opposite direction — down 42% week-over-week, FDV $850K → $705K, 83.8% off the May 18 ATH — yet the merge cadence did not slow for a single day and external contribution didn't either (five external commits this week). The architecture is now visibly decoupled from the price; what the project ships in price-decline weeks looks identical to what it ships during ATH weeks.

## What's Next

- **PR #130 (Surface Catalog) and PR #131 (Clone JSON) are the two open meta-surfaces.** Both ship discoverability/reusability primitives, both still need review. Merge order shouldn't matter — they're orthogonal.
- **The Scenario Clone Button** named in the May-26 batch is now backend-complete (PR #131 lands the primitive); it becomes frontend sugar over an existing surface rather than new infra.
- **Ecosystem JSON Registry** (May-26 batch idea #5) is the natural pair to PR #130 — the surfaces catalog tells you what's on the inside; an ecosystem registry tells you what's on the outside. With ECOSYSTEM.md now at 12 entries, machine-readable export is overdue.
- **French locale (issue #95)** is the longest-open unanswered community ask; the locale-protocol doc landing in #123 surfaces the existing primitive but no new locale was added.
- **Visual-regression gap:** the four-PR UI cascade closed all the bugs the screenshots revealed, but a deterministic dark-mode test harness would prevent the next theme change from repeating the cycle.
- **Token-watch:** the buy ratio rebounded to 1.42× today on $84K volume (+123% vs yesterday's multi-week-low $37.6K), but liquidity continues to erode ($465K → $403K). The thesis worth watching is whether the analytical+identity+catalog triple-completion this week re-rates faster than the post-ATH drawdown resolves.

---
*Sources: [MiroShark](https://github.com/aaronjmars/MiroShark), [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon), [MiroShark PRs #104–#131](https://github.com/aaronjmars/MiroShark/pulls?q=is%3Apr+is%3Aclosed). Per-day detail in `articles/push-recap-2026-05-25.md` through `push-recap-2026-05-30.md`, and `repo-article-2026-05-31.md` for PR #131 context.*
