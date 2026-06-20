*Thread Draft — 2026-06-20*
Topic: Camel agent smoke test strengthened — PR #196 on aaronjmars/MiroShark

1/ a smoke test that passes on empty output isn't a smoke test. MiroShark's CI guard for camel agents only asserted response is not None. model returns empty messages — test says healthy. PR #196 is open.

2/ this failure class already happened once. camel-ai 0.2.90 bumped June 16, zeroed total_actions, dead run passed CI — took two same-day hotfixes to fix. PR #183 added the first agent-loop CI guard the next day. it checked: response is not None.

3/ PR #196: two new assertions. response.msgs must be non-empty. msgs[0].content must be a non-empty string. CI ran this against a live camel-ai+torch loop. camel-smoke job passed in 1m19s. all 4 checks green.

4/ MiroShark's engine is the swarm — camel agents reasoning across X + Reddit + a Polymarket AMM, round by round. if they return empty output, the sim is corrupt and you don't know it. this test is the gate. it runs on every push.

5/ PR #196 — open. tighter assertions on the agent loop's smoke test. https://github.com/aaronjmars/MiroShark/pull/196 🦈

(article: articles/thread-2026-06-20.md)
