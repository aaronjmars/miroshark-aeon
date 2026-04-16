*Feature Built — 2026-04-16*

Mid-Simulation Event Injection (Director Mode)
MiroShark simulations now have a Director Mode — a live control panel that lets users inject breaking events into running simulations. During any active run, click the ⚡ Director button, type a one-sentence event like "Central bank unexpectedly raised rates by 100bps," and every agent in the simulation receives it as breaking context before their next round of actions. Agents react naturally — shifting stances, changing what they post about, altering trading behavior — all visible in real time.

Why this matters:
Until now, every MiroShark simulation ran on a single track: agents reacted to the uploaded document over N rounds with no external disruption. But the most valuable research question is about perturbation — "what happens to this debate when breaking news drops at round 5?" Director Mode is the experimental control primitive that computational social science papers need. OASIS, SOTOPIA, and Park et al. all include stimulus injection as a core mechanism. MiroShark now has it too, making it viable for serious research applications — not just demos. This was the #1 idea from repo-actions and the clearest differentiator from every other multi-agent simulation tool.

What was built:
- backend/scripts/director_events.py: New file-based event queue with atomic writes (temp file + rename). Stores pending events, tracks injection history, enforces max 3 events per simulation. Uses the same marker-replace pattern as cross-platform digests to inject events into agent system messages.
- backend/scripts/run_parallel_simulation.py: Both Twitter and Reddit simulation loops now check for pending director events at each round boundary. When found, events are injected into every active agent's system message as "BREAKING: {event}" before the round executes.
- backend/app/api/simulation.py: Two new endpoints — POST /director/inject (validates running state, enforces 3-event cap) and GET /director/events (returns full history + pending queue).
- frontend/src/components/Step3Simulation.vue: Director Mode button (amber, visible only while running), injection panel with textarea and char counter, event history cards with round numbers, pending event display, and horizontal event banners in the timeline feed.
- frontend/src/components/BeliefDriftChart.vue: Amber dashed vertical lines at injection rounds with ⚡ markers, visually marking exactly when external shocks hit the simulation.

How it works:
Events are queued via a file-based mechanism — the Flask API writes to director_events.json in the simulation directory, and the simulation subprocess reads and consumes them at each round boundary (between context injection and env.step()). This avoids IPC complexity since the event only needs to land between rounds, not mid-round. The injection uses the same marker-replace pattern already proven by cross-platform digests and market context: append a "# BREAKING EVENT" section to each agent's system message, which the LLM processes as new information when generating the next action. Events persist in a history file for the belief drift chart to render injection markers and for the article generator to reference in post-simulation analysis.

What's next:
Checkpoint & Resume (repo-actions #3) would pair naturally — users could inject an event, observe the result over 5 rounds, then fork from the pre-injection checkpoint to compare with and without the disruption. The article generator could also auto-include injection events as a "Methodology: External Stimuli" section.

PR: https://github.com/aaronjmars/MiroShark/pull/31
