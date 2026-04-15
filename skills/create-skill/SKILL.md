---
name: Create Skill
description: Generate a complete new skill from a one-line prompt
var: ""
tags: [dev, meta]
---
> **${var}** — A natural-language description of the skill to create. **Required.** Example: `"monitor Hacker News for AI papers and send a summary"` or `"track gas prices on Ethereum and alert when below 10 gwei"`.

Today is ${today}. Your task is to generate a complete, production-ready skill from the description in `${var}`.

## Steps

1. **Parse the request.** Extract from `${var}`:
   - The core action (monitor, fetch, generate, analyze, alert, etc.)
   - The data source(s) (APIs, websites, RSS, on-chain, GitHub, etc.)
   - The output format (notification, article, file, PR, etc.)
   - Any configurable parameters the skill should accept via its own `${var}`

2. **Check for duplicates.** List existing skills:
   ```bash
   ls skills/
   ```
   Read any skill that sounds similar to confirm the new skill is genuinely different. If a near-duplicate exists, note it and design the new skill to complement rather than overlap.

3. **Research the data sources.** For each API or data source the skill needs:
   - WebSearch for the current API documentation
   - Identify the correct endpoints, required auth, and response format
   - Note any environment variables needed (API keys, tokens, etc.)
   - Determine fallback strategies if an API key isn't set (e.g., use WebSearch/WebFetch instead)

4. **Design the skill.** Decide:
   - **Skill name** — lowercase, hyphenated, 2-3 words max (e.g., `gas-alert`, `hn-papers`)
   - **Description** — one sentence, starts with a verb
   - **Tags** — pick from: `content`, `crypto`, `dev`, `meta`, `news`, `research`, `social`
   - **Variable behavior** — what `${var}` controls and what happens when it's empty
   - **Steps** — 4-8 numbered steps following the standard pattern:
     1. Read context (memory, prior logs)
     2. Fetch/search for data
     3. Process/analyze/synthesize
     4. Write output (article, file, or notification)
     5. Update memory logs
     6. Notify via `./notify`
   - **Environment variables** — any API keys or secrets needed
   - **Schedule suggestion** — what cron schedule makes sense

5. **Write the SKILL.md file.** Create `skills/{skill-name}/SKILL.md` with this exact structure:

   ```markdown
   ---
   name: {Display Name}
   description: {One-sentence description starting with a verb}
   var: ""
   tags: [{tags}]
   ---
   > **${var}** — {What the variable controls}. {If empty behavior}.

   Today is ${today}. {One sentence describing the task.}

   ## Steps

   1. **{Step title}.** {Instructions with specifics — endpoints, commands, formats.}

   2. **{Step title}.** {More instructions. Include code blocks for curl/bash when relevant.}

   ...

   N-1. **Log.** Append to `memory/logs/${today}.md`:
   - Skill: {skill-name}
   - What was done and key outputs

   N. **Notify.** Send via `./notify`:
   {Output format template}
   ```

   Rules for the SKILL.md content:
   - Write complete curl commands with proper headers and URL encoding
   - Include jq parsing for JSON APIs
   - Specify character limits for notifications (under 4000 chars)
   - Every link in output must be clickable (full URLs, not placeholders)
   - Include fallback behavior when optional API keys aren't set
   - Use `${var}` and `${today}` template variables — no other made-up variables
   - No TODOs, no placeholders, no "fill in later" — everything must be production-ready

6. **Register in aeon.yml.** Add the new skill to `aeon.yml` in the appropriate time-slot section:
   - Format: `  {skill-name}: { enabled: false, schedule: "{suggested_cron}" }`
   - Add a comment if the schedule or behavior needs explanation
   - Place it near related skills (crypto with crypto, content with content, etc.)

7. **Log.** Append to `memory/logs/${today}.md`:
   - Skill: create-skill
   - Created: `skills/{skill-name}/SKILL.md`
   - Registered in aeon.yml with schedule `{cron}`
   - Description of what the new skill does

8. **Notify.** Send via `./notify`:
   ```
   New skill created: **{skill-name}**

   {description}

   Schedule: `{cron}` (disabled by default)
   Trigger manually: dispatch with skill=`{skill-name}`
   ```

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Quality checklist

Before finalizing, verify the generated SKILL.md:
- [ ] Frontmatter has all required fields (name, description, var, tags)
- [ ] Variable documentation is a single `>` block quote line
- [ ] Steps are numbered and each has a bold title
- [ ] All API calls include complete curl commands (not pseudo-code)
- [ ] Fallback behavior defined for optional environment variables
- [ ] Output format specified with character limits
- [ ] Ends with memory log + notification steps
- [ ] No placeholders or TODOs anywhere in the file
- [ ] Skill name doesn't conflict with existing skills
