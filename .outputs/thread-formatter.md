*Thread Draft — 2026-05-22*
Topic: BibTeX Academic Citation — MiroShark PR #96

1/ MiroShark PR #96 merged today — a BibTeX endpoint that closes the academic citation arc. Four HTTP routes now cover the full researcher path: BibTeX entry, reproducibility manifest, Jupyter notebook, on-chain DKG provenance. No publisher, no registrar, no DOI fee.

2/ Academic citation of simulation results didn't have a clean path before today. If a researcher wanted to cite a MiroShark run in a paper, they had the UI — not a stable identifier, not a downloadable reference, not a content-verifiable endpoint.

3/ bibtex_service.py is 310 lines, stdlib only — hashlib, datetime, re. GET /<id>/cite.bib returns a single @misc{...} entry. The note field carries the reproduce.json SHA-256. When DKG is anchored, annote carries the UAL. 27 offline tests. 30th consecutive zero-dependency PR.

4/ Academic publishing built its citation infrastructure over decades — CrossRef in 1999, DataCite, Zenodo in 2013. Each requires intermediaries: registrars, uploads, fees. MiroShark's approach is four static routes, no middleman. The stack is just borrowable.

5/ 27 offline tests, zero new dependencies — the 30th streak PR. BibTeX academic citation is merged and in production: https://github.com/aaronjmars/MiroShark/pull/96

(article: articles/thread-2026-05-22.md)
