# Direction status: evolving_support_cg

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** When is exact or restarted CG genuinely local, and can an
  evolving-support implementation avoid repeated-prefix and uncontrolled-halo
  work?
- **Model:** Exact ordinary CG for Qx=b from a seed-supported right-hand side, implemented by scanning only supp(p_k), plus exact principal-subsystem/restarted variants on evolving supports. The endpoint-path calibration uses exact algebraic-cell arithmetic, ambient path degrees, s=e_1, alpha_n=n^(-2), and x_0=0.
- **Accuracy namespace:** r=b-Qx and ||D^(-1/2)r||_infinity <= alpha*eps_ppr, which certifies degree-normalized PPR solution error eps_ppr.
- **Access and charged work:** Frontier CG charges vol(supp(p_k)) for each Qp_k plus the final verifier product; evolving principal methods charge every envelope scan, halo discovery, restart, and final residual recomputation. The path theorem separately reports adjacency reads/rounds, online stages, preprocessing, control, recurrence, response work, persistent memory, transient workspace, vector materialization, and emitted output.
- **Intended result:** Determine when Krylov acceleration is genuinely local and whether support evolution can avoid repeated-prefix work under a graph-uniform charged ledger.

## Claim ledger

- **Source:** Exact CG, CDPR/full orthogonalization, and flexible-CG background are source material; the note does not attribute its local theorems to those sources.
- **Proved here:** Exact CG finite propagation and frontier work (`thm:finite-propagation`, `cor:local-cg-work`); exact endpoint-path frontier-singleton residual, full-prefix directions, earliest certificate at K=n, and a fully charged quadratic literal ledger (`thm:endpoint-path-exact-cg-certificate`); the residual certificate and a trajectory/ball-volume conditional rate (`lem:certificate`, `cor:conditional-work`); principal-system monotonicity and boundary geometry (`thm:principal-geometry`); point-seed exact violation-only terminal-volume bound (`prop:violation-only-volume`); and logarithmic-restart/geometric revisit work in terms of terminal explored volume (`thm:geometric-envelope-work`).
- **Conditional:** Accelerated local work follows only from a bound on visited seed-ball or terminal-envelope volume (`cor:conditional-work`, `thm:geometric-envelope-work`).
- **Measured:** Synthetic path/spider/decoy experiments quantify restart tax and geometric-envelope behavior (Section “Executable evidence”).
- **Refuted:** Masking a live CG direction destroys Q-conjugacy (`prop:masking-obstruction`); a high-degree decoy refutes any factor-two-halo terminal-volume/work bound depending only on alpha and eps_ppr (`prop:decoy-obstruction`).
- **Open:** Structural ball/envelope sufficiency, a guarded hybrid, and signed-handoff/finite-precision composition with a certifying fallback. The path result does not address arbitrary supported polynomials, implicit or rational response methods, or a class lower bound.

## Central blocker

The exact endpoint-path CG trajectory is now resolved: for eps_ppr=1/10 its first certified iterate is K=n and its literal supported-row ledger is Theta(n^2). The broader blocker remains unchanged. The uniform factor-two halo theorem is refuted, not open; any useful geometric implementation must impose a hard volume/degree guard and fall back to certifying frontier or violation-only work. A class lower bound for arbitrary supported polynomial or implicit-response routes belongs to `local_solver_oracle_hierarchy`, not to this theorem.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: the shared PPR matrix/certificate and standard
  exact-CG identities.
- Supplies to: response_preconditioned_hybrid as an iterative-frontier baseline; local_solver_oracle_hierarchy as an algorithm-specific exact-CG calibration, not a class lower bound; and the shared warning that finite propagation or a singleton residual alone does not imply one-pass work.

## Resume here

- Exact file/section/lemma: `thm:endpoint-path-exact-cg-certificate` for the resolved path calibration; “Recommended algorithmic direction,” `cor:conditional-work`, and `thm:geometric-envelope-work` for the remaining guarded-hybrid program.
- Next concrete action: Use the exact path calibration as a regression target while analyzing frontier-sparse CG with a hard explored-volume guard, periodic exact residual verification, and a violation-only fallback.
- Stop/go test: Go only with a structural terminal-volume certificate or an explicit guarded fallback; stop any proof that bounds a nonviolating halo vertex's degree using only alpha and eps_ppr.

## Verification

- Source pointers checked: README.md, registry.toml, main.tex, experiments, literature index/topic notes, and shared ledgers were cross-read on 2026-08-21.
- Focused build/checks run: `make` and repository-wide `make note-audit` passed; exact formulas, full-prefix supports, termination, and prefix sums were checked numerically for n in {2,3,4,5,10,25,100}; scoped `git diff --check` passed. An independent read-only audit rederived the Krylov/Galerkin structure, continuant formulas, all endpoint cases, certificate inequality, prefix-volume sum, target-scale identity, eleven-coordinate implementation ledger, and scope and found no substantive defect.
- Known gaps: The README now states the point-seed and exact-principal-solve
  assumptions of `prop:violation-only-volume`. Hestenes--Stiefel and Notay remain only
  in the note-local bibliography, not `docs/literature/index.md`. Do not revive
  the factor-two halo as open or generalize the violation-only bound beyond
  its assumptions.
