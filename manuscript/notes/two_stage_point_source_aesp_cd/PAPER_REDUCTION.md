# From the 100-page audit to a compact theorem core and short paper

The 12-page executable core now exists as `short_main.ltx`.  It includes complete
proofs of the one-shot Green--CG lane, direct boundary-leakage gate, mass
cleanup, safe AESP publication, the hard-capped portfolio, star mechanism,
and remaining finite-precision problem. A conventional submission can expand this core
to 12--16 pages with related work, implementation detail, and experiments.
An even narrower six-page `strict_main.ltx` keeps only set
certification, one ordinary-PPR solve, the point-source tree closure, the
strict fresh-Stage-II measurements, and the randomized arbitrary-graph
closure.

## One-sentence claim

For canonical point-source PPR, run a constant-size certified portfolio and
restart at most once: return any target-accurate numerical checkpoint; continue
a lower-safe mass checkpoint by APPR/SOR; or solve one ordinary principal PPR
system after a genuinely set-only screen.

This is an **at-most-two-stage** result.  It does not claim that every instance
uses two stages or that exact RPPR support must be identified.

## The nine results that belong in the main paper

1. **One-shot Green--CG lane.** Point-source decay gives a certified rooted
   ball using no numerical values. Expose it once, solve one principal
   system, and race against APPR. This is unconditional with an
   instance-selective product-scale branch and strict high-accuracy wins on
   five graph families. On a certified fixed-treewidth envelope, replace CG
   by one sparse factorization and obtain an `O(1 / epsilon)` successful
   branch for fixed width.

2. **Direct boundary-leakage gate.** A coarse principal PPR point plus a
   residual error bar and one boundary scan certifies the envelope without
   RPPR or exact support.
3. **Approximate-envelope linearization.**  If RPPR amplitude outside \(E\)
   is at most \(\delta\), the ordinary principal PPR solution on \(E\) is
   within \(\rho+\delta\) of full PPR.
4. **Screen or solve.**  A numerical RPPR/APPR checkpoint used to certify an
   envelope is already a valid PPR output at the corresponding budget.  Do
   not force a redundant terminal solve.
5. **Set-only composition.**  A containing/approximate envelope of volume
   \(V_E\) gives a fixed linear tail in
   \(\widetilde O(V_E/\sqrt\alpha)\) work.
   If that tail is an exact structural solve, assign it zero numerical budget
   and spend the full tolerance on screening (`rho = epsilon` for RPPR or
   `delta = epsilon` for direct Green truncation).
6. **Mass-completion composition.**  A global PPR subsolution with mass
   deficit \(\mu\) can be finished by APPR/SOR in
   \(O(\mu/(\alpha\epsilon_{\rm ppr}))\) degree work.
7. **Safe AESP mass publication.**  A fixed envelope capturing
   \(1-O(\sqrt\alpha)\) principal PPR mass, signed scratch, and Stieltjes
   retraction yield the desired AESP--APPR handoff without identifying
   \(S^\star\).  The residual interval cheaply screens attempts.
8. **Hard-capped certified portfolio, including literal exact support.**
   Direct APPR is the universal lane.  Set-only and mass screens may win, but
   abort before their retained volume exceeds the declared cap.  Coarse APPR
   snapshots or positive-residual SOR may propose a support-safe face; one
   structural solve plus a KKT scan certifies exact $S^\star$, while failure
   resumes the same direct lane.  Round-robin scheduling loses only a
   constant factor to the best complete lane.  On point-source trees this
   conditional attempt becomes an unconditional exact algorithm: scalar
   descendant responses and propagated activation thresholds identify a
   strict positive frontier row or certify global KKT.  The implementation
   charges every root-path update and scans each admitted adjacency list once.
   An exact fixed-face tail uses zero terminal-error budget, so the optimized
   split is `rho = epsilon`, not the generic half-and-half split.
9. **Randomized threshold-batch closure.**  The companion OP2 theorem rebuilds
   only `O_tilde(1 / sqrt(alpha))` safe exposed faces, certifies every
   randomized SDD call by an exact residual scan, and returns a face of RPPR
   objective gap `eps_obj` in expected fully charged
   `O_tilde(log(1 / eps_obj) / (rho sqrt(alpha)))` work.  A new inner-face
   lemma turns that gap into exterior amplitude
   `sqrt(2 eps_obj / alpha)`.  Consequently, even a strict subset of `S*` is
   a valid set-only handoff to one ordinary principal-PPR solve.  This closes
   arbitrary graphs in the exact-real randomized word model; deterministic
   finite-precision and bit complexity remain open.

The experiments report two different costs for the exact-face lanes.  The
cheaper one returns the exact RPPR point already computed by the verifier.
The literal two-stage column additionally runs and charges a fresh ordinary
PPR solve.  This distinction is essential for APPR/SOR proposal lanes; on the
tree threshold-message lane the ordinary-PPR solve replaces RPPR recovery, so
there is no duplicated solve.
The fresh-solve column is conservative: a production verifier can retain its
certified $Q_A$ factorization and solve the ordinary-PPR right-hand side with
one additional backsolve.
The executable reuse charge changes APPR, SOR, and exact-batch
standalone/fair counts from \(4/2\), \(5/5\), and \(33/8\) to \(6/2\),
\(7/5\), and \(37/9\).  Reuse helps, but it does not change the main
conclusion that a cheap set certificate---not the fixed solve---is the
missing general-graph primitive.
The code also factors independent path, broom, and cycle systems once and
uses those retained factors for both the RPPR verifier and ordinary-PPR
right-hand sides, matching separate sparse direct solves on three named and
80 deterministic randomized structural systems.

The star barrier belongs beside Result 6: mass capture is instance-selective
and cannot replace the numerical \(\ell_\infty\) early-return rule.

## Suggested page budget

| Part | Pages | Content |
|---|---:|---|
| Motivation and contribution | 1.5 | point source, why forced Stage II is redundant |
| Problem and three certificates | 1.5 | numerical, set-only, mass-completion |
| At-most-two-stage algorithm | 1.0 | one flowchart/pseudocode |
| Set-only theorems | 3.0 | linearization, inner-face transfer, fixed-tail composition |
| AESP--APPR/SOR theorems | 3.0 | retraction, mass cleanup, residual interval, star barrier |
| Concrete lanes | 2.0 | APPR/SOR exact-face race, Green and mass screens |
| Certified race and experiments | 2.0 | equal-accuracy benchmark, no forced-tail claim |
| Randomized OP2 closure | 1.5 | batch-depth source theorem and literal two-stage corollary |
| Scope and limitations | 1.0 | deterministic finite precision and persistent reuse remain open |
| References | 1.5 | focused bibliography |
| **Total** | **18.0** | full proofs of the nine central results |

## Move to the companion proof audit

- correction-by-correction Lyapunov inequalities across support changes;
- Moreau face-shock transfer and admission convolution;
- Perron/constant-mode alignment and observable cap windows;
- rejected-window and permanent finite-inner replay ledgers;
- variable-port, cactus, treewidth, and kinetic-hull implementation details;
- the full catalogue of mixed-clipping, scratch-spill, decoy, and
  face-by-face counterexamples;
- exact checker traces and large parameter sweeps.

These results remain citable and valuable.  They are evidence and provider
lemmas, not prerequisites for the short theorem spine.

## Claims the short paper must not make

- The universal arbitrary-graph theorem is only an exact-real randomized
  word-model theorem; do not promote it to deterministic, floating-point, or
  coefficient-bit complexity.
- Exact \(S^\star\) is not required by the final PPR problem.
- Current APPR/SOR/AESP-gap numerical lanes do not become faster by forcing a
  second linear solve.
- The mass lane is not universally output-sensitive; diffuse stars are an
  exact obstruction.
- Point-source locality does not give the additive
  \(\operatorname{nnz}(s)\) guarantee for general sparse sources.
- Signed scratch is safe only on a fixed retained envelope followed by the
  certified publication map.

## Recommended paper title and framing

**Screen, Complete, or Solve: An At-Most-Two-Stage Point-Source Hybrid for
Local PageRank**

The contribution is a reduction and a certified portfolio, not a claim that
one new engine dominates every graph.  The clean positive theorem is the
composition interface plus randomized threshold-batch closure.  The clean
open target is a deterministic finite-precision or practical persistent
realization.  The mass lane remains the practical AESP--APPR alternative,
guarded by a hard cap and the star barrier.
