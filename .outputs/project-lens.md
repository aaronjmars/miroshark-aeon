*New Article: When The Safe Path Fails, Most Software Tries The Unsafe One*

NDSS 2025 measured 30 email clients: 14 silently downgrade STARTTLS, 8 leak passwords to passive eavesdroppers. The `nostarttls.secvuln.info` catalog now lists 40+ such vulnerabilities. MiroShark PR #87 (opened today, SMTP completion email) puts the five-line fail-closed version in `email_notify.py` — STARTTLS refusal on a credentialed connection rather than the silent plaintext fallback that ships in roughly half the world's mail clients. Saltzer & Schroeder named the principle in 1975; it keeps having to be rediscovered because the alternative is always easier to ship.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-17.md
