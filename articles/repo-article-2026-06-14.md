# MiroShark spent a full week building for its integrators and never touched the engine

The repo that promises to "simulate anything for $1" merged six pull requests between June 8 and June 14, 2026: a Japanese README, a contributor guide, a polling feed, a signed-result payload, and a query filter. Not one of them changed how MiroShark actually simulates. The engine sat still while everything around it — docs, access, verification — moved.

## The claim
> MiroShark shipped six merged PRs this week and not one touched the simulation engine — every change served an outside contributor or integrator, not the sim.

## Evidence

Walk the merge log. [PR #152](https://github.com/aaronjmars/MiroShark/pull/152) (commit `7b79e7b`) added `services/signed_result.py` (+215) and a signed-result route in `backend/app/api/simulation.py` (+112), backed by a 499-line test. It signs a finished sim's output with HMAC-SHA256 so a third party can verify it offline. That changes what an integrator can *prove* about a result — not how the result is produced.

[PR #153](https://github.com/aaronjmars/MiroShark/pull/153) (commit `97e39f8`) added `services/activity_feed.py` (+439) and `api/activity.py` (+144): an `/api/activity.json` "what-just-completed" polling feed so an external dashboard can watch runs land. It is read-only; `simulation_runner.py` never sees it. [PR #157](https://github.com/aaronjmars/MiroShark/pull/157) (commit `0a575db`) put 42 lines in `api/surfaces.py` and 39 in `services/surfaces_catalog.py` to let a caller filter the catalog of things you can simulate by `?type=`. That is querying the menu, not cooking.

The remaining three are documentation. [PR #155](https://github.com/aaronjmars/MiroShark/pull/155) and PR #156 added a zh-CN and a Japanese `README.ja.md`; [PR #162](https://github.com/aaronjmars/MiroShark/pull/162) (commit `bda04b3`) expanded `CONTRIBUTING.md` by +55 lines, including a section teaching a newcomer how to add an API endpoint. Every changed line across all six PRs lives in `backend/app/api/`, `backend/app/services/`, `docs/`, `frontend/src/api/`, or a README. None of it lives in `simulation_runner.py`, `simulation_manager.py`, or the swarm-agent core that turns a $1 prompt into hundreds of arguing agents.

## Counter-evidence / what would change my mind

The honest objection: `signed_result.py` and `activity_feed.py` are engine-adjacent — they read live simulation state, and #152 arguably strengthens trust in the sim more than a new agent behavior would. If "the engine" means "anything that makes a sim more useful," the week was not idle at all. And a frozen core can be a stable one: MiroShark's heavy simulation work — the Nemotron-seeded `demographic_sampler.py`, the outcome-distribution stats — landed in earlier weeks, so a quiet core may signal maturity, not stall. The claim is wrong the moment a PR edits `simulation_runner.py` or adds a new agent capability. This week, none did — I checked the file list of all six.

## Why it matters

For where MiroShark actually is, this is on-strategy, not drift. The repo carries 269 forks and a visible fork ecosystem ([AlexMikhalev/miroshark](https://github.com/AlexMikhalev/miroshark) is one of several), and it trends publicly on [Trendshift](https://trendshift.io/repositories/24822). An integrator-facing week — verifiable results, a polling feed, a contributor guide in three languages — is exactly what converts a fork into a real dependency. Open-source [maturity models](https://osr.finos.org/docs/bok/osmm/introduction) place this work — standardized OpenAPI surfaces, repeatable contributor onboarding — at the stage *after* a core stabilizes, not before.

The backdrop sharpens the point. MiroShark sits at 1,270 stars with only 4 open issues — a repo being watched closely and maintained tightly, not one starved of attention or buried in bug reports. A project that healthy going a full week without an engine commit is making a choice, not coasting: the maintainer is spending scarce review cycles on the people *around* the sim rather than the sim. That is defensible while the fork count climbs. It stops being defensible the moment those forks need a capability the engine still cannot deliver.

The risk is reading surface growth as substance growth. A stranger's first $1 run succeeds or fails on engine capability — what the swarm can model, how cheaply, how credibly — and that capability did not move this week. A repo can expand its API faster than its abilities, and the two diverge quietly. Watch which of the two the next six PRs touch.

---
*Sources*
- [PR #152 — signed-result.json (HMAC-SHA256)](https://github.com/aaronjmars/MiroShark/pull/152)
- [PR #153 — /api/activity.json polling feed](https://github.com/aaronjmars/MiroShark/pull/153)
- [PR #157 — surfaces.json ?type= filter](https://github.com/aaronjmars/MiroShark/pull/157)
- [PR #162 — expanded CONTRIBUTING guide](https://github.com/aaronjmars/MiroShark/pull/162)
- [aaronjmars/MiroShark on Trendshift](https://trendshift.io/repositories/24822)
- [AlexMikhalev/miroshark — a fork on the engine](https://github.com/AlexMikhalev/miroshark)
- [FINOS Open Source Maturity Model](https://osr.finos.org/docs/bok/osmm/introduction)
