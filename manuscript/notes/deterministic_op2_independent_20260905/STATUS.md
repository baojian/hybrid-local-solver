# Direction status: deterministic_op2_independent_20260905

Last reviewed: 2026-09-06
State: proved-open

## Exact question and contract

- **Question:** Can deterministic local RPPR attain the accelerated bound in Conjecture 2?
- **Model:** Finite connected simple unit-weight undirected graph, point seed, exact-real algebraic words.
- **Accuracy namespace:** `eps_obj` is additive objective gap; `rho` is regularization. They are distinct from degree-normalized PPR error.
- **Access and charged work:** Scalar arithmetic/comparisons, state reads/writes, every first/repeated adjacency entry, degrees, boundary handling, certificates, and output. No free preprocessing, support oracle, or inverse primitive.
- **Intended result:** Safe output `0 <= x_hat <= x_rho_star`, objective gap at most `eps_obj`, support volume at most `1/rho`, fully charged `Otilde(1/(rho sqrt(alpha)))` work in the nontrivial regime; add one for unrestricted `rho`.

## Claim ledger

- **Source:** Authorized `problem_definitions/main.tex`; standard Nesterov acceleration. AESP and Catalyst are later comparison sources, not proof premises.
- **Proved here:** The archived full proof establishes the theorem, diffuse-source continuation, two-energy control, repeated-volume bound, exact reporter, certified repair, and separately stated bounded-integer refinements. Internal audits found no remaining gap.
- **Conditional:** Ordinary floating-point execution does not inherit the exact-arithmetic guarantee without a separate stability proof. No conditional lemma is used to close the archived exact-real theorem.
- **Measured:** The fixed 183-case exact manifest, backend comparisons, component/prefix checks, and small timing studies are archived. Repeated backend runs are not distinct graph instances.
- **Refuted:** Earlier unsuccessful local arguments and corrected attempts remain in the research record. Their status is governed by later audits and the final proof; no universal impossibility claim follows from an unsuccessful route.
- **Open:** External peer review, formal verification, certified floating-point execution, and large-scale matched-accuracy performance studies.

## Central blocker

No remaining proof gap was identified by the internal audits for the stated
exact-real theorem. The next falsifiable target is an external line-by-line
review of the projection sector inequality and cumulative selected-flow bound.
Publication-level priority and production-performance claims remain separate.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `problem_definitions`.
- **Source/shared prerequisites:** Shared mathematical conventions and the point-seed exact-real computational model.
- **Context/provenance:** Developed independently in `Prove conjecture 2 deterministically`. The other task `Prove deterministic Conjecture 2` later reused and audited the core argument. It is not an imported lemma provider.
- **Supplies to:** Original proof and TeX, portable exact solver and wheel, validation and benchmark runners, two-energy/locality lemmas, failure records, and complete artifact hashes.

## Resume here

Read `main.tex` and `sections/` for the integrated overview. Extract the final
portable bundle outside `manuscript/notes`; follow its `START_HERE.md` and
`proof_to_implementation_map.md`. In the original proof, begin at labels
`lem:comparison`, `lem:sector`, `eq:response`, `eq:work`, and `lem:repair`.
Do not replace the proof with this status summary or with numerical tests.

## Verification

The original proof compiled to 20 pages and passed internal proof, model,
arithmetic, implementation, and visual audits. The portable 108-file archive
passed hash, extraction, link, and runner checks. `COMPLETION.json` records more
than ten active research hours. Fresh repository-integration checks are recorded
in `VERIFICATION.md`; original numerical results are preserved without rerunning
unrelated experiments or modifying their reported values.
