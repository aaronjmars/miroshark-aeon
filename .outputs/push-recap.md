*Push Recap — 2026-05-10*

MiroShark — 1 substantive main commit by aaronjmars; aeon — 30 routine cron auto-commits + 1 substantive PR opened on a branch.

*Lineage Navigator lands (PR #76 merged):* `e05bea4` shipped at 21:02 UTC yesterday. +1,778/-0 across 11 files, zero new deps (17-PR streak). New `GET /api/simulation/<id>/lineage` returns parent + public-only children sorted oldest-first capped at 50, with counterfactual trigger metadata inline. EmbedDialog gains a 🌳 panel that auto-shows only when there's a graph to navigate. Researchers running 3 counterfactual branches off a base scenario can finally walk parent → children from the share surface instead of remembering child IDs.

*Surface-stats feedback loop in flight:* PR #77 (`track reproduce.json + lineage in surface-stats`) and PR #78 (`trending sort — turn surface-stats into a discovery primitive`) both opened today, neither merged. Together with #74/#75/#76 they form the observability → distribution → discovery loop: hits get counted, trending sort surfaces the most-hit sims, more eyeballs compound.

*Aeon self-heals MEMORY.md:* `self-improve` caught that the index file had grown to 81 KB / 33K+ tokens — over Claude's 25K Read cap — meaning every skill following the "read MEMORY.md at task start" rule was failing. PR #33 re-applies the durable fix from closed #32: per-row caps in `skills/memory-flush/SKILL.md` (Skills Built ≤280, Recent Articles ≤220) plus a `wc -c` sanity check. MEMORY.md now 7.7 KB / 77 lines (-90%); detail preserved in logs + articles.

Key changes:
- `backend/app/services/lineage_service.py` (new, +390): pure-stdlib bidirectional lineage traversal with public-only privacy primitive, MAX_CHILDREN=50 cap, honest total_children
- `frontend/src/components/EmbedDialog.vue` (+505): green 🌳 Lineage panel between indigo repro section and orange watch section, eager-fetches on dialog open + isPublic flip
- `skills/memory-flush/SKILL.md` (+14, -3): new step 5 enforces per-row caps so the index can't balloon past the Read cap again

Tech debt: `feature` skill committed a stray `.aeon-tmp-verify-trending.py` (58 lines, unused) alongside its PR #78 output — should be cleaned up.

Stats: ~3,200 lines across 31 main commits; 11 distinct skills shipped today; all `chore(cron): X success` markers present (zero skill failures).
Full recap: articles/push-recap-2026-05-10.md (github.com/aaronjmars/miroshark-aeon)
