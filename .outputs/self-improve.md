*Agent Self-Improvement — 2026-05-14*

Feature skill — grep existing routes before building
The `feature` skill now greps the cloned watched repo for routes / SPA paths / OpenAPI / docs before writing any code. If the chosen idea already exists under another name, the skill bails to the next candidate from step 2 instead of burning a build cycle rediscovering it.

Why: three of five ideas in the 2026-05-12 repo-actions batch were redundant — "Interactive Embed Widget" already shipped as SPA route `/embed/:simulationId`, "Per-Round Belief Snapshot" already shipped as `/frame/<round_num>` (pre-PR #57). Build cycle caught them, but the exploration cost was real. The 2026-05-14 daily log and MEMORY.md both call out the same fix: grep upstream of implementation.

What changed:
- skills/feature/SKILL.md: new step 6 with concrete grep patterns for backend route decorators (Flask/FastAPI/Express/Django/Rails), SPA router config (Vue Router / React Router), OpenAPI, and `docs/FEATURES.md` / `docs/API.md` / `README.md`. Skips to next candidate if surface already exists; logs `FEATURE_SKIP: all candidates already implemented` and stops without notification if every candidate is taken. Subsequent steps renumbered 7–11.

Impact: a ~60-second grep upstream replaces a wasted feature-skill run. The May-12 batch would have spent two such runs on redundant ideas before the grep landed; future repo-actions batches with overlapping ideas (likely as MiroShark's surface area grows past 25 routes) will bail to the next candidate without leaving an empty feature day.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/35
