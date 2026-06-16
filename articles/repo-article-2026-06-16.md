# MiroShark's First Dependabot Wave Broke Its Own Engine on Day One

Eleven dependency bumps merged into MiroShark on June 16. One of them — camel-ai 0.2.78→0.2.90 — quietly tore out the method MiroShark overrides to run its agent loop, then refused to let the Docker container build. The bot did its job. The job included two same-day fixes by a human.

## The claim
> MiroShark's first Dependabot wave landed 11 bumps; the camel-ai 0.2.90 bump (#176) broke the agent loop and Docker build, forcing two same-day hotfixes (#181, #182).

## Evidence

The Dependabot config shipped the day before — [PR #166](https://github.com/aaronjmars/MiroShark/pull/166), merged 2026-06-15. Its first run fired today. Between 14:16 and 16:19 UTC, eleven bot PRs merged: [#167](https://github.com/aaronjmars/MiroShark/pull/167) through [#177](https://github.com/aaronjmars/MiroShark/pull/177) — concurrently, vue-router, vite 7→8, Python 3.11→3.14, checkout v4→v6, nashpy, pywebpush, and the rest.

[PR #176](https://github.com/aaronjmars/MiroShark/pull/176) was different. It bumped `camel-ai` from 0.2.78 to 0.2.90 in `backend/pyproject.toml` and `requirements.txt` — a two-line diff, filed under the "backend-minor-patch group." camel-ai is the multi-agent framework MiroShark's swarm runs on. Between those two releases, camel refactored `ChatAgent._aget_model_response` — dropping the `num_tokens` parameter and switching to keyword calls.

That matters because `SocialAgent` in `backend/wonderwall/social_agent/agent.py` *overrides* that exact method to filter empty messages and emit `llm_call` observability events. The PR body for the fix is blunt: the bump "silently breaks the entire agent simulation loop." The repair, [PR #181](https://github.com/aaronjmars/MiroShark/pull/181), is two lines in one file, merged 15:36 UTC — landed *before* #176 because it was written to be safe on the old pin and unblock the new one.

Then the container broke. Both `Dockerfile` and `Dockerfile.railway` run `uv sync --frozen`, which refuses to proceed when `uv.lock` disagrees with `pyproject.toml`. #176 left the lockfile at 0.2.78. [PR #182](https://github.com/aaronjmars/MiroShark/pull/182) regenerated it (`+99/−96` in `backend/uv.lock`), merged 16:33 UTC — caught, per its description, "while doing final Docker-build verification." Three PRs, one bump, one afternoon.

The other ten bumps in the wave merged clean — vite 7→8, vue-router 4→5, even Python 3.11→3.14, none of which needed a follow-up. That isolation is the point: the failure wasn't the volume of updates, it was one specific library MiroShark reaches into. The infra bumps (checkout, setup-python, build-push-action) touched only CI; the one that touched the simulation runtime is the one that bled.

## Counter-evidence / what would change my mind

The bot was right to surface this. The camel-ai pin was a known liability — `0.2.78` was exact-pinned precisely because the camel/tiktoken stack is sensitive, and a manual bump would have hit the same wall with less warning. Dependabot turned an invisible drift into a reviewable PR with a changelog attached, and the maintainer cleared it in roughly two hours. That's the system working, not failing. The breakage also wasn't auto-merged blind — a human reviewed, found the regression, and shipped #181/#182. If "broke" implies an outage shipped to users, that's wrong: `main` was red briefly, never the deployed product. The thesis is about cost and fragility, not about a regression reaching anyone's simulation.

## Why it matters

The trap is the label. Dependabot grouped `0.2.78→0.2.90` as "minor-patch" — but camel-ai is a pre-1.0 library, where a 0.2.x bump can and did change an internal API a downstream override depends on. MiroShark's whole pitch is "simulate anything for $1," and the thing doing the simulating is a third-party agent framework still moving fast under it. Every cheap, credible sim rides on a dependency that can refactor a private method out from under the engine between two minor releases. Automating the bumps doesn't remove that risk — it schedules it, surfaces it, and forces it into daylight where someone has to fix it the same afternoon. For a project selling trust in its sims, the lesson isn't "stop updating." It's that the engine's reliability is partly someone else's release cadence, and the only defense is exactly what happened here: tests, a frontend-build CI gate ([#180](https://github.com/aaronjmars/MiroShark/pull/180), also merged today), and a human reading the diff.

---
*Sources*
- [PR #176 — bump camel-ai 0.2.78→0.2.90](https://github.com/aaronjmars/MiroShark/pull/176)
- [PR #181 — wonderwall signature compat fix](https://github.com/aaronjmars/MiroShark/pull/181)
- [PR #182 — sync uv.lock (unbreaks Docker build)](https://github.com/aaronjmars/MiroShark/pull/182)
- [PR #166 — Dependabot config](https://github.com/aaronjmars/MiroShark/pull/166)
- [camel-ai releases (v0.2.90)](https://github.com/camel-ai/camel/releases)
- [GitHub Docs — about Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates)
