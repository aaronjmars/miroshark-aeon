# MiroShark's Engine Failed Quietly Twice This Week — and One Self-Hoster Found Both

When MiroShark's scenario suggester broke on June 18, it didn't crash. It returned `HTTP 200`, an empty list, and a one-line backend warning: `suggest-scenarios: LLM returned an empty response`. A user uploading a German PDF saw three blank suggestion slots and no reason why. That is the failure mode MiroShark spent its week fixing — not crashes, but success codes wrapped around nothing. Both bugs came from the same place: someone running the engine outside its defaults.

## The claim
> MiroShark's two engine bugs fixed this week failed silently — HTTP 200 with zero suggestions (#192), agents reverting to Chinese mid-run (#189) — surfaced by one self-hoster.

## Evidence

The first bug is [#187](https://github.com/aaronjmars/MiroShark/issues/187), filed by Daniel Andersen (`dan-and`), who runs MiroShark self-hosted on local LLMs. Upload a document and the engine asks a model for three scenario suggestions as a JSON array, capped at 700 tokens. A verbose or slow local model either times out or blows past the cap; the JSON truncates mid-object; `chat_json`'s strict `json.loads` raises; and `suggest_scenarios` catches the error and converts it into an empty list returned at `HTTP 200` ([simulation.py:546-552](https://github.com/aaronjmars/MiroShark/blob/main/backend/app/api/simulation.py)). The user sees no suggestions and no error.

The first fix, [#188](https://github.com/aaronjmars/MiroShark/pull/188), was a mitigation: raise the timeout 20s→40s and the token cap 700→1500 (`simulation.py:515` and `:550`, two lines changed). aaronjmars' own follow-up issue [#191](https://github.com/aaronjmars/MiroShark/issues/191) called it a mitigation rather than a real fix, and corrected the original diagnosis: there is no language directive in the prompt, so output language simply follows the input document. The real failure is verbose output in *any* language exceeding the cap — not "non-Chinese languages." [#192](https://github.com/aaronjmars/MiroShark/pull/192) shipped the actual repair: a new `backend/app/utils/json_repair.py` (4,904 bytes, +306/−119 across 6 files) that re-closes truncated strings and brackets, then trims back to the last complete object — so every fully-emitted suggestion survives and only the half-written last one is dropped. It is wired in opt-in via `chat_json(repair_truncated=True)`, used only here.

The second bug hides inside [#189](https://github.com/aaronjmars/MiroShark/pull/189), dan-and's German translation PR (+2,888 / −1,973 across 48 files). Buried in the description: the pre-i18n engine had agents that "sometimes jump back into chinese" mid-simulation even when a user picked Chinese, French, or English. A sim that runs to completion but narrates part of its agents in the wrong language is, again, a quiet degradation — the run looks healthy, the output is wrong. The PR reinforces language selection across agent profiles and communications to stop it.

Both bugs were surfaced by the same external contributor, running the engine in conditions the hosted demo never hits: local models that are slower and more verbose, and non-English document inputs.

## Counter-evidence / what would change my mind

The honest qualifier is in #191 itself: this is not really an "i18n broke the engine" story. The token-cap truncation is language-agnostic — a long enough English response fails identically. The language framing was dan-and's initial misdiagnosis, and aaronjmars corrected it in writing. So if you read the thesis as "non-English usage exposed bugs," that is only half true. What holds is narrower and more durable: the engine's silent-failure design — returning success on partial or empty output — is what both fixes target. And neither fix touches the swarm core (`simulation_runner.py`, `simulation_manager.py`); these are API-layer and prompt-layer repairs. "Engine bugs" here means the surface a user actually hits, not the inner agent loop, which stayed untouched this week.

## Why it matters

MiroShark's whole pitch is "simulate anything for $1," and the corollary is that a stranger's first self-hosted run is the number that matters most. Silent failures are the worst possible bug for that pitch. A crash tells a new user something went wrong; an `HTTP 200` with zero results tells them the product is empty — or worse, that it ran and had nothing to say. For a tool asking people to *trust* a cheap simulation, returning success on failure erodes exactly the trust it is trying to earn. The underlying pattern — JSON truncated past a token cap, parsed strictly, failing without a trace — is a well-documented trust-boundary problem across LLM apps ([dev.to](https://dev.to/nexadiag_nexa_312a4b5f603/why-jsonparse-fails-silently-on-truncated-llm-responses-and-what-i-did-about-it-3681), [tensoria.fr](https://tensoria.fr/en/blog/structured-outputs-llm-production)). MiroShark's edge cases all surface off the default path: local LLMs, verbose output, non-English input — the exact path every external adopter takes. Fixing them where strangers land is worth more than another feature on the demo.

---
*Sources*
- [Issue #187 — suggest_scenarios breaks + sharp LLM timeouts (dan-and)](https://github.com/aaronjmars/MiroShark/issues/187)
- [PR #188 — raise suggest-scenarios timeout and token limit](https://github.com/aaronjmars/MiroShark/pull/188)
- [Issue #191 — salvage truncated JSON instead of relying on the token cap](https://github.com/aaronjmars/MiroShark/issues/191)
- [PR #192 — salvage truncated suggest_scenarios JSON (json_repair.py)](https://github.com/aaronjmars/MiroShark/pull/192)
- [PR #189 — German translation + agent-language reinforcement (dan-and)](https://github.com/aaronjmars/MiroShark/pull/189)
- [Why JSON.parse() Fails Silently on Truncated LLM Responses — dev.to](https://dev.to/nexadiag_nexa_312a4b5f603/why-jsonparse-fails-silently-on-truncated-llm-responses-and-what-i-did-about-it-3681)
- [Why 15% of Your JSON Prompts Fail — tensoria.fr](https://tensoria.fr/en/blog/structured-outputs-llm-production)
