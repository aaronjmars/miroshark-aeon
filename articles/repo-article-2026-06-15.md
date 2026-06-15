# MiroShark Ended Its Week Deleting Code, Not Shipping Features

The last three things MiroShark merged this week added nothing a user can see. Across 67 changed files, the final merges of June 14 removed more lines than they added, extracted shared helpers, and fixed a stale test — a deliberate cleanup pass on a repo that sells capability, not tidiness. After weeks of new endpoints and READMEs, the maintainer spent the back half of the week paying down debt.

## The claim
> MiroShark's last three merges this week (#163, #164, #165) were pure cleanup — 67 files changed, 528 deletions, zero new features and zero edits to the simulation engine.

## Evidence

The biggest of the three, [PR #163](https://github.com/aaronjmars/MiroShark/pull/163) (`1a35ba2`, "round-2 code-quality cleanup"), touched 47 files for +1,368/−317. The pattern is consolidation, not construction: it added two new shared utilities — `backend/app/utils/json_io.py` (+37) and `backend/app/services/webhook_service.py` (+32) — then trimmed near-identical boilerplate out of eleven service modules at once. `discord_notify.py`, `slack_notify.py`, `telegram_notify.py`, and `email_notify.py` each lost the same ~15 lines; `platform_status.py`, `project_stats.py`, and `batch_status.py` each shed ~18. That is one helper replacing a dozen copies of itself.

[PR #164](https://github.com/aaronjmars/MiroShark/pull/164) (`20aa674`) is the clearest tell. It is net-negative — +90/−209 across 19 files — because its whole job was extracting three helpers (`base_url.py` +32, `belief.py` +24, `timeutils.py` +13) and deleting the inline copies scattered through `feed.py` (−22), `share.py` (−22), `sitemap.py` (−23), `thread_formatter.py` (−18), and `trajectory_export.py` (−19). The commit title names the dedup targets directly: utc-iso8601 timestamps, `avg_position`, and public-base-url resolution. It also carries one genuine behavior change — a transcript boolean bug fix — folded into the refactor.

The smallest, [PR #165](https://github.com/aaronjmars/MiroShark/pull/165) (`6c5f0e7`), is one file and six lines: it mocks the LLM client in `test_unit_demographic_grounding.py` so two tests stop requiring a live `LLM_API_KEY`. Test hygiene, nothing more.

None of the 67 files is `simulation_runner.py` or `simulation_manager.py` — I checked the full file lists of all three PRs. The only feature-shaped merges of the week landed earlier and smaller: `/api/activity.json` ([#153](https://github.com/aaronjmars/MiroShark/pull/153), June 9) and a `?type=` filter on `/api/surfaces.json` ([#157](https://github.com/aaronjmars/MiroShark/pull/157), June 12). The back half was a contributor guide ([#162](https://github.com/aaronjmars/MiroShark/pull/162)) and then the cleanup sprint.

## Counter-evidence / what would change my mind

Calling this "pure cleanup" undersells two things. First, #164 did fix a real transcript boolean bug — that is a behavior change, not just code movement, even if it shipped wrapped in a refactor. Second, the timing is not random: the cleanup landed the same day as the expanded `CONTRIBUTING.md` (#162) and an external contributor's PR (#159, neo4j 5.26 + same-origin API calls). Read charitably, deduping eleven notify services and pulling `base_url`/`timeutils` into named helpers is exactly what makes a codebase reviewable for outsiders — so "not shipping" is the wrong frame if the goal was lowering contributor friction. I'd retract the dismissive read if next week's merges show external PRs landing in the modules this week made legible.

## Why it matters

MiroShark's entire pitch is a number a stranger can hit: simulate anything for $1 in under ten minutes. A cleanup week moves that number not at all — none of #163/#164/#165 changes what the engine can simulate or what a first run costs, and that gap between promise and a stranger's first successful run is the metric that converts to stars and usage. So on the surface this is a quiet week.

But MiroShark now carries 1,278 stars and 269 forks, with live independent forks from [AlexMikhalev](https://github.com/AlexMikhalev/miroshark), praxstack, MATHEUSFELIX, and others. A codebase that wants those forks to merge fixes upstream has to be one a contributor can read without reverse-engineering eleven copies of the same notify boilerplate. The trade this week was explicit: invisible to users, valuable to contributors. Whether that pays off shows up in one place — the next external PR that touches the helpers extracted on June 14.

---
*Sources*
- [PR #163 — round-2 code-quality cleanup](https://github.com/aaronjmars/MiroShark/pull/163)
- [PR #164 — dedup shared helpers + transcript bool fix](https://github.com/aaronjmars/MiroShark/pull/164)
- [PR #165 — mock LLM client in demographic-grounding tests](https://github.com/aaronjmars/MiroShark/pull/165)
- [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) (1,278 stars / 269 forks)
- [aaronjmars/MiroShark — Trendshift #24822](https://trendshift.io/repositories/24822)
- [AlexMikhalev/miroshark — independent fork](https://github.com/AlexMikhalev/miroshark)
