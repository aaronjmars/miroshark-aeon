*Feature Built — 2026-06-15 — aaronjmars/MiroShark* 🦈

dependabot config — automated dependency updates across the whole repo

MiroShark had no automated dep tooling. Added `.github/dependabot.yml` so the repo now watches every dependency surface — backend Python, both npm packages, the GitHub Actions, the Docker base image — and opens a PR when something's behind. nothing rots silently anymore.

Why this matters:
`camel-ai==0.2.78` is exact-pinned in two files. exact pin = security patches never flow in, you find out when something breaks. but you can't just loosen it — the `tiktoken>=0.8.0` note in pyproject shows that stack is pinned on purpose for the py3.13 build. so the safe move isn't floating the pin, it's surfacing each update as its own reviewable, CI-tested PR. dependabot does exactly that. you stay in control of what lands.

What was built:
- `.github/dependabot.yml` (new): five update blocks — pip `/backend`, npm `/`, npm `/frontend`, github-actions `/`, docker `/`. weekly, monday.
- noise control baked in: minor + patch updates grouped into one PR per ecosystem; majors open on their own so breaking changes get real scrutiny.
- `chore:` commit prefix to match the repo's existing dep-bump convention; conservative PR limits per ecosystem.

How it works:
standard Dependabot v2 schema. GitHub reads the config on push and runs each ecosystem on its schedule against the declared manifests. the `groups` blocks collapse the minor/patch churn into a single weekly PR per ecosystem — so a normal week is a handful of PRs, not dozens. zero runtime change; CI (backend pytest) is untouched.

What's next:
first run will likely surface the camel-ai bump + a few npm/actions updates — each isolated and CI-gated for you to accept or skip. closes the dep-hygiene gap repo-actions flagged on 06-14.

PR: https://github.com/aaronjmars/MiroShark/pull/166
