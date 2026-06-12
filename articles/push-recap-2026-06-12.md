# Push Recap — 2026-06-12

## Verdict
> SHIPPING — `/api/surfaces.json` gains a `?type=` category filter for integrators.

**Shape:** 1 user-visible commit · 1 internal · 1 infra · 32 bot-filtered
**Volume:** 14 files changed, +341/−41 across 3 meaningful commits by 2 authors (auto-commit churn excluded)
**Merged PRs:** 2 (#157 filter surfaces.json by type; #60 validate feature diffs before shipping)

---

## aaronjmars/MiroShark

### Surface catalog gets a server-side category filter

**What this is:** Integrators polling `GET /api/surfaces.json` can now ask for a single category server-side (`?type=analytics`) instead of pulling the whole catalog and filtering client-side with `jq`. Narrow consumers transfer fewer bytes and get their own cache entry per category. It's the server-side promotion of a filter that the catalog and `FEATURES.md` already documented as client-only.

**Shipped to users**
- `0a575db` — feat: filter /api/surfaces.json by surface type via `?type=` (#157)
  - `backend/app/api/surfaces.py`: the route now reads `request.args.get("type")`, strips/lower-cases it, and routes on the value — empty/whitespace is treated as absent (full catalog, unchanged), an unrecognised value returns `400` with the list of valid categories rather than silently emptying the catalog, and a valid value narrows the response (+42/−9)
  - `backend/app/services/surfaces_catalog.py`: adds `is_valid_surface_type()` (validates against the `SURFACE_TYPES` set), threads an optional `surface_type` through `build_response_payload()` (filters `surfaces`, sets `count` to the filtered length, envelope shape unchanged), and extends `catalog_etag()` to append the category — so `surfaces-v1-30-analytics` never collides with the full-catalog ETag in a shared cache (+39/−9)
  - `backend/tests/test_unit_surfaces_catalog.py`: 8 new tests — every category validates, unknown/empty/wrong-case/non-string all reject, filtered counts partition the full catalog (no drops or double-counts), the no-filter call stays byte-identical (backward compat), filtered ETags are distinct and well-formed, and static guards assert the route + OpenAPI spec carry the param (+110/−0)
  - `backend/openapi.yaml`: documents the `type` query parameter with the seven-value category enum so `/api/docs` advertises it (+43/−10)
  - `docs/API.md`, `docs/FEATURES.md`: reference updates (+1/−1 each)

The change is fully backward compatible: every no-arg path is untouched, and the OpenAPI drift tests compare path-sets, which don't change. This is the same build the `feature` skill opened earlier today — merged by @aaronjmars at 13:39 UTC.

---

## Internal: aaronjmars/miroshark-aeon

No user-visible product changes here today — the meaningful commits are the agent tuning its own machinery. The other 32 commits are `aeonframework` auto-commit / `chore(cron)` / `chore(scheduler)` bookkeeping (skill outputs, cron-state) and are filtered as bot churn.

### Feature skill now validates before shipping

**What this is:** A developer-facing fix to the agent's own `feature` skill. It previously cloned target repos into `/tmp/feature-build-*`, where the autonomous sandbox blocks code execution — so it could never run a repo's tests before opening a PR against production. Today's MiroShark #157 shipped 8 tests that were never run for exactly this reason.

**Under the hood**
- `408fecd` — fix(feature): validate diffs before shipping PRs (#60): clones into workspace-relative `.feature-build/<repo>` (exec permitted there) instead of `/tmp`, adds an explicit step 7 "Validate before shipping" (run the suite, fix red diffs, state plainly when tests can't run — never imply a pass), renumbers steps 8–12, adds a Validation line to the log template, and gitignores `.feature-build/`. `skills/feature/SKILL.md` +28/−10; rest is logs/outputs/skill-health bookkeeping. Merged by @aaronjmars at 14:06 UTC.

**Infra**
- `74408d9` — chore(messages): disable inbound message handling: edits `.github/workflows/messages.yml` (+9/−1) to turn off the Telegram/Discord/Slack message → skill path (poll collection + the message-processing job). The cron scheduler tick is unchanged, so scheduled skills and chains keep running. Reversible via inline comments. Direct push to main by Aaron Elijah Mars.

---

## Developer notes
- **New dependencies:** none
- **Breaking changes:** none — `?type=` is additive and all no-arg paths are byte-identical
- **New public surface:** `GET /api/surfaces.json?type=<category>` query parameter (categories: analytics, visualization, export, embed, integration, platform, discovery); helper `is_valid_surface_type()` in the surfaces catalog service
- **Tech debt added:** none observed in the diffs

## Open threads
- No unmerged feature branches pushed in the window. MiroShark `repo-actions` carried over "Add SECURITY.md (responsible disclosure)" as the next pick — not yet a PR.
- Inbound messaging is now off on the aeon repo; outbound `./notify` is unaffected. Worth confirming this was intentional before any skill assumes the inbound path exists.

## Sources
- aaronjmars/MiroShark: ok
- aaronjmars/miroshark-aeon: ok
- gh api commits: ok
- gh pr list: ok
- gh api events: skipped (commits + PRs sufficient)
- bot-filtered: 32
- diff-truncated: 0
