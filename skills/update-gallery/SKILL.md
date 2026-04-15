---
name: Update Gallery
description: Sync articles, activity logs, and memory to the GitHub Pages site
var: ""
tags: [content]
---
> **${var}** — Optional single article filename to sync (e.g. `article-2026-04-01.md`). If empty, syncs all articles.

Publish Aeon's article outputs to the GitHub Pages gallery at `docs/_posts/`.

## Steps

1. Read `memory/MEMORY.md` for context on recent articles.

2. Run the site data sync script to populate `docs/_data/` with logs, memory, topics, and article metadata:
   ```bash
   bash scripts/sync-site-data.sh
   ```

3. List all markdown files in `articles/` (excluding `.gitkeep` and `feed.xml`):
   ```bash
   ls articles/*.md 2>/dev/null | grep -v feed.xml | sort
   ```

4. For each article file (or just the one in `${var}` if set), process it into a Jekyll post:

   **a) Parse the filename to extract date and slug.**
   Filenames follow patterns like:
   - `article-2026-04-01.md` → date `2026-04-01`, slug `article`
   - `changelog-2026-03-19.md` → date `2026-03-19`, slug `changelog`
   - `repo-actions-2026-03-30.md` → date `2026-03-30`, slug `repo-actions`
   - `token-report-2026-04-02.md` → date `2026-04-02`, slug `token-report`

   The date is the YYYY-MM-DD portion extracted from the filename using regex `([0-9]{4}-[0-9]{2}-[0-9]{2})`.
   The slug is everything before the date pattern, with trailing hyphens removed.

   **b) Extract the title** from the first `# Heading` in the file. If no heading exists, convert the filename slug to title case (e.g., `repo-actions` → `Repo Actions`).

   **c) Determine the category** from the slug:
   - `article`, `research-brief`, `repo-article` → `article`
   - `changelog`, `push-recap`, `code-health` → `changelog`
   - `token-report`, `token-alert`, `defi-overview` → `crypto`
   - `digest`, `rss-digest`, `hacker-news` → `digest`
   - Everything else → `article`

   **d) Check if the article already has Jekyll frontmatter** (starts with `---`). If it does, preserve existing frontmatter and skip re-adding.

   **e) Build the Jekyll post filename:** `docs/_posts/YYYY-MM-DD-<slug>-<sanitized-title-excerpt>.md`
   where the title excerpt is the title lowercased, spaces replaced with hyphens, special chars removed, truncated to 50 chars.

   **f) Write the post file** with this structure:
   ```markdown
   ---
   title: "<extracted title>"
   date: YYYY-MM-DD
   categories: [<category>]
   source_file: "<original-filename>"
   ---
   <article body — everything after the frontmatter if present, or the full content>
   ```

5. After processing all articles, check if any new files were added to `docs/_posts/` or `docs/_data/`:
   ```bash
   git status docs/
   ```

6. If there are new or changed files, create a branch, stage, commit, and open a PR:
   ```bash
   BRANCH="chore/gallery-sync-$(date +%Y-%m-%d)"
   git checkout -b "$BRANCH"
   git add docs/_posts/ docs/_data/
   git diff --cached --quiet || git commit -m "chore(gallery): sync articles and site data $(date +%Y-%m-%d)"
   ```

7. Push the branch and open a PR:
   ```bash
   git push -u origin "$BRANCH"
   gh pr create --title "chore(gallery): sync articles and site data $(date +%Y-%m-%d)" \
     --body "Automated gallery sync — new articles and site data updates."
   ```

8. Update `memory/logs/${today}.md` with:
   - How many articles were processed
   - How many new posts were added to `docs/_posts/`
   - Any articles that were skipped (already present)
   - Whether site data (logs, memory, topics) was synced

9. Send a notification via `./notify`:
   "Gallery updated: N articles published to GitHub Pages."

## Notes

- Jekyll post filenames must start with `YYYY-MM-DD-` and end with `.md`.
- Frontmatter values with colons or special chars must be quoted.
- If an article already exists in `docs/_posts/` (same source_file), skip it unless the source has changed (compare file sizes or first 100 bytes).
- Articles that have no date in their filename: fall back to the git commit date using `git log -1 --format="%as" -- articles/<filename>`.
- Never delete posts from `docs/_posts/` — only add or update.
