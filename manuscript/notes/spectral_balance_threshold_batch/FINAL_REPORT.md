# Deterministic spectral balance: final decision report

Date: 2026-08-31.  This report summarizes the audited working note; proofs,
counterexamples, and executable certificates are in `README.md`, `CLAIMS.md`,
`STATUS.md`, and `VERIFICATION.md`.

## Decision

The directed-random-walk paper can derandomize each *supplied-face* solve, but
it does not by itself remove the small `o(1)` factor or amortize the changing
faces.  Sharper current-face eigenvalues improve favorable instances, but a
fresh Chebyshev/CG solve on every face cannot meet the general target.  The
canonical ballasted broom keeps
`lambda_min(Q_UU)=Theta(alpha)` for `Theta(1/sqrt(alpha))` large faces, and an
endpoint path forces the same fresh-polynomial failure despite a one-edge
frontier.

A genuine optimizable theorem does exist after shifting the *obstacle prox*,
not merely retuning a fresh face solve.  With `sigma=tau^2`, a complete
shifted obstacle closure gives

```text
O_tilde(A/tau + B tau/mu_*),
```

where `mu_*=lambda_min(Q_(S*,S*))>=alpha`; in the graph-uniform case this is
`O_tilde(A/tau+B tau/alpha)`.  Here `A` charges fast filtering/response
production and `B` charges the persistent slow/reporting ledger; neither is a
free oracle parameter.  The clipped optimizer is
`tau=sqrt(A mu_*/B)` when it lies in `[sqrt(mu_*),1]`, with interior value
`2 sqrt(A B/mu_*)` up to logarithms.  For `A=B=M`, this is
`tau=sqrt(mu_*)` and work `O_tilde(M/sqrt(mu_*))`.

This yields unconditional deterministic no-small-`o(1)` algorithms on paths,
trees, supplied constant-treewidth graphs, and feedback-edge-rank `k`
instances with an explicit additive `k^omega_mat` core term (in particular,
the target bound when `k^omega_mat=O_tilde(M)`).  For general sparse graphs it
is a conditional theorem: the precise missing operation is a persistent,
support-local changing-principal response producer.  The weakest audited
capped form is
`AmortizedLowerShiftedApply(tau)`; `ShiftedProxClosure(tau)` and
`CenterLift(tau)` are stronger sufficient interfaces.

## 1. Concrete map from the directed-random-walk paper

For every exposed face `U`, degree coordinates give

```text
H_UU = a D_U - b A_U,
a=(1+alpha)/2,  b=(1-alpha)/2.
```

This is SDDM and can be represented as a grounded undirected Laplacian: use
internal edge weight `b` and add a ground edge of weight `alpha d_i` at row
`i`.  Consequently the
deterministic almost-linear directed-Laplacian machinery applies to a
*materialized fixed face*.  The map is:

| Our operation | Fixed-system operation in the paper | What transfers |
| --- | --- | --- |
| Solve `Q_UU x=c_U` | Solve grounded `H_UU y=D_U^(1/2)c_U` | Deterministic supplied-face energy approximation |
| Certify a numerical candidate | Sparse residual product on `U` | Our residual/retraction adapter makes a safe lower subsolution |
| Find the next active batch | Exterior signs of `c-Qz` | Not supplied by the paper |
| Reuse state after `U` grows | Dynamic principal inverse/Schur response | Not supplied by the paper |
| Charge only `vol(S*)` | No ambient preprocessing or old-face replay | Not supplied by the paper |

On a symmetric input the directed skew component vanishes, so the paper's
partial-symmetrization parameter is not our desired spectral cutoff.  Literal
composition therefore gives approximately

```text
O_tilde(M^(1+o(1))/sqrt(alpha)),
```

not `O_tilde(M/sqrt(alpha))`.  It is a valid deterministic replacement for
the randomized face solver when the small `o(1)` is acceptable.

## 2. What a narrower formed-face spectrum really buys

The exact face gap is

```text
mu_U = alpha + (1-alpha) delta_U/2,
```

where `delta_U` is the killed/Dirichlet normalized-Laplacian gap.  Therefore
the user's intuition is correct on well-exposed faces: certified
`mu_U>>alpha` accelerates both Chebyshev/CG and the batch-depth estimate.

It is not graph-uniform.  Every face has diagonal
`a=(1+alpha)/2`, hence `lambda_max(Q_UU)>=a>=1/2`.  If `mu_U=Theta(alpha)`,
the full condition number is still `Theta(1/alpha)`; degree/Jacobi scaling
only rescales both endpoints.  The exact fresh-face ledger is

```text
sum_j vol(U_j) sqrt(lambda_max(Q_Uj)/mu_Uj).
```

The ballasted broom makes this `Omega(M/alpha)`.  Thus an adaptive eigenvalue
certificate is useful as a portfolio branch, but cannot be the missing
general proof.

There is nevertheless a closed high-gap branch: if the final certified gap
is at least `sqrt(alpha)`, the product of
`O_tilde(1/sqrt(mu_*))` faces and
`O_tilde(M/sqrt(mu_*))` fresh work per face is
`O_tilde(M/mu_*)=O_tilde(M/sqrt(alpha))`.  Descending safe guesses plus the
existing residual certificate find this branch without knowing the gap in
advance.

The later accelerated phase also improves, not only the face solve.  For any
certified `alpha<=mu<=lambda_min(Q_UU)`, the audited companion metric

```text
F_mu = (1+mu)Q - Q^2 - mu a I
```

is Stieltjes/lattice compatible, contracts a held tuned-NAG step by
`1-sqrt(mu)`, and retains the exact negative cut-square term when the face
grows.  Decreasing dyadic gap estimates can be transported nonexpansively
after rescaling the physical state.  This closes gap-adaptive state transport;
it does not by itself turn the additive event bank into a publication-time
bound.

## 3. The valid balance and deterministic algorithms

Define the global obstacle resolvent

```text
T_sigma(x) = argmin_(z>=0) { Phi(z) + (sigma/2)||z-x||_2^2 }.
```

For every monotone lower subsolution,

```text
x <= T_sigma(x) <= x*,
||T_sigma(x)-x*||_2 <= sigma/(mu_*+sigma) ||x-x*||_2.
```

Taking `sigma=tau^2` needs
`O_tilde(1+tau^2/mu_*)` outer calls.  If one entire no-miss shifted active-set
closure costs `O_tilde(A/tau)`, multiplication gives the promised balance.
The deterministic residual/retraction adapter makes finite signed
Chebyshev/CG outputs safe, so numerical certification is closed.

Closed end-to-end classes are:

- endpoint paths: retained tridiagonal transfer gives exact linear work;
- trees: scalar Schur messages implement every shifted closure and give
  `O_tilde(M/tau+M tau/alpha)`;
- supplied constant treewidth: bounded-width elimination gives the same bound
  up to width factors;
- feedback-edge rank `k`: tree Green queries plus a `k x k` Woodbury core,
  solved by pivot-free recursive block inversion, give
  `O_tilde((M+k^omega_mat)/sqrt(alpha))` exact ordered-field operations for
  the certified capped output.  Here `omega_mat` is any admissible exact
  matrix-multiplication exponent.  Degree coordinates remove radicals.  This
  does not claim bit complexity, floating-point stability, that the last
  capped face equals the full exact support, or an improvement to the separate
  chronological `Mk^2+k^3` maintenance bound.

For arbitrary graphs the response update after adding a block `B` contains
the dense old-face lift

```text
-(Q_UU+tau^2 I)^(-1) Q_UB g_B.
```

Padded old CG directions remain mutually conjugate, but their orthogonality
against the new residual is broken by `P^T Q_UB g_B`.  A complete repair is
exactly the dense Schur lift.  Warm restart plus retraction therefore cannot
be charged only by the new coordinates; the endpoint-path regression and the
ballasted broom make this failure explicit.

No Green-leverage oracle is needed to terminate a capped prox.  If the
maintained lower correction `d>=0` has active residual
`e_U=r_U-(Q_UU+tau^2 I)d_U>=0` and a complete current boundary scan has
nonpositive exterior scores, then `(-e_U,0)` is a subgradient of the full
shifted obstacle objective.  If `d_prox*` is its exact minimizer, strong
convexity gives

```text
F(d)-F(d_prox*) <= ||e_U||_2^2/[2(alpha+tau^2)],
||d-d_prox*||_2 <= ||e_U||_2/(alpha+tau^2).
```

This pays every hidden cascade globally.  The scan is support-local in the
canonical point-source problem: the source is seeded, and a nonneighbor of
the current support has the known negative floor score.  Thus the remaining
producer is needed only when the boundary is currently quiet but the active
residual is too large for the requested objective cap.

For exact restricted-center or zero-margin support certification, a weaker
rowwise Green fact remains useful.  Put `C_v=-Q_vU>=0`; then

```text
0 <= C_v(Q_UU+tau^2 I)^(-1)e
   <= sqrt((a+tau^2)/(alpha+tau^2)) ||e||_2.
```

Every visibly positive current-score batch can be appended at correction
zero, preserving all old scores, and the appended sources over one nested
prox call have the global square bank
`sum_B||g_B||_2^2<=(1+tau^2)alpha`.  A norm-trigger buy count follows only in
reset-and-zero-append epochs; it is not a contraction theorem for arbitrary
intervening updates.

The remaining general theorem is now sharply isolated:

> Maintain a certified-lower accelerated shifted solve through all visible
> zero-appends.  Repeatedly rescan, append every positive current score, and
> reduce `||e||` until the global subgradient cap is met, with all response
> updates and rescans totaling `O_tilde(M/tau)` work and no old-volume replay.

The resulting deterministic skeleton is concrete:

```text
sigma <- tau^2;  x <- certified lower starting point
repeat outer prox calls until the manuscript objective cap:
    U <- supp(x) plus the seeded source;  d <- 0;  e <- r_U
    repeat:
        scan every edge leaving U
        append every row with current score > 0, setting its d-coordinate to 0
        if all current exterior scores <= 0 and
           ||e||^2 <= 2(alpha+sigma) epsilon_prox: commit x <- x+d; break
        perform a certified-lower accelerated shifted residual-reduction step
```

The scan, zero append, residual/retraction certificate, subgradient stop, and
outer contraction are proved.  On paths, trees, supplied bounded width, and
the stated low-cycle rebuild regime, the last line has an implemented
deterministic realization.  On a general sparse graph, amortizing that last
line and its rescans by `O_tilde(M/tau)` is exactly the remaining conjectural
interface—not an omitted call to a free SDD solver.

For the stronger `CenterLift` route, the positive inverse-square-root group
probe and canonical first-crossing/conservation ledger already pay the
reporting side by `O_tilde(M tau/alpha)`.  In the capped loop above, rescans
are charged directly in `AmortizedLowerShiftedApply`.  Either way, Gaussian
trace probes are no longer the core obstacle.

## 4. Follow-up literature verdict

No audited follow-up currently supplies the missing deterministic,
support-local, nested-principal response primitive.

- [Kyng--Meierhans--Probst Gutenberg](https://arxiv.org/abs/2208.10959)
  gives the deterministic fixed-system backend, with a subpolynomial
  overhead.
- [Wei--Yang](https://arxiv.org/abs/2608.16339) is the closest matching local
  active-set PageRank algorithm, but its advertised bound is high-probability
  and it explicitly re-solves the nested SDD systems and scans their
  boundaries.
- [Fountoulakis--Martinez-Rubio](https://arxiv.org/abs/2602.21138) gives a
  useful accelerated/local optimization comparison, not persistent Schur
  response maintenance.
- [Chuzhoy--Parter](https://arxiv.org/abs/2601.20718),
  [Li--Vaughn](https://arxiv.org/abs/2608.13910), and
  [Farfan--Ghadiri--Yang](https://arxiv.org/abs/2511.16570) improve
  deterministic routing/sparsification or fixed SDDM access, but retain
  ambient or subpolynomial costs and do not maintain solution responses on an
  unknown growing support.
- [Kadeethum--Ballarin--Choi--Lee](https://arxiv.org/abs/2606.17971) is a
  promising practical restricted-eigenspace recycling method.  Its active
  sets and global reference modes are supplied, and the needed rank/coherence
  bound is empirical rather than graph-uniform.

The three supplied convex-optimization papers are useful for the final
identification/refinement stage and for designing practical active-set
heuristics.  Their hypotheses begin after a useful global gradient/face is
already available; they do not charge unread-boundary discovery or the dense
Dirichlet-to-Neumann response.  They therefore do not close the Stage-I local
work theorem.

## 5. Exact delayed-clock correction

The strengthened exact verifier proves, over `Q(sqrt(10))`, that one canonical
34-vertex simple connected unit graph at `alpha=1/1000`, `rho=1/100000` has
projected-NAG publication times

```text
0, 1, 2, 3, 4, 38.
```

All exterior residuals at products 5 through 37 are nonpositive, with largest
exact value `-2e-8`; every lower-subsolution inequality holds; every quiet
early-stop test fails by squared ratio at least `4.09312681762e11`; and an
exact rational full solve is positive, hence `S*=V`.  This refutes only the
immediate-next-product lemma for that recurrence.  It is compatible with a
shared `O(1/sqrt(alpha))` clock and is not an algorithmic lower bound.

## Bottom line

The ten-hour direction was worthwhile: it found the right optimizable
parameterization, proved unconditional no-small-`o(1)` algorithms on several
nontrivial graph classes, derandomized fixed-face candidate selection, and
reduced the general problem to one weaker capped residual producer contract.
It did not prove an unconditional general-graph deterministic
`O_tilde(M/sqrt(alpha))` algorithm.  Further material is most valuable if it
addresses dynamic Schur responses, incremental principal inverse application,
or output-sensitive
obstacle multigrid; more generic active-set identification papers are unlikely
to resolve the remaining bottleneck.
