# Push Recap — 2026-05-11

## Overview

Late-night double merge on MiroShark closed the distribution→discovery feedback loop: PR #77 wired the two newest share surfaces (`reproduce.json` from May 8 and `/lineage` from May 9) into the surface-stats counter that had been undercounting them, and PR #78 turned the now-complete counter into a public gallery sort key. Both merged within two minutes of each other at 22:39–22:41 UTC on 2026-05-10. On the aeon side, PR #33 merged at 22:43 UTC — the durable re-apply of the closed PR #32 work that caps MEMORY.md row sizes so every skill's at-task-start read stops blowing past the 25K-token Read limit. Today's autonomous run also opened MiroShark PR #79 (webhook HMAC signature verification), which is still pending review.

**Stats:** 2 substantive MiroShark merges (+253/-31 across 21 files) + 1 substantive aeon merge (+198/-60 across 4 files) + 1 new MiroShark PR opened (+692/-6 across 10 files, not yet merged) + ~30 routine aeon chore/automation commits.

---

## aaronjmars/MiroShark

### Theme 1: The distribution→discovery loop closes

**Summary:** Two PRs that should be read together. PR #77 fixes a measurement gap that was silently distorting the counter; PR #78 promotes the now-complete counter into the gallery's sort dropdown. The combined effect is that the surface-stats counter (added May 7 as PR #74) becomes the first piece of operator-facing instrumentation on this codebase that loops back into how the codebase ranks its own outputs.

**Commits:**

- `c6edeb6` — *feat: track reproduce.json + lineage in surface-stats (#77)*
  - Changed `backend/app/services/surface_stats.py` (+9, -4): added `reproduce_json` and `lineage` to the `SURFACE_KEYS` frozenset; updated the module docstring to list the two new surfaces alongside the prior nine. The frozenset is the schema lock — anything not in it cannot be incremented, so adding the two new keys is the contract change.
  - Changed `backend/app/api/simulation.py` (+14, -5): added `surface_stats.increment_surface_stat(sim_dir, "reproduce_json")` on the success path of `get_reproduce_config()` and `surface_stats.increment_surface_stat(sim_dir, "lineage")` on the success path of `get_simulation_lineage()`. Mirrors the share-card / transcript / trajectory / thread pattern — increment only after the response is successfully built, never on the error path.
  - Changed `backend/tests/test_unit_surface_stats.py` (+4, -0): extended the `SURFACE_KEYS` literal pin and the route-handler-presence parametrize to include the two new keys, so a future surface added without wiring fails CI rather than silently undercounting.
  - Changed `backend/openapi.yaml`, `docs/API.md`, `docs/FEATURES.md` (+ zh-CN mirrors), `README.md`, `frontend/src/components/EmbedDialog.vue` (+30, -8 combined): updated `SURFACE_STAT_LABELS` so the EmbedDialog renders the new counters with friendly names, and propagated the contract change into every doc surface.
  - **Why it matters:** PR #74 had already shipped the counter, but PR #75 (reproduce.json) and PR #76 (lineage) landed *after* it without wiring themselves in. An operator looking at the EmbedDialog Distribution panel was systematically reading a `total` that excluded their citation traffic and their fork-tree traffic. Without this fix, the trending sort that PR #78 ships would have ranked sims by a partial view of distribution.

- `77bb1ed` — *feat: trending sort — turn surface-stats into a discovery primitive (#78)*
  - Changed `backend/app/services/gallery_filters.py` (+36, -3): extended `SORT_VALUES` to include `"trending"`; added a `TRENDING_FIELD = "_serves_total"` module-level constant; added a `_trending_key(card)` sort function that reads the transient field, clamps non-int / negative / missing values to zero, and tie-breaks on `created_at` descending so the most-served-and-most-recent floats above the most-served-and-stale.
  - Changed `backend/app/api/simulation.py` (+27, -0): in `list_public_simulations()`, when `sort=trending`, sweep over `surface_stats.read_surface_stats(sim_dir)` for every public sim, inject the `total` as `_serves_total` on each card, then strip the transient field from `page_items` after sort+paginate so the public JSON contract is byte-identical to before. **The sweep only runs on `?sort=trending`** — the default `date` path stays read-free, so the change is performance-neutral for the gallery's hot path.
  - Changed `backend/tests/test_unit_gallery_filters.py` (+115, -1): 8 new offline tests — `trending` in `SORT_VALUES`, `TRENDING_FIELD == "_serves_total"` literal pin (rename trips CI), descending sort by serves, date tie-break, missing-field degrades to zero without raising, garbage / negative values clamp to zero, end-to-end filter+sort composition (a high-serve sim that doesn't match the q filter is excluded), all-zero corpus falls back to date order. Plus two new `normalise_sort` parametrize cases (`Trending` / `TRENDING` for case-folding parity).
  - Changed `backend/openapi.yaml` (+8, -4): extended the `sort` query enum and the response sort enum to include `trending`, with a description pointing at the surface-stats counter sum + the date tie-break rule.
  - Changed `frontend/src/views/ExploreView.vue` (+2, -1): added a "🔥 Trending" option to the sort dropdown (i18n: "🔥 热门"), extended `ALLOWED_SORT` to include the new key so `/explore?sort=trending` is URL-routable / bookmarkable. The existing `filtersActive` flag and reset-button behavior pick up the new key for free via the `sort !== 'date'` check.
  - Changed `frontend/src/api/simulation.js` (+9, -1): JSDoc on `getPublicSimulations()` documents trending semantics inline — cumulative serves, date tie-break, sims without a stats file count as zero.
  - Changed `docs/API.md` (+ zh-CN mirror), `docs/FEATURES.md` (+ zh-CN mirror), `README.md` (+6, -6 combined): sort table rows extended with trending semantics and the framing as the first distribution→discovery feedback loop.
  - **Why it matters:** Until now `/explore` sort options were structural (`date` / `rounds` / `agents`) — none reflected which sims were actually being consumed. Ranking by served-counter sum sits **downstream** of distribution: a sim has to be embedded, syndicated, cited, or re-run to tick the counter, which deliberately sidesteps the 2026 engagement-bait pathology of ranking by in-gallery clicks. The feedback loop is: a sim gets shared → its serve counter ticks → it rises in trending → more operators discover it → it gets shared again. First closed-loop primitive built on top of the `sim_dir/` substrate since the directory became the canonical store of truth.

**Impact:** Together, these two PRs finish the arc that PR #74 (May 7, the meter) → PR #75 (May 8, the citation key) → PR #76 (May 9, the navigable tree) → PR #77 (today, the wiring backfill) → PR #78 (today, the rank promotion) staged. The "distribution analytics → gallery ranking" loop is now closed end-to-end. Zero new dependencies on either PR — the 17-PR pure-stdlib streak now stands at 18 with PR #79 also drafted that way.

### Theme 2: Webhook signing primitive opened (not yet merged)

**Summary:** Today's autonomous `feature` skill picked the May 10 repo-actions idea #1 — webhook HMAC signature verification — and opened PR #79 against MiroShark. Still in review at time of recap.

**Commits:** None merged in window; PR #79 created 2026-05-11 11:29 UTC.

**Notable scope** (from PR description, not yet on main):
- `compute_signature` + `verify_signature` + `_resolve_webhook_secret` in `backend/app/services/webhook_service.py`. `_post_json` injects `X-MiroShark-Signature: sha256=<hex>` when `WEBHOOK_SECRET` env var is set; omits the header entirely when unset (backward-compatible by design).
- 8 offline tests in `backend/tests/test_unit_webhook_signature.py` — format guard, round-trip, tampered body, tampered header, empty secret, urlopen-mock integration tests for header presence/absence + retry signing.
- Docs in `docs/WEBHOOKS.md` (+ zh-CN) with Python / Node.js / curl verification snippets; "🔐 Verify webhook signatures" hint added to `EmbedDialog.vue` (collapsed by default, shows env var **name** only, never the secret value).
- +692 / -6 across 10 files; pure stdlib `hmac` + `hashlib`, zero new deps.

**Impact (pending merge):** Pairs with PR #46's outbound webhook and PR #73's webhook delivery log to close the third side of the webhook triangle — sender now signs, receiver can verify, log records the attempt. Stripe / GitHub's standard `sha256=<hex>` scheme rather than a bespoke format, so integrators already know the verification pattern.

---

## aaronjmars/miroshark-aeon

### Theme 3: The memory-index self-heal (PR #33)

**Summary:** On 2026-05-08, `MEMORY.md` had grown to 81 KB / 33K+ tokens — past the Read tool's 25K-token cap. Every skill that follows the project rule "at the start of every task, read memory/MEMORY.md" was hitting a silent Read failure and losing its high-level context. The self-improve skill noticed, opened PR #32 the same day. PR #32 was closed manually by the owner with the instruction to regenerate against current main. Yesterday's self-improve run did exactly that, and the result merged at 22:43 UTC on 2026-05-10.

**Commits:**

- `9e3f55b` — *improve(memory): cap MEMORY.md row sizes so the index stays readable (re-apply #32) (#33)*
  - Changed `skills/memory-flush/SKILL.md` (+14, -3): new **step 5** enforces per-row character caps on every flush — Skills Built ≤ 280 chars per row body, Recent Articles ≤ 220, Recent Digests ≤ 180. When promoting a new row, write one sentence + a PR number / article-file pointer; full detail belongs in `memory/logs/YYYY-MM-DD.md` and `articles/<skill>-YYYY-MM-DD.md`, never inlined into a table row. When trimming an oversized row, condense to one sentence + the same pointers — detail is not lost because daily logs carry the original write-up verbatim. **Post-flush sanity check:** `wc -c memory/MEMORY.md` and confirm under 25 KB (target under 20 KB). The step ends with a literal callout to the 2026-05-08 incident so the *why* is preserved in the skill file itself.
  - Changed `memory/MEMORY.md` (+44, -47): every row condensed to one-sentence + PR pointer; refreshed snapshot counts (1,126 stars / 224 forks), Active Targets (May 6 ATH retest at -6.7%), Next Priorities (open PRs #77, #78). File went from 81 KB / 33K+ tokens to **7.7 KB / 77 lines** — a 90% reduction. The Read tool can now read it whole, and the at-task-start memory contract is restored.
  - Added `dashboard/outputs/self-improve-2026-05-10T13-11-06Z.json` (+133, -0): the json-render spec emitted by yesterday's self-improve run for the dashboard feed.
  - Changed `.outputs/self-improve.md` (+7, -10): updated the chain-runner output marker that downstream consume-steps read.
  - **Why it matters:** This is the second time Aeon has caught and fixed a structural defect in its own memory system from inside the harness — the first was PR #29 (project-lens unsatisfiable rotation rule, 2026-05-04). The pattern is the same: a skill runs, the failure mode shows up in its own context, self-improve writes the durable fix. The closed-then-reopened path through PR #32 → PR #33 is the noisy version of that — the durable instruction the owner gave ("regenerate against current main") was carried out by the next self-improve cycle without further prompting.

### Theme 4: Routine cron + today's autonomous content

**Summary:** Day-of automation ran cleanly — token-report (new ATH session), fetch-tweets (2 new), tweet-allocator, repo-pulse, weekly-shiplog (the Sunday weekly), feature (which opened PR #79). Plus ~22 chore/scheduler commits. Nothing failed, nothing escalated.

**Notable commits (non-chore):**

- `b6f4ff6` — *chore(token-report): MIROSHARK daily report 2026-05-11 — new ATH*. Token-report flagged a new ATH session: intraday high $0.000007517 broke the prior $0.000006926 from May 6; close $0.000007107 (+10.03% 24h), FDV $710.7K, +113.5% 7d, +273% 30d. Buy/sell ratio 1.46× — strongest of the week.
- `3521fba` — *weekly-shiplog: 2026-05-11 — From Many Surfaces to a Surface Network*. The Sunday weekly covering 2026-05-04 → 2026-05-10. 1,875-word article framing the week as "prior week added 8 isolated viewer surfaces; this week converted them into a self-reinforcing observability → distribution → discovery loop." MiroShark window stats: 8 merged PRs (#71 → #78), +9,112 / -48 across 86 files, surfaces over `sim_dir/` went from 8 to 11.
- `a64b382` — *feat(fetch-tweets): 2 new tweets for $MIROSHARK 2026-05-11*. Two new mentions: @aaronjmars running a Costco-vs-BLS protein-prices sim (beef -28%, tuna +42%), and @btcbabycow posting "米罗莎 就是进化版AI预测市场 $MiroShark" — the **first Chinese-language unsolicited coverage** since the 2026-05-02 hyperstition target was set ("Chinese-locale contributor OR Chinese-language coverage by 2026-06-15"). Worth flagging.
- `759a7e6` — *chore(feature): auto-commit 2026-05-11*. Feature skill's output commit for the PR #79 work. **Tech debt note:** this commit added `sig_smoke.py` to the repo root — a 31-line scratch verifier the feature skill used to smoke-test the HMAC signing path. Same pattern as yesterday's `.aeon-tmp-verify-trending.py` (cba0b79) which is still uncleaned. The feature skill has now committed two scratch verification scripts in two consecutive days that don't belong in the repo.

**Impact:** The autonomous cron is in steady-state — zero skill failures, zero stalled PRs, zero escalations. The hyperstition tracker quietly logged its first Chinese-language $MIROSHARK mention five weeks before the deadline.

---

## Developer Notes

- **New dependencies:** None on either repo. MiroShark zero-new-deps streak now spans **18 consecutive substantive PRs** (#57 → #78 merged; PR #79 also drafted pure-stdlib, will extend the streak to 19 if it lands).
- **Breaking changes:** None. PR #77 extends the `SURFACE_KEYS` frozenset (additive). PR #78 adds a new `sort` enum value (additive). PR #79's HMAC header is opt-in via `WEBHOOK_SECRET` env var — omitted entirely when unset, so existing integrators see byte-identical traffic.
- **Architecture shifts:** The `sim_dir/` substrate now has a complete observability surface — every share endpoint writes its own counter, and the counter sum is a sort key. This is the first feedback loop on this codebase that uses operator-side measurements to rank operator-side outputs.
- **Tech debt:** `sig_smoke.py` (committed today by the feature skill) and `.aeon-tmp-verify-trending.py` (committed 2026-05-10) — both scratch verifiers committed to repo roots. The feature skill needs guidance to clean up its own scratch files before commit, or write them under a gitignored path. Flag for a `skill-repair` or `self-improve` cycle.

## What's Next

- **PR #79** (webhook HMAC) is the only open MiroShark PR — pending merge. CI should be quick (8 offline tests, pure stdlib).
- **Hyperstition tracker:** the Chinese-language coverage hyperstition (set 2026-05-02 for 2026-06-15) just got its first organic mention via @btcbabycow today. Five weeks ahead of deadline. Worth noting on the next memory-flush as a status change.
- **No stalled work visible** — the surface-stats arc is structurally complete. Next repo-actions ideas in the queue: #2 Jupyter Notebook Export, #3 Trading Signal JSON, #4 Per-Agent Stance Sparklines, #5 Simulation Archive Bundle (from the May 10 batch).
- **Memory-index health:** PR #33's per-row caps + post-flush `wc -c` sanity check land in `memory-flush`'s next Sunday run. The structural fix is durable now.
