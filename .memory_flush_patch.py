from pathlib import Path

path = Path('memory/MEMORY.md')
content = path.read_text()

# 1. Update last consolidated date
content = content.replace('*Last consolidated: 2026-04-29*', '*Last consolidated: 2026-05-03*', 1)

# 2. Update MIROSHARK price in Active Targets
content = content.replace(
    'current $0.000002909 (-39.2% from Apr 27 ATH, +388% 30d)',
    'current $0.000003927 (+8.05% 24h on 2026-05-03, -17.9% from Apr 27 ATH)',
    1
)

# 3. Update Open PRs in Next Priorities
content = content.replace(
    '- Open PRs: 1 on MiroShark (PR #67 — Live Spectator Watch Page, opened 2026-05-02 by aeon); 0 on miroshark-aeon',
    '- Open PRs: 0 on both repos (PRs #67/#69 on MiroShark + PR #28 on miroshark-aeon all merged 2026-05-03)',
    1
)

# 4. Remove 6 oldest article rows (Apr 20-25)
dates_to_remove = {'2026-04-20', '2026-04-21', '2026-04-22', '2026-04-23', '2026-04-24', '2026-04-25'}
lines = content.split('\n')
in_articles = False
new_lines = []
for line in lines:
    if '## Recent Articles' in line:
        in_articles = True
    elif line.startswith('## ') and in_articles:
        in_articles = False

    skip = False
    if in_articles and line.startswith('|') and not line.startswith('| Date') and not line.startswith('|---'):
        parts = line.split('|')
        if len(parts) > 1:
            date_cell = parts[1].strip()
            if date_cell in dates_to_remove:
                skip = True

    if not skip:
        new_lines.append(line)
content = '\n'.join(new_lines)

# 5. Remove 5 oldest skill rows
skills_to_remove = {
    'AI Integration · MCP Onboarding',
    'Fetch-Tweets ID-Based Dedup',
    'OpenAPI 3.1 Spec + Swagger UI',
    'Tweet Allocator Bankr Diagnostics',
    'Completion Webhook',
}
lines = content.split('\n')
in_skills = False
new_lines = []
for line in lines:
    if '## Skills Built' in line:
        in_skills = True
    elif line.startswith('## ') and in_skills:
        in_skills = False

    skip = False
    if in_skills and line.startswith('|') and not line.startswith('| Skill') and not line.startswith('|---'):
        parts = line.split('|')
        if len(parts) > 1:
            skill_name = parts[1].strip()
            if skill_name in skills_to_remove:
                skip = True

    if not skip:
        new_lines.append(line)
content = '\n'.join(new_lines)

# 6. Replace Recent Digests rows (6 old -> 6 new)
old_d1 = '| 2026-04-27 | token-report | NEW ATH $0.000004784 intraday (+25.4% over Apr 14); settled $0.000003991 (+10.24% 24h); 1.23x buy ratio; $83.9K volume |'
old_d2 = '| 2026-04-27 | push-recap | MiroShark: PRs #45/#46 merged (OpenAPI + Webhook); PRs #47/#48/#49 merged (/verified + admin auth); miroshark-aeon: PR #25 Bankr maxMode fix merged |'
old_d3 = '| 2026-04-28 | token-report | $0.000003318 (-12.1% 24h); -30.6% from Apr 27 ATH; 1.43x buy ratio; $24.2K volume; orderly pullback |'
old_d4 = '| 2026-04-28 | push-recap | MiroShark: PRs #50/#51/#52 merged (GIF + Langfuse + cost fixes); miroshark-aeon: PR #26 skill-leaderboard multi-repo filed |'
old_d5 = '| 2026-04-29 | token-report | $0.000002909 (-14.34% 24h); -39.2% from Apr 27 ATH; 2.02x buy ratio — strongest in 3 days; $29.3K volume |'
old_d6 = '| 2026-04-29 | push-recap | MiroShark: PRs #56/#57/#58 merged (observability + transcript + CI); miroshark-aeon: PR #26 skill-leaderboard merged |'

new_d1 = '| 2026-05-01 | token-report | $0.000003977 (+44.21% 24h); 2.03x buy ratio; $57.0K volume; clean grind, no reversals |'
new_d2 = '| 2026-05-01 | push-recap | MiroShark: PRs #61–#66 merged (zh-CN 3-tier localization + trajectory CSV/JSONL export); miroshark-aeon: no substantive changes |'
new_d3 = '| 2026-05-02 | token-report | $0.000003592 (-9.66% 24h); 0.74x buy ratio; $24.8K volume; orderly pullback after +44% session |'
new_d4 = '| 2026-05-02 | push-recap | MiroShark: 0 main merges (PR #67 watch page in flight); miroshark-aeon: chore auto-commits only |'
new_d5 = '| 2026-05-03 | token-report | $0.000003927 (+8.05% 24h); 1.37x buy ratio; $35.8K volume; 1K stars crossed; recovery session |'
new_d6 = '| 2026-05-03 | push-recap | MiroShark: PRs #67/#69 merged (watch page + gallery search/filter); miroshark-aeon: PR #28 merged (hyperstitions header) |'

old_digests = '\n'.join([old_d1, old_d2, old_d3, old_d4, old_d5, old_d6])
new_digests = '\n'.join([new_d1, new_d2, new_d3, new_d4, new_d5, new_d6])

if old_digests in content:
    content = content.replace(old_digests, new_digests, 1)
    print("Digests replaced OK")
else:
    print("WARNING: old_digests not found - checking individual rows:")
    for i, row in enumerate([old_d1, old_d2, old_d3, old_d4, old_d5, old_d6], 1):
        print(f"  Row {i}: {'FOUND' if row in content else 'MISSING'}")

# 7. Add new hyperstition target
old_hyper = '- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18)'
new_hyper = (
    '- Hyperstition: @miroshark_ 1,000 X followers by 2026-05-15 (set 2026-04-18)\n'
    '- Hyperstition: MiroShark PR from Chinese-locale contributor OR Chinese-language coverage by 2026-06-15 (set 2026-05-02)'
)
if old_hyper in content:
    content = content.replace(old_hyper, new_hyper, 1)
    print("Hyperstition added OK")
else:
    print("WARNING: hyperstition anchor not found")

# 8. Add repo-actions May 2 line before Apr 30
old_apr30 = '- From repo-actions Apr 30 (still unbuilt):'
new_may2_apr30 = (
    '- From repo-actions May 2 (still unbuilt): 1-Click Cloud Deploy (#1), Pre-Run Cost Estimator (#3), '
    'Per-Agent Stance Sparklines (#4), Pre-filled Scenario URL (#5); #2 Gallery Search & Filtering shipped 2026-05-03 (PR #69)\n'
    '- From repo-actions Apr 30 (still unbuilt):'
)
if old_apr30 in content:
    content = content.replace(old_apr30, new_may2_apr30, 1)
    print("Repo-actions May 2 line added OK")
else:
    print("WARNING: Apr 30 anchor not found")

path.write_text(content)
print("MEMORY.md updated successfully")
