# Riva research kernel

Riva is the focused scan-time research layer for `vuln-scanner`. It does not
install scanners, send disclosures, open PRs, or manage lifecycle state.

## Research contract

Work on one target commit and one boundary-aligned slice at a time. Treat all
scanner output as candidates, not proof. Do not call a finding confirmed until
the existing triage and PoC-verification contract is satisfied.

## Sequence

1. Describe the system and the selected component.
2. Review relevant security history, prior fixes, open issues, and sibling implementations.
3. State protected assets and the attacker's starting capabilities.
4. State capabilities the attacker does not have and deployment assumptions.
5. Map trust boundaries and the controls that enforce them.
6. Write 3–7 testable invariants for the selected boundary.
7. Trace production entry points to sensitive sinks.
8. Produce candidates only when a constrained attacker can reach a concrete impact.
9. Run the bounded exploration rounds below.
10. Hand surviving candidates to the existing triage, prior-art, and PoC gates.

## Bounded exploration rounds

### Construct

Can the stated attacker violate an invariant through the selected production
entry point? Give the exact source-to-sink path, guards, prerequisites, and
achieved impact.

### Invert

Which default, fallback, type conversion, state transition, or authorization
assumption could be incomplete or inconsistently applied? Attempt to falsify
each assumption with a reachable input.

### Propagate

Search sibling handlers, alternate entry points, older versions, and related
adapters for the same invariant violation. Compare against the safest local or
upstream known-good implementation available.

Stop after two consecutive rounds produce no evidence-backed candidate. Never
use an adversarial assumption as evidence; it is only a hypothesis generator.

## Candidate record

Every serious candidate must include:

- target commit;
- selected slice and production entry point;
- protected asset;
- attacker controls and exclusions;
- invariant violated;
- exact source-to-sink call chain;
- prerequisites and deployment assumptions;
- concrete attacker-achieves impact;
- evidence status: `candidate`, `reproduced`, or `disproved`;
- prior-art result;
- verifier required by the existing scanner policy.

Write the candidate array to `/tmp/vuln-scan/riva-candidates.json` and validate
it with `./scripts/validate-riva-candidates.sh` before handing it to A4. The
validator checks file, line, severity, category, and a concrete claim; a
validation failure means no candidate promotion.

Do not report generic CWE possibilities, unreachable paths, intentional
same-privilege capabilities, or hardening advice as confirmed vulnerabilities.
