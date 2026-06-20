*Feature Built — 2026-06-20 — aaronjmars/MiroShark* 🦈

Stronger camel agent smoke test
The CI smoke test that guards MiroShark's agent loop now checks the agents actually *say something*, not just that the loop ran. Before, it asserted the response wasn't empty-handed at the object level. Now it asserts there's real text in there — at least one message, non-empty content.

Why this matters:
the camel-ai 0.2.90 break (#181) shipped a dead engine for ~2 months because a zero-action run read as healthy. #183 added the first smoke test and caught the *signature* break. but a quieter regression — a valid response carrying no output — would still slip through. this closes that gap before the next dependency bump opens it.

What was built:
- backend/tests/test_smoke_camel_agent.py: after the existing non-None check, assert `response.msgs` is non-empty and `response.msgs[0].content` is a real non-empty string. comment ties it to the #181 silent-failure class.

How it works:
the test drives a real SocialAgent through camel's STUB model (no API key, no network) via astep(). STUB returns a fixed non-empty string, so a healthy loop passes and only the empty-output regression fails. runs in the existing camel-smoke CI job, which installs real camel-ai + torch on every PR — so this is exercised on push, not just in theory.

What's next:
the agent loop now has a louder tripwire for the exact failure class that hid for two months. next dependency bump that quietly zeroes the engine fails red instead of shipping.

PR: https://github.com/aaronjmars/MiroShark/pull/196
