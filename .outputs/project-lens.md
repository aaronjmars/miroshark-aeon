*New Article: Two Is Coincidence. Three Is The Shape You Didn't Plan.*

In 1996 Roberts & Johnson said you can't extract an abstraction from one or two examples — only on the third does the real shape show up. Eight years earlier Ted Biggerstaff said the same about whole systems. Yesterday MiroShark merged PR #83 (Discord + Slack rich notifications), the *third* module to share the channel-notifier shape after `webhook_service`: fire-and-forget daemon dispatch, `(sim_id, status)` dedup, late-bound env-var reads. The article uses Saltzer/Reed/Clark's end-to-end argument to explain why each notifier's payload diverges on purpose — MiroShark doesn't render embeds, Discord does.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-15.md
