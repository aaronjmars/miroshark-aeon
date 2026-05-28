# Push Recap — 2026-05-28

## Overview

Five substantive merges across two repos in the last 24h — three by @aaronjmars (two README-polish PRs late on the 27th plus one Aeon-built feature today), one by external integrator noelclaw, and one self-improving fix on the Aeon repo itself. The thrust: the integrator-facing surface (PR #120 WEBHOOK_EVENTS) and integrator-list (PR #117 Noelclaw) both expanded in the same window, and the README pivoted from a feature wall to a use-case lede before the wall — three angles on the same "make this easier to subscribe to" arc.

**Stats:** ~10 files changed, +1,037 / −49 lines across 5 substantive commits (excluding the ~14 scheduler auto-commits in `miroshark-aeon`).

---

## aaronjmars/MiroShark

### Theme 1 — Integrator-Side Surface: WEBHOOK_EVENTS Dispatch Filter (24th surface)

**Summary:** Direct continuation of PR #109 (ECOSYSTEM.md, 10+ integrators). With that many downstream consumers, "fire on every completion" stops being the right default — a Polymarket bot only wants directional + high-confidence signals, a research pipeline only wants excellent-quality runs, a Bearish-flip alerter only wants one stance. PR #120 adds an opt-in allow-list at the source so each integrator can subscribe to its own slice without writing dispatch-side filter glue.

**Commits:**
- `85890ed` — **feat: add WEBHOOK_EVENTS dispatch filter (24th surface) (#120)** — Aeon-built, co-authored aeonframework + Claude Opus 4.7.
  - `backend/app/services/webhook_service.py` (+237 / −0) — Added `WEBHOOK_EVENTS_ENV_VAR` + seven token constants partitioned into three frozensets (`_DIRECTION_TOKENS = {bullish, neutral, bearish}`, `_CONFIDENCE_TOKENS = {high_confidence, medium_confidence}`, `_QUALITY_TOKENS = {good_quality, excellent_quality}`). New `_resolve_event_filter()` reads `os.environ[WEBHOOK_EVENTS]` late-bound (same pattern as `WEBHOOK_URL` / `WEBHOOK_SECRET`). New helpers `_payload_direction()`, `_payload_confidence_pct()`, `_payload_quality_key()` derive values from `final_consensus` using the `>=` plurality rule the Discord embed colour already uses (so filter outcome matches what viewers see). Main entry point `payload_passes_event_filter(payload, events) -> (bool, trace_dict)` wired into `fire_webhook_for_simulation` between `_mark_fired` and `_start_dispatch_thread`.
  - `backend/tests/test_unit_webhook_events.py` (+454 / −0, new file, 25 tests) — Covers token normalisation, OR-within / AND-across semantics for all three categories, confidence floors (`>= 75` / `[50, 75)`), quality bucket inclusion (`good_quality` matches both good and excellent), unknown-token tolerance, failed-status bypass, no-recognized-tokens fallthrough, and end-to-end `fire_webhook_for_simulation` behaviour with and without a filter set.
  - `docs/WEBHOOKS.md` (+46 / −0) — New "Filtering events" section: token reference table, OR/AND logic, four worked examples, suppressed-delivery log behaviour.
  - `docs/FEATURES.md` (+13 / −0) — New "Webhook Event Filtering" entry with the same semantics + implementation notes.
  - `.env.example` (+19 / −0) — Documented `WEBHOOK_EVENTS=` block alongside `WEBHOOK_SECRET=`.

**Design lines (visible in the diff):**
- **OR within, AND across** — `bullish,bearish` = "any directional consensus" (skip neutral), `bullish,high_confidence` = "directional AND high-confidence". Matches what a human would expect from a comma-separated list.
- **Failed sims always fire** — explicit `status == "failed"` bypass with a `trace["bypass"] = "failed_status"` tag. The alert an operator most needs to see should never be the one a filter swallows.
- **Unknown tokens silently ignored** — recorded in `trace["ignored_tokens"]` for the log but don't affect the verdict. A typo like `WEBHOOK_EVENTS=bulish` falls through as "no recognized rules" and dispatches normally.
- **Direction derivation reuses the share-card/Discord-embed `>=` plurality rule** — same code path the visual surfaces use, so `bullish` here means exactly what viewers call bullish.
- **Suppressed deliveries log but don't write to `webhook-log.jsonl`** — log is for *attempted* deliveries; an operator inspecting the log sees only what actually shipped.
- **Manual retries bypass the filter** — same pattern as the existing dedup bypass; explicit operator-driven re-send is always honoured.

**Impact:** Pulls a class of integration logic out of every downstream consumer and back into MiroShark. The 10+ integrators ECOSYSTEM.md now lists can each subscribe to the slice they care about without writing a request-side filter. Backward-compatible — blank `WEBHOOK_EVENTS` returns the original code path byte-for-byte. Zero new dependencies (frozensets + a few helpers, all stdlib). 24th surface.

---

### Theme 2 — README Polish: Use-Case Lede + Condensed Feature Table

**Summary:** Two back-to-back PRs on the evening of 2026-05-27 from @aaronjmars (both Claude Opus 4.7 co-authored), reshaping the README's information order. The feature table had grown to ~25 rows of multi-sentence "what it does" explanations; the use cases section was buried below it. Both changes pull the reader's first signal-of-fit (use cases) above the wall of capability detail and let the wall itself scan in one pass.

**Commits:**
- `ab6d12f` — **docs: condense feature table to one-liners + add diagram images (#118)** (40+/32− on `README.md`; 3 new images).
  - Every feature row rewritten to a single concise line. Example: `Trading Signal JSON` shrank from a 3-clause sentence (direction + confidence + risk tier + components) to "`signal.json` machine-readable `direction` + `confidence_pct` + `risk_tier` for quant / Zapier / alert pipelines". 25+ rows compressed similarly.
  - Added "Simulate anything" hero banner image (`docs/images/simulate-anything.jpg`) under the tagline — visual establishing shot before the prose.
  - Added grounding + graph-memory diagrams to the screenshots row (`docs/images/grounding.jpg`, `docs/images/graph-memory.jpg`).
- `287022f` — **docs: move Use cases section above Features in README (#119)** (10+/10− on `README.md`).
  - Moved the 7-item Use cases list (PR crisis testing, Market reaction, Advertisement, Policy analysis, Life decision, What-if history, Creative experiments) from below the feature table to directly under the launch instructions, before the feature wall starts.

**Impact:** A reader scanning the README hits "is this for me?" before "what does it have?", and the "what does it have?" answer is now a scannable single-page table rather than a multi-screen scroll. Net effect on the page: hero image → quick install → what it does → who it's for → feature scan → screenshots. The two PRs are 2-minute documentation work but they reorder the funnel.

---

### Theme 3 — Ecosystem Expansion: 11th Named Integrator

**Summary:** External contributor noelclaw added themselves to ECOSYSTEM.md — the inbound integrator list created by PR #109 (NurstarK, 2026-05-26). One row of ten lists previously: AntFleet / BlueAgent / Crucible / Echo / Monitor / Nookplot / RootAI / Signa / Supercompact / Xerg. Noelclaw is the 11th.

**Commits:**
- `d4c15f0` — **feat: add Noelclaw to ecosystem (#117)** by noelclaw (Claude Sonnet 4.6 co-authored).
  - `ECOSYSTEM.md` (+1 / −0) — One row: `| Noelclaw | [@noelclawfun](https://x.com/noelclawfun) · [noelclaw.com](https://noelclaw.com) · [mcp](https://github.com/noelclaw/mcp) |`. Three artefacts — X handle, custom domain, MCP server repo on GitHub — meaning Noelclaw isn't just an end-user, they've built a MiroShark-facing MCP server (their `mcp` repo) that other agents can talk to. Same "integrator product, not just user" pattern AntFleet (miroshark-bench) set.

**Impact:** PR #109's hyperstition was that publishing the integrator list would pull more integrator self-submissions. PR #117 is the second confirmation (PR #114 from "shak" was the first, opened the same day as #109). At 11 named external integrators, the list itself is becoming load-bearing — a passive recruitment surface.

---

## aaronjmars/miroshark-aeon

### Theme 4 — Self-Improving Skill: token-report Grok Query Spam Filter

**Summary:** The self-improve skill caught a quality regression in its own token-report output: today's log noted "all 5 Grok results are spam/bot accounts, 0 engagement. No organic signal. Pattern continues from prior days." Same scam-domain pattern (arbihunter.live, toknsite.live, toknsite.club, coinmarkettcap.fun) that triggered aeon PR #47's disable of fetch-tweets + tweet-allocator on 2026-05-27. The skill rewrote its own Grok prompt to filter the spam at query time instead of consuming the cached-but-useless social section.

**Commits:**
- `5da2ba5` — **improve: token-report Grok query filters zero-engagement spam (#48)** — Aeon-built, Claude Opus 4.7 co-authored.
  - `scripts/prefetch-xai.sh` (+1 / −1, single line at ~line 187) — Replaced the token-report Grok prompt with one that instructs Grok to apply three explicit pre-filters before picking results: (1) drop tweets with zero likes AND zero retweets (dominant bot pattern in low-cap cashtag streams); (2) drop contract-drop / "vote for" / "fam drop" / "exclusive drop" templates and known clone domains (the four named spam domains plus `*.live/*.club` farms); (3) drop duplicate-template spam (same wording across multiple handles). Tells Grok to return zero results rather than fall back to spam.
  - `memory/logs/2026-05-28.md` (+18 / −0), `.outputs/self-improve.md` (+6 / −6), `memory/token-usage.csv` (+1 / −0), `dashboard/outputs/self-improve-…json` (+171, new) — Logged the PR URL, status, and rationale per the skill's contract.

**Design lines (from the commit message):**
- **Query-level filter, not post-process filter** — Grok has full tweet metadata at picking time; a post-process filter sees only what made it into `output_text` and can't re-evaluate likes / RT count / template fingerprint.
- **Stay within the existing skill contract** — `token-report/SKILL.md` Path A still parses the same JSON shape; no skill-side change needed.
- **Zero results is acceptable** — explicit "do not fall back to spam" instruction. Path B already handles the empty case cleanly ("X/Grok data wasn't available for this run").
- **Domain list is illustrative, not exhaustive** — names four clone domains and instructs Grok to extrapolate; coding a hard regex would rot weekly.

**Why this complements aeon PR #47:** PR #47 disabled fetch-tweets + tweet-allocator because spam was burning real money (the allocator paid wallets, so a spam-account-only feed = $10 to scam handles). token-report only uses the social feed as one section of a price report — spam degraded the section but didn't burn money, so the right move was filtering at the prompt level rather than disabling the skill. Different cost model, different remediation.

**Impact:** Tomorrow's 06:00 UTC token-report validates end-to-end. On days with organic signal, the Social Pulse section keeps citing real handles; on days where only spam exists, the section degrades to "X/Grok data unavailable" instead of citing scam contract drops as sentiment evidence.

---

## Developer Notes

- **New dependencies:** None across all five PRs. The 24-surface streak of zero new dependencies on MiroShark continues.
- **Breaking changes:** None. `WEBHOOK_EVENTS` is opt-in — blank or unset returns the original code path byte-for-byte. The README reorder is presentation-only. ECOSYSTEM.md is additive.
- **Architecture shifts:** PR #120 introduces the first dispatch-side filter on the outbound webhook path. The pattern (parse env into a token set, evaluate against a derived view of the payload, return `(bool, trace)`) is reusable — Discord embed / Slack Block Kit / Telegram / SMTP dispatch paths could plausibly grow the same filter knob later, though they don't have it yet.
- **Tech debt:** None introduced. Unknown-token handling and failed-sim bypass are both explicit in the test suite (lines visible in the new `test_unit_webhook_events.py`).
- **Validation gap:** PR #120's 25-test suite is authoritative but `python` is blocked in the Aeon sandbox — CI on the MiroShark repo verifies. aeon PR #48 is bash-only (single-line prompt rewrite); next 06:00 UTC token-report run is end-to-end validation.

## What's Next

- **PR #106 (Railway, external/Devin) is the only open MiroShark PR** — has now been open >7 days, was already flagged in the 2026-05-26 heartbeat as stalled. Will reappear in the next heartbeat unless triaged.
- **Webhook Test Ping (re-eligible idea #4 from 2026-05-20)** is the natural sibling to PR #120 — now that operators can filter, they need a way to test that their filter works without waiting for a real sim. Today's repo-actions batch already named it as idea #4.
- **token-report Social Pulse will need a follow-up** if tomorrow's filtered Grok run still returns 0 organic tweets for 3+ consecutive days — at that point the section is structurally dead for $MIROSHARK and "skip the section entirely when empty" is cleaner than "filter then degrade".
- **ECOSYSTEM.md self-recruitment is working** — PR #117 (Noelclaw) is the second external self-submission since the list was published 2 days ago. If the cadence holds, the "≥3 publicly-named external integrators by 2026-07-31" hyperstition is on track well ahead of deadline.
