# Generic OP3: constrained diffusion after the objective-accuracy bridge

Second-night block 4 checkpoint, 8 September 2026 local time. General OP3
is **Open**. Resume here after checking the actual-time ledger; do not
repeat the completed special-family or accuracy audits.

## What is now established locally

The authoritative draft is `sec:op3-diffusion-accuracy` in
`sections/op3_diffusion_accuracy.tex`. For original physical coordinates,
`M=D-gamma*A`, `bar_alpha=1-gamma`, `b=e_v-lambda*d`, and
`lambda=eps_appr/2`, let `E(x)=x'Mx/2-b'x`, `x>=0`.
The zero ACL output handles `eps_appr*d_seed>=1`. Otherwise:

- **Proved here**, draft: `-1/(2*bar_alpha) <= E_* < -eps_appr/8`.
  Thus the initial negative optimum is separated from zero by a known
  requested-accuracy scale, rather than a hidden complementarity margin.
- **Proved here**, draft: any feasible `w` with
  `E(w)<=E_*/(1+eta)`, `eta=bar_alpha^2*(eps_appr/8)^2`, has uniform
  coordinate error at most `delta=eps_appr/8`. Downward clipping
  `uhat=max(0,w-delta)` gives `0<=e_seed-M*uhat<=eps_appr*d` and
  `supp(uhat) subset supp(u_exact)`. All degrees are original degrees.
- **Measured:** 1,233 exact original graph cases on all 30 connected
  graph-atlas graphs of orders two through five, every seed, three alpha
  values and three tolerances. There are 11,574 candidate certificates
  and 3,291 clipped false-positive coordinates. Candidate generation uses
  the exact optimum and halving; this is a validator, not a local solver.

The logarithm of `1/eta` is bounded by logarithms of `1/alpha` and
`1/eps_appr`. This resolves an accuracy-interface question. It does not
turn a global solver into a local one or supply a computable stopping
certificate involving the unknown optimum.

## Exact source obligations

Primary metadata and page pointers are synchronized in
`docs/literature/index.md` and `docs/literature/lcp-solvers.md`.

Chen–Peng–Wang, FOCS 2021, arXiv:2105.14629v2:

- Definitions 3.7–3.8, PDF p. 15, are the objective/approximation interface.
- Definition 3.13 and Fact 3.14, p. 16, construct a full supplied-graph
  residual instance, with shifted bounds and charged O(|G|) work.
- Assumption 3.15 and Lemmas 4.1–4.2, p. 17, retain the numerical-range
  condition on every encountered nonzero number, not merely the original
  edge weights. Claim 8.21's proof, p. 52, invokes it for proximal accuracy.
- Section 1.4, p. 8, identifies strongly local near-linear diffusion as open.

**Source/context only:** no fast constrained-diffusion algorithm is imported
by the new lemma. Its exact-real word model does not establish rational bit
complexity or numerical stability. The known initial energy floor is not a
proof that every recursive residual, breakpoint or elimination coefficient
has polynomial range.

The 2020 p-norm flow theorem retains maximum-degree and Dirichlet-curvature
factors. The 2023 weighted statement's printed beta bound needs a parameter
interpretation before import. A unit-weight path with m active coordinates,
strict next-coordinate slack and Rayleigh quotient
`6/((m+1)*(2*m+1))` refutes the candidate interpretation that minimum edge
weight universally lower-bounds that curvature, including the 2L convention.
It does not establish an OP3 lower bound or refute an unspecified parameter.
The 2024 noisy-label paper's introductory linear-support summary is not a
replacement for the quantified original theorem. Do not spend the next block
repeating this source check unless a precise new claim requires it.

## Next falsifiable targets, in priority order

1. **Numerical-range replacement.** Trace the constrained solver's tolerance
   uses and determine whether all required accuracies can be supplied from
   the known original objective interval and requested delta. A useful result
   must handle intermediate residual instances and possibly exponentially
   small nonzero scalar response events. If pruning or rounding is proposed,
   prove its accumulated energy/original-coordinate error, convexity, and
   work, rather than assuming small coefficients can be deleted. A counterexample
   to unqualified range inheritance is useful even if it does not obstruct
   a certified approximate implementation.
2. **A computable certificate.** Replace the unknown-optimum interface by
   a primal/dual or residual certificate of comparable cost. A supplied face
   with volume O(1/eps_appr) can be scanned once; repeatedly rebuilding a
   certificate after every new vertex is the original missing ledger.
   Count all candidate false positives and their row accesses before clipping.
   Small final support does not retroactively make those accesses local.
3. **Local construction.** Decide whether constrained elimination can be
   exposed lazily under original positive admission gates, or whether a
   different graph-local reduction gives geometrically amortized supplied
   instances. Every source sparsifier, tree, auxiliary edge, failed check,
   state copy and final output belongs in the work ledger. A source runtime
   linear in the supplied graph is insufficient without bounding total
   supplied-graph work across expansions.

The existing sparse coarse SDD construction is a second way to examine the
same repeated-work question: its current bound includes active cycle rank.
Do not infer a new bound merely from telescoping correction energy or the
new objective scale. If the generic direction stalls, identify a precise
source-interface obstruction or a narrower falsifiable lemma before returning
to more special graph families.

## Completed bounded admission probe

`prop:op3-harmonic-union-stream` bounds the cheapest of three known union
operations in the two-star family. At a twin admission, L remaining twins
and s reached old leaves with distinct pendant counts satisfy
`L*lambda*(2+q_max)<1`, `q_max>=s`. The new A response has at most
`2*s+2` genuine events. J such union updates therefore stream at most
`2*J+2*H_J/lambda` events, independent of the unknown ambient twin count.
Input curve construction and graph recognition are explicitly excluded
from that primitive's bound, not silently free in a local solver.

The full audit passed 96 legal original-degree trajectories, 6,712 positive
core admissions, 2,047 twin-budget checks and 216,453 complete affine-piece
identities. It falsifies the proposed naive cumulative obstruction for this
mechanism. Extending the residual/event association to arbitrary graphs is
**Open**; it is not the main next block.

## Continuation discipline

Use `OVERNIGHT_20260907_BLOCK4_AUDIT.json`, `VERIFICATION.md` and the
separate 480-minute ledger. Preserve all prior dated outcomes. General OP3
remains Open; draft claims stay out of the active manuscript and shared
results ledger. Commit and push verified blocks under the existing user
authorization. No further usage reset is available. Do not count first-night,
idle, scheduling or unverified time toward the requested eight new hours.
