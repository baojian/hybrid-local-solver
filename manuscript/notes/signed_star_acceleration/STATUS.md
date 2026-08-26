# Direction status: signed_star_acceleration

Last reviewed: 2026-08-27
State: proved-open

## Exact question and contract

- **Question:** On the center-seeded star, does allowing signed local
  relaxation yield a genuinely proved accelerated algorithm, and which
  familiar local-acceleration mechanisms fail under neighboring models?
- **Model:** The shared undirected PPR system, specialized to
  `K_{1,m}` with a center seed and `m = floor(1 / (8 eps_ppr))`.
- **Accuracy namespace:** Semantic error
  `max_i |pi_hat_i - pi_i| / d_i <= eps_ppr`.  The FISTA and ASPR comparisons
  are separately labeled as RPPR objective-gap statements.
- **Access and charged work:** An adjacency scan or coordinate relaxation at
  `u` costs `d_u`; repetitions and final output writes are charged.  The SOR
  theorem is a promised-star special case and includes an additive `m + 1`
  output charge.
- **Support evolution and primitive:** Fixed full-star support after the first
  leaf block; signed one-coordinate SOR with `0 < omega < 2`.
- **Intended result:** Close the exact star rung and use it as a diagnostic,
  without promoting it to a graph-uniform solver theorem.

## Claim ledger

- **Source:** The PPR/RPPR formulations and accuracy namespaces come from the
  shared problem definition.  The leaf-star FISTA obstruction is source claim
  `CARP-PROP-02` of Fountoulakis--Martínez-Rubio (2026).  The ASPR path result
  and literal AESP--LocGD star result are imported from their proof-owning
  sibling notes.
- **Proved here:** The exact block recurrence, exact semantic-error identity,
  and predetermined-stop SOR upper bound give
  `O(1 / (sqrt(alpha) eps_ppr))` work.  An energy/fast-mode argument gives the
  matching lower bound for every dissipative signed one-coordinate relaxation.
  For `0 < alpha <= 1/16`, a separate deficit argument gives
  `Omega(1 / (alpha eps_ppr))` for the nonnegative-residual one-hop class.
- **Conditional:** The graph-design lessons require a way to replace the
  star’s exact two-mode cancellation on changing general-graph supports.
- **Measured:** None of the main theorems is inferred from measurement.  The
  included verifier checks the star identities in exact rational arithmetic.
- **Refuted:** A residual-certificate block count is not the semantic
  complexity of optimal SOR on the star; it adds a spurious
  `log(1 / alpha)`.  Small optimal support alone does not guarantee FISTA
  locality, and safe nested supports alone do not prevent repeated-prefix
  work.
- **Open:** A graph-uniform support/work ledger, a locally checkable semantic
  stopping interface beyond the star, and safe transfer of signed acceleration
  across changing faces.

## Central blocker

The star proof uses that the entire error lies in two explicitly known modes
and that their semantic combination cancels the critically damped `k` factor.
On a changing general-graph face there is no proved local observable that
reproduces this cancellation while controlling exploration and reset work.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `aspr23_bound_audit`,
  `aesp_locgd_star_lower_bound`.
- **Context/provenance:** The live Fable class-separation draft motivated the
  signed-class question, but this note rederives its star lower bound and does
  not import that unregistered draft as proof authority.
- **Reusable outputs:** Exact star semantic-error formula, predetermined SOR
  stopping schedule, signed-class lower bound, monotone-class lower bound, and
  a taxonomy separating rate, locality, certificate, and restart failures.

## Resume here

- **Exact pointer:** `sec:signed-star-semantic-upper` for the new upper bound;
  `sec:signed-star-general-lessons` for the generalization boundary.
- **Next action:** Seek a fixed-face spectral decomposition whose high-mode
  contribution can be charged locally and whose low-mode semantic component
  admits an observable stopping surrogate.
- **Stop/go test:** Continue only if the proposed observable controls both
  semantic error and charged transient support; stop if it merely reuses a
  sufficient residual certificate and restores the logarithm.

## Verification

- **Focused checks:** `make` produced a 20-page PDF with no undefined
  references or citations; all pages were rendered and visually inspected.
  `python3 verify_star.py` passed 28 exact-rational parameter cells.  Focused
  Ruff checking of `verify_star.py` passed.
- **Repository checks:** `make note-audit`, `make agent-audit`, the explicit
  branch-scope audit, and all 210 tests passed on 2026-08-27.  Repository-wide
  `make lint` remains red on 1,345 pre-existing Ruff findings in checked-in
  `manuscript/claude-overnight-2026-08-24/` scripts; no reported finding is in
  this note or its verifier.
- **Known gaps:** The FISTA theorem’s ISTA comparison imports its cited
  support-containment and linear-rate facts; its FISTA activation half is
  proved in the source.  No accuracy conversion from RPPR objective gap to
  `eps_ppr` is asserted.
