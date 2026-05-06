*Repo Action Ideas — 2026-05-06*
Generated from analysis of MiroShark — ideas for autonomous implementation by the feature skill.

1. Simulation Config Export + Reproducibility Badge (DX/Research, Small)
   Complete config.json export + import that makes any MiroShark run reproducible — scenario, model config, agent count, rounds, all params; the primitive academic and quant audiences need before they can cite the tool seriously.

2. Python Client SDK via openapi-generator CI (Integration/DX, Small)
   CI job turns the existing OpenAPI spec into a generated Python client, published as a GitHub Release asset — closes the Jupyter-notebook / quant-pipeline gap without writing SDK code.

3. Director Event Timeline Overlay on Belief Chart (Feature, Small)
   Annotates the belief chart with vertical markers at director-mode injection points ("Liquidity Crisis — Round 15"), turning the raw belief curve into a causal narrative.

4. Share Surface Usage Analytics (DX/Feature, Small)
   One atomic counter per serve_* handler, one read endpoint — tells operators how many times each surface was used (share card vs RSS vs thread) for the first time.

5. Comparative Run View (Feature/Research, Small)
   /compare?a=<id>&b=<id> renders two published sims side-by-side with stance delta — pure frontend, uses existing embed-summary endpoint, zero new backend code.

Full details: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/repo-actions-2026-05-06.md
