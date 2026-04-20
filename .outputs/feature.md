*Feature Built — 2026-04-20*

Scenario Auto-Suggest from Document

MiroShark's Home screen now reads your uploaded document and drafts three prediction-market-style simulation scenarios for you before you type anything. Paste a URL or drop a .md/.txt file and within a couple of seconds three cards appear above the Simulation Prompt field — one Bull, one Bear, one Neutral framing of an outcome the document could drive, each with a concrete YES/NO question, a plausible initial probability band, and a one-sentence rationale. Click "Use this →" to fill the prompt, or dismiss and write your own.

Why this matters:
The Simulation Prompt was the last real friction point between uploading a document and launching a simulation. New users who aren't prediction-market researchers by training often froze on the blank field or typed generic prompts ("what will happen?") that produced weaker simulations than a well-framed split. This was the #1 outstanding repo-actions idea ("the last major friction point before first-value") and it directly addresses the academic/research funnel that the 5× perf PR from mbs5 and 133+ forks indicate is real. It also trains users over time — by seeing three well-framed scenarios, they learn what a good simulation prompt looks like.

What was built:
- backend/app/api/simulation.py: New POST /api/simulation/suggest-scenarios endpoint. Normalizes whitespace + clamps the preview to 2000 chars, SHA-256s it, checks an in-process LRU cache (cap 64), then calls create_llm_client().chat_json() with a compact prompt that asks for exactly one Bull/Bear/Neutral framing. _clean_suggestions validates every entry — labels must be Bull/Bear/Neutral, probability ranges clamped [0,100] (swaps if reversed), question 8–240 chars, rationale ≤200 chars — and silently drops malformed ones. On LLM unavailable / timeout / malformed output, returns 200 with suggestions:[] + a reason code so the UI can hide gracefully.
- frontend/src/components/ScenarioSuggestions.vue: New debounced card panel (800ms, 120-char min) with Bull/Bear/Neutral colored left-borders and badges, loading spinner, dismiss button, and a monotonic requestSeq guard so a late response from an outdated preview can't overwrite the current cards.
- frontend/src/views/Home.vue: Reads .md/.txt files client-side via File.slice(0,6000).text() (PDFs skip — their text extraction runs server-side during graph build), combines with every urlDocs[i].text, clamps to 6KB, and hands the combined preview to the component. handleSuggestionUse fills the Simulation Prompt textarea.
- frontend/src/api/simulation.js: suggestScenarios({ text_preview }) with a 25s override timeout so a single stuck LLM can't tie up an axios slot (default is 300s).
- README: New "Smart Setup (Scenario Auto-Suggest)" subsection under How It Works.

How it works:
The moment the user drops a file or a fetched URL adds text to urlDocs, a computed property in Home.vue concatenates up to 6KB of preview text and passes it to ScenarioSuggestions. The component debounces 800ms, then calls the backend endpoint. On the server, the same preview is re-normalized (whitespace-collapsed, clamped to 2KB) and SHA-256ed — identical previews skip the LLM entirely and return a cached result, so re-renders or edits above/below the sampled window cost nothing. Otherwise the LLM is invoked via the existing OpenAI-compatible client wrapper with a JSON-object response mode, the output runs through a strict validator (silently dropping any entry that fails), and up to three survivors are returned. The whole path is non-blocking: every soft failure returns 200 with an empty suggestions array, so the form below works exactly as before whether the LLM is configured or not. No new dependencies — hashlib is stdlib, everything else reuses existing wiring.

What's next:
Natural extension is a multipart/form-data variant that accepts a PDF directly and parses it with the existing FileParser so PDF-only uploads also trigger auto-suggest. A second follow-up is lightweight telemetry on which card position gets picked (0/1/2/none) plus document length — after ~50 runs that informs prompt tuning. Could also surface the model name on each card so users know which LLM drafted them.

PR: https://github.com/aaronjmars/MiroShark/pull/39
