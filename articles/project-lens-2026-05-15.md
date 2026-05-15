# Two Is Coincidence. Three Is The Shape You Didn't Plan.

In 1996, Don Roberts and Ralph Johnson published a paper called *Evolving Frameworks* with a small section labelled "Three Examples." Its claim was that you cannot build a reusable abstraction from one instance of a problem, and you cannot build it from two either. By the third instance the shape is in the room with you whether you sat down to design it or not — and refusing to extract it past that point is its own decision. Three years later, Martin Fowler put a sharper version into *Refactoring*, attributed to Roberts, that almost everyone in software has now heard: "The first time you do something, you just do it. The second time you do something similar, you wince at the duplication but do the duplicate thing anyway. The third time you do something similar, you refactor."

Eight years earlier, in 1988, Ted Biggerstaff had made the same claim about whole systems. His "3-system rule" was that you had to build three production systems in a domain before you had the right to design reusable components for it. Two systems gives you confidence in patterns that turn out to be coincidence. The third is where the abstraction stops being a guess.

## What the rule is actually about

Read carelessly, the rule is about code duplication and DRY. Read carefully, it is something stranger. It is a claim about *epistemology* — about how shape becomes visible. You don't know what you're building until the third one is in the same room as the first two. The first instance is just a thing. The second instance might rhyme with the first by accident. The third instance is where rhyme stops being plausible deniability. The discipline isn't extraction; it is *waiting until you've seen enough to extract honestly*.

Christopher Alexander, who supplied the original word "pattern" to software, was making this point a different way when he wrote that a pattern language "cannot be invented — it must either be discovered in actual use, or adapted to a new situation by methods of trial and error." The thing on the page in the 1996 Roberts–Johnson paper is the same thing as the thing in Alexander's *A Pattern Language* (1977): real abstractions get found, not authored.

## A small worked example, shipped this week

On May 15, 2026, MiroShark — an open-source multi-agent simulator — opened pull request #83: `feat: Discord rich-embed + Slack Block Kit completion notifications`. The PR adds two files to the backend services directory: `discord_notify.py` (~390 lines) and `slack_notify.py` (~370 lines). Both are pure standard library — the twenty-second consecutive zero-new-deps PR on the repo. Each is opt-in via a single environment variable (`DISCORD_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`) and sends a platform-native message when a simulation completes or fails.

By itself that's a feature. What makes it worth writing about is that it's the third one.

The first was `webhook_service`, which has been in the repo for months and POSTs raw JSON to whatever URL the operator configures. The second is `discord_notify`. The third is `slack_notify`. All three now share the same shape: a fire-and-forget dispatch on a daemon thread; a per-process `(simulation_id, status)` deduplication set so a noisy event loop can't double-fire; late-bound reads of the relevant environment variable at dispatch time so config changes don't require a process restart; a graceful no-op when the env var is unset. Nobody sat down to design a *channel notifier interface*. The project built one notifier, then built another, and on the third one the shape stood up and identified itself.

## What got extracted, and what didn't

The shape is the part that's the same. What's different across the three is the part that *should* be different. Each notifier owns its own payload assembly — `webhook_service` ships raw JSON, `discord_notify` builds a rich embed with a 100-character title cap and a four-state consensus colour map, `slack_notify` assembles Block Kit blocks with `mrkdwn` block-bar belief fields like `█████░░░░░ 52.0%`. That divergence isn't a bug; it's the end-to-end argument from Saltzer, Reed, and Clark's 1984 paper — push application-specific knowledge out to where the application lives. MiroShark doesn't render Discord embeds. Discord does. MiroShark hands Discord enough JSON in the shape Discord already understands, and Discord renders the picture.

The pattern that crystallised on instance three is therefore narrow on purpose. It is only the *transport choreography*: dispatch model, dedup key, env-var lifecycle, opt-in semantics. The fourth channel — a Telegram bridge, a Matrix room, an oncall pager — becomes, in the push-recap's own phrasing, "copy-paste." Not because the next module is trivial to *design*, but because the parts that were ever going to be the same are now legible enough to lift.

## The discipline this implies

A lot of software is built in the opposite shape. Someone identifies a future need ("we'll want to send to multiple channels"), writes a notification interface and an abstract base class in week one, and spends the next year discovering the interface was wrong because it was extracted from zero examples. The Roberts–Johnson move is the inverse and slightly painful: accept the wince on instance two, build the duplicate, and extract only on instance three when the *real* common axis is uncomplicated to see. Frameworks built this way tend to outlive frameworks designed up front, because they describe a shape that already worked three times instead of a guess about one that might.

MiroShark's notifier doesn't have a base class. It has three modules that happen to rhyme, and one line in today's push-recap — "channel notifier as reusable shape (3rd instance)" — that reads less like an announcement than a quiet field note. The base class, if it ever shows up, will arrive when channel five forces the issue. By that point everyone in the codebase will already know what it looks like, because they will have written it three more times.

---

*Sources:*
- *[Rule of three (computer programming) — Wikipedia](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))*
- *[Origins of "The Rule of Three" — Eoin Noble (eoinnoble.com)](https://eoinnoble.com/posts/origins-of-the-rule-of-three/)*
- *Roberts & Johnson, "Evolving Frameworks: A Pattern Language for Developing Object-Oriented Frameworks" (1996, PLoP)*
- *Saltzer, Reed, Clark, "[End-to-End Arguments in System Design](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf)" (ACM TOCS, 1984)*
- *Christopher Alexander, [*A Pattern Language*](https://en.wikipedia.org/wiki/A_Pattern_Language) (Oxford University Press, 1977)*
- *[MiroShark PR #83 — feat: Discord rich-embed + Slack Block Kit completion notifications](https://github.com/aaronjmars/MiroShark/pull/83)*
