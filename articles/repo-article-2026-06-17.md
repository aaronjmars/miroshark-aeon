# MiroShark Shipped Its Agent Loop Untested for Two Months — Then a Dependency Bump Returned Zero Agents

MiroShark's CI ran an offline unit suite that, by design, never touched camel-ai or the agent loop the whole product is built on. That hole stayed open from April until June 16, when a routine Dependabot bump — camel-ai 0.2.78 → 0.2.90 — silently zeroed every agent's output and slipped through review reading as a healthy run. The fix wasn't a patch; it was the engine's first regression guard.

## The claim
> For ~2 months MiroShark's CI never ran its real agent loop; only after camel-ai 0.2.90 silently zeroed it did #183 add the first smoke test.

## Evidence

The gap was structural, not an oversight in one PR. The `unit` job in [`.github/workflows/tests.yml`](https://github.com/aaronjmars/MiroShark/blob/main/.github/workflows/tests.yml) installs "only the thin dependencies the unit suite needs" and skips torch and camel-ai outright — the comment in the file says so. The workflow's last substantive edit before this week was in April (`d3cfff7`, the OASIS→Wonderwall rename); every commit since was a dependency bump. So from spring to June 16, nothing in CI exercised the camel ↔ wonderwall integration that actually drives a simulation.

Then `dependabot` opened [#176](https://github.com/aaronjmars/MiroShark/pull/176), bumping camel-ai to 0.2.90 inside the `backend-minor-patch` group. Camel had changed the signature of `ChatAgent._aget_model_response`; MiroShark's `SocialAgent` overrides that method, so the override broke and agents stopped producing actions. The repair, [#181](https://github.com/aaronjmars/MiroShark/pull/181) (`446ad7b`), was two lines — merged *before* #176 to unblock it.

The dangerous part is why nobody noticed first. [#183](https://github.com/aaronjmars/MiroShark/pull/183) (`fe6efc3`) documents it: `run_parallel_simulation.py` called `logger.log_simulation_end(total_rounds, 0)` — a hardcoded `0`. So a fully successful run logged `total_actions=0`, identical to a run where every agent had errored out. A dead agent loop and a healthy one printed the same number.

#183 closed both holes at once. It added `backend/tests/test_smoke_camel_agent.py` (78 new lines) that drives the *real* `SocialAgent` through camel's async model-response path using camel's STUB model — no API key, no network — and asserts the override stays signature-compatible. It also added a `camel-smoke` CI job that installs the real camel-ai from `requirements.txt`, "so a Dependabot bump re-triggers it." The PR reports the test "fails with the exact `TypeError: SocialAgent._aget_model_response() missing 1 required positional argument: 'num_tokens'` when the #181 fix is reverted." The same day, [#180](https://github.com/aaronjmars/MiroShark/pull/180) added a separate `frontend` build job (22 lines) after the 0.2.90 bump had also broken the Docker build via a stale `uv.lock` ([#182](https://github.com/aaronjmars/MiroShark/pull/182)). Two CI guards, both added reactively, within four hours of the breakage.

## Counter-evidence / what would change my mind

The unit suite is real and was expanded this week — #165 even fixed two demographic-grounding tests, so the project isn't testing-hostile. And the response was fast: the smoke test landed the same afternoon as the break, not weeks later. The strongest argument against reading this as a process failure is that #183's smoke test is narrow on purpose: it uses a stub model, so it guards *signature compatibility*, not output quality — a future camel-ai release that returns plausible-but-wrong content would still pass green. It also covers only the camel↔wonderwall seam; `simulation_runner` and `manager` remain untested, a fourth consecutive engine-frozen window per the project's own push logs. So MiroShark didn't get a regression *suite* this week. It got one tripwire on the exact wire that snapped.

## Why it matters

For a product whose entire pitch is "simulate anything for $1," a silently-zeroed agent loop is the worst possible failure mode: the run finishes, the bill lands, and the output is empty — yet the logs read healthy. That is precisely the silent-regression class the ML-testing field warns about, where dependency updates degrade behavior with nobody noticing ([Sentrial](https://www.sentrial.com/blog/ai-agent-regression-testing-that-catches-silent-failures)), and why smoke tests exist to validate a pipeline's "fundamental contract" after a dependency bump ([Sealos](https://sealos.io/blog/smoke-testing-for-ml-pipelines-catching-data-and-model-errors-before-they-hit-production/)). MiroShark just learned that lesson the expensive way and wired the tripwire that converts the next camel-ai break from a silent empty sim into a red CI check — which, for anyone deciding whether to trust a $1 run, is the part that matters.

---
*Sources*
- [tests.yml — unit job skips camel-ai/torch; camel-smoke + frontend jobs](https://github.com/aaronjmars/MiroShark/blob/main/.github/workflows/tests.yml)
- [PR #183 — total_actions fix + first camel agent smoke test](https://github.com/aaronjmars/MiroShark/pull/183)
- [PR #181 — camel-ai 0.2.90 _aget_model_response signature compat](https://github.com/aaronjmars/MiroShark/pull/181)
- [PR #180 — build the frontend on every PR](https://github.com/aaronjmars/MiroShark/pull/180)
- [Sentrial — agent regression testing that catches silent failures](https://www.sentrial.com/blog/ai-agent-regression-testing-that-catches-silent-failures)
- [Sealos — smoke testing for ML pipelines](https://sealos.io/blog/smoke-testing-for-ml-pipelines-catching-data-and-model-errors-before-they-hit-production/)
