*Push Recap — 2026-06-02*
MiroShark — 17 substantive commits to main by 2 authors. miroshark-aeon — 0 substantive (33 commits = cron churn).

Two new surfaces shipped paired: PR #132 Private Share-Link (merged 19:46Z Jun 1, +1,826 LoC, 18 tests) is the first tri-state sharing primitive — token-gated /preview/<token> with noindex + no-OG + no-store + identical-404 probe protection, grants the preview page only, all per-sim REST surfaces keep their is_public gate. PR #137 agents.json (merged 12:35Z Jun 2, +1,602 LoC, 24 tests) is the 26th publish-gated per-sim surface — roster export with name/handle/bio/persona/demographics/karma + final_stance, sorted most-bullish-first, ±0.2 stance threshold shared with sparklines.

README + docs visual-and-bilingual rebuild — 11 Aaron commits + PR #134 in a 78-minute evening session (18:48Z → 20:06Z Jun 1): logo + 5 diagrams refreshed, 6 product screenshots removed, README slimmed 314 → 242 lines (Highlights table + 40+-more link, full catalog moved to docs), Chinese FEATURES doubled (+590 lines, 21 missing sections + 9 missing catalog rows translated → parity 52 headings & 46-row catalog with English), first-ever Chinese DEMOGRAPHICS.zh-CN.md & NOTIFICATIONS.zh-CN.md added, PR #134 swapped diagrams PNG→JPG (~9.8 MB → 836 KB, ~92% smaller).

UI polish: PR #133 (merged 19:46Z, +107/-96) fixes global button{border-radius:9999px} leak on 3 list/tab classes + Step4Report's leftover light-theme palette black-on-dark — ~85 rgba(10,10,10,…) → rgba(244,241,255,…), dim violets brightened to #a78bfa/#c4b5fd.

Ecosystem grew to ≥16 named integrators: PR #138 HivemindOS (LiamVisionary), PR #139 Echo → Echo Oracle rename, PR #141 SyntheticsAI — all merged in 12 minutes (15:12–15:18Z Jun 2). PR #140 Capacitr still open at window close.

Key changes:
- agents.json answers *who was in the debate* in machine-readable form — AntFleet's benchmark pipeline no longer needs a transcript.md regex to extract roster composition
- Private share-link takes the per-sim sharing model from binary public/private to tri-state — first sharing primitive whose payload is strictly more restrictive than the public option
- Chinese deep-dive now at locale parity (52 headings each, 46-row catalog each) for the first time since the Chinese version forked

Stats: ~40 files changed, +4,550 / −259 lines across 17 commits. Catalog count 28 → 29. Zero-new-deps streak: 36th (#132) + 37th (#137). Aeon PR #50 (blocked-features registry) opened, not merged.

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-02.md
