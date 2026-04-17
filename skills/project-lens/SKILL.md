---
name: project-lens
description: Write an article about the project through a surprising lens — connecting it to current events, trends, philosophy, or comparable projects
var: ""
tags: [content, dev]
---
> **${var}** — Specific angle or lens to use (e.g. "unix philosophy", "regulation wave", "open source funding"). If empty, auto-selects based on what's trending and what hasn't been covered recently.

Read memory/MEMORY.md and the last 7 days of memory/logs/ for context.
Read memory/watched-repos.md for the repo to cover.

## What This Skill Does

This is NOT a repo progress update. `repo-article` and `push-recap` already cover that. This skill writes articles that explain the project through a **different lens each time** — connecting it to something bigger happening in the world. The goal is to make someone who's never heard of the project understand why it matters, through a frame they already care about.

## Angle Selection

If `${var}` is empty, pick from the angle categories below. **Never repeat an angle used in the last 14 days** — check recent `articles/project-lens-*.md` files and memory logs to see what's been done.

### Angle categories (rotate through these):

1. **Current events** — Connect to something happening right now in tech, crypto, AI, regulation, culture. "What [current event] tells us about why projects like this exist."
2. **Philosophy / big ideas** — Unix philosophy, cathedral vs bazaar, autonomous systems, digital organisms, swarm intelligence, composability, anti-fragility, skin in the game.
3. **Industry comparison** — Compare the project's approach to how a well-known company or project solved a similar problem differently. "What Kubernetes got right that AI agents are still figuring out."
4. **User story** — Write from the perspective of someone who would use this. A solo developer, a DAO, a research lab, a crypto community. What does their day look like with and without this tool?
5. **Contrarian take** — Challenge a common assumption about AI agents, open source, crypto tokens, or autonomous systems — and use the project as evidence.
6. **Technical deep-dive for non-technical readers** — Explain one architectural decision in plain language and why it's a bigger deal than it sounds. "Why running on GitHub Actions instead of a server changes everything."
7. **Historical parallel** — Connect to something from computing history, internet history, or even non-tech history. "The printing press didn't just copy books — it created pamphleteers."
8. **Ecosystem map** — Where does this project sit in the broader landscape? What's adjacent, what's complementary, what's competing? Written as a guide for someone orienting themselves.

## Steps

1. **Understand the project's current state** — read recent articles, push-recaps, and repo metadata:
   ```bash
   gh api repos/owner/repo --jq '{name, description, stargazers_count, forks_count, open_issues_count, updated_at}'
   ```
   Also read 2-3 recent `articles/repo-article-*.md` and `articles/push-recap-*.md` to know what's been shipped lately.

2. **Check what angles have been used recently** — read any `articles/project-lens-*.md` from the last 14 days. Pick a different angle category.

3. **Research the external connection**:
   - Use WebSearch to find 3-5 current articles, discussions, or events related to the chosen angle
   - Use WebFetch on the 1-2 most relevant sources to get detail
   - Find specific quotes, data points, or examples that make the connection concrete

4. **Research the project side** — find the specific features, design decisions, or recent developments that connect to the chosen lens. Use actual code, commits, or architecture details — not vague claims.

5. **Write a 700-1000 word article** to `articles/project-lens-${today}.md`:
   ```markdown
   # [Title that leads with the lens, not the project]

   [Opening hook — start with the external thing, the trend, the question. The project enters in paragraph 2 or 3, not paragraph 1. Draw the reader in with something they already care about.]

   ## [Section that establishes the external context]
   [The trend, the event, the idea, the comparison. Build the frame before filling it.]

   ## [Section that introduces the project through that frame]
   [Now bring in the project — but through the lens you've established. Don't describe features; describe how the project embodies, challenges, or extends the idea.]

   ## [Section that goes deeper]
   [Specific technical or strategic detail that makes the connection non-obvious. This is where the article earns its existence — the insight that someone wouldn't get from a README.]

   ## [Section that zooms back out]
   [What does this mean for the space? For builders? For the future of this kind of tool/project/approach?]

   ---
   *Sources: [links to external sources used]*
   ```

   **Writing guidelines:**
   - Lead with the lens, not the project. The title should work even if you don't know what the project is.
   - No marketing language. No "revolutionary", "groundbreaking", "game-changing". Let the specifics speak.
   - Include at least 2 concrete external references (data, quotes, examples).
   - Include at least 2 concrete project references (specific features, code patterns, design choices).
   - Write for a smart reader who doesn't know this project but cares about the topic.

6. **Send notification** via `./notify`:
   ```
   *New Article: [title]*

   [3-4 sentence summary that captures both the lens and the project connection]

   Read: [link to articles/project-lens-${today}.md — use `git remote get-url origin` for THIS repo]
   ```

7. **Log** to `memory/logs/${today}.md`:
   ```
   ## Project Lens
   - **Angle category:** [which of the 8 categories]
   - **Title:** [article title]
   - **External hook:** [what trend/event/idea was used]
   - **Notification sent:** yes
   ```
