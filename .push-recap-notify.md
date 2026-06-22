*Push Recap — 2026-06-22*
miroshark-aeon — SHIPPING — docs-sync: agent auto-publishes merged PRs as website changelog

Under the hood:
• docs-sync skill (#71, +179 lines): reads merged PRs, composes changelog entry, opens draft PR on miroshark-website — daily 08:00 UTC. Bootstrap mode creates the changelog page + nav on first run.
• attribution fix (#73): --global git config in aeon.yml + chain-runner.yml so every cloned repo commits as @aeonframework, not an unlinked fallback email
• MiroShark: 4 dependabot CI/Actions bumps (setup-node 5→6, docker/metadata 5→6, setup-qemu 3→4, dompurify 3.4.11 security patch) — all bot-filtered

Shape: 0 user-visible · 36 internal · 1 infra · 4 bot-filtered · 7 merged PRs
Volume: 9 significant files, +204/−10 lines

Full recap: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/push-recap-2026-06-22.md
