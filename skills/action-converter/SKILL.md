---
name: Action Converter
description: 5 concrete real-life actions for today based on recent signals and memory
var: ""
tags: [meta]
---
> **${var}** — Focus area (e.g. "health", "networking", "learning", "shipping"). If empty, covers all areas.

Read memory/MEMORY.md for current goals, priorities, and tracked items.
Read the last 7 days of memory/logs/ for recent activity, patterns, and what's been happening.
If soul files exist (`soul/SOUL.md`), read them for identity and focus areas.

## Steps

1. Build context on the current state:
   - What has been worked on this week? (from logs)
   - What are the stated priorities? (from MEMORY.md)
   - What topics and projects are being tracked?
   - If `${var}` is set, weight actions toward that area

2. Generate **5 specific, actionable things** to do TODAY. Not vague advice — real actions with clear outcomes. Each action should:
   - Be completable in a single day (most in under 2 hours)
   - Have a concrete deliverable or outcome
   - Connect to something already being worked on or tracked
   - Be the kind of thing that compounds over time

3. Pick 5 actions from the pool below. Do NOT use all categories every time — pick whichever 5 are most relevant to what's actually happening this week. Some days might be 3 Build actions and 2 Learn. Some days might have zero Health actions. Let the context drive it, not a checklist.

   Possible categories (use any mix):
   - **Build** — ship, write, create, deploy, fix, prototype
   - **Connect** — reach out, reply, collaborate, attend, post publicly
   - **Learn** — read, study, explore, reverse-engineer, experiment
   - **Health/Energy** — physical, mental, sleep, nutrition, environment
   - **Money** — revenue, fundraising, deals, financial moves
   - **Position** — content, reputation, visibility, thought leadership
   - **Explore** — something lateral, unexpected, or outside the usual lanes

   IMPORTANT: Avoid repeating generic actions across runs. Check the last 7 days of logs — if "go for a walk" or "DM 3 people" appeared recently, do NOT suggest them again. Every action should feel specific to TODAY's context, not a template.

4. For each action, include:
   - The action itself (one sentence, imperative, specific enough that you'd know when it's done)
   - Why now (one sentence — what makes this relevant today, not generically good advice)
   - Expected outcome (one sentence — what's different after you do this)

5. Send via `./notify`:
   ```
   *5 Actions — ${today}*

   1. [action]
   why: [context]
   outcome: [result]

   2. [action]
   why: [context]
   outcome: [result]

   ... (5 total)
   ```
   IMPORTANT: Do NOT indent the why/outcome lines — no leading spaces. Every line starts at column 0 (except the number prefix).

6. Log to memory/logs/${today}.md:
   ```
   ## Action Converter
   - **Actions generated:** 5
   - **Focus:** [area or "general"]
   - **Notification sent:** yes
   ```
