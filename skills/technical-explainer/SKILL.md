---
name: Technical Explainer
description: Generate a visual technical explanation of a recent topic using Replicate for the hero image
var: ""
tags: [content]
---
> **${var}** — Topic to explain (e.g. "free-market algorithm", "entropy trajectory reasoning", "reflexivity in prediction markets"). If empty, auto-selects from recent articles and conversations.

Read memory/MEMORY.md for context on recent topics.
Read the last 3 days of memory/logs/ to find discussed topics, articles written, and paper picks.

## Voice

If a `soul/` directory exists, read the soul files for voice calibration:
1. `soul/SOUL.md` — identity, worldview, opinions
2. `soul/STYLE.md` — writing style, sentence structure, anti-patterns

This is a *technical* explainer — you explaining a mechanism to a smart friend. More precision than the article skill, but same voice. No textbook tone. No "let's explore."

## Topic Selection

If `${var}` is set, use that as the topic. Otherwise:

1. **Check recent articles** — scan `articles/` for the last 3 articles written. Pick a core mechanism or concept from one that deserves a deeper technical breakdown.
2. **Check recent paper picks** — scan the last 7 days of logs for Paper Pick entries. A paper's key mechanism is often perfect explainer material.
3. **Check recent conversations** — look at memory/logs/ for any topic that came up in discussion, digests, or other skills that has a non-obvious technical mechanism worth visualizing.

Pick the topic with the best "aha" potential — something where a diagram or visual would actually help someone understand it.

## Research

1. Use WebSearch to find 3-5 sources explaining the technical mechanism.
2. If the topic is from a paper, fetch the paper abstract and any explainer blog posts:
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&limit=5&fields=title,authors,abstract,url,publicationDate,openAccessPdf"
   ```
3. Use WebFetch to read the 2-3 best sources in depth.
4. Identify the core mechanism — the one thing that, if you understood it, the rest clicks.

## Write the Explainer

Write a technical explanation (400-800 words) structured as:

- **Title**: Short, mechanism-focused. Not clickbait. e.g. "how free-market dynamics solve protein folding" not "This Wild New Algorithm Changes Everything"
- **The Setup** (2-3 sentences): What problem does this solve? Why should anyone care?
- **The Mechanism**: The core technical explanation. Use concrete examples. Analogies are good if they're precise — not "it's like a brain" hand-waving. Diagrams-in-words: walk through the process step by step.
- **Why It Matters** (2-3 sentences): The implication. What does this unlock? What breaks if this works?
- **Key Numbers**: 3-5 specific data points, benchmarks, or metrics that anchor the explanation.

### Voice Rules
- First person where it fits, but this is more explanatory than opinion.
- Technical precision > hedging. If you don't know, say so — don't fudge.
- Short paragraphs. Em dashes. Concrete > abstract.
- Reference specific systems, papers, people. No vague hand-waving.
- Cite sources inline with links.

## Generate Hero Image

Use Replicate's Nano Banana Pro to generate a visual that captures the core concept.

1. **Craft the prompt**: Create a detailed image generation prompt based on the technical concept. Think: what would a compelling diagram, visualization, or conceptual illustration of this mechanism look like? Aim for something technical and clean — not stock-photo energy. Good prompts include:
   - Specific visual elements (graphs, flows, network diagrams, molecular structures)
   - Style direction (technical illustration, blueprint style, dark background with bright accents, schematic)
   - Text labels if relevant (Nano Banana Pro handles text well)
   - Aspect ratio context (landscape for headers)

2. **Generate the image via Replicate API**:
   ```bash
   curl -s -X POST \
     -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
     -H "Content-Type: application/json" \
     -H "Prefer: wait" \
     -d '{
       "input": {
         "prompt": "YOUR_DETAILED_PROMPT_HERE",
         "aspect_ratio": "16:9",
         "number_of_images": 1,
         "safety_tolerance": 5
       }
     }' \
     "https://api.replicate.com/v1/models/google/nano-banana-pro/predictions"
   ```

3. **Extract the output URL** from the response JSON — it will be in the `output` field (a URL to the generated image on replicate.delivery).

4. **Persist the image to the repo** — Replicate CDN URLs are temporary and get deleted. Download the image and commit it:
   ```bash
   mkdir -p images
   # Extract extension from URL (jpg, jpeg, png, webp)
   EXT=$(echo "$IMAGE_URL" | grep -oE '\.(jpg|jpeg|png|webp)' | tail -1)
   EXT="${EXT:-.jpg}"
   LOCAL_PATH="images/explainer-${today}${EXT}"
   curl -sL "$IMAGE_URL" -o "$LOCAL_PATH"
   ```
   Then reference the local path in the article: `![hero](images/explainer-${today}${EXT})` (relative path).
   Also include the original Replicate URL in the notification (it works for immediate viewing).

5. **If the API call fails** (rate limit, timeout, etc.):
   - Retry once with `"allow_fallback_model": true` in the input
   - If still failing, skip the image and note it in the output — the explainer text stands on its own

## Save & Notify

1. Save the explainer to `articles/explainer-${today}.md` with:
   - The hero image at the top as `![hero](../images/explainer-${today}.ext)` (relative path to the committed image)
   - The image prompt used (in a comment or metadata block)
   - The full explainer text
   - Sources section at the bottom

2. Log to `memory/logs/${today}.md`:
   ```
   ## Technical Explainer
   - **Topic:** [topic]
   - **Title:** [title]
   - **Image:** [generated/failed]
   - **Image prompt:** [prompt used]
   - **File:** articles/explainer-${today}.md
   - **Notification sent:** yes/no
   ```

3. Send via `./notify`:
   ```
   technical explainer: [title]

   [2-3 sentence hook — the core mechanism in plain english]

   [hero image URL if generated]

   read it: [link to article file]
   ```

## Sandbox note

The sandbox may block outbound curl. Use **WebFetch** as a fallback for any URL fetch. For auth-required APIs, use the pre-fetch/post-process pattern (see CLAUDE.md).

## Environment Variables
- `REPLICATE_API_TOKEN` — Replicate API key (required for image generation, explainer text works without it)
