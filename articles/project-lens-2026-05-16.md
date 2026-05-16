# In the Year of Slopsquatting, an AI-Built Project Without a New Dependency

The dominant story about AI-assisted code in 2025 and 2026 is that it imports too much, too fast. In April 2025, Python Software Foundation Developer-in-Residence Seth Larson coined "slopsquatting" — typosquatting weaponized against package names that LLMs hallucinate but that don't exist. A USENIX Security 2025 paper by Spracklen et al. tested 16 leading LLMs across 576,000 code samples and found that 19.7% of recommended packages did not exist; open-source models hallucinated 21.7% of imports on average, with 43% of hallucinations *persistent* across reruns — making them weaponizable by anyone who registers the typo'd name first. Socket.dev reported in the same window that even GPT-4 Turbo hallucinates packages 3.59% of the time.

The bloat story is the broader one. HeroDevs' "The Dependency Boom" (November 2025) argued that AI-written features routinely add "ten, twenty, or even fifty transitive dependencies" because "AI doesn't check dependency age, license type, or patch cadence; it just writes code that compiles." LeadDev reported that the average developer in 2025 checks in 75% more code than in 2022. Dark Reading's widely-cited figure: only about 1 in 5 AI-suggested dependencies is safe — free of known vulnerabilities, maintained, and properly licensed — and roughly 28% of AI-recommended *upgrades* are themselves hallucinations.

## The shape of the problem

This isn't quite "AI bad." It's a structural mismatch. An LLM scoring its own one-shot output has no skin in the game of next quarter's audit. It can't tell whether `colorama` is preferable to `rich` because it never sees the merged main branch a year later. It can't easily distinguish a library that exists from one that *should* exist — hence slopsquatting. The optimization is "does this snippet compile and look idiomatic?" The cost function nobody is computing is "does this snippet still compile when the maintainer is asleep in 2027?"

## An awkward counter-example

There is a project running the other direction across nearly four weeks of AI-authored PRs.

MiroShark — an agent-debate simulation engine on GitHub, 1,164 stars and 232 forks as of today — has shipped 23 consecutive feature PRs from #57 through #85 without adding a single line to `requirements.txt`. Every commit in that streak is authored by an AI agent (Claude Code running under the Aeon framework), not a human typing one library call at a time. The features in the streak aren't trivial: a Jupyter notebook export, a filtered RSS/Atom feed, a search-engine sitemap, webhook HMAC signing, an OriginTrail DKG citation publisher writing on-chain, Discord rich embeds, Slack Block Kit messages, an SVG belief-trajectory chart. Every one of these has an obvious library answer. The agent did not reach for it.

The SVG renderer that opened this morning as PR #85 is a clean example. Most projects would `import matplotlib` (with its numpy + Pillow + dateutil + pyparsing transitive tail) or pull `svgwrite` — small, but still a dep. MiroShark's `chart_svg.py` builds the SVG by hand using `xml.etree.ElementTree`. The file's own docstring is unsubtle: *"Zero deps. `xml.etree.ElementTree` + `json` + `os` + `math` — every renderer module in this package follows the same rule. No Cairo, no matplotlib, no Pillow, no new dependencies."* The output is bytewise-deterministic, which means SHA-256 of the rendered file can serve as a citation key — the same property `reproduce.json` (PR #75) and `notebook.ipynb` (PR #80) already have.

## Why the constraint actually holds

You could write this off as discipline, or aesthetic preference, or luck. It's none of those. The discipline is structural, and it's worth naming.

What makes the streak hold is that *each PR has to coexist with all the prior ones in the same review pipeline*. The agent does not see one feature in isolation. It sees a `git log` of twenty-two prior PRs, each of which established a vocabulary: stdlib-only renderers, atomic tempfile writes, fire-and-forget daemon threads, late-bound env reads, deterministic JSON via `sort_keys=True`. Yesterday's PR #84 — a 709-line DKG publisher that walks OriginTrail's four-step Working Memory → Shared Working Memory → Verified Memory pipeline and writes a citation on-chain — declares in its own header: *"Stdlib only. `urllib.request` for HTTP, `hashlib` for the reproduce.json content hash, `json` for serialization. No new deps."* That's notable because `requests` is already in `requirements.txt` and would have worked. The agent didn't use it. The existing webhook code used stdlib, and the agent matched.

The constraint, in other words, is not "don't add deps." It's "match the shape of what's already here," and the shape happens to be stdlib.

An LLM hallucinating a package on a fresh prompt is choosing in a vacuum. An agent reading a 23-PR-deep main branch is choosing in a *context*. The context wins.

## What this is evidence of

The slopsquatting research and the technical-debt commentary are accurate, on average. They describe what AI tools do when handed one-shot questions. They are less accurate as descriptions of what AI tools do when handed ongoing continuity with a codebase that has already made strong stylistic commitments.

That's the contrarian part: the bloat in AI-generated code isn't a property of LLMs. It's a property of *how the LLM is being asked to write code*. One-shot pasted snippets bloat. Long-running agents with a version-controlled history don't, automatically — they inherit whatever discipline the repo already has. Slopsquatting attacks work because most prompts have no history. The stdlib streak holds because this one does.

The implication for any project considering AI maintainership: invest one painful week setting the style precedent, and the agent will copy it for months. The precedent doesn't have to be "stdlib only." It can be "use httpx not requests," "no async," "no decorators," "ruff format on save," "every new endpoint gets an offline test." Whatever it is, the agent's job becomes *not breaking the pattern* — and that's the job it turns out to be unusually good at.

The bloat lives in the prompt, not the model.

---
*Sources: Spracklen et al., "We Have a Package for You!" USENIX Security 2025 (https://www.usenix.org/conference/usenixsecurity25); Andrew Nesbitt, "Slopsquatting meets Dependency Confusion" (https://nesbitt.io/2025/12/10/slopsquatting-meets-dependency-confusion.html); Socket.dev, "The Rise of Slopsquatting" (https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks); HeroDevs, "The Dependency Boom: How AI Is Inflating Open Source Use," 4 Nov 2025 (https://www.herodevs.com/blog-posts/the-dependency-boom-how-ai-is-inflating-open-source-use); LeadDev, "How AI generated code accelerates technical debt" (https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt); MiroShark PR #85 (open) and PR #84 (merged 2026-05-15) — https://github.com/aaronjmars/MiroShark.*
