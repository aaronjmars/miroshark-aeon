export type ChangelogPR = { number: number; title: string; url: string; author: string };
export type ChangelogEntry = {
  date: string;
  title: string;
  summary: string;
  highlights: string[];
  prs: ChangelogPR[];
};

export const CHANGELOG: ChangelogEntry[] = [
  // newest first - PREPEND new entries here, never rewrite existing ones
  {
    date: "2026-07-12",
    title: "Python backend dependency maintenance",
    summary:
      "Dependabot bumped soupsieve from 2.8 to 2.8.4 in the Python backend, patching an inefficient attribute pattern. No simulation behavior changes.",
    highlights: [
      "Maintenance: 1 dependency bump (soupsieve 2.8 → 2.8.4, attribute pattern efficiency fix) (#244)",
    ],
    prs: [
      {
        number: 244,
        title: "chore: bump soupsieve from 2.8 to 2.8.4 in /backend in the uv group across 1 directory",
        url: "https://github.com/aaronjmars/MiroShark/pull/244",
        author: "dependabot[bot]",
      },
    ],
  },
  {
    date: "2026-07-09",
    title: "French coverage at 87%, social agent fixes",
    summary:
      "Zarbel974 pushed French UI coverage from 74% to 86.9% across 20 components, adding ~340 translation pairs including dense panels like EmbedDialog and WhatIfPanel. dan-and addressed empty-response failures in persona handling — the social agent now handles edge cases that caused blank agent outputs mid-simulation.",
    highlights: [
      "French translations completed to 86.9% (1723/1984 tr() calls), up from 74%; 20 components, ~340 new pairs (#239)",
      "Social agent: empty response handling in persona tool messages fixed — reduces silent failures mid-run (#241)",
      "RootAI ecosystem profile image updated to current Twitter avatar in ECOSYSTEM.md (#242)",
    ],
    prs: [
      {
        number: 239,
        title: "feat(i18n): complete French translations to 86.9% (1723/1984 tr() calls)",
        url: "https://github.com/aaronjmars/MiroShark/pull/239",
        author: "Zarbel974",
      },
      {
        number: 241,
        title: "Fix/social agent tool messages",
        url: "https://github.com/aaronjmars/MiroShark/pull/241",
        author: "dan-and",
      },
      {
        number: 242,
        title: "docs(ecosystem): update RootAI profile image",
        url: "https://github.com/aaronjmars/MiroShark/pull/242",
        author: "aaronjmars",
      },
    ],
  },
  {
    date: "2026-07-06",
    title: "French i18n, CVE sweep, multi-model compatibility",
    summary:
      "External contributor Zarbel974 landed French translations for ~1,627 UI strings across all Vue components, the largest single i18n contribution since DE. A CVE sweep closed vulnerabilities in werkzeug, requests, starlette, cryptography, pyjwt, and pytest; the social agent message filter was fixed to preserve tool_calls, restoring compatibility with Gemini, Azure, and GPT-5.4.",
    highlights: [
      "French frontend translations from Zarbel974 — ~1,627 tr() calls across all Vue components (~74% coverage) (#222)",
      "Social agent now preserves tool_calls when filtering empty LLM messages; fixes Gemini, Azure, and GPT-5.4 compatibility (#232)",
      "Nemotron datasets now persist across container recreates; bind-mount added to all three compose files (#238)",
      "CVE sweep (patch/minor): werkzeug CVE-2026-21860/-27199, requests CVE-2026-25645, and 8 other packages (#229)",
      "Major CVE fixes behind camel-ai MCP: starlette 1.x, cryptography 49.x, pyjwt 2.13 (#230)",
      "pytest bumped to 9.1.1 + pytest-asyncio 1.4.0, closing CVE-2025-71176 (#231)",
      "SECURITY.md + CONTRIBUTING.md added; community health files consolidated under .github/ (#235)",
      "FUNDING.yml added: Sponsor button wired to miroshark.xyz, Bankr, DexScreener, BaseScan (#237)",
      "LICENSE moved back to repo root so GitHub license detection works (#236)",
      "Maintenance: 1 dependency bump (uv group, 6 packages) (#233)",
    ],
    prs: [
      {
        number: 222,
        title: "feat(i18n): French (fr) frontend translations for ~1627 tr() calls",
        url: "https://github.com/aaronjmars/MiroShark/pull/222",
        author: "Zarbel974",
      },
      {
        number: 229,
        title: "fix(deps): safe patch/minor bumps for Dependabot alerts (A+B)",
        url: "https://github.com/aaronjmars/MiroShark/pull/229",
        author: "aaronjmars",
      },
      {
        number: 230,
        title: "fix(deps): major bumps behind camel-ai MCP — starlette 1.x, cryptography, pyjwt, python-multipart (C)",
        url: "https://github.com/aaronjmars/MiroShark/pull/230",
        author: "aaronjmars",
      },
      {
        number: 231,
        title: "fix(deps): bump pytest 8→9.1.1 + pytest-asyncio (CVE-2025-71176) (D)",
        url: "https://github.com/aaronjmars/MiroShark/pull/231",
        author: "aaronjmars",
      },
      {
        number: 232,
        title: "fix(social-agent): preserve tool_calls when filtering empty LLM messages",
        url: "https://github.com/aaronjmars/MiroShark/pull/232",
        author: "dan-and",
      },
      {
        number: 233,
        title: "chore: bump the uv group across 1 directory with 6 updates",
        url: "https://github.com/aaronjmars/MiroShark/pull/233",
        author: "dependabot[bot]",
      },
      {
        number: 235,
        title:
          "chore: add SECURITY + CONTRIBUTING, consolidate community docs under .github/",
        url: "https://github.com/aaronjmars/MiroShark/pull/235",
        author: "aaronjmars",
      },
      {
        number: 236,
        title: "fix: move LICENSE back to repo root so GitHub detects it",
        url: "https://github.com/aaronjmars/MiroShark/pull/236",
        author: "aaronjmars",
      },
      {
        number: 237,
        title: "chore: add FUNDING.yml (Sponsor button)",
        url: "https://github.com/aaronjmars/MiroShark/pull/237",
        author: "aaronjmars",
      },
      {
        number: 238,
        title:
          "fix(compose): persist backend/data so Nemotron datasets survive recreation",
        url: "https://github.com/aaronjmars/MiroShark/pull/238",
        author: "aaronjmars",
      },
    ],
  },
  {
    date: "2026-07-03",
    title: "New default models across all agent slots",
    summary:
      "The default model lineup is replaced: base agent work moves to inception/mercury-2:nitro, smart reasoning and NER to google/gemini-3-flash-preview, Wonderwall to deepseek/deepseek-v4-flash:nitro, and web search to deepseek/deepseek-v4-flash:online. Fresh installs pick these up automatically; existing deployments can override per-slot via env.",
    highlights: [
      "Default models rotated across all slots: base → mercury-2:nitro, smart/NER → gemini-3-flash-preview, Wonderwall → deepseek-v4-flash:nitro, web search → deepseek-v4-flash:online (#223)",
      "Maintenance: 1 dependency bump (vite 8.1.3) (#225)",
    ],
    prs: [
      {
        number: 223,
        title: "chore(config): switch default model lineup",
        url: "https://github.com/aaronjmars/MiroShark/pull/223",
        author: "aaronjmars",
      },
      {
        number: 225,
        title:
          "chore: bump vite from 8.1.0 to 8.1.3 in /frontend in the frontend-minor-patch group",
        url: "https://github.com/aaronjmars/MiroShark/pull/225",
        author: "dependabot[bot]",
      },
    ],
  },
  {
    date: "2026-06-30",
    title: "Docker, Actions, and frontend dependency bumps",
    summary:
      "Four maintenance bumps cleared the queue: the frontend locked in axios 1.18.1 (HTTP adapter fixes), vue, and vite; GitHub Actions moved to actions/checkout v7 and Node 24-based docker/login-action v4 and docker/setup-buildx-action v4.",
    highlights: [
      "Maintenance: 4 dependency/CI bumps (axios 1.18.1, vue, vite, actions/checkout 7, docker/login-action 4, docker/setup-buildx-action 4) (#218–#221)",
    ],
    prs: [
      {
        number: 221,
        title:
          "chore: bump the frontend-minor-patch group in /frontend with 3 updates",
        url: "https://github.com/aaronjmars/MiroShark/pull/221",
        author: "dependabot[bot]",
      },
      {
        number: 220,
        title: "chore: bump actions/checkout from 6 to 7",
        url: "https://github.com/aaronjmars/MiroShark/pull/220",
        author: "dependabot[bot]",
      },
      {
        number: 219,
        title: "chore: bump docker/login-action from 3 to 4",
        url: "https://github.com/aaronjmars/MiroShark/pull/219",
        author: "dependabot[bot]",
      },
      {
        number: 218,
        title: "chore: bump docker/setup-buildx-action from 3 to 4",
        url: "https://github.com/aaronjmars/MiroShark/pull/218",
        author: "dependabot[bot]",
      },
    ],
  },
  {
    date: "2026-06-27",
    title: "Stop subcommand, interview hang fixes, locale hardening",
    summary:
      "The CLI now has a stop subcommand to cancel running simulations, completing the cost/wait/stop scriptable pipeline. dan-and contributed three engine fixes in the same batch: persona interviews no longer hang silently on slow or thinking models, non-English locale no longer drifts mid-run, and local LLM config tuning prevents JSON truncation and timeout failures.",
    highlights: [
      "stop subcommand added: cancels a running simulation, exits 0 on success or 1 on error (#216)",
      "Non-English locale now held across per-round agent actions and report sections, not just at session start (#213)",
      "Persona and batch interviews no longer hang on slow/thinking models; errors surface with a message instead of dying silently (#214)",
      "Local LLM tuning: AGENTS_PER_BATCH halved to 7, summary lengths raised to 500 for richer context, name-based agent matching added (#212)",
      "--json flag placement clarified in stop CLI docs: must precede the subcommand, not trail it (#217)",
    ],
    prs: [
      {
        number: 217,
        title: "docs(cli): clarify --json must precede the stop subcommand",
        url: "https://github.com/aaronjmars/MiroShark/pull/217",
        author: "aaronjmars",
      },
      {
        number: 216,
        title: "feat(cli): add stop subcommand to cancel a running simulation",
        url: "https://github.com/aaronjmars/MiroShark/pull/216",
        author: "aaronjmars",
      },
      {
        number: 214,
        title: "fix(interview): Persona-interviews hang prevention, error surfacing, and…",
        url: "https://github.com/aaronjmars/MiroShark/pull/214",
        author: "dan-and",
      },
      {
        number: 213,
        title: "fix(i18n): keep non-English locale in agent actions and report sections",
        url: "https://github.com/aaronjmars/MiroShark/pull/213",
        author: "dan-and",
      },
      {
        number: 212,
        title: "chore: performance and robustness tuning for local llm usage",
        url: "https://github.com/aaronjmars/MiroShark/pull/212",
        author: "dan-and",
      },
    ],
  },
  {
    date: "2026-06-25",
    title: "Wait subcommand: block until simulation finishes",
    summary:
      "The CLI can now block on a running simulation and exit with a machine-readable code: 0 for completed, 1 for failed/stopped, 2 for timeout. Progress lines print to stderr so stdout stays clean for --json piping, making wait → cost → report pipelines scriptable without polling.",
    highlights: [
      "wait subcommand added to CLI: polls run-status until terminal state, exits 0/1/2, progress to stderr (#215)",
    ],
    prs: [
      {
        number: 215,
        title: "feat(cli): add wait subcommand to block until a simulation finishes",
        url: "https://github.com/aaronjmars/MiroShark/pull/215",
        author: "aaronjmars",
      },
    ],
  },
  {
    date: "2026-06-24",
    title: "Thinking model robustness, JSON repair, and cost CLI",
    summary:
      "The LLM pipeline got a hardening pass from external contributor dan-and: thinking-model budget, <think> block stripping, and JSON repair so truncated or malformed reasoning output no longer silently breaks runs. The cost CLI subcommand also shipped, letting scripts read per-run spend with `python cli.py cost <id>` without touching the API.",
    highlights: [
      "Thinking model robustness: budget param, <think> stripping, JSON/control-char repair, None guards on empty content (#209)",
      "Cost subcommand added to CLI: `python cli.py cost <id>` prints per-run USD estimate by phase (#208)",
      "Config guard: blank LLM_MODEL_NAME= now falls back to mimo-v2.5 instead of sending an empty model string (#210)",
      "Graph search fan-out restored: semantic default queries re-added after #209 narrowed the fallback to one query (#211)",
    ],
    prs: [
      {
        number: 211,
        title: "fix(graph): restore semantic default fan-out in sub-query fallback",
        url: "https://github.com/aaronjmars/MiroShark/pull/211",
        author: "aaronjmars",
      },
      {
        number: 210,
        title: "fix(config): fall back to default when LLM_MODEL_NAME is blank",
        url: "https://github.com/aaronjmars/MiroShark/pull/210",
        author: "aaronjmars",
      },
      {
        number: 209,
        title: "fix(llm): thinking model robustness — budget, JSON repair, None guards",
        url: "https://github.com/aaronjmars/MiroShark/pull/209",
        author: "dan-and",
      },
      {
        number: 208,
        title: "feat(cli): add cost subcommand surfacing per-run USD estimate",
        url: "https://github.com/aaronjmars/MiroShark/pull/208",
        author: "aaronjmars",
      },
    ],
  },
  {
    date: "2026-06-23",
    title: "Model fix, rebrand, and code audit",
    summary:
      "The default model (mimo-v2-flash) was delisted by OpenRouter and is replaced with mimo-v2.5 across config, deploy templates, presets, and docs - fresh installs no longer 404. The project adopted a new tagline and a targeted 8-agent code audit removed dead classes and unused health-check stubs from the backend and frontend.",
    highlights: [
      "Default model swapped from mimo-v2-flash to mimo-v2.5 across config, presets, docs, and deploy templates (#207)",
      "New tagline: \"Simulate anything, for $1 & less than 10 min.\" + OpenRouter attribution updated to miroshark.xyz (#206)",
      "Targeted 8-agent code audit removed dead classes and health-check stubs; backend and frontend trimmed (#205)",
      "Maintenance: 4 dependency/CI bumps (actions/setup-node 6, docker/metadata-action 6, docker/setup-qemu-action 4, dompurify 3.4.11)",
    ],
    prs: [
      {
        number: 207,
        title: "chore(models): switch default model from mimo-v2-flash to mimo-v2.5",
        url: "https://github.com/aaronjmars/MiroShark/pull/207",
        author: "aaronjmars",
      },
      {
        number: 206,
        title: "chore(branding): adopt new tagline and point OpenRouter attribution at miroshark.xyz",
        url: "https://github.com/aaronjmars/MiroShark/pull/206",
        author: "aaronjmars",
      },
      {
        number: 205,
        title: "refactor: code-quality cleanup across backend and frontend",
        url: "https://github.com/aaronjmars/MiroShark/pull/205",
        author: "aaronjmars",
      },
      {
        number: 202,
        title: "chore: bump dompurify from 3.4.10 to 3.4.11 in /frontend in the frontend-minor-patch group",
        url: "https://github.com/aaronjmars/MiroShark/pull/202",
        author: "dependabot[bot]",
      },
      {
        number: 201,
        title: "chore: bump actions/setup-node from 5 to 6",
        url: "https://github.com/aaronjmars/MiroShark/pull/201",
        author: "dependabot[bot]",
      },
      {
        number: 200,
        title: "chore: bump docker/metadata-action from 5 to 6",
        url: "https://github.com/aaronjmars/MiroShark/pull/200",
        author: "dependabot[bot]",
      },
      {
        number: 199,
        title: "chore: bump docker/setup-qemu-action from 3 to 4",
        url: "https://github.com/aaronjmars/MiroShark/pull/199",
        author: "dependabot[bot]",
      },
    ],
  },
  {
    date: "2026-06-22",
    title: "Full DE/FR locales + engine hardening",
    summary:
      "MiroShark now runs fully in German and French - all agent prompts, persona grounding, and reports, not just UI chrome. The $1 cost claim lands as a visible pill on every public embed, a camel-ai 0.2.90 break was caught and patched the same day it merged, and a locale-threading bug in the fallback interview path is closed.",
    highlights: [
      "Locale state threaded through ThreadPoolExecutor in graph_tools fallback interview (#198)",
      "CLAUDE.md added - agent-readable codebase map for Claude Code contributors (#197)",
      "Camel smoke test now asserts non-empty message content, not just a non-None response (#196)",
      "Report agent wired to locale registry so reports generate in the session language (#194)",
      "suggest_scenarios JSON salvaged from truncated LLM responses via json_repair; no more zero-result returns (#192)",
      "Cost pill (~$X) rendered on public embed view, making the $1-per-sim claim visible to visitors (#190)",
      "German added to frontend UI and all agent-communication locales; locale reinforcement across DE/FR/ZH/EN (#189)",
      "suggest_scenarios timeout raised 20s→40s, max_tokens 700→1500 for verbose languages and slow local LLMs (#188)",
      "French prompt locale fully translated - all 7 modules filled (was empty stubs after #184) + CI coverage gate (#186)",
      "French README and language-switcher entry added; FR now fully discoverable (#185)",
      "Locale helpers generalized to EN/ZH/DE/FR; 199 existing call sites unchanged (#184)",
      "total_actions corrected from hardcoded 0 on every successful run; first camel agent smoke test added (#183)",
      "uv.lock synced to camel-ai 0.2.90, unblocking Docker builds that refused to proceed (#182)",
      "camel-ai 0.2.90 agent loop break patched the same day the bump merged (#181)",
      "Frontend now builds on every PR - was tag-triggered only, so breaks reached release undetected (#180)",
      "Per-sim cost.json endpoint: queryable USD cost breakdown by model and phase, flagged is_estimate (#179)",
      "SearXNG + Firecrawl support: self-hosted web search and scraping for local-LLM deployments (#178)",
      "Maintenance: 11 dependency/CI bumps (Dependabot wave - vite, vue-router, camel-ai, python, Actions)",
    ],
    prs: [
      {
        number: 198,
        title: "fix(i18n): thread locale through graph_tools fallback interview ThreadPoolExecutor",
        url: "https://github.com/aaronjmars/MiroShark/pull/198",
        author: "aaronjmars",
      },
      {
        number: 197,
        title: "docs: add CLAUDE.md for AI coding agents",
        url: "https://github.com/aaronjmars/MiroShark/pull/197",
        author: "aaronjmars",
      },
      {
        number: 196,
        title: "test: assert camel smoke test produces real agent output",
        url: "https://github.com/aaronjmars/MiroShark/pull/196",
        author: "aaronjmars",
      },
      {
        number: 194,
        title: "i18n(report-agent): wire language aware prompts through locale registry with English",
        url: "https://github.com/aaronjmars/MiroShark/pull/194",
        author: "dan-and",
      },
      {
        number: 192,
        title: "fix(simulation): salvage truncated suggest_scenarios JSON (#191)",
        url: "https://github.com/aaronjmars/MiroShark/pull/192",
        author: "aaronjmars",
      },
      {
        number: 190,
        title: "feat: show estimated run cost on public simulation embeds",
        url: "https://github.com/aaronjmars/MiroShark/pull/190",
        author: "aaronjmars",
      },
      {
        number: 189,
        title: "Translation de in Frontend and Agent-Description/Communication",
        url: "https://github.com/aaronjmars/MiroShark/pull/189",
        author: "dan-and",
      },
      {
        number: 188,
        title: "fix(simulation): raise suggest-scenarios timeout and token limit",
        url: "https://github.com/aaronjmars/MiroShark/pull/188",
        author: "dan-and",
      },
      {
        number: 186,
        title: "feat(i18n): translate French (fr) prompt locale + CI coverage gate",
        url: "https://github.com/aaronjmars/MiroShark/pull/186",
        author: "aaronjmars",
      },
      {
        number: 185,
        title: "docs(i18n): add French README + wire FR into language switcher",
        url: "https://github.com/aaronjmars/MiroShark/pull/185",
        author: "aaronjmars",
      },
      {
        number: 184,
        title: "feat(i18n): generalize locale helpers + German/French foundation (#161, #95)",
        url: "https://github.com/aaronjmars/MiroShark/pull/184",
        author: "aaronjmars",
      },
      {
        number: 183,
        title: "fix+ci: correct total_actions reporting + add camel agent smoke test (#181 follow-ups)",
        url: "https://github.com/aaronjmars/MiroShark/pull/183",
        author: "aaronjmars",
      },
      {
        number: 182,
        title: "fix: sync uv.lock with camel-ai 0.2.90 (unbreaks Docker build)",
        url: "https://github.com/aaronjmars/MiroShark/pull/182",
        author: "aaronjmars",
      },
      {
        number: 181,
        title: "fix(wonderwall): camel-ai 0.2.90 _aget_model_response signature compat (unblocks #176)",
        url: "https://github.com/aaronjmars/MiroShark/pull/181",
        author: "aaronjmars",
      },
      {
        number: 180,
        title: "ci: build the frontend on every PR",
        url: "https://github.com/aaronjmars/MiroShark/pull/180",
        author: "aaronjmars",
      },
      {
        number: 179,
        title: "feat: GET /api/simulation/<id>/cost.json - per-sim cost breakdown ($1-to-simulate, queryable)",
        url: "https://github.com/aaronjmars/MiroShark/pull/179",
        author: "aaronjmars",
      },
      {
        number: 178,
        title: "Alternative websearch/scrape via SearXNG / Firecrawl for non-websearch capable LLMs",
        url: "https://github.com/aaronjmars/MiroShark/pull/178",
        author: "dan-and",
      },
      {
        number: 177,
        title: "chore: bump vite from 7.2.7 to 8.0.16 in /frontend",
        url: "https://github.com/aaronjmars/MiroShark/pull/177",
        author: "dependabot[bot]",
      },
      {
        number: 176,
        title: "chore: bump camel-ai from 0.2.78 to 0.2.90 in /backend",
        url: "https://github.com/aaronjmars/MiroShark/pull/176",
        author: "dependabot[bot]",
      },
      {
        number: 175,
        title: "chore: bump vue-router from 4.6.3 to 5.1.0 in /frontend",
        url: "https://github.com/aaronjmars/MiroShark/pull/175",
        author: "dependabot[bot]",
      },
      {
        number: 174,
        title: "chore: bump the frontend-minor-patch group in /frontend with 5 updates",
        url: "https://github.com/aaronjmars/MiroShark/pull/174",
        author: "dependabot[bot]",
      },
      {
        number: 173,
        title: "chore: update pywebpush requirement from >=2.0.0 to >=2.3.0 in /backend",
        url: "https://github.com/aaronjmars/MiroShark/pull/173",
        author: "dependabot[bot]",
      },
      {
        number: 172,
        title: "chore: update nashpy requirement from >=0.0.41 to >=0.0.43 in /backend",
        url: "https://github.com/aaronjmars/MiroShark/pull/172",
        author: "dependabot[bot]",
      },
      {
        number: 171,
        title: "chore: bump actions/setup-python from 5 to 6",
        url: "https://github.com/aaronjmars/MiroShark/pull/171",
        author: "dependabot[bot]",
      },
      {
        number: 170,
        title: "chore: bump actions/checkout from 4 to 6",
        url: "https://github.com/aaronjmars/MiroShark/pull/170",
        author: "dependabot[bot]",
      },
      {
        number: 169,
        title: "chore: bump docker/build-push-action from 5 to 7",
        url: "https://github.com/aaronjmars/MiroShark/pull/169",
        author: "dependabot[bot]",
      },
      {
        number: 168,
        title: "chore: bump python from 3.11 to 3.14",
        url: "https://github.com/aaronjmars/MiroShark/pull/168",
        author: "dependabot[bot]",
      },
      {
        number: 166,
        title: "chore: add Dependabot config for pip, npm, GitHub Actions & Docker",
        url: "https://github.com/aaronjmars/MiroShark/pull/166",
        author: "aaronjmars",
      },
    ],
  },
  {
    date: "2026-06-21",
    title: "Contributor on-ramp + same-origin API",
    summary:
      "Earlier in the same window: the contributor guide grew from a test-only stub into a full guide, two rounds of code-quality cleanup landed, same-origin API calls plus a Neo4j 5.26 bump went in, and flaky demographic-grounding tests were fixed.",
    highlights: [
      "Same-origin API calls now supported; Neo4j bumped to 5.26 for better indexing. (#159)",
      "Expanded CONTRIBUTING from a test-only stub to a full contributor guide. (#162)",
      "Round-2 code-quality cleanup: DRY helpers, type fixes, dead-import removal, error handling. (#163)",
      "Deduped shared helpers (utc_iso8601, avg_position, public-base-url) and fixed a transcript bool bug. (#164)",
      "Fixed two demographic-grounding tests that failed without an LLM_API_KEY. (#165)",
      "Maintenance: concurrently bumped 9.2.1 → 10.0.3. (#167)",
    ],
    prs: [
      {
        number: 159,
        title: "chore: allow same origin api calls and neo4j v5.26 bump",
        url: "https://github.com/aaronjmars/MiroShark/pull/159",
        author: "dan-and",
      },
      {
        number: 162,
        title:
          "docs: expand CONTRIBUTING from test-only stub to full contributor guide",
        url: "https://github.com/aaronjmars/MiroShark/pull/162",
        author: "aaronjmars",
      },
      {
        number: 163,
        title:
          "chore: round-2 code-quality cleanup (DRY, types, weak-types, dead-imports, error-handling)",
        url: "https://github.com/aaronjmars/MiroShark/pull/163",
        author: "aaronjmars",
      },
      {
        number: 164,
        title:
          "refactor: dedup shared helpers (utc-iso8601, avg_position, public-base-url) + fix transcript bool bug",
        url: "https://github.com/aaronjmars/MiroShark/pull/164",
        author: "aaronjmars",
      },
      {
        number: 165,
        title: "test: fix 2 demographic-grounding tests that required LLM_API_KEY",
        url: "https://github.com/aaronjmars/MiroShark/pull/165",
        author: "aaronjmars",
      },
      {
        number: 167,
        title: "chore: bump concurrently from 9.2.1 to 10.0.3",
        url: "https://github.com/aaronjmars/MiroShark/pull/167",
        author: "dependabot[bot]",
      },
    ],
  },
];
export const PUBLISHED_PR_NUMBERS = CHANGELOG.flatMap((e) => e.prs.map((p) => p.number));
