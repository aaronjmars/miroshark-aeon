*Push Recap — 2026-05-25*
MiroShark — 3 commits · miroshark-aeon — 1 substantive (+47 scheduler auto-commits) · all by aaronjmars + 1 external

Platform self-description surfaces: MiroShark merged its oEmbed provider (#107) and Platform Stats API + badge (#105) back-to-back — the first endpoints that describe the *platform itself*, not one simulation. /api/stats returns aggregate consensus/confidence/view counts (+ a Shields.io badge for READMEs); /oembed makes share links auto-unfurl into rich cards on Notion/Ghost/Substack/WordPress. Both pure stdlib, zero new deps.

Repo hygiene: #104 (ext contributor Void Freud) collapsed five explicit .env lines into one .env.* wildcard + !.env.example — fourth distinct external contributor on the repo.

Agent self-hardening: aeon #45 adds an EXIT trap to prefetch-bankr.sh that stamps a 'crashed' status with the exit code, so tweet-allocator can tell a crashed prefetch from one that never ran (fixes the misleading May-24 alert).

Key changes:
- New platform_stats.py (+444): one O(n) scan over all public+completed sims, 60s cache, ETag/304
- New oembed_service.py (+207): host-allow-listed URL→sim_id parsing, never dereferences inbound url, JSON/XML payload
- prefetch-bankr.sh EXIT trap (+25): writes {status:crashed, exit_code} when the script bails before its normal write_status

Stats: 22 files, +2,418 / -10 across 4 substantive commits. 3 of 4 recently-open MiroShark PRs merged today (#106 Railway still open).
Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-05-25.md
