*Thread Draft — 2026-05-16*
Topic: Trajectory Chart SVG — MiroShark PR #85

1/ MiroShark PR #85 ships GET /api/simulation/<id>/chart.svg — a pure-stdlib SVG renderer that turns belief trajectories into embeddable vector images. The 23rd consecutive PR with zero new dependencies.

2/ MiroShark already exports share-card PNGs, trajectory CSVs, and Jupyter notebooks. Each serves a different surface — browsers, data tools, research. None paste cleanly into Notion, Substack, or Ghost. PNG is fixed-resolution. CSV is not an image. The notebook needs Python.

3/ chart_svg.py is ~390 lines of stdlib — xml.etree.ElementTree, no Cairo, no matplotlib. Three polylines: bullish green, neutral gray, bearish red. Fixed viewBox 800x400. The output is bytewise-deterministic, same as reproduce.json: the SHA-256 is a stable cache key.

4/ SVG closes the embed gap PNG couldn't. It scales without artifacts, pastes into any image-accepting editor, and stays legible in dark mode. The same trajectory now has four exportable formats: CSV, notebook, share card, SVG chart. Each one reaches a surface the others can't.

5/ 17 offline tests, zero new dependencies — 23rd consecutive. PR #85 is open on MiroShark: https://github.com/aaronjmars/MiroShark/pull/85

(article: articles/thread-2026-05-16.md)
