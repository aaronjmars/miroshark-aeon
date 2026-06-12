# Dispatches from the Simulation #5

**Apr 26, 2026** | [https://aaronjmars.substack.com/p/dispatches-from-the-simulation-5](https://aaronjmars.substack.com/p/dispatches-from-the-simulation-5)

---

[

![](https://substackcdn.com/image/fetch/$s_!iAHt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F761a267a-a812-41c3-a6e1-8e06e9cee14d_1280x853.jpeg)

](https://substackcdn.com/image/fetch/$s_!iAHt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F761a267a-a812-41c3-a6e1-8e06e9cee14d_1280x853.jpeg)

#

>

the channel kept circling back to one question this week: who owns the loop. your keystrokes feed someone’s model. an agent spends $500M without asking. a hair dryer wins a weather market. world models just got 3x bigger. the through-line — every system is becoming reflexive, and most people are still pretending it isn’t.

a post mid-week framed it cleanly: *“belief is reality. what is believed by the individual is expressed through them as personal reality, influence on consensus — collective belief in something makes it effectively real.”* ([#2433](https://t.me/hyperstiti0ns/2433)). hyperstition 101. the rest of the week was just examples.

## **your keystrokes are the training set**

>

reuters dropped a story this week: meta is now capturing employee mouse movements and keystrokes for AI training ([#2443](https://t.me/hyperstiti0ns/2443)). the only response in the channel was “wow.” correct response. the data layer has fully collapsed into the training layer. there is no separation anymore between using a tool and being the dataset for the next version of that tool.

this isn’t new. we’ve been training the algorithms with every scroll for fifteen years. what’s new is the explicitness — meta isn’t pretending the keystrokes are for product analytics anymore. they’re for the model. the labor is the corpus.

the counter-stack showed up on the same channel, same week, which is the part that doesn’t get talked about enough. tlsnotary shipped a new “proxy mode” with explicit trust-speed tradeoffs ([#2447](https://t.me/hyperstiti0ns/2447)) — the zkTLS stack is getting more pragmatic instead of more zealous, which is what infra needs to actually ship. open anonymity project dropped oa-chat and oa-desktop with unlinkable inference ([#2455](https://t.me/hyperstiti0ns/2455)). and openai of all people open-sourced a PII detector ([#2456](https://t.me/hyperstiti0ns/2456)) — small thing, but the optics matter when they’re also the ones eating every API call.

the cypherpunk position was correct ten years early and looks correct on time now. without crypto + zk + private inference, total surveillance was inevitable. canada froze trucker bank accounts without trial. china runs social credit. the question was never *if* the surveillance state arrives, it was whether there’d be a parallel rail by then. this week looked like the parallel rail is finally getting built by people who ship instead of people who tweet about it.

## **agents are starting to spend money**

>

@therollupco posted that there’s now $500M in agent-to-agent commerce with no humans involved, 18 months from concept to execution ([#2436](https://t.me/hyperstiti0ns/2436)). the channel reaction: “why is it literally the same scene as tbpn lmao.” correct. but laugh and then look at the number again.

x402 got natively integrated into google. coinbase shipped the http-native micropayment rails. now you have agents paying agents for inference, for data, for tasks — and the throughput just hit half a billion. nobody noticed because the AI conversation is still trapped in “will it take my job” instead of “what economy is forming on top of it.”

openrouter shipped spawn this week — agents on any cloud ([#2464](https://t.me/hyperstiti0ns/2464)). the channel comment was “always early,” and that’s the right read. the picks-and-shovels for the agent economy are landing while everyone’s still arguing about model rankings.

and then the dark side: someone built an authorization-letter generator that bypasses claude’s safeguards ([#2462](https://t.me/hyperstiti0ns/2462)). “lmaooo” was the response, but the deeper point — every guardrail becomes a market. jailbreak generators are just the unauthorized layer of the same agent economy. the moment you have agents transacting with money, the incentive to manipulate them is now a real number, not a hypothetical.

aaron’s own simulation tweet on spacex/cursor acquisition scenarios ([#2444](https://t.me/hyperstiti0ns/2444)) ties back into this — agents reasoning about agents, scenarios about scenarios. the meta-layer just got cheap enough to play with.

## **the hair dryer and the open-source polymarket**

>

a guy pointed a hair dryer at a weather sensor and netted $34,000 from polymarket ([#2449](https://t.me/hyperstiti0ns/2449)). channel comment: “the elon stimmy package this month will be great.” the story went mega-viral — was the all-time peak interaction story for the channel by a wide margin.

this is the funniest possible illustration of the reflexivity problem. polymarket sells itself as “predicting reality.” the hair dryer guy didn’t predict anything. he *manufactured* the temperature reading. for $34K. with a $30 appliance. the gap between “information aggregation mechanism” and “coordination mechanism” is exactly this hair dryer wide.

people will read the story as “lol funny exploit, bug fix coming.” wrong frame. it’s a feature of how oracle-dependent markets work. polymarket is on a deadchain pulling weather data from sensors that can be aimed at by hair dryers — and is *still* one of the most successful consumer products in crypto. the bar is on the floor and they’re winning. the “uniswap moment for prediction markets” is sitting right there waiting for someone to actually ship curation + liquidity instead of yet another permissionless launch.

related and equally interesting: an open-source polymarket terminal shipped this week with a live book and self-custodial trading ([#2448](https://t.me/hyperstiti0ns/2448)). channel response: “cool.” correct again. the closed CLOB on a centralized stack is the weak point. the terminal layer going open is the first crack. polymarket has no composability story. that’s the wedge.

## **world models are not a 2027 thing anymore**

>

odyssey shipped odyssey-2 max this week — 3x larger model, 10x more compute, physics benchmark jumped from 49 to 58 on vbench 2, 120+ seconds of coherent interactive world simulation ([#2442](https://t.me/hyperstiti0ns/2442)). private beta to robotics, gaming, defense, simulation, healthcare partners.

the are.na page tracking world model funding rounds ([#2458](https://t.me/hyperstiti0ns/2458)) tells the same story from the capital side — money is moving fast.

read the application list. defense and robotics are the actual customers. gaming is the demo. the same way generative video went from “neat” in 2023 to a hollywood line item in 2025, world models are now in the “private beta to defense” stage, which historically takes about 18 months to become consumer-grade. coconut simulator ([#2460](https://t.me/hyperstiti0ns/2460)) is the toy version. odyssey-2 max is the unsexy version that will eat the toy version’s lunch.

simulation just stopped being the cheap word people use for “AI video” and started being the actual product. that matters because the whole hyperstition thesis assumes you can run the future before you build it. world models are the hardware for that.

## **quick hits**

- diy genome sequencing on a kitchen table — full tutorial site ([#2434](https://t.me/hyperstiti0ns/2434)). the bio decentralization arc is real and underpriced.
- solomon binding demons with the signet ring as a metaphor for deploying subagents ([#2438](https://t.me/hyperstiti0ns/2438)). the esoteric x AI takes keep landing.
- aave $11.7B in outflows after the rsETH exploit ([#2446](https://t.me/hyperstiti0ns/2446)). $300M hack, $15B vaporized — the structural fragility nobody wants to price in.
- mitsui + hitachi exploring data centers on used boats ([#2440](https://t.me/hyperstiti0ns/2440)). the energy-bottleneck workarounds are getting weirder.
- joe rogan x palmer luckey ([#2441](https://t.me/hyperstiti0ns/2441)). anduril is the most underrated company in tech.
- synthetic aperture radar — see through clouds, smoke, rain, darkness, from orbit ([#2439](https://t.me/hyperstiti0ns/2439)). the surveillance stack keeps quietly upgrading.
- open reward standard ([#2461](https://t.me/hyperstiti0ns/2461)). incentive primitives going protocol-level. worth tracking.

---

>

*sourced from [@hyperstiti0ns](https://t.me/hyperstiti0ns) — 2026-04-19 to 2026-04-26*
