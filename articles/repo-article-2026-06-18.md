# MiroShark's Outside Contributors Are Fixing the Install, Not the Engine

The biggest external pull request MiroShark merged this week — 1,167 lines across 19 files — does not teach the engine to simulate anything new. It teaches the engine to run on a laptop. That tells you exactly where strangers get stuck, and it isn't the swarm.

## The claim
> MiroShark's outside contributors fix how to run it, not what it simulates: 8 of 9 external code PRs touch deployment/self-hosting/security, none the swarm core.

## Evidence

Strip out the maintainer (`aaronjmars`), Dependabot, and the ECOSYSTEM.md vanity listings, and MiroShark has merged nine code PRs from external contributors. Walk the list and one pattern dominates. [#178](https://github.com/aaronjmars/MiroShark/pull/178) from `dan-and` adds self-hosted SearXNG search and Firecrawl scraping so the engine can run on "(local) models that do not need websearch capabilities" — its files include `docker-compose.ollama.yml`, `searxng_client.py`, `url_fetcher.py`, and `railway.env.example`. The same contributor's earlier [#159](https://github.com/aaronjmars/MiroShark/pull/159) reworked path recognition for same-origin API calls and bumped Neo4j from 5.15 to 5.26 because "5.15 version struggled with indexing."

The rest rhyme. #106 prepared a Railway deployment; #104 collapsed `.env` profiles into a wildcard; #100 let the launcher skip a local Neo4j when pointed at Aura; #89 forced an explicit `NEO4J_PASSWORD` instead of a hardcoded default; #98 validated `project_id` to block path traversal; #38 read config lazily so `POST /api/settings` actually takes effect. Eight of the nine are about installing, configuring, deploying, or hardening MiroShark — not about widening what it can model.

The one exception proves the rule's edge. `mbs5`'s [#36](https://github.com/aaronjmars/MiroShark/pull/36) parallelized report generation for a ~5x speedup — but it edits a single file, `backend/app/services/report_agent.py`, the output stage. The actual swarm core, [`backend/app/services/simulation_runner.py`](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/services/simulation_runner.py) and `simulation_manager.py`, has not been touched by a single external PR. Outsiders are circling the building, fixing the doors and the wiring. Nobody from outside has walked into the engine room.

## Counter-evidence / what would change my mind

This could be read as a maintainer keeping the core close — and that's partly true, since `aaronjmars` authors the engine-adjacent work himself. But the contributor behavior is the tell regardless of intent: when people who aren't paid to care reach for MiroShark, they file deployment fixes. `dan-and` didn't ask for a new simulation primitive; he opened [issue #160](https://github.com/aaronjmars/MiroShark/issues/160) to announce he was building offline-model support on his own fork first. You could also argue the sample is small (nine PRs) and self-hosting is just what early open-source contributors always do. Fair. But the ecosystem outside the repo says the same thing: `nikmcfly/MiroFish-Offline` is a public fork whose entire pitch is "offline multi-agent simulation… with Neo4j + Ollama local stack." Two independent parties, same instinct — make it run locally first.

## Why it matters

MiroShark's promise is "simulate anything, for $1 & less than 10 min." The strategy that follows from that promise treats one gap as priority-zero: the distance between the pitch and a stranger's first successful run. The contributor data is the cleanest map of that gap anyone could ask for. People aren't blocked on what the swarm can imagine; they're blocked on Neo4j indexing, on same-origin routing, on whether they can avoid paying a hosted, websearch-capable model just to run a round. `dan-and`'s Ollama-plus-SearXNG path attacks the cost floor directly — the $1 is only credible if you aren't forced onto an expensive model to hit it, and self-hosted search plus a local model is how that number survives contact with a skeptic.

The lesson for anyone shipping an "anything-engine" is unglamorous: your moat may be the simulation, but your adoption curve is the install. MiroShark's outside contributors have been quietly writing its deployment guide in the form of merged code. The repo would do well to read it as a roadmap, not a chore — fold #178's local-model path into the documented quickstart, and the next stranger's first run gets a lot closer to free.

---
*Sources*
- [PR #178 — SearXNG / Firecrawl for non-websearch LLMs (dan-and)](https://github.com/aaronjmars/MiroShark/pull/178)
- [PR #159 — same-origin API calls + Neo4j 5.26 (dan-and)](https://github.com/aaronjmars/MiroShark/pull/159)
- [Issue #160 — "Building support for Websearch and Webretrieval"](https://github.com/aaronjmars/MiroShark/issues/160)
- [simulation_runner.py — the swarm core, untouched by external PRs](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/services/simulation_runner.py)
- [nikmcfly/MiroFish-Offline — Neo4j + Ollama local fork](https://github.com/nikmcfly/MiroFish-Offline)
- [Running LLMs Locally in 2026: Ollama, llama.cpp, and Self-Hosted AI (daily.dev)](https://daily.dev/blog/running-llms-locally-ollama-llama-cpp-self-hosted-ai-developers/)
