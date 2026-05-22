# Academic Publishing Already Built The Stack For Citing Things. The Stack Is Borrowable.

The problem of "how do I make this thing citable" was treated as solved by 2015. CrossRef started minting DOIs in 1999. arXiv had been issuing stable preprint IDs since 1991. Zenodo, operated by CERN under the EU OpenAIRE programme, launched in 2013 and was hosting more than 70% of all persistently citable software by 2018 (DataCite's number, not Zenodo's). And on August 19, 2021, GitHub turned a community spec called CITATION.cff into a first-class repository feature — a YAML file in the root of a default branch, rendered as a "Cite this repository" sidebar that emits BibTeX or APA on demand. Hundreds of new CITATION.cff files have been landing in public repos per week ever since.

Read across those four layers and there is a quiet agreement on what a citation actually needs to be: a stable identifier, a manifest of metadata, a hash or version, a path back to the source. None of the four systems requires a journal. Three of them don't require a publishing house. One — CITATION.cff — doesn't even require a registrar.

That is the lens. The project worth looking at through it shipped its closing piece this morning.

## The four-layer stack

The four systems didn't replace each other; they layered.

- **CrossRef / DataCite** sit at the bottom: a paid registrar membership, a fee per DOI, in exchange for a globally resolvable URL that outlives institutional shutdowns. By 2018, Zenodo alone had registered DOIs for more software than any other source on the DataCite network.
- **arXiv** built a single-domain alternative for one community (physics, math, CS). Stable IDs, no DOI, no editorial gate. The cost is centralisation: arXiv decides what counts.
- **Zenodo** wrapped DataCite. Every uploaded artifact gets a DOI for free, GitHub releases auto-deposit, and the deposit page renders BibTeX inline. Most software citations between 2018 and 2024 went through this path.
- **CITATION.cff** moved the metadata into the source repository itself. Zotero parses it. Zenodo parses it. GitHub parses it. The "registrar" became the file next to the README.

What's been missing is the next move: take the same shape down to the artifact level. Not "cite the repo," not "cite the release" — cite the specific output the repo produced.

## Where the project enters

`aaronjmars/MiroShark` is a swarm-intelligence simulation engine: each run produces a finished artifact — a multi-agent trajectory, a stance distribution, a consensus signal. PR #96, **merged today at 13:32 UTC** (`gh pr view 96 --json state` → `MERGED`), adds the route the four-layer stack above implies but doesn't actually provide:

```
GET /api/simulation/<id>/cite.bib
```

It returns a single `@misc{…}` BibTeX entry, `text/plain; charset=utf-8`, which Zotero and Mendeley both import directly from an HTTP URL. The route is the 14th publish-gated surface attached to the same simulation object — sitting alongside `chart.svg`, `signal.json`, `reproduce.json`, `notebook.ipynb`, `archive.zip`, `dkg-citation`, `badge.svg`, the Atom and RSS feeds, the sitemap, the Farcaster frame, the share card, and the lineage graph. Same `is_public` gate, same `Cache-Control: max-age=300`, same bytewise-deterministic builder. Zero new dependencies — `bibtex_service.py` is ~310 lines of stdlib `hashlib` / `datetime` / `re`, and it lands inside a 30-PR streak with nothing new in `requirements.txt` or `package.json`.

## The non-obvious detail

The interesting part isn't the BibTeX. BibTeX is forty years old. The interesting part is what goes in two specific fields.

`note` carries the SHA-256 of the simulation's `reproduce.json` — the canonical bytes of the input parameters needed to re-run the simulation deterministically. Precedence is `DKG-anchor > fresh-compute > omit`: if the run has already been published to OriginTrail's Decentralized Knowledge Graph (PR #84, merged 2026-05-15), the on-chain hash wins, because the on-chain hash is the source of truth. `annote` carries the DKG UAL — the Universal Asset Locator — for the same anchor.

What this gives a researcher: a citation that arrives with its own integrity check (`sha256sum --check` against `<url>/reproduce.json`) and an on-chain provenance pointer that doesn't depend on the host being alive in 2031. CrossRef provides resolver stability; this provides cryptographic stability. They are not the same property, and the second one used to require a Zenodo deposit, a GitHub release, and a DataCite DOI in sequence.

The repository was already four endpoints into the idea before PR #96. `reproduce.json` (PR #79, merged 2026-05-11) provides the inputs. `notebook.ipynb` provides the analysis surface. `dkg-citation` provides the on-chain anchor. `cite.bib` is the human-readable layer that makes all three discoverable from a single LaTeX `\cite{}`. The citation arc closes today.

## Why the layer mattered

The publishing stack works because each layer solved one thing well — identifier, registrar, repository, metadata file — and let the next layer compose on top. The piece nobody had built for AI-style ephemeral outputs is the *per-artifact* citation endpoint: not "cite this codebase," but "cite this specific run, this specific stance distribution, this specific consensus result, with a hash and a UAL embedded in the citation itself." That is the cell of the matrix academic infrastructure was always implying but hadn't been forced to occupy, because journal articles don't proliferate at the rate simulation outputs do.

A simulation that didn't exist ten minutes ago can now be referenced in a published paper, verified at byte level by any reader, and re-found in 2031 — with no registrar, no upload step, and no publisher. The stack publishing built turned out to be borrowable as long as someone supplied the missing bottom layer: the per-artifact endpoint that knows its own hash and its own anchor.

The next surface that ships will tell us which empty cell in the matrix the project moves to next. The fact that we can already name the empty cells is the part the citation arc just unlocked.

---
*Sources: [Citation File Format spec](https://citation-file-format.github.io/) · [GitHub Cite-this-repository announcement (Front Matter, 2021-08)](https://blog.front-matter.de/posts/step-forward-for-software-citation/) · [Zenodo FAQ — What is a DOI?](https://support.zenodo.org/help/en-gb/18-general/216-what-is-a-doi) · [Zenodo (Wikipedia)](https://en.wikipedia.org/wiki/Zenodo) · MiroShark PRs [#79 reproduce.json](https://github.com/aaronjmars/MiroShark/pull/79), [#84 DKG citation](https://github.com/aaronjmars/MiroShark/pull/84), [#96 cite.bib](https://github.com/aaronjmars/MiroShark/pull/96).*
