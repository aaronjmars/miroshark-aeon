# When Your Async API Can't Block, Someone Else Writes the Polling Loop

Every async API eventually ships webhooks. A simulation finishes. A batch job completes. A report is ready. The server-side pattern has become reflexive: register an endpoint, receive a POST when the work is done. The abstraction seems clean until you try to use it from a shell script.

Webhooks require a server. Not metaphorically — a process running, a port listening, a publicly-accessible URL the originating system can reach. If that URL sits behind NAT or a firewall, the webhook doesn't arrive. If the receiving process crashes between trigger and delivery, the event is lost unless someone implemented a dead-letter queue. If the same event fires twice — which retry logic makes likely — the handler needs idempotency checks. Each piece is a new operational dependency added to what was nominally just "wait for the result."

## The Alternative Is Older Than the Web

Unix tools communicate through exit codes and standard streams: success exits 0, failure exits non-zero, progress goes to stderr, data goes to stdout. This is not a limited interface. It is a universal composition protocol that works in a terminal, a CI job, a cron tab, and any GitHub Actions YAML written today.

Research benchmarks on using CLI tools with AI agents found that a CLI-based approach consumed [97% fewer tokens than an equivalent MCP-based approach](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/) for the same automation scenario — 4,150 tokens versus 145,000 — because structured output arrives without protocol wrapper overhead. The composability argument extends further: when the interface is exit-code plus streams, `&&` is the integration API. No registration. No public endpoint. No retry infrastructure.

The webhook failure mode is well-documented on the other side. [System design analysis of polling versus webhooks](https://bugfree.ai/knowledge-hub/webhook-vs-polling-system-design-tradeoffs) identifies receiving-endpoint unavailability as the central operational risk: if the server that registered for callbacks goes down between trigger and delivery, the event is gone, "requiring additional logic to handle retries or failures." For a developer who wants to script "run a simulation, then print the report," that infrastructure is entirely out of proportion to the problem.

## What an Exit Code Buys You

Commit `959aef8` makes the tradeoff explicit. `cmd_wait` in `cli.py` polls `/api/simulation/<id>/run-status` on a monotonic deadline: exit 0 on completed, exit 1 on failed or stopped, exit 2 on timeout. Progress messages go to `stderr` so `stdout` stays clean for downstream piping. Transient poll errors — network hiccups, 5xx responses — warn and keep going rather than treating a momentary server failure as a simulation failure.

The pipeline documented in PR #215: `python cli.py wait "$SIM" && python cli.py report "$SIM"`. The `&&` is not decorative. If the simulation failed, `wait` exits 1, `&&` short-circuits, `report` never runs. A CI build that runs a simulation, waits, and either reports or fails the build is four lines of YAML. No endpoint to expose. No event handler to write.

This is the structural assumption the `wait` design makes visible. The integration context isn't "the user is running a server that can receive our POST." It's "the user has a shell." That's a smaller assumption, and it covers more ground: every developer has a terminal, open-source CI pipelines default to GitHub Actions (which is a shell environment), and every cron job ever written uses exit codes.

## The Stderr Detail That Makes It Composable

The choice to route progress output to `stderr` rather than `stdout` is the non-obvious design decision. If progress strings and structured data share the same stream, any pipe breaks — `wait "$SIM" | jq .` would receive mixed content, making JSON parsing fail on the progress lines. The stderr/stdout split is what lets `wait` chain cleanly with `report`, `cost`, `jq`, or any downstream tool that reads stdout.

The `--interval` (default 5s) and `--timeout` (default 600s) flags give the integrator control over the latency tradeoff without the server needing to know anything. The client sets its own polling frequency. That client-side control is [the core operational advantage of polling over webhooks](https://agnost.ai/blog/long-running-tasks-mcp/): the polling loop can't arrive at a server that's down, be blocked by a firewall, or get lost in a retry queue. The integrator decides how often to check and when to give up.

The architectural bet is explicit: the right async contract for shell-script and CI integrators is an exit code, not a webhook. If that describes the median integrator, the design is correct. If most integrations are server-side code rather than scripts, webhooks would have been the right call.

## What This Predicts

Async AI APIs will diverge. Consumer-facing platforms — where users want live notifications in a browser or mobile app — will keep building webhooks. Webhooks are the right interface when the consumer is a long-running process that can't block.

For batch automation — CI pipelines, scripted workflows, scheduled jobs, GitHub Actions — the blocking CLI with exit codes is the more composable primitive. The platforms that don't ship it will have their integrations written around it anyway, by users hand-rolling `while not done: sleep` loops because there was no `wait` command. [At scale, polling 10,000 users every 10 seconds generates 2.5 billion monthly API calls](https://medium.com/@nile.bits/webhooks-vs-polling-431294f5af8a) — but for one-shot automation, where the shell is already blocking, polling a single endpoint on a 5-second interval is exactly proportionate.

By 2027, the blocking-CLI pattern will be a standard line item in AI batch-API documentation, the same way streaming normalized event-stream format for token-by-token output. The gap between "the job is running" and "the script knows it finished" is too ubiquitous and too simple to leave unresolved for every integrator to solve independently. The platforms that ship `wait` first set the integration floor the rest of the category measures against.

---

*Sources:*
- [CLI Tools: 35x Smarter AI Agents](https://jannikreinhard.com/2026/02/22/why-cli-tools-are-beating-mcp-for-ai-agents/) — Jannik Reinhard (Feb 2026); CLI vs MCP token efficiency in real automation; 97% token reduction (4,150 vs 145,000 tokens); composability via exit codes
- [Webhook vs Polling: System Design Tradeoffs](https://bugfree.ai/knowledge-hub/webhook-vs-polling-system-design-tradeoffs) — bugfree.ai; receiving-endpoint unavailability as the core webhook operational failure mode; retry infrastructure overhead
- [Long Running Tasks in MCP: The Call-Now, Fetch-Later Pattern](https://agnost.ai/blog/long-running-tasks-mcp/) — Agnost AI; client-side control as polling's core advantage; alternative async patterns and when blocking is preferable
- [Webhooks vs. Polling](https://medium.com/@nile.bits/webhooks-vs-polling-431294f5af8a) — Medium / Nile Bits; 2.5 billion monthly API calls for polling at scale vs 1 million for equivalent webhooks; scale asymmetry
- [MiroShark — aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — commit 959aef8 / PR #215 (`wait` subcommand, `cmd_wait` in `cli.py`); exit codes 0/1/2; stderr/stdout stream split; `--interval`/`--timeout` flags; `/api/simulation/<id>/run-status` endpoint
