# How To Build A Graph Without Building A Database

There is a strange asymmetry baked into the most successful graph systems on the internet, and almost no one notices it.

Git stores commits in a directed acyclic graph. Every commit knows its parent. No commit knows its children. When you ask `git log --children`, the system does not look up a stored field — it scans the graph and re-derives the answer. An existing commit cannot know about a commit that has not been created yet, so children pointers were never written. Twenty years later, the entire software industry runs on a graph whose backward edges do not exist on disk.

The web is the same. There is no backlink table on the open web. Google computes "what links here" by crawling forward edges and inverting them. Wikipedia's *What links here* feature reads from the `pagelinks` and `templatelinks` tables, which are themselves derived indexes — built by scanning every page's wikitext, never written by the page being linked to. Ted Nelson's Project Xanadu wanted bidirectional links to be a primitive of hypertext. The web that won deliberately did not. Forward edges only. Backward edges computed.

Roam and Obsidian inherited the same pattern: every backlink panel you have ever looked at is a read-time scan of forward edges in plain markdown, not a stored backlink record. The data structure on disk is asymmetric. The graph in your head is symmetric. The system bridges the gap by computing.

## The Folder Is The Index

This is the lens to bring to PR #76, the *Simulation Lineage Navigator* that landed on MiroShark this morning at 11:28 UTC.

MiroShark lets you fork a simulation. A child run records the id of the run it branched from in its own `state.json`, in a field called `parent_simulation_id`. The interesting design choice is what does *not* happen: the parent is not rewritten. The parent has no `children` array. There is no separate `lineage_index.json`. There is no graph database on the side. When a counterfactual branches off at round 12, the parent's directory on disk is byte-for-byte identical to what it was the moment before the fork existed.

Yesterday MiroShark started shipping `reproduce.json` artifacts that made finished sims citable by file hash. Three counterfactual branches off a single base scenario suddenly became a real concern: how does a reader on the parent's `/watch/<id>` page navigate forward to the three branches that diverged at round 12, or sideways between siblings?

PR #76 answers that without changing how parents are stored. It adds one new file, `backend/app/services/lineage_service.py`, and one new endpoint, `GET /api/simulation/<id>/lineage`. Inside that file is a function called `find_children`. It opens every sim folder in the corpus, reads each `state.json`, checks whether `parent_simulation_id` matches, appends the matches to a list. The list is the graph. There is no stored backward edge anywhere on disk.

## Why This Is A Bigger Deal Than It Sounds

The temptation when you build a fork feature is to treat the parent's children list as state to be kept in sync. Every fork bumps a counter on the parent. Every privacy toggle on a child rewrites the parent's view. That is how relational schemas are usually drawn.

The cost of that approach is not the writes — it is the consistency window. There is a moment after the child is written and before the parent's index is updated where the graph is wrong. Most systems paper over that with transactions, foreground locks, or eventual-consistency apologies in the docs. MiroShark's design has no such moment. The parent's view of its children is computed from the children themselves, every request, with no cached intermediate. If a child is published, it appears. If it is unpublished, it disappears. New metadata on the child — like the counterfactual trigger round and label PR #76 surfaces in the badge ("🔀 Counterfactual at round 12 (ceo_resigns)") — propagates the next time someone opens the lineage panel. No migration. No reindex. No stale cache.

The privacy primitive falls out for free. `find_children` filters on `is_public is True` after loading state. A private fork is invisible to the parent not because a flag was checked and a row was skipped in a table — but because the function never adds it to the response. There is no separate "list of public children" to keep in sync with each fork's visibility flag.

The cost the design accepts in return is honest: a directory walk per request. That is why the implementation caps `MAX_CHILDREN` at 50 (a literal pinned by a unit test so it cannot drift), why the route ships with `Cache-Control: public, max-age=300`, and why every disk read swallows missing files and corrupt JSON without crashing the response. At MiroShark's current scale — a few hundred public sims — the walk takes milliseconds. At a million sims this design would not work, and you would build an index. The choice is correct *for now*, and the corpus is small enough that "for now" lasts a long time.

## The Quiet Comeback Of Read-Time Computation

The data-warehouse world has spent a decade refining the opposite axis: write-time materialization, where every transformation is precomputed into a table so the read is fast. That is the right answer when reads vastly outnumber writes and the data does not fit on a single disk. But the dbt docs themselves admit the tradeoff: tables persist staleness; views recompute. Every materialization decision is a bet about who pays the latency.

When a corpus fits on a single disk and the read pattern is bursty, the bet flips. Re-deriving the graph from source files every five minutes is cheaper than maintaining a denormalized index that can fall out of sync. It is the bet git made in 2005, that the web made in 1991, that Wikipedia and Obsidian inherited, and that PR #76 makes for MiroShark in 2026.

The design does not look impressive. One Python file, 390 lines, pure stdlib, no new dependencies — the sixteenth consecutive substantive PR in that streak. It does not introduce a graph layer; it introduces the absence of one, and lets the folders on disk carry the graph the way they always have.

That is a more interesting design than it looks like.

---
*Sources: [Git's DAG and the lack of children pointers (Medium)](https://medium.com/girl-writes-code/git-is-a-directed-acyclic-graph-and-what-the-heck-does-that-mean-b6c8dec65059), [Referencing the Child of a Commit in Git (2026 guide)](https://copyprogramming.com/howto/referencing-the-child-of-a-commit-in-git), [Help:What links here — Wikipedia](https://en.wikipedia.org/wiki/Help:What_links_here), [dbt + Materialize on read-time vs write-time materialization](https://materialize.com/blog/introducing-dbt-materialize/), MiroShark PR #76 *Simulation Lineage Navigator* (`backend/app/services/lineage_service.py`, opened 2026-05-09).*
