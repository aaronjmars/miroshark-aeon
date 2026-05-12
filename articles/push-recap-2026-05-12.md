# Push Recap — 2026-05-12

## Overview

Two MiroShark PRs merged in the same window, back-to-back arcs both **first-of-their-kind**: PR #79 closed transport security (HMAC-signed webhooks, the first surface whose check runs on recipient hardware), and PR #80 opened a second institutional-targeted artifact (a pre-populated Jupyter notebook, the second "ready-to-run" export after `trajectory.csv`). On the aeon side, the agent shipped its 2026-05-12 `repo-actions` batch (5 new ideas for what to build next) and opened PR #34 — self-improvement work cleaning up a behavioral pattern the agent itself caught yesterday (the `feature` skill was leaking scratch verifier `.py` files to repo root on consecutive days).

**Stats:** 21 files changed, +2,128 / -9 lines across 2 merged MiroShark PRs (#79 + #80) + 1 open aeon PR (#34) + the agent's daily skill output commits.

---

## aaronjmars/MiroShark

### Theme 1: Institutional-Researcher Surface Lands (PR #80, Jupyter Notebook Export)

**Summary:** `GET /api/simulation/<id>/notebook.ipynb` now returns a pre-populated nbformat 4 Jupyter notebook with the trajectory CSV embedded directly inside the file and a 7-cell analysis sequence already scaffolded around it: markdown header → imports → CSV load via `pd.read_csv(io.StringIO(...))` → belief-evolution line chart → final-consensus bar chart → quality + participation summary DataFrame → markdown footer with SHA-256 of the embedded trajectory. The notebook is **standalone-runnable** — anyone with the `.ipynb` file can hit Run All in an air-gapped JupyterLab, VS Code, or Colab kernel and produce the analysis without any network call back to the MiroShark host. This is the second institution-targeted export after `trajectory.csv`: the CSV told analysts *"here is the data"*, the notebook tells them *"here is the analysis, ready to run."*

**Commits:**
- `1d1865d` — feat: Jupyter notebook export — analysis-ready surface for institutional researchers (#80) — merged 2026-05-12 12:35 UTC
    - New file `backend/app/services/notebook_export.py` (+559 lines): pure-stdlib (`json` + `os` + `hashlib`) notebook builder. `SCHEMA_VERSION = "1"`, a `CELL_ORDER` constant pinning the 7-cell layout so a refactor cannot silently reshuffle, `build_notebook()` returns the dict, `render_notebook_bytes()` serializes with `sort_keys=True + indent=2 + trailing newline` so two exports of the same finished simulation produce bytewise-identical notebooks. Reuses `trajectory_export.build_rows` + `trajectory_export.render_csv` so the embedded CSV bytes match what `trajectory.csv` serves exactly — SHA-256 hashes line up across the two surfaces. Reuses `repro_export.build_repro_config` for header metadata.
    - Modified `backend/app/api/simulation.py` (+108 lines): new `get_notebook_ipynb` Flask route, publish-gated (404 if not public, 403 if not yet published), `Content-Disposition: attachment; filename="miroshark-<id12>-notebook.ipynb"`, `Cache-Control: public, max-age=300` matching the `reproduce.json` cache window, `application/x-ipynb+json` mimetype. Same 4-step retrieval pattern: load summary → check `is_public` → fetch sim state from `SimulationManager` → build CSV + repro config → render notebook bytes.
    - New file `backend/tests/test_unit_notebook_export.py` (+427 lines): 20 offline unit tests pinning schema (no nbformat 5+ leak through), cell-order invariants, nbformat shape, CSV embed round-trip via `ast.literal_eval`, pathological-quote/backslash round-trip (the CSV is embedded as a Python string literal via `repr()` so safety matters), deterministic bytes, full JSON round-trip, missing-blob graceful degradation, counterfactual lineage in header metadata, surface key registration, route + import + openapi + schema wiring guards.
    - Modified `backend/app/services/surface_stats.py` (+3 / -1 lines) + `backend/tests/test_unit_surface_stats.py` (+2 lines): `notebook_ipynb` added to `SURFACE_KEYS` frozenset so the counter accepts the new key (was previously rejected as unknown).
    - Modified `backend/openapi.yaml` (+63 lines): new path entry under "Publish & Embed" tag with full description, parameter ref, 200/403/404 responses, `application/x-ipynb+json` schema, `miroshark` metadata block schema documented.
    - Modified `frontend/src/api/simulation.js` (+30 lines): `getNotebookUrl(simId)` helper returning the absolute URL.
    - Modified `frontend/src/components/EmbedDialog.vue` (+90 lines): new 📓 Jupyter notebook panel in the Distribution section. Pure-download UX (no inline preview — the .ipynb body is 30+ KB JSON the SPA shouldn't pull just to render a button). Curl snippet, Copy URL button, download anchor, bilingual (en + zh-CN) labels matching the rest of EmbedDialog.
    - Modified `docs/FEATURES.md` (+25 lines) + `docs/API.md` (+12 lines) + `README.md` (+2 / -1 lines): "Jupyter Notebook Export" feature section, endpoint row in the Publish & Embed API table, README feature table row.

**Impact:** This is the 11th publish-gated surface over `sim_dir/` and the 2nd specifically aimed at institutional / academic observers (the 1st was `reproduce.json`, also citation-hash-friendly). The "open in JupyterLab → Run All → see the analysis" path now takes zero boilerplate-writing, which is the exact friction researchers cited when MiroShark surfaces first showed up in academic threads. The bytewise-stable export means a notebook hash is a stable citation key — same property `reproduce.json` has, the property paper-appendix references need. Zero new dependencies: the chart code cells are *strings* (Matplotlib is referenced inside the cells the analyst runs, never imported at generation time), preserving the now-19-deep zero-new-deps streak.

### Theme 2: Transport-Layer Security Goes Live (PR #79, Webhook HMAC Signing — merged from yesterday's draft)

**Summary:** Yesterday's draft landed: `WEBHOOK_SECRET` env var, when set, causes every dispatched webhook payload to be signed with `hmac-sha256(secret, body_bytes)` and the digest shipped as the `X-MiroShark-Signature: sha256=<hex>` header on every POST — auto-fire, retry, and "Send test event" all share the dispatch path so all three sign consistently. Backward-compatible by design: blank secret → header omitted entirely, existing Slack/Discord/Zapier/Make/n8n integrations untouched. Same scheme Stripe and GitHub use; recipients verify in three lines of stdlib `hmac` on the receiving end.

**Commits:**
- `ca41c62` — feat: webhook HMAC signature verification (X-MiroShark-Signature) (#79) — merged 2026-05-11 23:36 UTC
    - Modified `backend/app/services/webhook_service.py` (+85 / -6 lines): three new public functions — `_resolve_webhook_secret` (late-binding read of the env var so a Settings change takes effect immediately, mirrors `_resolve_webhook_url`); `compute_signature(payload_bytes, secret=None)` returns `f"sha256={digest}"` or `None` if no secret; `verify_signature(payload_bytes, header_value, secret)` for constant-time receiver-side checks via `hmac.compare_digest`. `_post_json` injects the header only when `compute_signature` returns non-None. Signature covers **raw body bytes** — recipients must verify before parsing JSON because re-serializing can reorder keys / change whitespace and break the digest.
    - New file `backend/tests/test_unit_webhook_signature.py` (+312 lines): 8 offline tests — format guard (`sha256=<64 hex>`), round-trip, tampered body fails verification, tampered header fails verification, empty secret → no header, header present when secret set (urlopen-mock integration), header absent when secret unset, retry dispatch carries its own signature (each delivery signs its own body, including the `retry: true` field).
    - Modified `backend/openapi.yaml` (+8 lines): `WebhookDeliveryEntry` description gains a "Note on HMAC signing" callout explicitly flagging the header as **transport-only** — only `url_masked` is persisted to disk; neither the secret nor the signature value lands in the delivery log.
    - Modified `docs/WEBHOOKS.md` (+65) + `WEBHOOKS.zh-CN.md` (+65): parallel "Verifying webhook signatures" sections with Python / Node.js / curl snippets, header table refreshed, security notes calling out transport-only behavior.
    - Modified `docs/FEATURES.md` (+13) + `FEATURES.zh-CN.md` (+13): "Webhook Signature Verification" section added beneath "Webhook Delivery Log".
    - Modified `frontend/src/components/EmbedDialog.vue` (+119 lines): 🔐 "Verify webhook signatures" hint beneath the Retry button, collapsed by default, appears only after a successful delivery, shows env var NAME only — never the secret value.
    - Modified `README.md` (+2) + `.env.example` (+10): feature-table row, `WEBHOOK_SECRET` documented with a `token_hex(32)` generation hint.

**Impact:** This is the first MiroShark surface whose verification step runs on the **recipient's hardware** rather than on Aaron's instance. Eleven prior surfaces (gallery, share, embed, reproduce.json, lineage, webhook log, surface-stats, trending, notebook) are all served *from* MiroShark — the trust model is implicit-in-the-domain. PR #79 inverts that: the integrity check is a constant-time hmac comparison on the receiver. Structural twin of `reproduce.json` (PR #75): the repro blob made *content* citable (SHA-256 over bytewise-stable JSON); PR #79 makes *transport* citable (HMAC-SHA-256 over raw body bytes). Both are SHA-256 over deterministic bytes; both are verifiable without trusting the server. Now-live integrations (Revault, CancerHawk) can adopt incrementally — set the secret, header appears, verify or ignore on receipt.

---

## aaronjmars/miroshark-aeon

### Theme 3: Repo-Actions Batch — Five New Ideas Aimed At The Integration Tail (`5954e49`)

**Summary:** The `repo-actions` skill ran on aaronjmars/MiroShark and produced five new build-candidate ideas, targeting the integration / discovery / SEO end of the platform now that the analysis-export and transport-security gaps are closed. The new ideas explicitly avoid the last 7 days of already-batched ideas (Python Client SDK, Director Event Timeline, Comparative Run from May 6; oEmbed, Peak-Round, Operator Profile from May 8; Trading Signal JSON, Per-Agent Sparklines, Simulation Archive from May 10 — of those, HMAC signing → PR #79 and Jupyter notebook → PR #80 already shipped).

**Commits:**
- `5954e49` — feat(repo-actions): 2026-05-12 batch — lifecycle webhooks, embed widget, filtered feed, round API, sitemap
    - New file `articles/repo-actions-2026-05-12.md` (+101 lines): the five ideas, each scoped Small, each zero-new-deps:
      1. **Simulation Lifecycle Webhooks** — granular event subscriptions (`started`, `consensus_reached`, `quality_milestone`, `round_complete`) via a `WEBHOOK_EVENTS` env var. Reasoning: live integrations (Revault, CancerHawk) get MiroShark webhooks today, but only on *completion* — they want mid-run events. Webhook + HMAC infrastructure is in place; event vocabulary is the gap.
      2. **Interactive Embed Widget** — `GET /embed/<id>` no-chrome iframe with live belief bars for Substack / Notion / Ghost. Reasoning: the share card is a static PNG (PR #42), the GIF is animation (PR #50), the watch page is a full SPA. The lightweight live `<iframe>` for the platforms that allow iframes but not the SPA router is missing.
      3. **Filtered RSS/Atom Feed** — `?consensus=&quality=&sort=` query params on the existing feed using the same `gallery_filters.py` logic the gallery search uses.
      4. **Per-Round Belief Snapshot API** — `GET /api/simulation/<id>/round/<n>` addressable round-level belief state + post samples. Enables tools that quote a specific round.
      5. **Sitemap.xml for Published Simulations** — auto-regenerated XML sitemap of every public sim's `/share/<id>` and `/watch/<id>` URL for Google Search Console.
    - Modified `memory/logs/2026-05-12.md` (+14 lines): logging entry with snapshot + signals + idea-exclusion list.

**Impact:** This is the seed for tomorrow's `feature` skill run. Idea #1 (Lifecycle Webhooks) is the natural next-step after PR #79 — it leverages the HMAC infrastructure that just landed and answers the explicit ask from live integrations. Idea #5 (Sitemap) is a compounding-over-time SEO move: each published sim becomes a Google entry point. The batch reflects the agent recognizing momentum points (back-to-back PRs in one day) and biasing toward ideas that build *on* that momentum rather than reset the focus.

### Theme 4: Self-Repair — Feature Skill Stops Leaking Scratch Verifiers (PR #34, OPEN — not yet merged)

**Summary:** Yesterday's push-recap flagged tech debt: the `feature` skill had committed scratch HMAC verifier `.py` files to the agent repo root on two consecutive days (`.aeon-tmp-verify-trending.py` on May 10, `sig_smoke.py` on May 11). The pattern repeats because chain-runner does `git add -A && git commit` and the `feature` skill's prompt doesn't specify where throwaway verifier scripts should live, so they land in cwd. Today the `self-improve` skill picked this up, opened PR #34 to fix it.

**Commits / changes (open on `improve/feature-scratch-cleanup`, head `08491e4`):**
- Removed `sig_smoke.py` (−31 lines), `_smoke_webhook.py` (0), `.aeon-tmp-verify-trending.py` (−58 lines) — three dead Python files that had been writing probe scripts targeting `/tmp/build-target/backend` but living in the agent repo cwd.
- Modified `skills/feature/SKILL.md` (+7 lines): step 6 gains a "Scratch / verifier scripts — repo root is OFF-LIMITS" block. Lists past leak filenames as concrete examples, mandates `/tmp/verify-${feature}.py`, requires a pre-finish `ls *.py .*-tmp-* _smoke_*.py sig_smoke.py` cleanup check, and reminds that all file edits should target `/tmp/build-target/` not cwd.
- Modified `.gitignore` (+8 lines): safety net against future drops — patterns for `.aeon-tmp-*.py`, `_smoke_*.py`, `sig_smoke.py`, etc., so even if the prompt change doesn't catch every variant, git won't pick them up.

**Impact:** Behavioral pattern caught from two consecutive days of identical evidence — neither slip alone would have triggered this. The fix is two-layer (prompt change + .gitignore) because the prompt-only fix can fail open (skill ignores the rule), while the .gitignore alone can also fail (different filename pattern). Both layers together mean the bug needs *two* independent failure modes simultaneously to recur. This is the third aeon self-repair this week (PR #28 hyperstitions header, PR #29 project-lens angle rotation, PR #31 heartbeat header-line, PR #33 MEMORY.md row caps re-apply, now PR #34 feature-scratch cleanup). PR #34 not yet merged at recap time.

### Theme 5: Daily Cron Steady-State

**Summary:** Routine daily skill outputs landed without incident — but two of them recorded notable signals worth lifting up.

**Commits:**
- `97186b9` — chore(token-report): $MIROSHARK daily report 2026-05-12
    - **Big move:** Price $0.00001278 (+76.1% 24h), new intraday ATH **$0.0000160** nearly doubles prior ATH of $0.000007517 set yesterday. FDV $1.28M — **crossed the $1M milestone** for the first time. Volume $636.5K (+1,109% vs yesterday's $52.6K session). Buy/sell ratio 1.69× (highest in dataset). 7d: +266%; 30d: +634%.
- `05e3138` — chore(fetch-tweets): 8 new $MIROSHARK tweets for 2026-05-12
    - @Whale_AI_net (21L/6RT): "$100K → $700K, the adoption is getting real."
    - @Mnosh06 (17L/4RT): deep tech breakdown — names Revault (sneaker market intelligence using MiroShark for predictions) + top 10 oosmetrics RL listing + multi-agent sims on $DRB + upcoming public cloud + aeon-framework features (skill chaining, contributor-spotlight, swarm v4). This is the most substantive third-party tech writeup yet.
    - @btcbabycow (0L): reply to @miroshark_ — "你们可以合作" (Chinese: "you can collaborate"). Second consecutive day of Chinese-language $MIROSHARK engagement (yesterday: "米罗莎 就是进化版AI预测市场"). Hyperstition: Chinese-locale contributor or coverage by 2026-06-15 — signal continues to accumulate 5+ weeks ahead of deadline.
- `25dc331` — chore(cron): repo-pulse 2026-05-12 — 1134 stars (+3), 224 forks (0 net) — three new stars (AIGoose, ajmz, Zniniz).
- `5a7f4de` — tweet-allocator: $10.00 distributed to 5 wallets ($4.29 @Whale_AI_net, $3.19 @Mnosh06, $0.99 / $0.99 / $0.54 to remaining wallets).
- Yesterday's tail commits (also in window): `0880de2` project-lens ecosystem-map (#8 angle, four-neighborhood AI forecasting stack mapped), `cc2f6a1` push-recap article auto-commit, `a6eea51` repo-article auto-commit ("The First Surface MiroShark Doesn't Own"), `3d86a78` heartbeat HEARTBEAT_OK.

**Impact:** Two simultaneous signals are converging — token momentum (ATH doubled in 24h, FDV crossed $1M, volume up 11x) and external technical attention (@Mnosh06's deep-tech writeup is the most detailed third-party MiroShark coverage to date, named two live integrations by name). The repo-actions batch's bias toward integration-tail ideas (lifecycle webhooks specifically) aligns with the @Mnosh06 framing — Revault and CancerHawk are doing the kind of mid-run multi-agent work that would benefit most from the granular event vocabulary idea #1 proposes.

---

## Developer Notes

- **New dependencies:** Zero on the MiroShark side. The streak is now **20 consecutive zero-new-deps substantive PRs** (#57 → #80 merged). Both PR #79 and PR #80 went pure stdlib (`hmac` + `hashlib` for #79; `json` + `os` + `hashlib` for #80).
- **Bytewise-stable export pattern propagation:** PR #80 picks up the same `sort_keys=True + indent=2 + trailing newline` trick PR #75's `reproduce.json` introduced. Two surfaces now produce citation-hash-friendly bytes: the repro config and the notebook. Pattern is becoming a project convention rather than a one-off.
- **Cell-order pinned as a public contract:** `CELL_ORDER` in `notebook_export.py` + a dedicated test in `test_unit_notebook_export.py` lock the 7-cell sequence. Downstream tools that pin "the chart cell is at index 4" won't break on a future refactor. Worth pointing out because it's a contract the *file format* now enforces, separate from the API schema.
- **Transport vs. content signing:** PR #79 (HMAC, signs body bytes) + PR #75 (`reproduce.json`, SHA-256 of body bytes) now form a matched pair — both verifiable on receiver hardware without trusting Aaron's instance. Architecture pattern: "anywhere a byte stream leaves MiroShark, the receiver should be able to prove its provenance without re-fetching."
- **Tech debt cleared:** Two days of scratch-verifier-leak (`.aeon-tmp-verify-trending.py`, `sig_smoke.py`, `_smoke_webhook.py`) being addressed by PR #34. New tech debt: PR #34 itself not yet merged — needs a merge to actually close the loop on the prompt + gitignore patch.
- **Architecture shifts:** None — all four changes (PR #79, PR #80, PR #34, repo-actions batch) extend existing patterns rather than introduce new ones. The 20-PR zero-new-deps streak is a sign these have all been additive, not refactor-driven.

## What's Next

- **MiroShark PR #81 candidate:** Idea #1 from today's batch — Simulation Lifecycle Webhooks (`started`, `consensus_reached`, `quality_milestone`, `round_complete`). It's the natural next step: PR #79's HMAC infrastructure makes the mid-run event stream verifiable; PR #80 confirms the institutional-researcher target audience; @Mnosh06's writeup names the live integrations (Revault, CancerHawk) that will consume the mid-run events. The webhook service, dispatch path, and signing layer are all in place — only the event vocabulary is missing.
- **aeon PR #34 merge:** The feature-skill scratch-verifier cleanup needs to merge before the next `feature` skill run, or the leak pattern will repeat for a third consecutive day. Open as of 2026-05-12 13:19 UTC.
- **Watch for:** Chinese-locale engagement is hitting two consecutive days. Hyperstition deadline 2026-06-15 — the @btcbabycow "你们可以合作" thread is an explicit collaboration invitation; worth tracking whether it converts to an issue or PR.
- **$MIROSHARK at FDV $1.28M, ATH $0.0000160:** The momentum is now visible to second-tier crypto Twitter (@cryptallergy, @WazzupCrypto, @Whale_AI_net all posted today). Watch for the next leg up or a cool-off retest of yesterday's $0.000007517 prior ATH.
- **Branches without merged PR:** `improve/feature-scratch-cleanup` (PR #34, open). No stale MiroShark branches.
