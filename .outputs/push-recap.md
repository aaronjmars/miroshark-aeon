*Push Recap — 2026-05-16*
MiroShark — 3 merges + 1 PR open / aeon — 1 PR open (all aaronjmars-authored)

Theme 1 — Citation gap closes on-chain: PR #84 (OriginTrail DKG citation, merged, +1988/-2) anchors finished sims as DKG Knowledge Assets. Reproduce.json's SHA-256 becomes a blockchain-anchored citation key — same provenance property a DOI gives a paper. Caps the 11-surface arc PRs #57–#84.

Theme 2 — First operational hotfix loop: PR #86 (merged, +44/-44) swaps xAI's deprecated grok-4.1-fast (now returning 404 on OpenRouter) → google/gemini-3-flash-preview across 3 cloud-preset slots + EN/ZH docs. Same-day open + merge.

Theme 3 — Vector embed surface: PR #85 (open) adds GET /api/simulation/<id>/chart.svg via pure-stdlib xml.etree. Byte-stable, embeddable in Notion/Substack/Ghost/LaTeX. Closes May-14 batch idea #3 once merged.

Theme 4 — Channel-notifier idiom at 4 instances: webhook_service + discord_notify + slack_notify + dkg_publisher all share fire-and-forget + (sim_id, status) dedup + late-bound env-var reads. First on-chain channel.

Theme 5 — Aeon self-correction: PR #40 (open, +3/-0) hardens project-lens to verify PR state via 'gh pr view' before notify. 24h round-trip from yesterday's 'merged'/'opened' drift bug to in-CI prompt fix.

Key changes:
- New backend/app/services/dkg_publisher.py (+709 LoC stdlib) — walks WM → SWM → VM publish pipeline, persists dkg-citation.json atomically for idempotence
- EmbedDialog grows DKG citation card (testnet/mainnet chip + UAL + Merkle + tx hash + explorer link) + 📈 Trajectory Chart SVG section
- backend/app/api/settings.py 'cheap' preset label flips 'Mimo V2 Flash + Grok-4.1 Fast' → 'Mimo V2 Flash + Gemini 3 Flash'

Stats: ~53 files / +4,301 / -47 lines merged (PR #83 + #84 + #86) + 1,099 / -4 staged in open PR #85. 23rd consecutive zero-new-deps MiroShark PR.
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-16.md
