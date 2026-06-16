# Everyone Advertises a Price for AI. Almost Nobody Lets You Check the Bill.

The number on the label and the number on the invoice have quietly come apart. A team buys an AI coding assistant at a tidy monthly rate, and three months later the finance lead is staring at a line item nobody can explain. One 2026 audit of agent deployments put the average *hidden* cost — spend on top of the advertised subscription — at [$327 a month, a 1,635% markup over the sticker price](https://aiempiremedia.com/the-hidden-cost-of-ai-agents-2026/). The $20 plan was real. So was the $347 bill.

This is not fraud. It is structure. And it has made the most important question about an AI product — *what does it actually cost to run?* — one of the hardest to answer honestly.

## Why the bill is unknowable

Two mechanisms drive the gap. The first is the way agents consume tokens. A chatbot sends one message and gets one reply. An agent loops: it reasons, calls a tool, reads the result, reasons again — and every step re-sends the entire accumulated history to the model. By step 20 you are paying for the same prompt twenty times over. A [LeanOps teardown using Claude Sonnet 4.6](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) measured a five-step task at $0.158 against a single call's $0.049 — 3.2x. Extend the loop and the curve bends hard: past 50 steps the multiplier clears 30x, and a 200-step debugging run exceeds 100x — one developer in the same writeup "hit $4,200 in API fees over a long weekend" on a single refactoring job.

The second mechanism is that the prices themselves are not real prices. As one analysis of [AI-first SaaS economics](https://www.getmonetizely.com/blogs/the-economics-of-ai-first-b2b-saas-in-2026) puts it bluntly: "Even as inference becomes 50–100× cheaper every few years, prices remain below true economic cost, propped up by Big Tech." GitHub Copilot charged roughly $10 a user while heavy users burned up to $80 in compute; the vendor eats the difference until the credits run out.

So a quoted price is a marketing decision on top of a subsidy on top of a consumption pattern nobody fully metered. The honest answer to "what does this cost" is usually: *we don't expose that.*

## A product whose entire pitch is a price

That backdrop is what makes a small piece of plumbing shipped on June 16 worth looking at. There is an open-source engine whose headline is, literally, a number: *simulate anything, for $1 and less than 10 minutes.* It spawns hundreds of language-model agents, seeds them from real demographics, and lets them argue and trade until their collective belief settles into a forecast. The whole proposition rests on that dollar.

And until this week, you could not check it. The system already priced every model call internally — `app/utils/run_summary.py` multiplies token counts against a pricing table the moment a run finishes — but only wrote the result into a human-readable file in the simulation's directory. The tokens were exposed over the API; the dollars were not. An evaluator who ran a simulation could not programmatically answer the first question anyone asks: *what did that cost?*

The new route, `GET /api/simulation/<id>/cost.json`, closes exactly that gap and nothing wider. It returns a headline `estimated_cost_usd` — `0.9312` in the reference payload — plus token totals and per-model, per-phase breakdowns. The pitch, made queryable.

## The number is engineered to be too low

When a company finally does surface a cost figure, every pressure pushes it to flatter the product — round down, exclude the overhead, quote the happy path. This endpoint does the opposite on purpose. Its payload carries `is_estimate: true` and a `pricing_basis` note stating that calls on any model *absent from the pricing table count as $0.00 — so the true spend is at or above this figure.* The headline number is deliberately a **lower bound**: untracked usage doesn't get hand-waved, it drops out, and the design says so out loud rather than hiding the omission. In a market where the whole problem is numbers that turn out *larger* than advertised, that is a strange thing to ship — a vendor optimizing for the demo would round the other way.

The second tell is structural. The new `cost_service.py` does not re-derive prices — it reads the *same* aggregation the on-disk summary uses, both routed through one `MODEL_PRICING` table. The JSON surface and the human-readable file are mechanically incapable of disagreeing, because there is only one source of truth. And the route inherits the same publish gate as every other read surface: `403` if the run is private, `404` if no calls are logged yet. You cannot use it to peek at someone else's spend, and it returns nothing it cannot stand behind.

A read-only, single-source, deliberately-underestimated cost figure is not a marketing surface. It is built to be audited by a skeptic — the opposite of how the field treats its pricing.

## What this predicts

A claim specific enough to be wrong on a schedule: as the inference subsidies thin out over the next 18 months and real bills start arriving, the AI tools that hold trust will be the ones that exposed their unit cost as a checkable number *before* anyone forced them to — and the tell will be exactly this plumbing: a per-run cost endpoint, a stated pricing basis, an estimate flagged as an estimate. The products still quoting one clean monthly figure with no way to verify it are running the Copilot-at-$10-costing-$80 trade, and that trade ends when the credits do.

The hidden cost of AI didn't appear because the numbers were hard to compute — every one of these systems knows what a run cost the instant it finishes. It's hidden because exposing it is a choice, and almost nobody makes it. The first engines wiring the real number into a public, auditable, deliberately-conservative endpoint are betting that in a market full of bills you can't see, the scarce good is a price you can check.

---
*Sources:*
- [The Hidden Cost of AI Agents 2026 — AI Empire Media](https://aiempiremedia.com/the-hidden-cost-of-ai-agents-2026/) — average hidden cost $327/month, 1,635% markup over advertised subscription; "$20 becomes $347" framing
- [Agentic AI Cost Runaway: Token Budgets in 2026 — LeanOps](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) — agent-loop token re-sending; 5-step task $0.158 vs $0.049 single call (Claude Sonnet 4.6, 3.2x); >30x at 50 steps, >100x at 200; $4,200-over-a-weekend developer case
- [The Economics of AI-First B2B SaaS in 2026 — Monetizely](https://www.getmonetizely.com/blogs/the-economics-of-ai-first-b2b-saas-in-2026) — inference priced below true cost "propped up by Big Tech"; GitHub Copilot $10 charged vs up to $80 compute
- [MiroShark repository](https://github.com/aaronjmars/MiroShark) — `GET /api/simulation/<id>/cost.json` (PR #179); `run_summary.py` `collect_cost_summary()` + single `MODEL_PRICING` table; `cost_service.py` read-only payload; `is_estimate: true` / `pricing_basis` lower-bound design; `403`/`404` publish gate
