# The Trending Sort Was Invented In A Bar In Omaha. Most Software Still Hasn't Caught Up.

Sometime between the end of World War II and 1953, a man named Todd Storz sat in a bar in Omaha with friends and watched the jukebox. The same five or six songs kept playing. He asked a waitress why she kept punching the same buttons. She said: "I like 'em." Then he watched the next waitress, and the next. Same songs. Same answer.

Storz ran a radio station in Omaha called KOWH. Radio at the time worked the way most editorial systems still work: a programmer chose what to broadcast, taste imposed top-down, listeners on the receiving end. The jukebox flipped that picture. The jukebox didn't tell anyone what to play. It played what was paid for, and it counted. It was distribution data exposed as a sort key. And what the waitresses liked turned out to be what most listeners liked too — because the data already knew.

By 1953, KOWH had stopped playing what its programmers thought listeners *should* hear and started playing what the jukebox said they were already paying to hear. Repeat the top sellers more than anything else. Cut the talk. Cut the experimentation. Sort by what got played the most. That sort key became the Top 40 format. Within five years it was the dominant programming style in the United States.

## A Loop Nobody Was Closing Before

The thing that made Top 40 powerful was not the music. It was the fact that it closed a loop. A song that sold well at the record store got played more on the jukebox. Jukebox plays got tallied by Billboard, which had launched its first national sales chart on July 27, 1940 — a 10-position list called "National List of Best Selling Retail Records," polling stores from New York to Los Angeles. Chart numbers told stations what to spin. Spinning it on the radio drove more record sales. And on around the loop. Distribution data fed discovery. Discovery drove more distribution.

Before 1940, no one was running that loop on a national scale for music. Before 1953, no one had wired the loop directly into radio programming. The data existed — record stores knew their bestsellers, jukebox operators knew their top punches — but nobody had connected the metering to the playback. Storz did. The historian Eric Weisbard, in *Top 40 Democracy*, captures the moment plainly: a waitress, asked why she kept playing the same record, said "I like 'em," and Storz watched it happen "time after time." He didn't invent the demand. He noticed it was already being measured, and that nobody was showing it back to the audience.

## The Same Loop, Built In Python This Week

PR #78 on MiroShark, opened May 10, 2026, is that same loop.

MiroShark hosts public economic and policy simulations. People share them. Each share hits one of several "surfaces" — an embed dialog, a `reproduce.json` citation artifact, a `/watch/<id>` page, a counterfactual fork, a lineage panel. PR #74 — which shipped three days earlier on May 7 — added a per-simulation counter called `_serves_total` that increments every time one of those surfaces is served. PR #78 takes that counter and turns it into a sort key. The endpoint is `/explore?sort=trending`. The frontend dropdown calls it "🔥 Trending."

The implementation is small enough to read in a sitting. A new module-level constant, `TRENDING_FIELD = "_serves_total"`, pins the field name so renaming it trips CI. A new `_trending_key(card)` function reads the counter, clamps non-integer or negative inputs to zero, and tie-breaks on `created_at` descending. The route handler sweeps `surface_stats.read_surface_stats(sim_dir)` for every public simulation *only when `sort=trending` is requested* — the default `date` path stays read-free, so the new code costs nothing on the hot path. After the sort, the transient field is stripped from the response, so the public JSON contract is unchanged. Eight offline unit tests pin every load-bearing invariant. Zero new dependencies. Seventeenth consecutive PR in that streak.

## Why "First Loop" Is Doing The Work In That Sentence

The PR's commit message describes the change as "the first feedback loop from distribution analytics back into gallery ranking." That phrase is doing more work than it looks like.

Most software tools — research platforms, document repositories, simulation galleries, B2B SaaS dashboards — sort by date, alphabet, or editorial pin. Some sort by upvotes or stars, but those measure user *intent* (clicked the button), not user *behavior* (consumed the artifact). A trending sort that runs on actual serves is rarer than it should be, because it requires three things to already be in place: a counter on the artifact (PR #74), public surfaces worth counting (the entire share-surface arc since late April — transcript export, RSS, watch pages, gallery search, scenario links, thread export, webhook log, reproduce.json, lineage), and the willingness to expose the counter as a discovery affordance. The third one is where most tools stop. They count, and they show the count to the operator on a dashboard, and they never wire it back into how visitors *find* things.

KOWH did. PR #78 does. The waitress in Omaha already had the answer in 1953. It just took most of the software industry a while to remember that the same loop works on simulations.

## What Compounds From Here

The interesting prediction is not that "trending sort" will become the dominant gallery view on MiroShark — it probably won't, because dates remain the default and most users don't change defaults. The interesting prediction is that once the loop is closed, it stays closed. A simulation that gets shared gets served gets ranked gets seen gets shared. The differential between a popular sim and an unseen one widens, not narrows, with time. That's how Top 40 worked. That's how Billboard's chart positions self-perpetuated. That's how PageRank worked when it shipped in 1998 — counting links to compute rank, then surfacing the rank, then watching links accumulate against the rank.

In each case the technical innovation was small and the structural innovation was large. The technical innovation in PR #78 is one Python file, one constant, one sort key, and a one-week-old counter. The structural innovation is closing a loop that most research tools haven't closed yet — and that took 73 years to come back around from a bar in Omaha.

---
*Sources: [Happy Birthday, Billboard Charts! On July 27, 1940, the First Song Sales Survey Debuted (Billboard)](https://www.billboard.com/pro/happy-birthday-billboard-charts/), [Todd Storz — Wikipedia](https://en.wikipedia.org/wiki/Todd_Storz), [Top 40 Democracy excerpt — Eric Weisbard, University of Chicago Press](https://press.uchicago.edu/books/excerpt/2014/Weisbard_Top_40_Democracy.html), [Todd Storz: Radio for a New Era — Nebraska State Historical Society](https://history.nebraska.gov/todd-storz-radio-for-a-new-era/), MiroShark PR #78 *Trending Simulations Sort* (`backend/app/services/gallery_filters.py`, opened 2026-05-10), MiroShark PR #74 *Surface Usage Analytics* (May 7, 2026).*
