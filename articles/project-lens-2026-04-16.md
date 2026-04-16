# Every Simulation Needs Someone Willing to Break It

In June 1983, more than 200 senior military and government officials gathered for a war game called Proud Prophet. The Secretary of Defense and the Chairman of the Joint Chiefs participated — a first for a U.S. simulation exercise. The scenario tested a core assumption of Reagan-era nuclear strategy: that a limited nuclear strike could compel the Soviet Union to back down without triggering full escalation.

The simulation broke that assumption in seven days. Rather than capitulating, the Red Team interpreted American strikes as existential threats and escalated without restraint. By day seven, every major city in Germany and Poland had been destroyed, along with Paris, London, Amsterdam, and Brussels. The estimated toll: half a billion dead. The exercise didn't predict the future — it stress-tested a belief, and the belief failed catastrophically. Reagan's advisors spent years afterward revamping U.S. war plans, abandoning the notion that nuclear conflict could be managed.

The lesson wasn't about nuclear policy. It was about what happens when you inject the unexpected into a model and force it to respond honestly.

## The Umpire's Lineage

This technique is older than computers. In 1824, Lieutenant Georg Leopold von Reiswitz presented Kriegsspiel to the Prussian court — a tabletop war game using topographical maps, dice, and color-coded armies. The key innovation wasn't the map or the rules. It was the umpire: an official who controlled information flow between opposing sides, enforced the fog of war, and could introduce surprise attacks and friction at will. Players submitted orders blind; the umpire decided what they could see and what hit them next.

Prussia adopted Kriegsspiel across every regiment. When Prussia defeated France in 1870 — despite no significant advantage in weapons, numbers, or training — many historians credited the war-gaming culture that had trained an entire officer corps to make decisions under uncertainty, with an umpire constantly disrupting their plans.

Two centuries later, the technique is standard practice under a different name: tabletop exercises. CISA, the IMF, and cybersecurity firms all run structured simulations where a facilitator introduces "injects" — pre-scripted disruptions that force participants to react in real time. A data exfiltration in round two. A regulator inquiry in round four. A ransom demand in round six. The facilitator's job, as one practitioner puts it, is to create "healthy tension and realism" by challenging assumptions and pushing participants into uncomfortable but realistic decision territory. The inject is the point. Without it, the exercise is rehearsal. With it, the exercise is discovery.

## The Director Enters the Simulation

MiroShark, an open-source multi-agent simulation engine at 698 GitHub stars, just shipped a feature that puts this two-century-old technique into a software interface.

Director Mode, merged this week as PR #31, lets users inject breaking events into running simulations. Type "Central bank raised rates by 100bps" or "CEO arrested for fraud" into the Director panel, and every agent in the simulation — hundreds of AI personas reacting across simulated Twitter, Reddit, and Polymarket — receives the event at the next round boundary. Their posts, trades, and stance shifts all incorporate the disruption. The belief drift chart marks injection points with amber dashed lines, so researchers can see exactly when the perturbation hit and how the population responded.

The implementation is deliberately constrained. A file-based event queue handles injection with atomic writes. Events are consumed at round boundaries, not mid-turn, preserving simulation integrity. A cap of three events per simulation prevents abuse. The architecture is six files and 724 lines of code — small enough to audit, powerful enough to transform what the tool can do.

Before Director Mode, MiroShark ran single-track simulations: upload a document, generate agents, watch them react. The output was valuable but static — a single timeline of a single scenario. After Director Mode, a researcher can fork the timeline mid-stream. Run the same simulation twice: once clean, once with a market crash injected at round four. Compare the belief drift charts. See which agents held conviction and which flipped. The simulation becomes an experiment, not just a forecast.

## Why the Disruption Is the Product

The pattern across two centuries is consistent: the value of a simulation is not in its baseline run. It's in the moment someone breaks it.

Kriegsspiel's umpire didn't make the game more entertaining — he made it useful. Proud Prophet didn't validate Reagan's strategy — it demolished it, and that demolition changed policy. Tabletop exercise facilitators don't run smooth scenarios — they inject complications specifically to expose gaps that comfortable rehearsal would never reveal.

MiroShark's Director Mode sits in that lineage. The feature is small — a panel, an API endpoint, a queue. But it converts the tool from a simulation engine into a perturbation-research instrument. The question it lets you ask isn't "what will happen?" but "what happens if this happens?" — and that second question, as Proud Prophet's 200 participants learned in 1983, is almost always the one that matters.

In a landscape where most AI agent tools are racing to automate execution, the more interesting engineering might be happening in the tools that let you stress-test ideas before they touch the real world. The umpire's power — the ability to inject the unexpected and watch what breaks — turns out to be as relevant to AI-driven simulation as it was to a Prussian tabletop in 1824.

---
*Sources: [Kriegsspiel: How a 19th Century War Game Changed History](https://militaryhistorynow.com/2019/04/19/kriegsspiel-how-a-19th-century-war-game-changed-history/) · [Proud Prophet War Game (Wikipedia)](https://en.wikipedia.org/wiki/Proud_Prophet) · [The Ultimate Guide to a Cyber Tabletop Exercise in 2026](https://www.cm-alliance.com/cybersecurity-blog/the-ultimate-guide-to-a-cyber-tabletop-exercise-in-2026) · [Brief History of Military Gaming (Central Florida Tech Grove)](https://centralfloridatechgrove.org/brief-history-of-military-gaming-how-simulations-shaped-modern-combat-training/) · [aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)*
