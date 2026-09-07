# Next probe: sparse coarse downdates and a global determinant budget

Date: 7 September 2026. **Proved here: derived algebraic identities, draft
exact-audited and awaiting independent review. Open: a faster maintained
response algorithm.** Do not infer an OP3 complexity theorem from the
potential budget alone.

The geometric producer removes repeated exceptional-candidate scans from
the ACL algorithm. The remaining explicit quadratic rank cost is the dense
coarse inverse update. The inverse can change densely even when its inverse
matrix, the coarse Schur matrix K, changes only in at most two coordinates.

## Sparse ordinary-admission update

Let P be the current permanent ports and I=U\P. Keep the **physical** coarse
load f (not the uniformly shifted load) and K=Schur_P(M_UU), with J=K^{-1}.
For the unique old parent i of a new leaf j, write its old conditional
response as

`u_i = zeta_i + a_i^T*u_P`,

where a_i has at most two nonzero entries and g_ii=(M_II^{-1})_ii, extended
by zero at a retained parent. The existing named Green query supplies these
quantities: from its physical u_i, subtract a_i^T*u_P to obtain zeta_i.
Equivalently convert the stored shifted offset z_i by
zeta_i=z_i+C*(1-a_i^T*1).

Eliminate the old interiors I before eliminating j. The Schur system on
P plus j is

`[[K, -gamma*a_i], [-gamma*a_i^T, tau]]`,
`rhs = [f, c]`,
`tau = d_j - gamma^2*g_ii`, `c = -lambda*d_j + gamma*zeta_i`.

Here tau >= bar_alpha*d_j. Eliminating j therefore gives exactly

`K_new = K - (gamma^2/tau)*a_i*a_i^T`,
`f_new = f + (gamma*c/tau)*a_i`.

The matrix update touches at most four ordered entries, the load at most
two. Since the physical seed is always retained, every interior physical
load is negative; inverse positivity gives zeta_i<=0 and c<0. In particular,
the physical coarse load decreases coordinatewise along ordinary updates.
Do not substitute the shifted offset directly into c.

Define

`chi = gamma^2*(a_i^T*J*a_i)/tau`,
`delta = tau*(1-chi)`.

Then 0<chi<1 and delta is the full original admission pivot from the previous
inverse transaction. The determinant lemma gives

`det(K_new)/det(K) = 1-chi`.

This is only a sparse update identity. Computing a_i, g_ii and chi still
uses the current response representation; do not count an exact leverage
query as free in a proposed alternative.

## A determinant potential through changing ports

For every current port set P define

`Phi = log(det(K)/(bar_alpha^|P| * product_{i in P} d_i))`.

Schur minimization of M_UU >= bar_alpha*D_U gives K>=bar_alpha*D_P, so
Phi>=0. Every Schur diagonal is at most the original degree. Hadamard's
inequality therefore also gives Phi<=|P|*log(1/bar_alpha).

The singleton begins at Phi=log(1/bar_alpha). An ordinary admission
decreases Phi by -log(1-chi).

Follow the actual cycle transaction, including its temporary parent:

1. Promote an old interior vertex i. If Q=P union {i}, eliminating i from
   the new coarse matrix K_Q recovers K_P. Hence the determinant ratio is
   (K_Q)_ii. Promotion increases Phi by
   log((K_Q)_ii/(bar_alpha*d_i)), a value in [0,log(1/bar_alpha)].
   Repeat this identity for all promoted old vertices, using a fixed order.
2. Border the newly admitted original vertex j, after every active parent
   is retained. The determinant ratio is its full positive Schur pivot
   delta_j. The corresponding increase is
   log(delta_j/(bar_alpha*d_j)), also in [0,log(1/bar_alpha)].
3. If a temporary old parent i is then dropped, elimination divides the
   determinant by the current coarse diagonal (K_before_drop)_ii. This
   decreases Phi by log((K_before_drop)_ii/(bar_alpha*d_i))>=0.

Let p be the final permanent port count and t the number of transient
old-parent promotion/drop occurrences. The initial seed plus all permanent
promotions/new retained admissions contribute p injections, and transient
promotions contribute t additional ones. Since the final potential is
nonnegative,

`sum_ordinary[-log(1-chi)] + sum_transient[log(K_ii/(bar_alpha*d_i))]`
`<= (p+t)*log(1/bar_alpha) <= 2*p*log(1/bar_alpha)`.

Here t<=b<=p-1. This accounting spans all port promotions and all cycle
births; restarting the p*log bound independently at every birth would lose
another factor p unnecessarily.

An exact audit can avoid floating-point logarithms. Multiply the factors
tau/delta for ordinary updates and K_ii/(bar_alpha*d_i) for temporary drops;
verify that this product is at most (1/bar_alpha)^(p+t). Also verify the
potential multiplicative identity through each promotion and border.

For a fixed threshold 0<theta<1, this limits ordinary updates with chi>=theta
to at most (p+t)*log(1/bar_alpha)/(-log(1-theta)). This is a derived count,
not a complete work bound for a data structure.

## Required exact audit

- Run source-driven admissions, not arbitrary matrix perturbations.
- Before every ordinary admission, capture the old current response,
  conditional variance, original degree and physical port means.
- Independently assemble old and new original-matrix Schur systems and
  compare both K and the physical load f with the sparse formulas.
- Check tau, delta, chi, at-most-two-coordinate support, c<0, determinant
  ratio and normalized potential bounds exactly.
- At a cycle birth, independently form the intermediate Schur systems for
  old-port promotion, new-vertex border and optional temporary-port drop.
  Charge these dense computations as reference work, not an algorithm.
- Verify the global multiplicative budget across complete traces, including
  high-parent-count births and repeated temporary promotion of a vertex.
- Include actual geometric-publication traces as well as exact-gate traces
  where practical. Their admission order can differ, but the algebraic
  ledger depends only on source-valid positive admissions.

## What remains Open even if the audit passes

A sparse, spectrally small matrix update does not automatically give a
coordinatewise error band for its positive active-face solution. The physical
coarse load changes too, and its positive source term can cancel negative
eliminated loads. Existing constant-relative Schur-key counterexamples must
remain in the review set.

The budget still contains p. Paying one whole coarse solve per counted event
would generally leave superlinear work. A successful next mechanism must
amortize approximate factor maintenance and locate original-coordinate
publications through many small updates, with certified residual/band errors.
Possible directions are a multilevel response representation, paid batching
of sparse downdates, or a structural decomposition beyond global cycle rank.
Each needs a concrete cost contract; none is supplied by this potential.

## Completed exact audit

`COARSE_SCHUR_DOWNDATE_AUDIT.json` records 6,472 complete traces on all
142 connected atlas graphs through six vertices: every seed, two parameter
pairs, two policies and both exact-gate and publication admission rules.
All 58,359 independent original Schur systems/determinants, 25,254 global
product checks, 11,668 sparse matrix/load/determinant identities, 7,209 old
port promotions, 7,114 new borders and 2,308 temporary eliminations pass.
There are 77 two-port ordinary downdates and 2,054 updates with chi>=1/4.
Every determinant calculation is reference-only and cannot select admissions.
The audit completed in 94.979 seconds. The response-maintenance work target
remains Open. A separate, simpler static coarse-solve composition is now
specified in `CERTIFIED_COARSE_SDD_PROBE.md`.
