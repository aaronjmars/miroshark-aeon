# Sub-Second Tests: The Boring Discipline Letting Some Teams Ship Daily While AI Slows Others Down

The 2025 DORA report on AI-assisted software development arrived with a paradox in the headline. AI tools improved developer throughput by 30 to 40 percent — and pushed change failure rates up by 15 to 25 percent. Teams shipping faster are also breaking more. DORA's framing is that AI is "an amplifier": it makes good engineering organizations better and weak ones worse.

What the report doesn't quite say, but the data shows, is that the amplifier picks one weakness to magnify above all others: **slow feedback loops**. Where engineers cannot run a test suite in seconds, AI-generated code lands without anyone re-checking it. A separate line of research from this spring is sharper still — 68 to 73 percent of AI-generated code contains real security or correctness flaws, and the unit tests AI agents write alongside that code generally fail to catch them, because both come out of the same training-data blind spots. Coverage numbers go up. Defect catch rates go down. The tests are tautological: they verify that the code does what the code does.

This is the moment to look at projects still moving cleanly, and ask why.

## The trap

The slowest part of any working software project tends not to be writing code. It is the loop between writing a change and learning whether it broke anything. When that loop is fast — under a second, ideally — engineers run tests after every keystroke and pre-empt regressions before they leave the laptop. When the loop is slow, engineers run tests rarely, batch their changes, and find the problems in production. Google's testing organization made this argument again last October, advocating a pattern called *functional core, imperative shell*: keep the logic of the program separate from the parts that touch the network and the database, so the logic can be tested in milliseconds without booting the rest of the system. The pattern is old — Gary Bernhardt named it in 2012 — but the urgency is new. AI is pushing far more code through the loop than ever before, and projects whose loops are slow are silently going to the back of the line.

## What the pattern looks like in practice

MiroShark, an open-source agent-based simulation engine, shipped its fourth public discovery surface in eight days yesterday: an RSS and Atom feed of the simulation gallery. PR #60 added 1,604 lines and exactly **17 new unit tests** — and those 17 tests, plus all 80-odd tests written for the discovery surfaces shipped this past week, finish in well under a second on a laptop, with no Flask server running, no internet, no database, no fixtures.

It isn't magic. It's a structural choice visible plainly in the test file. The renderer for the new feed lives in `backend/app/services/feed.py`. It is a function. Hand it a list of dictionaries describing public simulations, get back an XML string. There is no "fetch the gallery from the database" step, because the function never asks for one. A separate, much smaller request handler takes the web call, pulls cards off disk, and passes them to the renderer. The renderer doesn't know it's on the internet. It can be tested with hand-built dictionaries the way you'd test a calculator.

The 17 tests do exactly that. They check that an Atom feed with three cards has three `<entry>` elements. They check that a 100-character scenario gets truncated with an ellipsis. They check that the verified-only filter changes the title. They check that a card missing optional fields produces "(untitled scenario)" instead of crashing. None calls the real internet. None spawns a real server. None needs a real simulation to have ever been run.

## Why it's bigger than it sounds

Three things flow from that structural decision, and they compound:

**The tests are fast enough to actually get run.** The five share surfaces shipped this past week — share card, replay GIF, transcript, RSS feed, verified-outcome page — collectively added roughly 80 unit tests. The whole backend suite still runs in seconds. There is no point in the workflow at which an engineer says "I'll skip the tests, they take too long."

**The tests survive AI generation.** The tautology making AI-written tests rotten — *the test asserts what the code happens to do* — depends on the test mirroring the implementation's structure. A test that constructs a fake gallery card and asserts the resulting feed says "62.0%" mirrors the *requirements'* structure, not the code's. An AI assistant rewriting the renderer would still have to make that test pass.

**The tests double as the contract.** One test checks the OpenAPI spec hasn't drifted from the live Flask routes. Another checks the transcript's YAML front matter parses. Another checks the RSS feed's `<guid>` is stable across deployments. These aren't implementation details. They're promises the project has made to its users — promises the suite enforces every commit. Documentation lies. Production lies. A unit test that runs in 30 milliseconds does not.

## What it means

The DORA paradox — faster output, more breakage — looks like a tooling problem. Underneath, it's an architectural one. The teams getting AI's speed without AI's instability are not using better AI; they are running on codebases where the feedback loop was already short enough to catch AI's mistakes the same minute they're made. The teams paying the failure-rate tax are running on codebases where the loop was always slow, and AI is now hammering them with five times more changes than the loop can absorb.

The fix is not exotic. It is the discipline of separating the logic from the world, and writing tests against the logic in isolation. It is unfashionable, in 2026, to call a 1990s testing principle a hidden lever of competitive advantage. But the projects quietly compounding through this period — shipping every day, never breaking what shipped the day before — are the ones doing exactly that. MiroShark's RSS feed shipping today, with its 17-test offline suite, is what that discipline looks like from outside the codebase.

The teams that build for the AI decade will not be the ones with the best AI. They will be the ones whose tests still finish in under a second.

---
*Sources: [DORA | State of AI-assisted Software Development 2025](https://dora.dev/dora-report-2025/) · [Google Testing Blog: Simplify Your Code — Functional Core, Imperative Shell (Oct 20, 2025)](https://testing.googleblog.com/2025/10/simplify-your-code-functional-core.html) · [Why Unit Tests Fail AI-Generated Code | testkube](https://testkube.io/blog/system-level-testing-ai-generated-code) · [The Hidden Costs of AI-Generated Code in 2026 | Codebridge](https://www.codebridge.tech/articles/the-hidden-costs-of-ai-generated-software-why-it-works-isnt-enough) · [Functional Core, Imperative Shell — Destroy All Software (Gary Bernhardt, 2012)](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) · MiroShark PR #60 (RSS / Atom feeds, merged 2026-04-30 13:12 UTC), PR #57 (transcript, Apr 29), PR #50 (replay GIF, Apr 28), PR #47 (`/verified`, Apr 27), PR #46 (webhook, Apr 26), PR #45 (OpenAPI, Apr 25)*
