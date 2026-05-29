*Push Recap — 2026-05-29*
aaronjmars/MiroShark — 3 PRs merged in a 2-min window (14:36–14:38 UTC), 2 authors. miroshark-aeon: scheduler chore only.

*Analytics:* PR #124 `/volatility` — 25th surface, Aeon-built today. Distribution of round-over-round belief swings (mean / std dev / max / 0–100 index / stable-converging-contested trend). Reuses peak_round.load_trajectory_rounds so max_delta_round matches peak-round's most_volatile_round by construction; the new info is the *distribution*, not the max. Closes the analytical triangle with signal.json (where) and peak-round (when) — a quant tool can finally tell high-volatility Bullish from low-volatility Bullish.

*Frontend:* PR #122 — light Hyperstitions → dark deep-space-violet. Token remap in App.vue (orange→violet, green→soft violet, white→deep panel, black→light text, background→#05030a) cascaded through 27 components. Eight stacked commits as the cascade exposed dark-on-dark + invisible-CTA bugs; final commit flipped #0A0A0A literal → #f4f1ff across 13 files. Step3 sim view + Settings + TemplateGallery + HistoryDatabase + every visualization canvas reskinned. Logic untouched on Home (refs/computed/handlers 1:1).

*Docs:* PR #123 — locale negotiation protocol (`?lang=` → X-MiroShark-Locale → Accept-Language → en) was already in code but undiscoverable. Now documented in API.md + API.zh-CN.md with curl examples. Answers issue #95 (French locale).

Key changes:
- backend/app/services/volatility_service.py (new, +206 LoC stdlib) — math + json + os, reuses peak-round's stance split (±0.2) for byte-consistent cross-surface numbers
- frontend/src/App.vue (+28/-18) — :root token remap cascades the whole palette flip via legacy names
- frontend/src/views/Home.vue (+996/-1237) — full rewrite to deep-space radial bg + glossy violet console + Geist font system

Stats: 48 files, +4782 / -3452 lines, zero new deps (33rd straight PR since Nemotron). PR #124 first push failed CI (`SURFACE_KEYS` test had hard-coded set without 'volatility' — fixed in same PR).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-29.md
