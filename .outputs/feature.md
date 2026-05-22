## Summary

Built **BibTeX Academic Citation Export** for the watched MiroShark repo. Picked #2 from the 2026-05-20 repo-actions batch — closes the academic-citation arc that started with reproduce.json (PR #79), notebook.ipynb (PR #80), and the OriginTrail DKG citation (PR #84).

**PR:** https://github.com/aaronjmars/MiroShark/pull/96 — branch `feat/cite-bib-academic-citation`. 10 files changed, 1213 insertions.

**What shipped:**
- `backend/app/services/bibtex_service.py` — pure stdlib (~310 LoC) BibTeX builder with citation-key sanitizer, BibTeX-special escaper, ISO-8601 → year/month derivation, and SHA-256 sourcing precedence (DKG anchor > fresh hash > omit).
- `backend/app/api/simulation.py` — `GET /<id>/cite.bib` route serving `text/plain` with the `.bib` Content-Disposition that Zotero / Mendeley "Import from URL" consumes directly.
- `backend/tests/test_unit_bibtex_service.py` — 27 offline unit tests covering escaping, key shape, SHA precedence, URL composition, bytewise determinism, defensive fallbacks.
- `frontend/src/components/EmbedDialog.vue` — new 📖 BibTeX section between the notebook + DKG panels: copyable URL, curl snippet, `\cite{miroshark-...}` LaTeX reference snippet, Download .bib anchor.
- `backend/openapi.yaml`, `docs/API.md`, `docs/FEATURES.md` — full spec + docs.
- `cite_bib` counter wired into `SURFACE_KEYS` (with the test expected-set updated in lockstep).

Zero new dependencies — 30-PR zero-deps streak. Notification queued in `.pending-notify/1779449617.md` for post-run delivery. Memory log + MEMORY.md skills table + Next Priorities updated. May-20 batch now 2/5 addressed.
