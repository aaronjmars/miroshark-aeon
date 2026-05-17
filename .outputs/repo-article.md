*New Article: MiroShark's Last Notification Channel Is Just a Protocol*

PR #87 (SMTP completion-email notifications, opened today 11:35 UTC) is the first MiroShark notification channel whose far end can be a protocol relay (`localhost:25`) instead of a vendor URL — closing the four-channel quadrant (webhook/Discord/Slack/email). Notable design moves: transport-selection table keyed on port (no parallel TLS_MODE env var), auth-optional posture for unauthenticated LAN relays, and credential-leak refusal on STARTTLS failure. Channel-notifier idiom now at 5 instances; 25-PR zero-dep streak preserved.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-article-2026-05-17.md
