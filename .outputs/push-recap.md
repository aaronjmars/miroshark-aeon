*Push Recap — 2026-04-30*
MiroShark + miroshark-aeon — 3 substantive commits by 1 human author (aaronjmars), Claude Opus 4.7 1M-ctx co-author on all three.

*Discovery loop closes — RSS / Atom feeds (PR #60, MiroShark, +1,604/−1):* `/api/feed.atom` + `/api/feed.rss` syndicate the public gallery as a fourth orthogonal share/discovery surface alongside share card (Apr 22) + replay GIF (Apr 28) + transcript Markdown/JSON (Apr 29). Pure stdlib `xml.etree.ElementTree`; same `_build_gallery_card_payload` + ±0.2 stance threshold across five surfaces, one folder. Per-entry payload carries the share-card PNG + replay GIF as media enclosures and outcome+quality as `<category>`; `?verified=1` mirrors `/verified`. 17 offline tests, openapi drift test passes. Repo-actions Apr 28 idea #3.

*Wonderwall per-slot endpoint override + Cloud preset refresh (PR #59, MiroShark, +267/−266):* New `WONDERWALL_BASE_URL` + `WONDERWALL_API_KEY` so the simulation loop (the #1 cost driver, 850+ calls/run) can target any OpenAI-compatible endpoint — self-hosted vLLM, Modal, fine-tunes, remote Ollama — without touching Default/Smart/NER. `simulation_runner.py:start_simulation()` forwards Config values into subprocess env so Settings UI mutations apply on next run without a Flask restart. *Best preset deleted entirely* — the new Cloud preset (`xiaomi/mimo-v2-flash` + `x-ai/grok-4.1-fast`) hits the same ~$1/run budget that made the Claude tier redundant for most users.

*Aeon: Heartbeat day-of-week accuracy (PR #27, miroshark-aeon, +130/−9; +20 substantive):* Apr 29 heartbeat opened "Date: Tuesday Apr 29" when it was Wednesday — LLM hallucinated weekday from the YYYY-MM-DD `${today}` value and re-classified an on-schedule memory-flush run as "off-schedule". Fix: explicit Step 0 runs `date -u +%A/%u/%d`; report header anchored on shell output; cron-translation note added (cron `0=Sun` vs `+%u` `7=Sun` silently off-by-one); ground-truth guidance for every-other-day cron expressions points at `cron-state.json` `last_dispatch` history.

Key changes:
- `backend/app/services/feed.py` (NEW, +584) + `backend/app/api/feed.py` (NEW, +144) + `backend/tests/test_unit_feed.py` (NEW, +566) — the full RSS/Atom service + blueprint + 17-test guard
- `backend/app/api/settings.py` (+14/−27) drops the Best preset and adds Wonderwall base_url/api_key fields; `simulation_runner.py` (+10) forwards Config.WONDERWALL_* into subprocess env at spawn
- `skills/heartbeat/SKILL.md` (+20) — Step 0 shells out for the canonical weekday rather than letting the LLM guess

Stats: 35 files changed, +2,001/−276
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-04-30.md
