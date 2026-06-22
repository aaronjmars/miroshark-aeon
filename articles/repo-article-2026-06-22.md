# MiroShark's Default Model Is Dead on Arrival — and an Outsider Caught It First

Clone MiroShark today, copy `.env.example`, run the example, and your first simulation returns a 404 before a single agent speaks. The shipped default `LLM_MODEL_NAME` is `xiaomi/mimo-v2-flash` — a model OpenRouter began auto-routing away on June 18 and fully deprecates June 30. The product promise is "$1 to simulate anything." The out-of-the-box reality, right now, is an HTTP error code. And it wasn't the maintainer who flagged it.

## The claim
> MiroShark ships a dead default model: OpenRouter deprecated `xiaomi/mimo-v2-flash`, so a clean install's first run 404s — the second vendor-deprecation break in five weeks.

## Evidence

The default is still live and still dead. On `main` as of this writing, [`backend/app/config.py:37`](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/config.py#L37) reads `LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'xiaomi/mimo-v2-flash')`. OpenRouter's own model page states MiMo-V2-Flash began auto-routing to V2.5 on June 18, 2026 and is fully deprecated by June 30 ([OpenRouter](https://openrouter.ai/xiaomi/mimo-v2-flash)). The replacement contributor — [PR #204](https://github.com/aaronjmars/MiroShark/pull/204), opened June 22 by `tomer-liran`, an account that had never touched this repo before — pastes the live failure: `Error code: 404 - {'error': {'message': 'This model has been deprecated. It is recommended to migrate to xiaomi/mimo-v2.5'}}`, triggered by the `graph_tools` fallback interview hitting the default slot.

This isn't one constant in one file. PR #204 changes the slug in **18 files** with 37 replacements: the config default, the cloud "cheap" preset in `backend/app/api/settings.py`, the pricing table in `run_summary.py`, `.env.example`, the Railway and Cloud Run example envs, `docs/CONFIGURATION.md` / `INSTALL.md` / `MODELS.md`, all four README translations, and the frontend model placeholder. The model identifier was copy-pasted across every surface a new user reads first, so a single vendor sunset breaks the config, the docs, and the presets at once.

It has happened before. Commit [`44d1c4e`](https://github.com/aaronjmars/MiroShark/commit/44d1c4e) (PR #86, May 16) carries the message `fix: swap deprecated x-ai/grok-4.1-fast → google/gemini-3-flash-preview`. Same class, same provider, five weeks earlier: a hardcoded model slug went dead at the vendor and had to be hand-swapped after the fact. Two deprecation-driven breaks in five weeks is a pattern, not bad luck — and OpenRouter notes more than 70 models have been pulled or deprecated across providers ([OpenRouter blog](https://openrouter.ai/blog/tutorials/keep-your-agent-running-when-models-disappear/)).

There is no failover to absorb it. `backend/app/utils/llm_client.py` has no OpenRouter `models=[...]` fallback array — its `except` blocks handle JSON repair and empty responses, not a dead model ID. So when the single configured slug 404s, the call 404s. OpenRouter's documented remedy for exactly this — route through a fallback array or a preset so one edit fixes every caller — is the thing MiroShark doesn't do; its "presets" hardcode the same dead slug that the default does.

## Counter-evidence / what would change my mind

The honest case against alarm: the fix is trivial and already in flight. PR #204 is a 37-line find-and-replace, reports `1424 passed` on the offline suite and a green frontend build, and only needs a merge. The swarm engine (`simulation_runner` / `simulation_manager`) is untouched — this is configuration, not core. A self-hoster who sets their own `LLM_MODEL_NAME` never hits it; only users on the shipped default 404. But that default *is* the stranger's path — the $1 cloud cheap preset is precisely what a first-time runner uses — so "only the default" is the opposite of reassuring. The thesis would be wrong if `main` already carried `xiaomi/mimo-v2.5`, or if #86 didn't exist and this were a one-off; both were checked, and both hold.

## Why it matters

MiroShark's stated priority-zero is the gap between "$1 to simulate anything" and a stranger's first successful run. A deprecated default model puts a 404 at the very front of that path — the worst possible first impression, on the exact flow meant to convert curiosity into a run. And because the breaking input is a vendor-controlled identifier, it will recur on a schedule no one in the repo controls. The May grok swap and the June mimo swap are the first two instances; with 70-plus model retirements already logged across providers, the third is a matter of when. Until the default routes through a fallback array or pins a dated slug like `xiaomi/mimo-v2.5-20260422`, every provider sunset is a fresh first-run outage that an outside contributor has to notice before the maintainer does — which, this week, is exactly what happened.

---
*Sources*
- [PR #204 — migrate deprecated xiaomi/mimo-v2-flash → xiaomi/mimo-v2.5](https://github.com/aaronjmars/MiroShark/pull/204) (in-repo)
- [config.py:37 — live default on `main`](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/config.py#L37) (in-repo)
- [Commit 44d1c4e / PR #86 — prior deprecated-model swap (grok → gemini)](https://github.com/aaronjmars/MiroShark/commit/44d1c4e) (in-repo)
- [OpenRouter — MiMo-V2-Flash model page (deprecation timeline)](https://openrouter.ai/xiaomi/mimo-v2-flash) (external)
- [OpenRouter — "Keep Your Agent Running When Models Disappear"](https://openrouter.ai/blog/tutorials/keep-your-agent-running-when-models-disappear/) (external)
- [LiteLLM #20521 — 39 OpenRouter models no longer exist in the API](https://github.com/BerriAI/litellm/issues/20521) (external)
