---
name: Idea Capture
description: Quick note capture triggered via Telegram — stores to memory
var: ""
tags: [creative]
---
> **${var}** — The idea or note to capture.

If `${var}` is set, use it as the idea to capture.


This skill is triggered on demand via Telegram. The user sends a quick idea, thought, or note.

Steps:
1. Read memory/MEMORY.md for context.
2. Parse the incoming message for the idea/note content.
3. Categorize the idea:
   - **Article idea** — topic worth writing about
   - **Feature idea** — something to build
   - **Research lead** — paper, person, or concept to explore
   - **Reminder** — something to follow up on
   - **General note** — anything else
4. Append to memory/logs/${today}.md:
   ```markdown
   ### Idea Captured
   - **Category**: type
   - **Note**: the idea
   - **Source**: Telegram
   ```
5. If it's actionable (feature idea or reminder), also add to MEMORY.md under "Next Priorities."
6. Confirm via `./notify`: "Captured: [brief summary]"
