# The remaining weighted-constructor review

**Status: Conditional.** This is a concrete next review task for the
supplied solver, separate from local graph discovery. It does not promote
the constructor hypothesis to an unconditional theorem.

The target contract is stated in `sections/op3_supplied_recursion.tex`:
for the actual positive weights encountered recursively, construct a
rooted forest/core preconditioner with the stated spectral quality, core
size, charged work and requested failure probability. Our edge-floor
wrapper, range induction and numerical recursion are already separate
proved drafts; they do not establish the constructor contract by themselves.

## Source map and remaining checks

1. **Low-stretch tree.** The checked Abraham–Neiman arbitrary-positive-weight
   extension supplies the appropriate candidate primitive. Track its input
   and work model explicitly instead of citing only CPW's restricted
   top-level lemma.
2. **Forest decomposition and routing.** CPW Sections 5.4–5.6, Algorithms
   4–5 and Lemmas 5.8–5.12 give the structural route. Rewrite the actual
   weighted decomposition, congestion sums, minimum-edge selection and
   routing bounds as a complete contract. Include singleton cores,
   one-piece decompositions, choice of roots, all copies and parallel-edge
   aggregation. These edge cases are review obligations, not asserted
   counterexamples to the construction.
3. **Core sparsification and confidence.** The checked Koutis–Levin–Peng
   general weighted primitive and the new median/Chernoff wrapper address
   fixed accuracy and confidence. Record which random calls are independent,
   charge all estimate vectors and sampling buffers, and apply the proved
   abort guard before allocating samples for invalid score vectors.

Only after these pieces are reconciled should the full supplied recurrence
lose its Conditional label. Even that would leave the local envelope or
cumulative boundary-event problem open.

## A source display mismatch to handle explicitly

CPW arXiv:2105.14629v2, **Claim 5.14, PDF p.28**, was re-read and visually
checked during the final review. Its displayed two-case condition reverses
the cases used in the proof below it. The no-additional-length case applies
when the deleted edge is **absent** from the original routed tree path.
When it is present, routing toward the retained root can add tree length.
The proof's cases and the subsequent sum over affected edges in equation
(5), PDF p.29, are consistent with this reading.

A small geometry check makes the distinction explicit. On a unit path
numbered 0 through 10, retain roots 0 and 10 and delete edge (4,5).
The original edge (4,5) has tree stretch one. Its canonical rerouting
uses the path from 4 to root 0, of length four, inside the left component.
Thus its local stretch there is four, contradicting the displayed
no-additional-length bound for a deleted edge lying in the original path.
The proof's additional-length case allows it. The piece can be embedded
between two adjacent pieces if shared boundary vertices are required.

This is a mismatch in the displayed claim, not a refutation of the source's
final spectral theorem. It joins the previously recorded Lemma 5.8 display
and Lift constant issues as a reason to verify the full argument rather
than transplant isolated displays.

Primary source: [CPW version 2](https://arxiv.org/pdf/2105.14629v2).
The paper metadata and other checked sources are in
`docs/literature/lcp-solvers.md`; no downloaded PDF is added to the repository.
