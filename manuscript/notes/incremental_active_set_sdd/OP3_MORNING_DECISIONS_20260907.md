# OP3: morning findings and proposed decisions

7 September 2026. **General OP3 remains Open.** The overnight work produced
concrete local constructions, sharper structural bounds, and counterexamples
that narrow the next search. The strongest positive statements are **Proved
here** as proof drafts awaiting independent review; they have not been
promoted into the active manuscript or the shared results ledger.

The question is the third conjecture in `problem_definitions`: original
ACL/APPR accuracy with local work `O_tilde(1/eps_appr)` on arbitrary graphs,
without a polynomial dependence on `1/alpha`. OP2's RPPR objective target is
a different question. The results below use finite simple connected
unweighted graphs, original full degrees, local degree/adjacency access,
and exact-real word arithmetic; displayed inverse-accuracy bounds use
`0<eps_appr,rho<1`. Rational bit complexity and numerical
stability remain outside the claims. All discovery, failed searches,
updates, copies, histories, source calls and output are charged.

## What the exploration established

| Result | Current status | What it gives and what remains |
| --- | --- | --- |
| Persistent response reporters on arbitrary trees and unicyclic graphs | **Proved here**, draft | Exact obstacle work `O(cvol(U) log^4(2+cvol(U)))`; ACL work `O_tilde(1/eps_appr)`. Application callbacks are implemented; online top-tree balancing is an explicit **Source** import. |
| Geometric publication on arbitrary graphs | **Proved here**, draft | Cached deliveries remove repeated shared-candidate searches and the revealed-rank factor. Exact inverse maintenance gives ACL work `O_tilde((1+r^2)/eps_appr)`. |
| Certified sparse coarse publication | **Proved here**, draft | Replacing the dense inverse gives `E[W] = O_tilde((1+E[r])/eps_appr)`. A fixed sufficient bound `r<=R` gives `O_tilde((1+R)/eps_appr)`. The sparse SDD solver and top-tree balancing are **Source** imports. |
| Clique cores with arbitrary unequal private leaves, core seed | **Proved here**, draft; full special-case algorithm implemented | An exact scalar breakpoint sweep gives local work `O(cvol(U) log(2+cvol(U)))`. The clique structure is promised; the method discovers its unknown size from the positive seed row. Large cycle rank does not force a rank factor on this family. |
| Multipartite cores with unequal private leaves | **Conditional / Open** local extension | The supplied-part scalar algebra passes exact original-matrix checks. Positive-only part discovery and an incremental event structure still need an end-to-end implementation and proof. |

Here `U` is the reached positive support, `cvol(U)=sum_{i in U}(1+d_i)`,
and `r` is its internal cycle rank. For the certified algorithm the support
can depend on solver randomness, hence the expectation on `r` is essential.
The deterministic sufficient `R` can be the cycle rank of the exact
`lambda=eps_appr/2` obstacle support containing every admitted vertex.

The certified solver uses the exact sparse inequality
`|f-K*t| <= delta*bar_alpha*d_P`. Inverse positivity and substochastic
conditional responses turn that inequality into a uniform error band on
every active coordinate. Lower publications remain safe, and one downward
repair at termination gives the original ACL certificate. This avoids
requiring an exact obstacle solution. Its ACL-only stopping argument gives
no exact RPPR or OP2 conclusion.

The clique solver is different: eliminating the private leaves makes each
core value a three-piece function of the single total core response. The
sum has fewer than `2k+1` affine intervals and slope below one. Sorting and
crossing breakpoints finds the exact fixed point without an alpha-dependent
iteration count. This special-case implementation needs neither of the
imported fast data structures. Separately choosing `lambda=rho` gives an
exact RPPR solution on this promised family; choosing `lambda=eps_appr/2`
gives ACL accuracy.

## Routes that should not be reused without a new argument

**Refuted:** cheap sparse matrix updates alone pay for complete coarse
solution refreshes. There is a legal clique-with-leaves family with
`1/eps_appr=Theta(k^2)` and `cvol(U)=Theta(k^2)` on which every one of
`k^2` leaf admissions invalidates the fixed absolute residual budget.
Rewriting the `k` retained coordinates costs `Omega(k^3)` words. This
obstruction concerns that representation and policy. The scalar clique
solver solves the same family efficiently, so it is not an OP3 lower bound.

**Refuted:** geometric coordinate domination automatically passes a coarse
supersolution test. On a triangle, the true response is `(1/2,1/10,1/10)`
and the geometric upper envelope is `(51/80,11/80,11/80)`, yet
`f-K*upper=(-19/80,1/80,1/80)`. The test remains sufficient when it passes;
it simply rejects this valid upper envelope. Adaptive or coupled error
certificates remain open.

Earlier notes also retain exact witnesses against stale root-threshold
ordering, constant-relative Schur-key quietness, and explicit inverse
maintenance on growing branching cores. Their usefulness is to identify
the missing paid operation, rather than to rule out local algorithms.

## Recommended next work

1. **Review and consolidate the completed proofs.** Independently check the
   top-tree callback interface, certified SDD source accuracy/retry argument,
   original residual repair, and all retained-state charges. Separate a
   concise theorem narrative from the longer record of failed approaches.
   The exact audit programs validate application logic; they do not implement
   the imported sources' fast numerical solver or online balancing routine.
2. **Make the multipartite extension the next bounded construction.** Keep
   the promise that every core vertex has at least two core neighbors. Two
   positive rows can reveal the core identifiers. A new part should be read
   only when its original gate is positive; its complement scan must be paid
   by removed identifiers and actual incident edges. Implement one persistent
   event heap so adding a part does not rebuild old curves. The falsifiable
   target is local `O_tilde(cvol(U))` exact-obstacle work, including early
   stopping before undiscovered parts. Details and current algebraic evidence
   are in `MULTIPARTITE_CORE_PROBE.md`.
3. **Keep the arbitrary-graph mechanism as the central longer-term problem.**
   A successful approach must avoid repeated whole-port writes, repeated
   all-component queries, and cycle-triggered full reconstruction. Candidate
   tools are implicit coarse responses, adaptive original-coordinate bands,
   and a hierarchy of coupled responses. A determinant or energy potential
   alone is insufficient until it pays for these actual operations.

The structural extension is attractive because unequal local responses
already work despite dense coupling. It tests whether a simple coupling
representation, rather than low cycle rank or degree-equitable shells,
is the useful general principle. Scalar breakpoint search itself is
classical; novelty of the graph-local construction has not been established.
The companion-note and primary-source comparison is recorded in
`LOCAL_CLIQUE_PENDANT_PROBE.md`.

## Evidence and review limits

The final research block added five exact-arithmetic audits:

- Certified coarse publication: **67,856 complete original ACL checks**,
  **223,514 independently solved faces**, and **3,228,290 error/due-row checks**.
  The test provider deliberately sends two rejected perturbations followed
  by a certified nonzero perturbation. This tests acceptance and recovery,
  not the performance of the imported sparse numerical solver.
- Sparse residual epochs: **4,866 complete ACL checks**, including **26
  accepted reuse events** on targeted paths and six forced-refresh families.
- Geometric supersolution obstruction: **16,446 independent Schur systems**,
  including the exact equality boundary and both signs of the gap.
- Actual local clique solver: **1,464 explicit original obstacle comparisons**
  and **six implicit original-equation checks**. One graph has `10^18+11`
  vertices while only six positive rows and 24 incidences are read.
- Supplied-part multipartite algebra: **261 original obstacle comparisons**,
  **704 scalar fixed points**, and **182 positive part insertions**. The
  reference rebuilds curves and knows the partition; it supports no local
  complexity claim yet.

The numerical counts are **Measured**, not proofs of asymptotic bounds.
The proof authority is `main.tex`, especially stable labels
`thm:op3-certified-linear-rank`, `prop:op3-clique-leaf-refresh`,
`prop:op3-coarse-geometric-supersolution`, and
`thm:op3-local-clique-pendants`. Reproduction commands, source hashes,
build checks and pre-existing repository failures are recorded in
`VERIFICATION.md` and `OVERNIGHT_BLOCK14_AUDIT.json`. The active-time ledger
is `OVERNIGHT_WORK_LOG.json`; idle and unverified gaps are excluded.
