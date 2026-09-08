# Supplied global recursion: next bounded target

**Block 12 outcome.** Two accelerated levels, persistent forests, compression/refinement and paid spectral stopping are implemented and exact-audited. The complete supplied size/work/confidence recurrence is now a Conditional theorem with a nonconstant dense base cost. The unreconciled positive-weight constructor contract remains explicit. Local discovery is Open; see `SIGNIFICANT_ENVELOPE_PROBE.md` and `OP3_MORNING_DECISIONS_20260908.md`. The earlier proposal follows.

Block 11 continuation, 8 September 2026. **General OP3 remains Open.**
The edge-floor and simultaneous range statements are now proved drafts
and exact-audited in `sec:op3-recursive-vwf-ranges`. The earlier probe is
historical. The following full-recursion derivation is still **Conditional**.

## Source constructor contract to finish checking

CPW Lemma 4.4, PDF p.19, explicitly assumes polynomial weight ratio;
Algorithm 3 and its recurrence are on p.20. Do not silently remove this
hypothesis. Sections 5.1–5.6 use a weighted low-stretch tree, weighted
tree decomposition and exact flow routing, then a constant-factor core
spectral sparsifier. The algebraic routing arguments involve positive
weights without a numerical gap. A complete source-derived extension
still needs its assumptions and failure probability stated explicitly.

New primary sources checked:

- Abraham–Neiman, *Using Petal-Decompositions to Build a Low Stretch
  Spanning Tree*, SIAM J. Comput. 48(2):227–248 (2019). Checked author's
  March 22, 2012 full version, PDF pp.2,17–18 (printed pp.1,16–17),
  https://www.cs.bgu.ac.il/~neimano/spanning-full1.pdf . Theorem 1 and
  Sections 6–7 explicitly cover arbitrary positive weights using scale
  contraction; the running-time argument does not scan every global scale.
- Koutis–Levin–Peng, *Faster spectral sparsification and numerical
  algorithms for SDD matrices*, ACM Trans. Algorithms 12(2), Article 17
  (2015), DOI 10.1145/2743021. Checked arXiv:1209.5821v3,
  https://arxiv.org/pdf/1209.5821v3 , Sections 3.1,3.4,4.1–4.2 and
  Theorem 4.2 (PDF p.9). Its general spectral sparsifier uses fixed
  precision and O(n log n) edges. Later dense-graph/integer-weight
  shortcuts are unnecessary. The source uses a symmetric approximate
  inverse operator, not an arbitrary adaptive nonlinear solver.

CPW PDF pp.19–20, AN PDF pp.17–18 and KLP PDF p.9 were rendered and
visually checked. Cached PDFs/text are under /tmp/op3-{cpw2021v2,an19,klp15}.
No PDF was added to the tracked library. Bibliographic index and topic
note must be synchronized when these two sources are recorded.

Candidate construction contract, for a global logarithmic bound L:
given current graph with m edges and target j>=10, obtain a j-tree Q
with quality O(m L^2/j), O(j L) core edges and O(m poly(L)) work,
for all positive weights that actually occur. Choose the failure
probability for the total recursion, not merely inverse-polynomial in
the shrinking current n. Standard sampling/JL confidence changes may
replace log n by L but must be checked against the source concentration
statement. Apply the implemented spectral floor afterward; quality only
doubles and no forest edge disappears.

## Candidate full work recurrence

Let M=m+S_input, where S_input is total scalar piece count. Initial input
has finite minimum and Phi(0)<=0; obtain a computable B0>=-Phi* from the
canonical input-gap proposition or the original capped diffusion bound.
Let L dominate log(2+M0), all initial numerical logarithms and requested
confidence. Use one global quality K=A*L^12, with a sufficiently large
universal A, and stop recursing whenever m<=a polynomial in L.

Choose j of order m*L^2/K, absorbing the source constants and rounding.
Above the base threshold it is at least 10. Adjusted preconditioner quality
is at most K and exact forest elimination has input size O(M).
Along a path depth is O(log M0). The simultaneous range theorem gives
O(L^2) bins per compressed vertex (the O(log M0) depth and O(log P)
factors are both retained; do not replace them by O(L) without proof).
Thus each recursive child has

    m_child = O(m*L^3/K),
    S_child = O(m*L^4/K),
    M_child = O(M*L^4/K).

One outer mixed APG call uses O(sqrt(K)) inner calls; every inner call
uses O(log K)<=O(L) compressed residual calls. The number of children
is at most O(sqrt(K)*L), so their total input size is

    O(M*L^5/sqrt(K)) <= M/2

for a large enough A. Nonrecursive work includes full graph construction,
every exact persistent forest pass, export, residual copy, compressor bin
scan, objective guard, canonical scan, reconstruction and output. It is
O(M*poly(L)); all newly allocated words obey the same kind of bound.
Summing levels with total child size at most half parent size gives
O(M0*poly(L)) work. Do not claim the source's particular log^8 exponent.

Base cases need explicit piece-dependent cost. The proved forward-piece
dense policy uses at most S_input+1 bound QPs. Strict face growth makes
at most n principal solves per QP; ordinary dense elimination costs O(n^3)
per solve. When n<=poly(L), this gives O((S_input+n)*poly(L)) word work
and allocations. It is not O(1) when the scalar curves still have many
pieces. A single retained root can instead be minimized by a derivative
zero crossing and exact forest recovery.

Correctness follows inductively from the mixed recursion schedule:
eta_child=eta_parent/(2^34*K). The gap at the final outer output is at
most (Delta+eta)/32, giving the requested 2-relative-plus-additive oracle.
For a final pure absolute target, guarded beta=2 refinement with a
computable initial gap bound can reduce the gap geometrically; an extra
logarithm is allowed. For original ACL, use the already proved boxing,
gap certificate and original residual conversion; do not infer locality.

## Useful implementation check before claiming closure

Wire the actual mixed APG outer updates to persistent forest elimination,
export, residual compression, guarded refinement and recovery. Replace
the current dense coarse reference by a second mixed APG on a small
three-root core whose inner preconditioner is a tree. Its scalar inner
minimum can be computed exactly with the persistent primitive. Keep
dense original KKT/minima only as validators. This tests two genuinely
nested accelerated levels and catches normalization/copy/accuracy errors
that separate interface audits cannot catch. Use bounded cases and
dyadic candidate rounding with exact energy checks to control reference
denominator growth. All backtracking work must remain in the ledger.

Even a repaired supplied global theorem does not settle OP3: unknown
support discovery and cumulative supplied-face work remain central.
The morning synthesis should recommend a next local-work target and
distinguish proved structural algorithms, source-based numerical imports,
conditional full recursion, implemented references and open claims.
