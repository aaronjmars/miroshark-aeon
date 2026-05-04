*Push Recap — 2026-05-04*
MiroShark — 1 substantive merge (PR #71). miroshark-aeon — 0 substantive merges (~30 harness chore commits only).

PR #71 *Shareable Scenario Links* (filed 11:46 UTC, merged 12:56 UTC): the eight surfaces shipped to date all serialize a *finished* sim — gallery card / share card / replay GIF / transcript / RSS / trajectory CSV / live watch / gallery search. PR #71 covers the inverse direction, the un-run scenario. `?scenario=…&url=…&ask=…&template=<slug>` query params on `/` pre-fill the New Sim form (or auto-launch a preset template via the existing `setPendingTemplate` flow); inverse-direction 🔗 *Share as link* button beneath the Simulation Prompt + per-template-card 🔗 copy the URL from live form state. Pure frontend, zero new deps (DOMPurify already pinned for the markdown renderer). The Fork-this-scenario buttons that PR #67 added to `/share` and `/watch` already covered the un-run-from-finished direction; PR #71 covers the un-run-from-tweet-or-blog direction.

Key changes:
- NEW `frontend/src/utils/urlParams.js` (+116) — DOMPurify-backed sanitizer; HTML / `javascript:` URIs / control chars stripped, length-capped (scenario 500 / ask 300 / url 2000), `template=` restricted to `[a-z0-9_-]+`, `?url=` rejected unless `http(s):`. One source of truth for read on `/` and write on `/` + per-template card.
- `Home.vue` (+385 / −2) — `onMounted` reads + applies, fires one-shot `fetchUrlDoc()` for `?url=`, hands `?template=<slug>` to existing template-launch flow with redirect, strips params via `router.replace` so refresh / address-bar copy reflects edited state. Dismissible orange-edged banner + `🔗 Share as link` button.
- `TemplateGallery.vue` (+68 / −10) — every preset card gets a 🔗 sibling next to Launch that copies `?template=<slug>` with brief ✓ flash.

Stats: 6 files changed, +613 / −12. Zero-new-deps streak now 10 consecutive PRs.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-04.md
