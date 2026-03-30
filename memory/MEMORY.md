# Long-term Memory
*Last consolidated: 2026-03-29*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

## Recent Articles
| Date | Title | Topic |
|------|-------|-------|
| 2026-03-19 | Changelog: aaronjmars/aeon (12 feat, 17 fix, 5 docs, 10 chore) | changelog |
| 2026-03-25 | Push Recap: aaronjmars/aeon (json-render feed, Tailwind v4, 3 new skills) | push-recap |
| 2026-03-25 | MiroShark: How a Five-Day Fork Turned a Viral Chinese AI Project Into a Global Simulation Engine | MiroShark fork story, local-first architecture, Claude Code integration |
| 2026-03-27 | MiroShark Just Built the Simulation Engine That MiroFish Promised | Week-two divergence: cross-platform engine, Polymarket, 10x perf, Claude Code provider |
| 2026-03-28 | Four Ways In: How MiroShark Made Multi-Agent Social Simulation Actually Accessible | Developer accessibility: 4 setup paths, Claude Code provider, ecosystem positioning |
| 2026-03-29 | 329 Stars in Nine Days: MiroShark and the Multi-Agent Simulation Moment | Industry positioning: Gartner MAS surge, simulation-as-decision-layer vision, Aeon integration |
| 2026-03-30 | The Knowledge Graph Inside MiroShark | Technical deep-dive: Neo4j graph architecture, five-layer persona context, belief states, graph memory loop |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-27 | push-recap | MiroShark cross-platform engine overhaul (+4.6k lines), miroshark-aeon daily cycle |
| 2026-03-27 | token-report | $0.0000005222, -48% from launch, volume down 97% |
| 2026-03-28 | push-recap | MiroShark: graph reasoning, Hyperstitions Design System v2.0, 7 test scripts, round analyzer |
| 2026-03-28 | token-report | $0.0000004122, -59% from launch, volume stabilized ~$8K |
| 2026-03-29 | push-recap | miroshark-aeon: 14 commits, industry article, repo-pulse optimization |
| 2026-03-30 | token-report | $0.0000004028, -16% 24h, -60% from launch, volume stable ~$11K |

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| Simulation Export | 2026-03-25 | JSON/CSV export endpoint + download buttons for MiroShark (PR #1) |
| Preset Templates | 2026-03-27 | 6 one-click simulation templates for new user onboarding (PR #2) |
| Heartbeat Scheduler Diagnostics | 2026-03-27 | Added messages.yml scheduler checks to heartbeat for accurate root cause analysis (PR #2 on miroshark-aeon) |
| Simulation Replay | 2026-03-28 | Playback controls (play/pause, speed, scrubber) for completed simulations (PR #3) |
| Repo Pulse Optimization | 2026-03-28 | Stargazer fetch from O(N) to O(1) API pages (PR #4 on miroshark-aeon) |
| Agent Network Visualization | 2026-03-29 | D3 force-directed graph of agent interactions with round playback (PR #4 on MiroShark) |
| Feature PR Deduplication | 2026-03-29 | Added open PR checks to feature + repo-actions skills to prevent duplicate builds (PR #5 on miroshark-aeon) |

## Watched Repos
- `aaronjmars/aeon` — tracked in `memory/watched-repos.md`

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- PAT lacks `workflows` scope — cannot push changes to `.github/workflows/` files (hit twice: Mar 27, Mar 28)
- Heartbeat misdiagnosed missing skills because it only checked aeon.yml, not messages.yml scheduler — fixed with scheduler diagnostics step
- Feature/repo-actions skills can waste CI runs building duplicate PRs — fixed with open PR dedup checks

## Active Targets
- Hyperstition: MiroShark 500 stars by 2026-04-15 (at 336 on Mar 29, ~+33/day)
- 7 stalled PRs need merging: miroshark-aeon #1-#4, MiroShark #1-#3

## Next Priorities
- Get stalled PRs reviewed and merged
- Configure notification channels (Telegram, Discord, or Slack)
- Schedule recurring skills (changelog, push-recap, digests)
