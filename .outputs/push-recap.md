*Push Recap — 2026-05-22*
aaronjmars/MiroShark — 1 PR merged · aaronjmars/miroshark-aeon — 1 PR merged · 0 open PRs end-of-window

*The citation arc closes (MiroShark PR #96):* GET /<id>/cite.bib lands the 14th publish-gated surface — one-call @misc{…} BibTeX entry, text/plain at a static URL, drops into LaTeX \bibliography{} and imports via Zotero/Mendeley "Import from URL". Pure stdlib (hashlib+datetime+re), bytewise-deterministic. The `note` field carries the reproduce.json SHA-256 (DKG-anchor > fresh > omit), `annote` carries the OriginTrail UAL when anchored on-chain. Closes the four-step chain: BibTeX → notebook.ipynb → reproduce.json → DKG anchor. DOI-grade citation infrastructure delivered as four static endpoints.

*Self-correction cycle #4 (aeon PR #44):* RESERVED_X_PATHS filter on prefetch-bankr.sh — `@i` from `x.com/i/status/<id>` XAI annotation citations was consuming one Bankr Agent Max-Mode slot per prefetch run. Diagnosed in yesterday's recap, PR opened and merged 14 minutes apart, <22h symptom-to-ship. Four self-correction PRs in seven days, cycle is tightening (PR #40 ~24h → PR #42 ~36h → PR #43 ~30h → PR #44 <22h).

*Architecture decoupled from price:* $MIROSHARK -23.85% to $0.00002141 (-50.9% from ATH), volume halved to $318K. PR #44 + PR #96 + token-report + 11 skill cycles all shipped clean through the correction.

Key changes:
- bibtex_service.py (+338 new, 27 offline tests): citation-key sanitizer, BibTeX seven-special escapes with NUL-sentinel for backslash, max-age=300 matches reproduce.json/notebook cadence
- prefetch-bankr.sh (+14, -2): grep -viE chain for 27 reserved X.com path tokens; agent-timeout status now reflects only real-handle latency
- SURFACE_KEYS now 14 entries — pattern lock confirmed (PR #96 mirrors signal_service/badge_service/repro_export structurally)

Stats: 11 files changed, +1,227/-2 across 2 substantive PRs. 30-PR zero-new-deps streak (PR #96 = #30). Stars 1186→1190 (+4); forks 241→243 (+2).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-22.md
