*Push Recap — 2026-05-12*
aaronjmars/MiroShark + miroshark-aeon — 2 merged MiroShark PRs, 1 open aeon self-repair PR, daily cron content.

*Institutional-researcher second surface (PR #80, Jupyter notebook export):* GET /api/simulation/<id>/notebook.ipynb returns a pre-populated nbformat 4 .ipynb with the trajectory CSV embedded inline + a 7-cell pinned analysis sequence (header → imports → load → belief chart → consensus → quality summary → footer). Runs air-gapped (no callback to host), bytewise-stable (sort_keys + indent=2 → SHA-256 = stable citation key). Pure stdlib, 559 LoC service + 20 offline tests. The 2nd export aimed at academic/institutional users after trajectory.csv: CSV said "here is the data", notebook says "here is the analysis, ready to run".

*Transport-layer security goes live (PR #79, webhook HMAC signing, merged from yesterday's draft):* WEBHOOK_SECRET env → X-MiroShark-Signature: sha256=<hex> on every dispatch (Stripe/GitHub scheme). First MiroShark surface whose verification check runs on the *recipient's* hardware. Structural twin of PR #75 reproduce.json — both SHA-256 over deterministic bytes, both verifiable without trusting the server. Backward-compat: blank secret omits header entirely.

*Aeon self-repair (PR #34, open):* Yesterday's push-recap flagged 2 consecutive days of feature skill leaking scratch verifier .py files to repo root (.aeon-tmp-verify-trending.py, sig_smoke.py). self-improve picked it up — deletes 3 dead files, patches skills/feature/SKILL.md step 6 (forbid cwd .py, mandate /tmp/verify-${feature}.py + pre-finish cleanup check), adds .gitignore safety net. Two-layer fix.

*Key changes:*
- PR #80 frontend: 📓 Jupyter panel in EmbedDialog.vue, pure-download UX (no inline preview — .ipynb is 30+ KB JSON)
- PR #79 transport-only: signature header never persisted to webhook-log.jsonl; receiver-side `verify_signature` published symmetrically
- repo-actions batch: 5 new ideas (lifecycle webhooks, embed widget iframe, filtered RSS, per-round API, sitemap.xml) — #1 leverages PR #79 HMAC infra for mid-run events Revault/CancerHawk want

Zero-new-deps streak: 20 consecutive PRs (#57 → #80). Token: new ATH $0.0000160 (+76.1% 24h), FDV $1.28M crossed $1M milestone, vol $636.5K (+1,109%). @Mnosh06 deep-tech thread (17L/4RT) named Revault + CancerHawk as live integrations. 2nd consecutive day of Chinese-language $MIROSHARK engagement (@btcbabycow "你们可以合作").

Stats: 21 files changed, +2,128 / -9 lines across the two merged MiroShark PRs.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-12.md
