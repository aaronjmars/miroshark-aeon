*Feature Built — 2026-06-23 — aaronjmars/MiroShark* 🦈

cost CLI subcommand
`python -m cli cost <sim_id>` now prints what a run actually cost, right in the terminal. One line: estimated dollars, total tokens, LLM call count — then a per-phase breakdown (graph build / simulation / report). The "$1 to simulate anything" claim, queryable from a script.

Why this matters:
the cost number already existed — `/cost.json` since #179, the `~$0.92` pill on EmbedView since #190 — but neither was reachable from a script. integrators running pipelines (AntFleet miroshark-bench and friends) had no way to audit spend without scraping a webpage. cost observability is table stakes, and the headline promise should be checkable the same way you run the sim: from the command line.

What was built:
- backend/cli.py: new `cmd_cost` + `cost` subparser, reusing the existing `_api` helper. prints `~$X` when the figure is an estimate (mirrors the embed pill), plus token/call totals and a per-phase cost table.
- backend/tests/test_unit_cli.py: registers `cost` in the subcommand assertion + adds `test_cost_parses_positional`.
- docs/CLI.md + docs/CLI.zh-CN.md: command, exit codes, lower-bound caveat — translations in sync.

How it works:
thin client, no new deps — argparse + urllib only, same as the rest of the CLI. it GETs `/cost.json`, which returns the payload directly on success and `{success:false}` on error. exit codes carry meaning: 0 done, 1 private/server error, 2 not-ready (404, no LLM calls yet) so a script can tell "still running" from "failed". honest by construction — the `~` says lower bound, because models off the price table count as $0. no new endpoint, so the openapi drift test stays green.

What's next:
pairs naturally with a `wait` command for a full `ask → wait → cost → report` one-liner. validation note: Python exec is blocked in the build sandbox, so unit tests run on the repo's CI on push, not here.

PR: https://github.com/aaronjmars/MiroShark/pull/208
