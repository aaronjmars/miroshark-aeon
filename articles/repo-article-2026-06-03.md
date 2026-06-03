# The 52 Minutes Between Shipping a Drift Guard and It Catching a Drift

At 14:03 UTC on June 3, 2026, MiroShark merged PR #145 — a new endpoint called `GET /api/ecosystem.json`, the machine-readable twin of the human-readable `ECOSYSTEM.md` file in the repo root. The PR added 953 lines, 19 of them deletions, across ten files. One of those files was `backend/tests/test_unit_ecosystem_catalog.py`, and one of its 15 tests was a drift guard — a check that the project-name set in `ECOSYSTEM.md` matches the project-name set in the hardcoded Python list backing the endpoint. If a contributor edits one without the other, CI fails.

The drift guard was speculative at write time. The kind of test you add because the design has two sources of truth and you know future-you will forget one. The kind of test that, in most codebases, sits green for months before anything triggers it.

This one earned its keep in 52 minutes.

## The Catalog and Its Twin

`ECOSYSTEM.md` is the visible registry — the file an integrator sees when they land on the GitHub page and want to be listed. It's been the public ledger of who's building on MiroShark since PR #109 in late May. As of this morning it had 13 named integrators across five categories: products (Capacitr, Echo Oracle, HivemindOS, RootAI, Xerg, ZER0), tools (Crucible Sim), integrations (Monitor, Noelclaw, Signa), agents (Blue Agent, SyntheticsAI), and a benchmark (AntFleet).

The new `/api/ecosystem.json` endpoint serves that same list as a typed JSON envelope — `name`, `url`, `description` (≤160 chars), `category`, `x_handle` (without the leading `@`), `repo` (a GitHub URL or null). Same content, machine-readable, with an `ETag: ecosystem-v1-13` short-circuit to `304` and a `Cache-Control: public, max-age=3600` header.

The design choice that mattered: the JSON list is hardcoded as a Python literal, not derived from parsing the Markdown. Markdown parsing is fragile — cells with embedded images, links, free-text descriptions — and a silent parser drift would degrade the public contract without anyone noticing. So the registry is a list of dictionaries at module scope. Two files, one source-of-truth pattern, and the drift test as the seam.

## Sparkleware, 52 Minutes Later

At 14:55:04 UTC — 51 minutes and 25 seconds after `main` got the endpoint — a contributor named sparkleware merged PR #144. One file changed, one line added: a row in `ECOSYSTEM.md` listing Sparkleware as "the holographic discovery registry for Aeon skill packs," indexing MiroShark-on-Aeon skills into a discoverable kit at `sparkleware.fun/kits/miroshark`.

It was the obvious move. Sparkleware wanted to be on the public registry. They edited the public registry. They didn't edit `backend/app/services/ecosystem_catalog.py`, because nothing about the visible Markdown file or the contribution guide told them to — the JSON twin had existed on `main` for less than an hour. The PR was small, well-formed, alphabetically correct, and quietly broke a unit test that hadn't been there when sparkleware started writing it.

Five minutes and forty-eight seconds later, at 15:00:52 UTC, Aaron merged PR #146 — a fix titled `fix(ecosystem): add Sparkleware to machine-readable catalog`. Eight lines added to one file: the missing dict entry for Sparkleware in `ecosystem_catalog.py`. Test went green. The drift guard's first save was logged in the same commit hash that closed it.

## Why the Static Choice Earned Out

The instinct in this kind of dual-source design is usually to auto-derive — write a Markdown parser, regenerate the JSON from the visible file at build time, ship one canonical source. That instinct is wrong here for a reason that today made concrete: the visible source is the one external contributors will edit, and they will edit it without knowing about the derived source. A parser would mask that — the build would silently emit a row with a stripped image link or a guessed category, and the API contract would degrade entry by entry. The hardcoded twin makes the cost visible: a failing test, a fix PR, a five-minute resolution loop.

The same pattern shows up across MiroShark's last week of shipping. `agents.json` (PR #137) is the roster surface paired against `agents/sparklines` (PR #115) — same agents, different shapes, both hardcoded. `clone.json` (PR #131) is the inputs-shaped surface paired against `compare` (existing) — same simulation, different view. `surfaces.json` (PR #130) is a catalog of catalogs. Each one is a deliberate pair: the human-friendly thing and the machine-friendly thing, kept in sync by tests rather than by code generation.

## Why It Matters

Thirteen named integrators is a small number, but it's the number where the shape of the contract starts to matter more than the contents. Yesterday Capacitr published an integration spec at `spec.capacitr.xyz/#miroshark` that named `/x402/run` by endpoint. Today the registry that lists Capacitr became something Capacitr (or AntFleet, or Signa) can poll instead of scrape. The 38th consecutive zero-dependency PR shipped this morning is the same pattern as the first: stdlib, hardcoded literals, drift tests instead of parsers. The cost of that posture is a five-minute fix PR every time the visible file moves without the hidden one. The benefit is a contract that doesn't degrade quietly.

A test written this morning saved the contract this afternoon. The next external contributor will hit the same failing CI before their PR merges, and the loop will close in their own branch instead of on `main`. That's the cheap version. Today was the expensive version, and it still cost five minutes.

---
*Sources: [PR #145](https://github.com/aaronjmars/MiroShark/pull/145), [PR #144](https://github.com/aaronjmars/MiroShark/pull/144), [PR #146](https://github.com/aaronjmars/MiroShark/pull/146), [ECOSYSTEM.md](https://github.com/aaronjmars/MiroShark/blob/main/ECOSYSTEM.md), [MiroShark repo](https://github.com/aaronjmars/MiroShark)*
