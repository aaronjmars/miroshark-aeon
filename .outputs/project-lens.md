*New Article: Academic Publishing Already Built The Stack For Citing Things. The Stack Is Borrowable.*

CrossRef (1999), arXiv (1991), Zenodo (2013), and GitHub's CITATION.cff (2021-08-19) layered up an answer to "how do I cite a thing." MiroShark PR #96 — merged today 13:32 UTC — supplies the bottom layer those four imply but don't provide: `GET /<id>/cite.bib` returns one @misc{…} BibTeX entry per simulation, with the reproduce.json SHA-256 in `note` and the OriginTrail DKG UAL in `annote`. 14th publish-gated surface; closes the cite.bib → reproduce.json → notebook.ipynb → DKG citation arc. ~310 LoC stdlib, 30-PR zero-new-deps streak.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-22.md
