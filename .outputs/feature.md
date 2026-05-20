*Feature Built — 2026-05-20*

Simulation Archive Bundle
MiroShark just gained a one-click "take this sim home" feature. A single `GET /api/simulation/<id>/archive.zip` call now bundles up to nine of the project's publish-gated surfaces — share card, chart SVG, trajectory CSV + JSONL, transcript, tweet thread, reproduce.json, Jupyter notebook, and signal.json — into one timestamped ZIP, plus a `manifest.json` that pairs every contained file with its SHA-256, byte size, MIME type, and canonical URL. Researchers no longer need to chain nine `curl` calls to archive a finished run.

Why this matters:
For the last fourteen days every shipped feature has been a *new surface*. Eleven separate publish-gated routes existed by the time PR #91 (signal.json) merged yesterday. The implicit cost of that growth fell on anyone trying to take a sim *out* of MiroShark — researchers writing papers, quant teams running comparison studies, integrators citing results with OriginTrail DKG hashes (PR #84). The May-18 repo-actions batch flagged this as the second-priority idea, right after the trading signal. With #91 merged, the archive becomes the composite the citation arc needed.

What was built:
- `backend/app/services/archive_service.py`: ~430 LoC pure-stdlib compositor. Iterates a locked canonical surface list, calls each existing per-surface renderer (`share_card.render_share_card`, `chart_svg.render_chart_svg_bytes`, etc.), wraps every call in try/except so a missing artifact omits the file rather than failing the request, then builds a `ZIP_DEFLATED` archive with a fixed per-entry `date_time` so the file portion is reproducible across two builds.
- `backend/app/api/simulation.py`: new `archive.zip` route — publish-gated, 404 when zero surfaces could be assembled, `Content-Disposition: attachment` with a date-stamped filename, and an `X-MiroShark-Archive-Files` response header so a HEAD request can preview the file count without downloading the body.
- `backend/openapi.yaml`: new `ArchiveManifest` + `ArchiveManifestEntry` schemas; `archive_zip` counter added to the surface-stats schema; full Publish & Embed operation entry.
- `frontend/src/components/EmbedDialog.vue`: 📦 Archive bundle section beneath the trading-signal row with a live file-count badge, a summary grid, a Download archive.zip anchor, and a `curl -OJ` copy-snippet.
- `backend/tests/test_unit_archive_service.py`: 20 offline tests — manifest schema lock, deterministic byte rendering, valid-ZIP parseability, per-file SHA-256 + size integrity, canonical order, MIME-type coverage, route presence, surface-stats registration, fixed timestamps.

How it works:
Every bundled file inside `archive.zip` is byte-for-byte identical to what the standalone surface route serves — the archive service reuses the same renderers rather than re-deriving anything. That means SHA-256 hashes in the manifest match what `curl …/share-card.png | sha256sum` would produce against the standalone URL, so OriginTrail DKG citation chains can verify integrity against either distribution path. Each `ZipInfo` entry carries the same fixed `date_time` (`1980-01-01T00:00:00`) so the contained-file portion of the archive is bytewise reproducible; only `archive_generated_at` in the manifest drifts across two builds. Pure stdlib — `zipfile`, `hashlib`, `io`, `json`, `datetime` — preserving the 27-PR zero-new-deps streak (now 28).

What's next:
Three May-18 ideas remain unbuilt (per-agent stance sparklines, scenario clone button on the share page, Chinese + Japanese README translations). The archive itself opens follow-ups too — a `?include=...` filter to skip individual surfaces, an `?inline_summary=1` toggle for a JSON-only "what's in the archive" response, and Frame v2 image / replay GIF entries once their byte interfaces stabilize.

PR: https://github.com/aaronjmars/MiroShark/pull/92
