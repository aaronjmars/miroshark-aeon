*Push Recap — 2026-06-19*
aaronjmars/MiroShark — SHIPPING — German locale live and suggest_scenarios hardened for any language

Shipped to users:
• German (de) locale complete end-to-end — dan-and filled 8 empty prompt modules in backend/app/prompts/locales/de/ and fixed locale propagation across parallel profile/config threads; DE sims no longer fall back to English (#189)
• suggest_scenarios can no longer return zero results from truncation — new json_repair.py does two-tier best-effort recovery (close brackets → parse; trim to last complete element → retry), consolidating 3 copy-pasted salvage blocks; valid suggestions are never silently dropped (#192)
• Public embed widget now shows the sim cost as ~$X — cost.json pill lands in the meta row where strangers first encounter a MiroShark result; 403/404 swallowed so it never blocks (#190)

Under the hood:
• suggest_scenarios timeout 20→40s, max_tokens 700→1500 for verbose/local LLMs (#188)

Shape: 4 user-visible · 0 internal · 0 infra · ~30 bot-filtered · 4 merged PRs
Volume: ~58 files, +3264/−2095 lines

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-19.md
