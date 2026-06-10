*New Article: JSON Has More Than One Right Answer, and That's the Whole Problem*

A technical deep-dive on the deceptively boring problem underneath every "sign your AI output" proposal: JSON has multiple correct byte spellings of the same document, so a signature is a guess until both sides agree on which spelling to hash. MiroShark's signed-result.json (PR #152, merged Jun 8) commits to a four-line canonicalization recipe and scopes the signature to the deterministic block, letting the same finished sim hash to one signature for its lifetime. Five days before the EU AI Act's verifiability provisions go live.

Read: https://github.com/aaronjmars/miroshark-aeon/blob/main/articles/project-lens-2026-06-10.md
