# From Pointer to Graph: MiroShark Turns Counterfactual Branches Into a Navigable Tree

Yesterday MiroShark made a finished simulation citable. Today, twenty-two hours later, it made the *family of simulations around it* navigable. PR #76 — "Simulation Lineage Navigator" — opened on May 9 at 11:28 UTC and closes a gap that PR #75 created the moment it merged: every `reproduce.json` carried a `parent_simulation_id` field, but a parent had no way to enumerate its children. A researcher running three counterfactual branches off a base scenario had to remember each child sim id by hand. Today that's a `GET` away.

## Current State

MiroShark sits at **1,122 stars / 223 forks / 2 open issues / 1 open PR** as of this morning, fifty days after first push. The 24-hour delta — six new stars, one new fork — is the post-1K cooldown pattern that's held for a week. The shipping cadence has not cooled: PR #76 makes **sixteen consecutive substantive PRs with zero new dependencies** since #57 in late April (counting #63 and #64 as README-only). Every feature in the share-surface arc — transcript export, RSS/Atom, trajectory CSV/JSONL, watch page, gallery search, scenario links, thread export, surface analytics, webhook log, reproduce.json, and now lineage — has shipped against pure stdlib `json` and `os`.

On the token side, $MIROSHARK closed the 24-hour window at $0.000005080 (+15.5%), with $289K liquidity and a 1.24× buy ratio on $29.2K of volume. The 30-day chart still reads +671%; ATH from May 6 sits 27% above current. Volume is normalizing post-spike.

## What Shipped Today

`GET /api/simulation/<id>/lineage` returns the lineage slice rooted at the requested sim:

```json
{
  "simulation_id": "sim_abc...",
  "lineage_kind": "original" | "fork" | "counterfactual",
  "parent": null | { "simulation_id", "scenario_preview", "created_at", "is_public" },
  "children": [...],
  "total_children": 3,
  "counterfactual": null | { "trigger_round", "label" }
}
```

Children are public-only (a privately forked branch in progress doesn't leak into a tweeted parent), sorted oldest-first, capped at 50 entries with the pre-cap `total_children` count preserved so the UI can honestly say "showing first 50 of 87." Each child carries its own kind — fork or counterfactual — and counterfactual rows surface the trigger round + label inline, so the badge reads "🔀 Counterfactual at round 12 (ceo_resigns)" without making the reader open the parent to find out what diverged.

The EmbedDialog gains a 🌳 Lineage panel that renders only when there is something to navigate to — `v-if="hasLineageGraph"`. Originals with no forks see nothing; the dialog stays compact. PR stats: +1,778 / -0 lines across 11 files, CI clean, branch `feat/simulation-lineage-navigator`.

## Technical Depth

The implementation lives in `backend/app/services/lineage_service.py` — about 390 lines of pure stdlib `json` + `os`, no new dependencies. The interesting piece is `_kind_for(state, cf)`, the discriminator that decides whether a sim is original, fork, or counterfactual based on the presence of `parent_simulation_id` plus the on-disk `counterfactual_injection.json` file. `find_children(parent_id, data_dir)` walks the corpus looking for reverse pointers; corrupt child `state.json` files are silently skipped rather than blanking the rest, self-pointers don't recurse, missing data dirs don't crash.

Sixteen offline unit tests pin every load-bearing invariant: the `MAX_CHILDREN=50` literal, the `SCENARIO_PREVIEW_CHARS=80` truncation, the public-children-only filter, the oldest-first sort, the legacy-state fallback for sims pre-dating the lineage schema, the OpenAPI drift guard. Frontend build green, 728 modules, vite v7.2.7. Aaron tweeted yesterday that the trio @aeonframework + @miroshark_ + @hyperstiti0ns is the "king-agent + simulation + prediction-markets" coordination layer; PR #76 makes the simulation node addressable as a graph, not just a flat document store.

## Why It Matters

The 2026 academic conversation around counterfactual reasoning has converged on a few load-bearing terms — *Counterfactual World Simulation Models*, *explanatory multiverse*, *multiverse analysis* — all of which describe the same workflow: vary one decision, run the world forward, compare the trajectories. Recent provenance work (PROV-AGENT, ContextSubstrate, Cray User Group's hybrid simulation-AI lineage frameworks) has been pushing the same pattern in HPC: make the lineage between runs queryable, content-addressed, navigable.

MiroShark just put that primitive in a public web API behind a five-minute cache, callable from a Markdown link in a Substack post. Yesterday's reproduce.json gave the citation; today's lineage endpoint gives the *graph* you cite *into*. A researcher writing up "what happens if the CEO resigns at round 12" can now link to the parent and let readers walk the three branches themselves — fork badge, counterfactual badge, trigger round, label, all rendered inline.

Sixteen surfaces, sixteen days of zero-new-deps PRs, and the simulator's data model is now bidirectional. The substrate is starting to look less like a demo and more like a research tool that happens to be tweetable.

---
*Sources:*
- [PR #76 — feat: simulation lineage navigator](https://github.com/aaronjmars/MiroShark/pull/76)
- [PR #75 — reproducibility config export (yesterday)](https://github.com/aaronjmars/MiroShark/pull/75)
- [Counterfactual simulation in causal cognition — Sciencedirect](https://www.sciencedirect.com/science/article/abs/pii/S1364661324001074)
- [Navigating explanatory multiverse through counterfactual path geometry — Springer](https://link.springer.com/article/10.1007/s10994-025-06769-2)
- [When AI meets counterfactuals: ethical implications of counterfactual world simulation models — Springer](https://link.springer.com/article/10.1007/s43681-025-00718-4)
- [PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions — arXiv](https://arxiv.org/html/2508.02866v1)
- [Framework for tracking metadata, lineage and model provenance in hybrid simulation-AI HPC workflows — Cray User Group](https://dl.acm.org/doi/abs/10.1145/3757348.3757364)
