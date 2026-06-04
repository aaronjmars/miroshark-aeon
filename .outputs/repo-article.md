*New Article: The Workspace Layer MiroShark Was Missing*

PR #147 (merged today 15:16 UTC) shipped `GET /api/project/<id>/stats` — the per-project sibling of `/api/stats`. Until today MiroShark's API had only two granularities: 26 per-sim surfaces or one whole-platform aggregate. Per-project stats is what the module's own docstring calls 'the missing middle' — workspace-scoped consensus, average confidence, and a new `quality_distribution` (excellent/good/fair/poor). 39th consecutive zero-deps PR. The stats.py blueprint now serves three surfaces, not two.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-article-2026-06-04.md
