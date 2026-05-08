# There Is No AI Reproducibility Crisis. There's a File-Saving Crisis.

The dominant story about AI reproducibility in 2026 goes like this: large language models are nondeterministic, even with `temperature=0`, even with a fixed seed, even when you call the same endpoint twice in a row. Therefore, the argument continues, scientific use of LLMs is broken until somebody fixes inference. Last November, Thinking Machines Lab published "Defeating Nondeterminism in LLM Inference" and got the framing into the discourse. The NeurIPS 2025 paper *Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference* won an oral slot for showing that batch size, GPU count, and floating-point precision can each shift the same prompt's output. A whole genre of explainer blog posts followed: the "reproducibility crisis" needs FP32 inference, batch-invariant kernels, and bitwise-stable matmul.

It's good work. It also misframes the problem.

## The crisis you can solve at the inference layer is not the crisis most people have

The Thinking Machines team showed they can hit one thousand identical runs with one hundred percent bitwise-identical outputs under dynamic batching, at a 10–40% performance cost. Take that as won. Now ask: what fraction of the AI research, agent, and simulation work happening in 2026 would become reproducible if every model on every API magically produced bitwise-stable outputs tomorrow?

The honest answer is: a small minority. Because the bottleneck isn't model determinism. It's that nobody wrote the inputs down.

Try to reproduce a result from a typical 2026 agent paper or product demo. The model? Often unspecified, or a versioned name like "the production tier in March." The prompt? Maybe in an appendix, maybe truncated. The tools wired to the agent? "We used a search tool and a Python sandbox." The environment seed, the retrieval corpus snapshot, the moderator settings, the evaluation rubric, the agent population's persona distribution? Almost never. A study published in *IJGIS* this year found that even after journals adopted Open Data + FAIR policies, reproducing computational results required active outreach to original authors in the majority of attempted cases — and that was for traditional code-and-data papers, not LLM-driven ones.

Bitwise-deterministic logits don't help if the inputs that produced those logits live only in one engineer's tab history.

## What the reproducibility crisis actually looks like up close

Bench science figured this out decades ago. The reason a 1998 *Nature* paper can be replicated today isn't that 1998 lab equipment was deterministic — it wasn't. It's that the materials, methods, and inputs were written down in a format anyone could read, and the outputs were associated with a stable identifier you could cite. That discipline migrated into computational science as Snakemake and Nextflow workflows, MLflow runs, Weights & Biases configs, FAIR principles' globally unique persistent identifiers, the Software Heritage SWHID system. Every one of these is structurally the same idea: serialize the inputs to a stable file format, hash it, attach the hash to the publication.

This is unglamorous. It is also the only thing that has ever worked.

The agent and simulator side of AI mostly skipped this step. The community went straight from "the model is magic" to "the model is nondeterministic, alas" without pausing on "did we even write the parameters down?" Most agent products in 2026 don't expose the configuration that produced a run as a citable file. You can screenshot the output. You can copy the URL. You can't pin the inputs.

## A small file shipped today as a quiet rebuttal

MiroShark, a multi-agent debate simulator, merged PR #75 a few hours ago. It's called *Reproducibility Config Export*. The whole thing is one new endpoint — `GET /api/simulation/<id>/reproduce.json` — backed by about 370 lines of pure-stdlib Python in `backend/app/services/repro_export.py`. No new dependencies. Twenty-two offline unit tests. The endpoint returns a v1-schema JSON document carrying the scenario text, the agent count, the round count, the platform toggles, the four cadence parameters that govern timing, the director-event injections that steered the run, and a lineage block stating whether this simulation is an original, a fork, or a counterfactual branch off another sim.

Two implementation choices make the whole exercise actually useful, rather than another "we exported some metadata" feature.

The first is a constant called `SCHEMA_VERSION = "1"`, paired with a `REQUIRED_KEYS` frozenset pinned by tests. A future refactor cannot silently drop a field that v1 consumers rely on. If the schema needs to evolve, the version increments and old citations still parse against v1.

The second is a function called `render_json_bytes`. It serializes the blob with `sort_keys=True`, `indent=2`, and a trailing newline. The same simulation, exported twice, produces byte-for-byte identical output. Run `sha256sum` on it. That hash is now a stable citation key. A paper appendix can say "Simulation reproducibility hash 9e3c2a…" and a reader years later, with a different copy of the file, can verify they're looking at the same inputs. This is what FAIR principles call a globally unique, persistent identifier — implemented in roughly fifteen lines of stdlib code.

## What this implies for the next decade of agent work

Agent and simulator output volume is going to outrun the citation infrastructure for it by orders of magnitude. The teams that figure out the boring file-saving discipline first will own the canon. Their runs will end up in papers, in syllabi, in tooling that ingests JSON specs and replays them. Everyone else's outputs will look magical for six months and then become un-citable Slack screenshots.

The reasoning-model arms race captures attention because it sounds like progress. But the compounding move in 2026 is the one nobody's writing thinkpieces about: serialize the inputs, sort the keys, hash the file, attach it to the paper. The crisis was solved before LLMs existed. The question is which projects bother to apply the answer.

---
*Sources:*
- *[Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)* — Thinking Machines Lab, November 2025
- *[Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference](https://arxiv.org/abs/2506.09501)* — NeurIPS 2025 (oral)
- *[Applying the FAIR Principles to computational workflows](https://www.nature.com/articles/s41597-025-04451-9)* — Scientific Data, 2025
- *[The computational reproducibility of articles published under the Open Data + FAIR policy of IJGIS](https://www.tandfonline.com/doi/full/10.1080/13658816.2025.2603586)* — Tandfonline, 2025
- *[MLflow vs Weights & Biases vs Neptune: Experiment Tracking Tools Compared 2026](https://reintech.io/blog/mlflow-vs-weights-and-biases-vs-neptune-experiment-tracking-comparison)* — Reintech, 2026
- MiroShark PR #75 *Reproducibility Config Export* — `backend/app/services/repro_export.py`, merged 2026-05-08
