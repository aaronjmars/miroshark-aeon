# Push Recap — 2026-06-16

## Verdict
> MIXED — shipped a queryable per-sim cost surface + self-hosted web search, then survived a 12-PR dependency sweep that silently broke the engine.

**Shape:** 3 user-visible commits · 5 infra · 9 bot-filtered (MiroShark) · agent repo internal-only
**Volume:** 52 files changed, +3,386/−1,203 lines across 17 merged PRs by 3 authors (aaronjmars, dan-and, dependabot)
**Merged PRs:** 17 — #166 dependabot config; #167–#177 dependency bumps; #178 SearXNG/Firecrawl; #179 cost.json; #180 frontend CI; #181 camel-ai signature fix; #182 uv.lock resync

---

## Top impact today
1. `8bdaa73` — **#178 Alternative websearch/scrape via SearXNG / Firecrawl**. First *community* (dan-and) engine capability of the week: persona research can now be grounded with SearXNG snippets synthesized by the default LLM (works with local Ollama) and URL imports scraped via Firecrawl — so a self-hosted run no longer needs a websearch-capable model. Ships settings UI, a `test-searxng` endpoint, i18n prompts, and unit tests. (19 files, +1,167/−55)
2. `a52ea34` — **#179 GET /api/simulation/<id>/cost.json**. The "$1 to simulate anything" number is now machine-readable per run: headline `estimated_cost_usd` + token/latency totals + `by_model`/`by_phase`, priced off the same `MODEL_PRICING` table as the markdown report so the two can't disagree. Honest by construction — `is_estimate=true`, untracked models count as $0 (explicit lower bound). (9 files, +699/−25)
3. `446ad7b` — **#181 camel-ai 0.2.90 `_aget_model_response` signature compat**. Two-line fix, engine-critical: under the camel-ai 0.2.90 bump every `SocialAgent` step raised `TypeError: missing 1 required positional argument: 'num_tokens'`, swallowed per-agent — so simulations "completed" with **zero agent actions** and still wrote a report. A silent total failure backend CI can't catch (CI doesn't install camel-ai). After the fix, a 1-round/3-platform run produced twitter 7 posts, reddit 5 posts + 22 comments, polymarket 8 trades. (1 file, +2/−2)

---

## aaronjmars/MiroShark

### The engine kept moving — cost surface + community web search

**What this is:** Two genuinely new user-facing surfaces landed. The cost endpoint makes the headline value-prop number queryable per simulation; the SearXNG/Firecrawl integration is the first external-contributor capability in weeks and lowers the bar for self-hosted runs (no websearch-capable LLM required).

**Shipped to users**
- `a52ea34` — **#179 feat: GET /api/simulation/<id>/cost.json — per-sim cost breakdown** (Aeon-authored)
  - `backend/app/services/cost_service.py` (new): shapes the aggregate into a stable public envelope — headline `estimated_cost_usd`, token/latency totals, `by_model`/`by_phase`; flagged `is_estimate` with a `pricing_basis` note. (part of +699)
  - `backend/app/utils/run_summary.py`: extracted `_collect_llm_events()` + a pure `collect_cost_summary()` (no write/print) so the JSON surface and the markdown report price calls off one `MODEL_PRICING` table.
  - `backend/app/api/simulation.py`: new route with the same publish gate as every share surface (403 private / 404 no-calls-yet), 60s cache, surface_stats counter.
  - `backend/openapi.yaml` + `docs/API.md`: documented the surface (`CostResponse`/`CostBreakdownRow`); `backend/tests/test_unit_cost_service.py` (new) covers aggregation + the pricing lower-bound.
- `8bdaa73` — **#178 SearXNG / Firecrawl web search & scrape** (dan-and, external contributor)
  - Adds SearXNG-grounded persona research (snippets synthesized by the default LLM) and Firecrawl URL scraping, falling back to `WEB_SEARCH_MODEL` on failure; degrades gracefully when file logging is unwritable.
  - Settings UI + `test-searxng` endpoint + i18n prompts + unit tests; `MIROSHARK`-prefixed `FIRECRAWL`/`SEARXNG` env vars. Also fixes same-origin `/api` routing behind a reverse proxy and adds Traefik config + a neo4j 5.15→5.26 alignment across driver pins and docs. (19 files, +1,167/−55)

### Surviving the dependency sweep — the engine fix and the build fixes

**What this is:** Aeon's own Dependabot config (#166, merged late yesterday) opened the floodgates: 11 bumps merged today, several of them major (vite 7→8, vue-router 4→5, python 3.11→3.14, concurrently 9→10). Two of those bumps silently broke the product, and a human caught both same-day.

**Shipped to users**
- `446ad7b` — **#181 fix(wonderwall): camel-ai 0.2.90 signature compat** — the bump in #176 would have left every simulation doing zero agent actions while still emitting a report. The fix forwards model-response args via `*args` instead of the removed `num_tokens` param, so it's safe on both 0.2.78 and 0.2.90 and unblocked #176. The single most important commit of the day despite being two lines. (1 file, +2/−2)

**Infra**
- `fb7995e` — **#177 vite 7.2.7 → 8.0.16** — Vite 8's Rolldown bundler requires `manualChunks` to be a function; the object form threw `TypeError` and failed `vite build`. Human follow-up rewrote chunking as a function (same d3 / vue-vendor buckets) and bumped the Dockerfile to NodeSource Node 22 (Vite 8 needs Node ≥20.19/22.12). (4 files, +544/−681)
- `0f23339` — **#180 ci: build the frontend on every PR** — tests.yml only ran backend unit tests, so frontend dep bumps sailed through green even when the frontend wouldn't compile. Adds a `Frontend build` job (`npm ci && npm run build` on Node 22) — the gap that let #177/#175 land broken is now closed. (1 file, +22/−0)
- `63b9053` — **#182 fix: sync uv.lock with camel-ai 0.2.90** — #176 bumped camel-ai in `pyproject.toml`/`requirements.txt` but left `backend/uv.lock` at 0.2.78; both Dockerfiles run `uv sync --frozen`, which refuses a stale lockfile — so the image build was broken on main. Regenerated the lock; `uv lock --check` passes again. (1 file, +99/−96)
- `9329209` — **#168 python 3.11 → 3.14** (Dockerfile base image, dependabot).
- `3a56a19` — **#166 chore: add Dependabot config** (Aeon-authored, merged 18:38 yesterday) — covers all five dependency surfaces (backend pip, root npm, frontend npm, GitHub Actions, Docker); minor/patch grouped per ecosystem, majors individual. This is the commit that produced today's sweep.

**Bot-filtered (dependency bumps, 9):** #167 concurrently 9→10, #169 docker/build-push-action 5→7, #170 actions/checkout 4→6, #171 actions/setup-python 5→6, #172 nashpy ≥0.0.43, #173 pywebpush ≥2.3.0, #174 frontend-minor group (axios/dompurify/marked/vue/@vitejs/plugin-vue), #175 vue-router 4→5, #176 camel-ai 0.2.78→0.2.90.

---

### Internal: aaronjmars/miroshark-aeon (agent tooling)

Self-improvement only — no MiroShark product impact, out of the simulation lane (STRATEGY #5). 3 PRs merged; ~31 `chore(cron)`/`chore(scheduler)` auto-commits filtered.
- `e83f732` — #63 fix(feature): stop over-promising local pytest validation in sandbox (the 06-15/06-16 lesson that Python execution is blocked regardless of clone path).
- `c17dbcb` — #64 disable operator-scorecard; enrich repo-pulse with stargazer/forker profiles.
- `838a775` — #65 repo-pulse: surface bio, drop noisy 0/low-follower counts.

---

## Developer notes
- **New dependencies:** SearXNG + Firecrawl (self-hosted web search/scrape, optional, `MIROSHARK_`-prefixed env). Bumped: camel-ai 0.2.90, vite 8.0.16, vue-router 5.1.0, concurrently 10.0.3, python 3.14, neo4j 5.26, axios 1.18.0, vue 3.5.38, nashpy 0.0.43, pywebpush 2.3.0, plus several GitHub Actions majors.
- **Breaking changes:** Node floor raised to ≥22 (concurrently 10 + vite 8 require it; `engines.node` and the Dockerfile updated). vue-router 4→5 and vite 7→8 are majors — frontend builds now require the new toolchain.
- **New public surface:** `GET /api/simulation/<id>/cost.json` (cost breakdown); `test-searxng` settings endpoint; `MIROSHARK_FIRECRAWL_*` / `MIROSHARK_SEARXNG_*` env vars; optional Vite dev env vars documented in `.env.example`.
- **Tech debt added:** none visible in diffs. Note the latent risk pattern: camel-ai overrides (#181) and lockfile drift (#182) are both failures backend CI structurally can't catch — #180 closes the frontend half of that gap, the backend half remains.

## Open threads
- The Dependabot sweep is not fully drained — earlier logs noted ~12 bumps opened (#167–#177); confirm none remain open/red after the #177/#181/#182 fixes.
- SearXNG/Firecrawl (#178) is a strong candidate for a "prove a sim is worth trusting" worked example: a fully self-hosted, local-LLM run grounded with real web snippets at a known cost — pairs naturally with the new cost.json surface.

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok (internal/agent repo — agent-tooling PRs only)
- gh api events: not used (commits + PR list sufficient)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 9 (MiroShark dependency bumps) + ~31 (aeon chore/cron auto-commits)
- diff-truncated: 0
</content>
</invoke>
