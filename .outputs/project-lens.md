*New Article: 1 in 277 — The Citation Layer Failed In Public, And What Survives Is The Artifact*

On May 7 *The Lancet* counted 4,406 fabricated references across 2.5M PubMed papers — 1 in 277 papers in 2026, up 12× in two years. Topaz's fix defends the citation. The deeper shift, visible in NIST's April 7 critical-infrastructure note and in MiroShark's PR #80 Jupyter notebook export, defends the artifact instead: system-emitted, bytes pinned with sort_keys+indent=2, SHA-256 in the footer as the citation key. The same discipline already in reproduce.json (PR #75) and HMAC body sigs (PR #79). The tools still trustworthy after the citation layer finishes failing will be the ones that emit, embed, sort, and hash.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-12.md
