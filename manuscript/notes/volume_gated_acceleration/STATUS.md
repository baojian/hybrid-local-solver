# Direction status: volume_gated_acceleration

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** Can safe RPPR support gates preserve accelerated progress across certified subspace additions without a full restart or old-face scan per admission?
- **Model:** Shared PPR plus RPPR safe-support gates. A signed accelerated candidate is retracted to a lower envelope, negative outside KKT violations are admitted, and restricted acceleration continues on expanding certified subspaces.
- **Accuracy namespace:** Final PPR target is ||D^(-1/2)(x_hat-x^0)||_infinity <= eps_ppr. rho is RPPR regularization and tau is a one-sided KKT/error gate; the main choice is rho=tau=eps_ppr/2.
- **Access and charged work:** A full restricted step on U costs vol(U); every admission scan, old-face recurrence/response application, factor or Schur update/query, state write, materialization, validation, and output is charged in the shared eleven-coordinate order.
- **Round-013 exact path contract:** 0<q<=1/4, alpha=q^2, rho=tau=q/5, zero start, transported centers, ambient degrees, the internal complete all-violations gate, the full moving global correction, and one terminal external certificate/output return. The candidate subfamily sets q=1/(16m) on the complete endpoint path P_m.
- **Intended result:** Uniform peak volume O(1/eps_ppr) and graph-uniform O_tilde(1/(rho*sqrt(alpha))) work, hence the PPR product scale after rho=Theta(eps_ppr).

## Claim ledger

- **Source:** RPPR/FISTA support and confinement facts, the classical bad-star phenomenon, LocCH, and AESP are source ingredients (`sec:scope`).
- **Proved here:** Principal conditioning and spider geometry; the exact-PPR core; RPPR support/error conversion; safe lower-envelope admission and certificate; exact peak-volume gate; the Schur gain, transported-center, weighted-shock, and endpoint-path append-only-response ledgers; the accuracy-driven swept-prefix lower family; the constant-ratio support/product floor; and the exact q=1/5 failure of frontier-only gate logic. Stable anchors are `lem:principal-conditioning`, `thm:exact-core`, `cor:accuracy-volume`, `prop:transported-schur-ledger`, `lem:weighted-shock-occupation`, `prop:path-implicit-transport-ledger`, `prop:path-zero-start-swept-separation`, `prop:path-constant-ratio-floor`, and `prop:path-frontier-only-gate-fails`.
- **Proved here (Round 012):** For the exact-real constant-ratio path execution, the full moving correction satisfies a pointwise energy bound independent of its maximizer. Every visited face admits or certifies within K_q=O(q^(-1) log(1/q)) steps, so T=O(q^(-2) log(1/q)) and mathfrak V_T=O(q^(-3) log(1/q)); `eq:path-moving-max-eleven-upper` charges all eleven coordinates (`thm:path-moving-max-soft-upper`).
- **Conditional:** In Round 013, on a fixed full P_m face and assuming the nonnegativity projection is inactive, the affine normalized residual obeys `eq:path-full-face-two-state` and `eq:path-full-face-residual-recurrence`. Its exact two mode roots are `(1-q) cos(h*pi/(2m)) exp(+/- i h*pi/(2m))` (`lem:path-full-face-linearized-roots`). This calculation does not establish full-face entry coefficients, projection inactivity, envelope unclipping, or a residual-range lower bound for the actual trajectory.
- **Measured:** The floating-point table in `main.tex` suggests T=Theta(q^(-2)) and mathfrak V_T=Theta(q^(-3)); it is scaffolding only.
- **Refuted:** The spider growing-condition-number route; an alpha-uniform logarithmic ordinary-restart count; shock-free zero-padding across admission; universal O(sqrt(alpha) * sum_t Delta_t) packing of the weighted Schur tail; log-free O(nu_fin/sqrt(alpha)) swept-prefix work on the accuracy-driven literal path family; and frontier/seed-only gate logic. See the stable theorem/proposition labels in `sec:ledger`.
- **Refuted proof attempt (Round 013):** Two independent audits rejected the proposed terminal-face logarithmic lower theorem. Correct characteristic roots do not provide the actual packet/cosine coefficients or anti-cancellation, and deleting nonpositive fragments is not monotone for oscillation. The rapid-front/Pascal argument lacked explicit base and endpoint-row derivations; projection inactivity and the unclipped-envelope margin were not proved uniformly through k0=Theta(q^(-1) log(1/q)). The withdrawn theorem and all dependent lower-ledger/refutation claims have been removed.
- **Open:** At rho=tau=q/5, a uniform K_face=O(q^(-1)) bound, a logarithmic fixed-face lower bound, aggregate removal of the upper logarithm, matching Omega(q^(-2)) stages and Omega(q^(-3)) swept work, and the observed exact power laws are all open. The literal zero-padded signed defect, transported remaining-gain occupancy, soft-order separation, nonpath response growth, branching/cyclic extensions, finite precision, and graph-uniform total work also remain open.

## Central blocker

The Round-012 upper bound loses one logarithm. The Round-013 slow-mode lower route stops because it never proves that the actual full-face entry amplitude begins above the terminal tolerance alpha*tau=q^3/5 by a sufficient q-dependent factor, nor that cancellation, projection, and clipping preserve such a lower bound to k0. The alternative upper route must exploit admission-specific energy, normalized error, or a space--time potential while retaining the moving global correction.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: `aesp_cd_l1_rppr`.
- Source/shared prerequisites: shared RPPR support and KKT facts.
- Supplies to: response-preconditioned and hybrid-synthesis directions through the safe gate, peak-volume cap, restart obstruction, endpoint-edge shock warnings, transported-center and weighted-shock ledgers, path response ledger, and the reviewed moving-maximum upper bound. Round 013 supplies no promotable asymptotic result; its conditional root lemma and finite checks stay direction-local scaffolding.

## Resume here

- Exact anchors: `sec:path-constant-ratio`, `lem:path-global-envelope-gate`, `prop:path-constant-ratio-floor`, `prop:path-frontier-only-gate-fails`, `thm:path-moving-max-soft-upper`, and `lem:path-full-face-linearized-roots`; retain `eq:weighted-shock-occupation` as the separate analytical-shock ledger.
- Next concrete action: Either prove K_face=O(q^(-1)), T=O(q^(-2)), and mathfrak V_T=O(q^(-3)) with an admission-specific potential, or derive the literal full-face entry coefficients and a uniform anti-cancellation/range lower while proving the actual projection/envelope margins through k0. Never replace the moving global correction by a frontier or seed surrogate.
- Stop/go test: GO only after every conditional-regime obligation is explicit. STOP any logarithmic lower promotion based only on roots, central-binomial size, finite plots, or the m=2,4,8 checker. No asymptotic lower eleven-vector currently exists.

## Verification

- Rounds 004--012 retain their previously reviewed exact identities, rational checks, direction builds, note audits, graph audits where applicable, control-character/conflict scans, and scoped diff checks.
- Round-013 finite scaffolding: `check_round013.py` uses exact `Fraction` arithmetic at (m,q)=(2,1/32),(4,1/64),(8,1/128). It verifies those actual finite admission prefixes, the conditional full-face residual recurrence, inactive projection and unclipped moving envelope over 16,32,64 terminal steps, and non-certification over those same finite prefixes. It does not test the asymptotic k0 range or prove a packet coefficient, anti-cancellation, or a theorem.
- Audit record: two independent reviews rejected promotion for the missing coefficient/anti-cancellation, rapid-front boundary/base, and uniform projection/envelope arguments. The central-binomial sentence was removed rather than used to cover those gaps.
- Reconciliation checks passed on 2026-08-21: the exact finite checker, direction build (with resolved references), `make note-audit` (18 notes across 5 tracks), `make note-graph`, control-character/conflict scan, and scoped tracked/untracked diff checks.

## Known gaps

The transported-center recurrence changes the estimate center at admission and therefore does not prove the literal zero-padded conjecture. Existing eleven-vectors are for internally gated exact-real path implementations with R_int=1 and one terminal external certificate/output stage. Intermediate external emissions, finite precision, bit complexity, matching global constant-ratio lower powers, upper-log removal, and nonpath response growth remain open. The exact PPR core is existential, whereas the RPPR gate is the implementable mechanism.
