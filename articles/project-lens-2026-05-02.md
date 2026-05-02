# Before Radio: 70,000 People Who Watched a Wooden Board Pretend to Play Baseball

On October 14, 1911, the New York Giants were 100 miles away in Philadelphia playing Game 1 of the World Series at Shibe Park. Thirty-eight thousand people were in the stadium. Seventy thousand were in Herald Square, on a Manhattan sidewalk, watching a wooden board.

The board was called a Playograph. A painted diamond with pegs for fielders and a baseball strung on wires. Two operators stood behind it. A telegraph operator in the back read updates off Western Union and called them out. The Playograph operators moved the ball — *fastball directly toward home, curveball with a sharp twist at the end* — and an announcer called the play through a megaphone. The Evening Telegram counted the crowd. Almost twice as many people watched the board as watched the actual game. Some had paid fifty cents to be there.

This pattern repeated every World Series for sixteen years. Times Square, Herald Square, Park Row. Bulletins called the Star Ball Player, Nokes Electrascore, Bowman's Playograph. Edward Van Zile patented one in 1888. Frank Chapman built a 1895 model with three-foot marionette players and an umpire who waved his arms. By 1912, electric bulbs marked stolen bases and home runs, and Times Square was packed so densely the police had to close the streetcar tracks. Then radio arrived in the 1920s, television in 1939, and the wooden boards were obsolete.

You could read this as a stopgap before the real thing showed up. That reading misses what the Playograph actually was. It wasn't a poor substitute for radio. It was a separate medium with its own logic, solving a specific problem: **how do you let many people watch the same thing happen, together, while it is happening, when the thing itself is somewhere else and the only data you have is a thin event stream?**

That problem is older than baseball, and it hasn't gone away. It just keeps finding new substrates.

## What the wire actually carried

The thing modern eyes miss is how *little* the telegraph carried. Western Union sent score updates "every half inning" to subscribing venues. Some operators got pitch-by-pitch but most got something closer to: *Bottom 7th, Mathewson struck out Collins, runner stranded at second.* That was the entire payload. The cheer, the wind, the crowd noise, the tension between pitches — all of it was generated locally, in real time, by the operators, from imagination. Ronald Reagan would later make a career of this on radio for the Cubs out of WHO Des Moines, embellishing wire reports with weather and crowd reactions he invented on the spot.

The architecture was strict. The wire didn't know it was driving a board. The board would have worked just as well if a different feed — a runner from a press box, a pigeon from Brooklyn — had brought the same updates. The wire's job was the data. The board's job was to make the data legible *as motion in real time* and to hold the attention of a crowd until the game ended. Two distinct surfaces, one event source.

## A live spectator page in 2026

Last week, MiroShark — an open-source agent-based simulator that runs LLM-driven agents through 30–40 rounds of opinion exchange about a scenario, then publishes the run — added a page called `/watch/<id>`. A typical run takes about seven minutes.

The watch page is what a spectator looks at *while the run is happening*. A pulsing live badge. Three belief bars — bullish, neutral, bearish — that slide as the rounds advance. A round counter (`Round 14 / 30`). A vanilla-JavaScript poller that hits two existing REST endpoints every fifteen seconds and updates the bars in place. When the run reaches a terminal state, the badge changes to "done" and two CTAs appear: open the full simulation, or fork the scenario to run your own. A tweet of the URL auto-unfurls into a 1200×630 social card with current state baked in (`Round 14/30 · Bullish 47% · Neutral 22% · Bearish 31% — watch live.`) and clicks through to a page that *keeps moving*.

The page is, architecturally, the Playograph. The wire is the simulator's existing event endpoints (`/api/simulation/<id>/embed-summary` and `/run-status`). The surface is a separate, self-contained HTML document built specifically for live spectating. The polling cadence is the same fifteen-second cadence the early electric scoreboards reached when telegraph operators got sophisticated.

## Why a separate surface is the entire point

The simulator already had six other surfaces — a public gallery card, a static share image, an animated GIF replay, a transcript export, an RSS feed, a CSV trajectory dump. All six describe a *finished* simulation. The watch page is the seventh and the only one architected for live consumption.

A modern product instinct would ask: why not just embed the live state in the existing simulation page? The answer is the same one the New York newspapers worked out in 1911. The full simulation page is a control surface — chrome for editing scenarios, configuring agents, inspecting individual posts, downloading artifacts. It is built for an operator. The Playograph wasn't a stripped-down Shibe Park. It was a different artifact for a different audience: the spectator, who is not the operator and never will be, who wants to be there *now* and has fifteen seconds of attention. That audience needs its own page, with its own pacing, its own copy. Conflating the live page with the operator page would have been the same category error newspapers would have made if they'd pointed Herald Square at Shibe Park's scorecard ledger.

The key engineering discipline in the watch page is a constant called `STANCE_THRESHOLD = 0.2`. Every other surface — share card, gallery, GIF, transcript, RSS, CSV — uses the same number to bucket agent positions into bullish, neutral, bearish. A viewer who sees the share card on Twitter, clicks to the watch page, then later opens the gallery never sees the numbers shift. One threshold. One folder of artifacts on disk. Seven ways to look at it. The 1911 Playograph operators had the same discipline by necessity: their score had to match the score Western Union was sending to the rival board across the street, or the audience would notice and dissolve.

## The shape that keeps coming back

Every generation builds a Playograph. Teletype tickers in brokerage houses. The newspaper window in 1936 with election returns chalked on butcher paper and a crowd outside. ESPN's GameCast in the 2000s — the little animated diamond updating every pitch from a satellite-delayed feed. Pump.fun's bonding-curve page where holders watch a token mature in real time without owning the contract. Twitch, which is the Playograph with the wire fat enough to carry video.

The shape, every time: an event happening somewhere; a thin signal extracted from it; a presentation surface built specifically for live group watching; an audience that *prefers* the surface to the source because the surface is faster, shareable, public, and shaped for watching rather than doing.

Software for autonomous agents has reached the point in its lifecycle where the operator dashboard exists, the artifact is exportable, the API is documented, the gallery is browseable — and the thing missing is the broadcast. The artifact is the game. The dashboard is the press box. The gallery is the box score. The watch page is the wooden board in Herald Square at three in the afternoon, with the police closing traffic and 70,000 people leaning in to see how it ends.

---
*Sources:*
- [Playograph — Wikipedia](https://en.wikipedia.org/wiki/Playograph)
- [How Fans Followed Baseball Games Before TV or Radio — Mental Floss](https://www.mentalfloss.com/article/56804/how-fans-followed-baseball-games-tv-or-radio)
- [100 Years of Scoreboard Watching — Mental Floss](https://mentalfloss.com/article/24976/100-years-scoreboard-watching)
- [Re-creating Our National Pastime — Connecticut History](https://connecticuthistory.org/re-creating-our-national-pastime/)
- [Listening to the World Series in Times Square — Ephemeral New York](https://ephemeralnewyork.wordpress.com/2009/10/06/listening-to-the-world-series-in-times-square/)
