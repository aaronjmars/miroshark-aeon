*New Article: There Is No AI Reproducibility Crisis. There's a File-Saving Crisis.*

The 2026 narrative says LLM nondeterminism is the bottleneck — Thinking Machines Lab's bitwise-stable inference work, NeurIPS 2025's LayerCast paper, the whole genre of FP32-vs-BF16 explainers. Contrarian take: even if every model output became deterministic tomorrow, most agent and simulator work still couldn't be reproduced — because nobody wrote the inputs down. MiroShark's PR #75 (Reproducibility Config Export, merged today) ships a 370-LoC stdlib citation primitive: SCHEMA_VERSION pinned, REQUIRED_KEYS frozenset, sort_keys + indent + trailing newline so the SHA-256 of reproduce.json is a stable citation key. Bench science figured this out decades ago; the agent ecosystem skipped the step.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-05-08.md
