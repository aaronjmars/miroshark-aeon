*Feature Built — 2026-06-13 — aaronjmars/MiroShark* 🦈

SECURITY.md — responsible-disclosure policy
MiroShark now has a front door for security reports. Instead of a stranger posting a vuln on a public issue for everyone to see, there's a private channel — GitHub's "Report a vulnerability" — plus a clear table of what's supported, how fast we respond, and how disclosure gets coordinated. Also bolted on an operator hardening checklist: don't expose Neo4j ports, set a real password, keep your LLM keys secret.

Why this matters:
1,200+ stars, named production integrators (RevaultDrops, AntFleet, Capacitr), an AGPL engine running a Neo4j graph full of whatever docs you fed it — and zero private way to report a hole. This already bit us: the hardcoded Neo4j password (#88) got reported on a *public* issue because no private path existed. That's the exact pattern this file kills. It also lights up the GitHub Security tab.

What was built:
- SECURITY.md (new): private reporting via GitHub advisories, supported-versions table, 3-day ack / 7-day assessment SLA, coordinated-disclosure terms, operator hardening checklist, scope section. Cites #88 as the reason it exists.
- README.md: one row in the docs table linking to SECURITY.md.

How it works:
Pure markdown — no code touched, so nothing in the engine moves and CI (pytest only) is unaffected. The reporting path leans on GitHub's native private vulnerability reporting, which is what actually populates the Security tab and lets us credit reporters in a published advisory. Picked it over an email address so there's no inbox to maintain or leak.

What's next:
Repo-actions also flagged a CONTRIBUTING.md expansion and issue templates — both still open. The CI security-scan idea (pip-audit/bandit) is parked: the token can't push to .github/workflows. Trust infra first; lower the bar to a stranger's first run next.

PR: https://github.com/aaronjmars/MiroShark/pull/158
