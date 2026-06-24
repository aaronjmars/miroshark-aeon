# MiroShark's Engine Reliability Has a Bus Factor of One — and It Isn't the Owner

aaronjmars merged 14 PRs into MiroShark this week. None of them changed how the simulation engine runs. The person actually fixing the engine's runtime — the hangs, the dead loops, the silent worker deaths — is a self-hoster in Hamburg named Daniel Andersen, who doesn't own the repo and merged every outside PR it accepted.

## The claim
> MiroShark's only outside human contributor this week is Daniel Andersen — and his open PR #214 proposes the first behavioral change to simulation_runner.py since May.

## Evidence

Count the merges in the 06-17→06-24 window. aaronjmars shipped tooling and polish: the `wait` CLI ([#215](https://github.com/aaronjmars/MiroShark/pull/215), 959aef8), the `cost` CLI ([#208](https://github.com/aaronjmars/MiroShark/pull/208), cef787b), a tagline rebrand ([#206](https://github.com/aaronjmars/MiroShark/pull/206)), a code-quality pass ([#205](https://github.com/aaronjmars/MiroShark/pull/205)), four dependabot bumps (#199–#202). Useful work — all of it around the engine, none of it inside it. Every other human PR that merged is dan-and's: [#209](https://github.com/aaronjmars/MiroShark/pull/209), [#194](https://github.com/aaronjmars/MiroShark/pull/194), [#189](https://github.com/aaronjmars/MiroShark/pull/189), [#188](https://github.com/aaronjmars/MiroShark/pull/188). No third contributor cleared review in seven days.

His work has been getting deeper, not wider. The arc: #159 (06-14) bumped neo4j and fixed same-origin API calls; #178 (06-16) added SearXNG/Firecrawl search for LLMs that can't web-search. Plumbing. Then #188 raised the suggest-scenarios timeout for local models, #194 (3e054f4) wired report-agent prompts through the locale registry, and #209 (7a9dffa) hardened the thinking-model path — None guards, JSON repair, separate reasoning budget. Each PR sits closer to the hot loop than the last.

PR [#214](https://github.com/aaronjmars/MiroShark/pull/214) (open, 06-23, +197/-69 across 10 files) is where it lands inside the engine. It edits `backend/app/services/simulation_runner.py`, `simulation_ipc.py`, `wonderwall/environment/env.py`, `wonderwall/social_platform/platform.py`, and `social_agent/agent.py` — the swarm core. The fixes are real failures, not cosmetics: `platform.running()` was swallowing a dead dispatch loop and blocking `perform_action` forever; `env.step()` ran a synchronous PyTorch `update_rec_table()` on interview-only steps and starved the asyncio worker timeout; `check_env_alive()` trusted a status file that said "alive" over a crashed PID. The runner itself gets lifecycle fixes — `_ensure_env_alive()` resets a stale RUNNING state before restart, and the monitor stops overwriting STOPPED with FAILED on an intentional kill.

That matters because `simulation_runner.py` hasn't had a behavioral change in over a month. Its June history is one commit — #205 (6cf32a8, 06-22), a code-quality refactor. The last commits that altered how it actually runs were the May notification features (#93, 05-21; #87, 05-17). The engine has been frozen by everyone with merge rights. The first patch in weeks that proposes to *change its behavior* is sitting in an outsider's open PR, alongside #212 and #213, filed the same evening.

## Counter-evidence / what would change my mind

This is not the textbook bus factor, where the maintainer vanishes. aaronjmars is the opposite of absent — 14 merges in a week, and he merged dan-and's #209 the same day it landed. The review pipeline works. #214 is still open and could be reshaped or rejected before it touches main, so technically the engine isn't unfrozen yet — only proposed-to-be. And nobody, dan-and included, has changed the *simulation algorithm*: the belief-update math and the swarm loop are untouched. What's concentrated isn't capability — it's runtime correctness on the path nobody at the top runs. The claim would be wrong if another non-bot account had merged code this week (none did), or if #214 left `simulation_runner.py` alone (it doesn't).

## Why it matters

MiroShark's pitch is "$1 to simulate anything." The stranger who tries that on their own box hits exactly dan-and's bugs — slow thinking models that hang, local LLMs that return None, env workers that die quietly while the status file lies. aaronjmars runs the hosted OpenRouter default, so those paths don't break for him; they break for the audience the north-star metric depends on. The self-hosted engine's reliability currently rests on one contributor who happens to run it under load and care enough to debug the asyncio. That's a bus factor of one on the surface that converts curiosity into a working first run. Ingress-Nginx just entered best-effort retirement on two part-time maintainers; the failure mode isn't a dramatic abandonment, it's a quiet path that nobody left is positioned to fix. MiroShark's owner ships the tooling around the engine. The engine's runtime needs a second person who runs it the way strangers will.

---
*Sources*
- [PR #214 — interview hang prevention + stop-lifecycle fixes](https://github.com/aaronjmars/MiroShark/pull/214) (in-repo)
- [PR #209 — thinking-model None guards / JSON repair / budget](https://github.com/aaronjmars/MiroShark/pull/209) (in-repo)
- [PR #178 — SearXNG/Firecrawl search for non-websearch LLMs](https://github.com/aaronjmars/MiroShark/pull/178) (in-repo)
- [aaronjmars/MiroShark — Universal Swarm Intelligence Engine](https://github.com/aaronjmars/MiroShark) (in-repo)
- [MiroShark — Openflows](https://openflows.org/currency/currents/miroshark/) (external)
- [Missing the Bus: When the "Bus Factor" Threatens Open Source — Post Status](https://poststatus.com/missing-the-bus/) (external)
- [The "Bus Factor" (Project Health) — OpenTechHub](https://www.opentechhub.io/resource/governance-bus-factor/) (external)
