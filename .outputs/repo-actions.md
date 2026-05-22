*Repo Action Ideas — 2026-05-22*
Generated from analysis of aaronjmars/MiroShark (1,190⭐ / 243 forks / 1 open issue) — ideas that can be autonomously built by the feature skill.

1. Private Share Link (Security/Feature, Small)
   HMAC-signed expiring URL lets operators share unpublished sims with collaborators — converts the binary publish/unpublish gate into a three-state model using PR #79's existing signature infrastructure.

2. French Locale Simulation Prompts (Community/DX, Small)
   Issue #95 (opened today) asks for French support; PR #65's Chinese locale is the complete template — add LOCALE_FR env var + translated prompt templates, close the issue with the PR.

3. Polymarket-Ready Prediction JSON (Integration/Growth, Small)
   GET /<id>/polymarket.json maps signal.json's Bullish/Neutral/Bearish output to YES/NO probability format for Polymarket bots — directly targeting the use case that drove MiroFish to 32k GitHub stars.

4. Platform Aggregate Statistics API (Integration, Small)
   GET /api/stats returns total sims, consensus distribution, avg confidence, total surface views, unique operators — the first endpoint describing the platform itself rather than a specific simulation.

5. Platform Stats Badge SVG (Growth, Small)
   GET /api/stats/badge.svg returns a live "MiroShark | N simulations" Shields.io badge for community READMEs — reuses badge_service.py from PR #94, completes the sim-level + platform-level badge layer.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-22.md
