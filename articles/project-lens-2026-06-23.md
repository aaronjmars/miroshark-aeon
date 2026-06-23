# The Most Dangerous AI Failure Mode Isn't in the Model. It's Between the Models.

On June 6, 2026, the US government issued a mandate. Frontier AI models deployed in regulated industries must undergo mandatory red-teaming — adversarial testing — before deployment. The EU follows on August 2 with penalties up to €35 million. [NIST's June 2026 guidance](https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-red-teaming-standards-202603/) requires re-testing within 72 hours when underlying models update, prompts change meaningfully, or new tools or data sources are connected.

The tests are real. The failure mode they miss is also real.

## What Red-Teaming Actually Measures

Isolation is the premise. You probe a model: prompt injection, jailbreaks, data exfiltration, unbounded consumption. The agent gets a clean bill of health. Deployed.

But enterprises aren't deploying one agent. Deloitte's _State of AI in the Enterprise_ projects that [75% of businesses will deploy AI agents by year-end](https://www.raconteur.net/technology/autonomous-ai-agents-2026-the-new-rules-for-business-governance). By December, a midsize company might run dozens of agents handling procurement, finance, HR workflow, and customer response — each making decisions that become the next agent's inputs.

Here's what that looks like when it breaks. A procurement agent flags a vendor anomaly. A finance agent, seeing that flag in its context, escalates a payment hold. An HR agent, seeing the hold status, pauses a headcount request that was waiting on that vendor's contract. Three agents, each behaving exactly as their individual red-team test said they should — together producing an unintentional freeze nobody authorized, that no single agent's log explains.

A [March 2026 survey](https://www.helpnetsecurity.com/2026/03/03/enterprise-ai-agent-security-2026/) found that 80% of organizations had already encountered risky agent behaviors: unauthorized system access, improper data exposure. More telling: only 21% had complete visibility into what their agents were doing, what permissions they held, what tools they were using. These aren't model failures. The models passed their tests. They're interaction failures — cascades that emerge only when agents operate in a network, treating each other's outputs as trusted inputs, errors compounding at a speed no audit catches in time.

Red-teaming tells you what one agent does wrong. It says nothing about what happens when a hundred of them work together.

## The Architecture That Tests the Network

This is the gap that multi-agent simulation fills — and the reason the simulation layer is more operationally interesting than it looks from the outside.

MiroShark's `backend/wonderwall/` implements the interaction layer that red-teaming structurally cannot reach. Agents don't just respond to a prompt in isolation. They produce output into a shared environment, see what other agents produced, and update their internal states before the next round starts. The substrate is `social_agent/`, built on the CAMEL multi-agent framework — originally designed for research on how agent behavior in isolation differs from agent behavior in a network. The research finding that motivated the architecture: it differs significantly, and not in ways you can predict from isolated testing.

The `suggest_scenarios` endpoint operationalizes this. Drop in a real scenario — a procurement policy change, a regulatory update, a supply chain disruption — and watch what the network does across rounds. Not what one agent does with the input. What the propagation looks like. Which agents amplify the signal, which dampen it, where the cascade stops or doesn't.

`director_mode` goes further. Inject a new event mid-run — a contradictory data source, a market shock — after the agents have already been operating for an hour. That's the failure condition isolated testing can't reach by definition. You find out about it in production, days after the bad output has propagated through four downstream systems.

Commit `cef787b`, shipping this month, added a CLI cost subcommand that surfaces the per-run USD estimate. The full multi-agent run — hundreds of agents across multiple rounds, interaction passes included — comes out around a dollar.

## What the Next Requirement Will Be

The testing regime will keep expanding. The EU's August enforcement wave already includes decision-transparency requirements for high-risk AI systems. When a network of agents makes an error that costs something measurable — a patient misrouted, a financial cascade attributed nowhere, an HR decision that fails an audit — the post-mortem will ask: was the interaction tested? Not the model. The chain.

By 2028, expect mandatory multi-agent interaction testing standards in regulated industries. The categories are predictable: financial agents making interdependent decisions on shared data, healthcare agents routing patient information across systems, HR agents filtering candidates through networked criteria. These are exactly the failure patterns that 80% of organizations are already encountering — and that current testing requirements don't cover.

When that standard arrives, the infrastructure for running the test at a dollar per run rather than a hundred thousand per engagement will determine who actually stress-tests versus who certifies a single agent and calls the network compliant.

Governments just mandated testing the thing that was easiest to specify: what a model does alone. The second mandate will cover what models do together — and that's where the damage is already happening.

---

*Sources:*
- [Enterprise AI Agent Security 2026](https://www.helpnetsecurity.com/2026/03/03/enterprise-ai-agent-security-2026/) — HelpNetSecurity; 80% of organizations reporting risky agent behaviors; only 21% with complete visibility into agent permissions and tool usage
- [Autonomous AI Agents: The New Rules for Business Governance](https://www.raconteur.net/technology/autonomous-ai-agents-2026-the-new-rules-for-business-governance) — Raconteur; 75% enterprise AI agent deployment projected by end of 2026; compounding failure patterns and decision opacity
- [NIST AI Agent Red-Teaming Standards 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-red-teaming-standards-202603/) — Cloud Security Alliance / NIST; mandatory 72-hour re-testing requirements; attack categories including unbounded consumption and excessive agency
- [MiroShark — aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark) — wonderwall/ multi-agent interaction layer; social_agent/ CAMEL substrate; suggest_scenarios endpoint; director_mode; commit cef787b (CLI cost subcommand)
