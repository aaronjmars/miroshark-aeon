*Feature Built — 2026-05-12*

Jupyter Notebook Export
MiroShark simulations can now be downloaded as a pre-populated Jupyter notebook — `GET /api/simulation/<id>/notebook.ipynb` returns an analysis-ready `.ipynb` file with the trajectory data embedded directly inside and the standard charts (belief evolution, final consensus, quality summary) already scaffolded. An institutional researcher who lands on a published sim downloads one file, opens it in JupyterLab / VS Code / Google Colab, hits Run All, and has a working analysis — no `pd.read_csv()` + `import matplotlib` + axis-config boilerplate to write.

Why this matters:
Lorimer Ventures following Aaron this week was the first VC-tier signal in the project's history, and @TheGodfath13541's deep-dive thread names Revault + CancerHawk + x402 as active integrations — institutional eyeballs are landing. The trajectory CSV (PR #66) gave that audience the data, but opening a CSV in Jupyter still requires writing the same boilerplate every time. This notebook closes the gap between "here is the data" and "here is the analysis, ready to run", and it is the artifact academic collaboration happens in: a paper appendix or archive submission a co-author can run without setup. Picked from the 2026-05-10 repo-actions batch idea #2.

What was built:
- backend/app/services/notebook_export.py (new, ~560 LoC, pure stdlib): SCHEMA_VERSION = "1", CELL_ORDER constant pinning the 7-cell layout, build_notebook + render_notebook_bytes. The trajectory CSV is embedded via repr() so pathological inputs (multiple consecutive quotes, backslashes, embedded newlines) round-trip safely.
- backend/app/api/simulation.py: new @simulation_bp.route('/<id>/notebook.ipynb') handler — publish-gated, 5-min cache, attachment Content-Disposition, application/x-ipynb+json mimetype. Reuses trajectory_export.build_rows + render_csv so the embedded bytes match what trajectory.csv serves, and repro_export.build_repro_config for header metadata.
- backend/app/services/surface_stats.py + openapi.yaml + EmbedDialog: surface key notebook_ipynb added to SURFACE_KEYS + SimulationSurfaceStats schema + the Distribution panel labels — every notebook serve is counted alongside every other share surface.
- frontend/src/components/EmbedDialog.vue: 📓 Jupyter notebook panel beneath the reproducibility config — Download button, curl snippet, Copy URL button. Pure-download UX (no inline preview).
- backend/tests/test_unit_notebook_export.py (new, ~430 LoC, 20 tests): schema + cell-order pins, nbformat 4 shape, CSV embed round-trip via ast.literal_eval, pathological-quote/backslash round-trip, deterministic bytes, JSON round-trip, missing-blob degradation, counterfactual lineage in header, route + import + openapi + schema wiring guards.
- docs/FEATURES.md + docs/API.md + README.md: new Jupyter Notebook Export section, endpoint table row, analyst quickstart extended with a curl … jupyter lab example.

How it works:
The .ipynb format is plain JSON, so generation needs no Jupyter dependency on the server. The trajectory CSV is rendered by the same code path GET /trajectory.csv serves, then embedded into the load cell as `TRAJECTORY_CSV = <repr-of-csv>` and read back via pd.read_csv(io.StringIO(...)). The chart cells are strings — matplotlib is referenced inside the cells the user runs, never imported at generation time. The notebook is rendered with sort_keys + indent=2 + trailing newline, so two exports of the same finished sim are bytewise-identical: the SHA-256 of the file is a stable citation key (same property reproduce.json has). The trajectory SHA-256 is also exposed inside metadata.miroshark + the markdown footer so a reviewer can verify the embedded data wasn't tampered with after the download.

What's next:
A Colab-direct ?colab=1 variant with runtime hints, or a richer notebook that also pulls reproduce.json + transcript.json for cross-surface analysis — both build on the CELL_ORDER invariant this PR pins.

PR: https://github.com/aaronjmars/MiroShark/pull/80
