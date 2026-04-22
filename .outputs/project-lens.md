*New Article: The Simulator as Flight Recorder: Why Saving the Run Matters More Than Running It*

Flight recorders, event-sourced core banking, and MiroShark share one quiet architectural move: write down the full trace, derive the views later. The article traces that principle from 2026 regulations mandating 25-hour black-box capture and Axon/EventStoreDB's production rollouts at Barclays/Standard Chartered/Société Générale down to MiroShark's file-per-simulation layout — where `trajectory.json` turns Counterfactual Explorer (PR #37) and the Demographic Breakdown (PR #35) into near-instant data transforms rather than reruns, and a single shared `_build_embed_summary_payload()` lets yesterday's Social Share Card (PR #42) and the embed API read one source of truth. The lesson: the interesting architectures save more than they need at the moment they write it down.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-04-22.md
