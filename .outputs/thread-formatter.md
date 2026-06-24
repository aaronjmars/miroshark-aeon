*Thread Draft — 2026-06-24*
Topic: wait CLI subcommand (PR #215 on aaronjmars/MiroShark)

1/ MiroShark just shipped `wait` — a blocking CLI call that returns when a sim terminates. exit 0 if completed, exit 1 if failed, exit 2 if timeout. that's the whole interface.

2/ before this, scripting a run end-to-end meant writing your own poll loop. `status` returns a snapshot. cost and report only make sense once a run terminates. so integrators were rolling `while not done: sleep(5)` before they could do anything downstream.

3/ PR #215: argparse + urllib, no new deps. polls `/run-status`, matches `runner_status` against terminal sets from the RunnerStatus enum. progress goes to stderr, stdout stays clean for `--json`. monotonic deadline, sleep capped to remaining time.

4/ the practical consequence: `python cli.py wait <id> && python cli.py cost <id>`. that's a composable pipeline. run a sim, wait for it, check what it cost — no dashboard, no webhook, no glue code. the $1 claim becomes auditable from a shell script.

5/ PR #215 — wait CLI subcommand on MiroShark. https://github.com/aaronjmars/MiroShark/pull/215 🦈

(article: articles/thread-2026-06-24.md)
