# MiroShark Stopped Marketing the $1 and Started Letting You Audit It

The repo's tagline is "simulate anything, for $1 & less than 10 min." For most of its life that number lived in a README. This week it moved into the product. Three cost surfaces shipped in eight days — an API endpoint, a public embed pill, and now a CLI command that prints the bill from your own terminal. None of them claims the run was cheap. Each one shows you exactly how cheap, and admits where the figure is a floor.

## The claim
> MiroShark turned "$1 to simulate" from a tagline into a number you can audit: three cost surfaces in eight days, each an honest lower bound.

## Evidence

The triad starts with [`GET /api/simulation/<id>/cost.json`](https://github.com/aaronjmars/MiroShark/pull/179) (PR #179, commit `a52ea34`, merged 06-16). It returns `estimated_cost_usd` plus `by_model` and `by_phase` breakdowns — the "$1" claim made queryable per run. The payload carries its own disclaimer: `is_estimate: true` and a `pricing_basis` string that spells out the catch — "untracked models count as $0.00, so the true spend is at or above this figure." The number is a floor, stated as one.

Three days later the floor went where strangers actually look. [PR #190](https://github.com/aaronjmars/MiroShark/pull/190) (commit `09a60cf`, merged 06-19) put a `~$X` cost pill on the public `EmbedView` — the shareable simulation card. The `~` is doing real work: it signals the estimate caveat to someone who will never read `cost.json`.

The gap that closed today: neither of those was reachable from a script. [PR #208](https://github.com/aaronjmars/MiroShark/pull/208) (commit `cef787b`, merged 06-23) adds a `cost` subcommand to the CLI. `python backend/cli.py cost sim_abc123` prints `~$0.9213 (1,284,902 tokens, 871 LLM calls)` with a per-phase breakdown. The implementation (`cmd_cost`, `backend/cli.py:201` on `main`) calls the same `cost.json` endpoint and mirrors the embed's `~` prefix off the same `is_estimate` flag (`cli.py:220`). It even degrades honestly: exit code `2` when no cost is logged yet, `--json` for the raw payload. Cost observability is now a one-line audit after any run — matching the existing `status` / `report` / `publish` command surface.

The connective tissue across all three is the refusal to round up. Same flag, same caveat, same `~`. The product would rather show you `$0.92` with an asterisk than `$1.00` with a straight face.

## Counter-evidence / what would change my mind

The honest hole: this is one source of truth with three readers, not three independent measurements. The embed pill and the CLI both re-read `cost.json`. If the endpoint undercounts — and by its own `pricing_basis` it does, treating untracked models as $0 — all three undercount identically. More surfaces don't make the floor higher. They make the same floor visible in more places.

And none of this makes a simulation cheaper. The engine core (`simulation_runner` / `simulation_manager`) sat untouched again this window — the $1 is being *measured*, not lowered. Worse for the velocity story: two of the eight days went to firefighting, not cost work. The shipped default model `xiaomi/mimo-v2-flash` had been deprecated by OpenRouter, so [PR #207](https://github.com/aaronjmars/MiroShark/pull/207) swapped it to `mimo-v2.5` (06-22) and [PR #210](https://github.com/aaronjmars/MiroShark/pull/210) patched a blank-env-var fallback (06-23). The cost surfaces shipped next to a reactive cleanup, not in a clean sprint. The thesis would be wrong if fewer than three cost surfaces had landed, or if any of them quietly dropped the lower-bound caveat. Both held up — I checked the live `cli.py` and the `cost.json` payload schema.

## Why it matters

The hardest distance in this repo is between the words "$1 to simulate anything" and a stranger's first run that actually costs about a dollar. A claim a person can verify from their own checkout — `python cli.py cost <id>`, no dashboard, no signup — is the thing that converts a tagline into trust, and trust into repeat runs.

The contrast with the rest of the field is the point. Cost tracking in 2026 mostly means a hosted dashboard you instrument and log into: [Langfuse](https://langfuse.com/docs/observability/features/token-and-cost-tracking), Helicone, LangSmith — all SaaS, all behind an account ([Braintrust's 2026 roundup](https://www.braintrust.dev/articles/best-llm-tracing-tools-2026) is a fair map). MiroShark's cost surface lives inside the open-source repo, runs on the machine that ran the sim, and ships the caveat in the payload instead of in a pricing-page footnote. Most products advertise a price. Almost nobody hands you the command to check the bill. 🦈

---
*Sources*
- [PR #208 — CLI `cost` subcommand](https://github.com/aaronjmars/MiroShark/pull/208) (in-repo)
- [PR #190 — cost pill on public embeds](https://github.com/aaronjmars/MiroShark/pull/190) (in-repo)
- [PR #179 — `cost.json` per-sim endpoint](https://github.com/aaronjmars/MiroShark/pull/179) (in-repo)
- [PR #210 — blank `LLM_MODEL_NAME` fallback](https://github.com/aaronjmars/MiroShark/pull/210) (in-repo)
- [Langfuse — token & cost tracking docs](https://langfuse.com/docs/observability/features/token-and-cost-tracking) (external)
- [Braintrust — best LLM tracing tools, 2026 review](https://www.braintrust.dev/articles/best-llm-tracing-tools-2026) (external)
