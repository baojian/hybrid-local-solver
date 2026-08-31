# Audit map: what is closed and what is not

This file is the short claim map for `README.md`.  It deliberately separates
an implemented/end-to-end work theorem, a proved algebraic or oracle theorem,
and a conjectural producer.  The notation is

```text
M=vol(S*),   alpha=PageRank floor,   sqrt(alpha)<=tau<=1.
```

Here `S*=supp(x_rho*)` for the canonical point-source RPPR instance, and all
work is exact-real adjacency-list work with repeated scans, response
applications, validation, materialization, and output charged.  The accuracy
namespace is `eps_obj`; no `eps_ppr` conversion or deterministic bit bound is
claimed.  In repository vocabulary, Sections A and the unconditional parts of
B are **Proved here**, premise-dependent rows are **Conditional**, Section C
is **Refuted** only for each named inference, and the missing producer in
Section D is **Open**.

## A. Closed end-to-end deterministic branches

| Branch | Certified work | Scope |
|---|---:|---|
| Boundary-exposed faces | `O_tilde(M/(alpha+phi_trace))` | `phi_trace=min d_out,U(i)/d_i` over the realized face trace.  It reaches `M/sqrt(alpha)` when `phi_trace=Omega(sqrt(alpha))`. |
| Endpoint path | `O(M)` for the exact response recurrence | The one-dimensional frontier is retained rather than re-solved. |
| Trees via shifted obstacle prox | `O_tilde(M/tau+M tau/alpha)` | Exact scalar Schur messages and the zero-threshold depth theorem; optimize at `tau=sqrt(alpha)`. |
| Supplied constant treewidth | `O_tilde(M/tau+M tau/alpha)` up to width factors | Exact bounded-width elimination. |
| Feedback-edge rank `k` | `O_tilde((M+k^omega_mat)/sqrt(alpha))` | `omega_mat` is an admissible exact matrix-multiplication exponent over the ordered input field.  Rebuild a grounded-tree Green factor plus a dense `k x k` Woodbury core on each capped maximal face and solve the core by recursive block inversion.  This returns the certified approximate/capped output; it does not claim the last face is the full exact support, bit complexity, or faster singleton-persistent maintenance. |
| Bounded chronological fill | `O_tilde(R_chol+(F_chol+M)/tau+(F_chol+M)tau/mu_*)` | `R_chol,F_chol` are measured elimination-tree reach/fill parameters; optimize the displayed expression. |
| Small final support | `O(s^3+sM)`, `s=|S*|` | Exact dense principal solve and boundary validation; useful as a portfolio branch. |

Every approximate fixed-face branch may use the proved residual/retraction
adapter.  It turns a normwise CG/Chebyshev residual into a nonnegative lower
subsolution and preserves no-miss admission and quiet-KKT correctness.

## B. Closed theorems that do not by themselves implement the general case

| Theorem | Exact conclusion | Missing operation |
|---|---|---|
| Current-gap high branch | A charged certificate `Q_U>=beta I` gives at most `O_tilde(1/sqrt(beta))` prefix faces and fresh-CG work `O_tilde(M/beta)`. | No theorem bounds the low-gap suffix by `beta/alpha`; the broom refutes that inference. |
| Shifted prox reduction | If one entire `tau^2`-shifted obstacle closure costs `O_tilde(M/tau)`, outer contraction gives `O_tilde(M/tau+M tau/alpha)`. | `ShiftedProxClosure(tau)` on a general sparse growing face. |
| Global capped subgradient stop | If `d>=0`, `e_U=r_U-(Q_UU+tau^2 I)d_U>=0`, and all current exterior scores are nonpositive, then `(-e_U,0)` is a full obstacle subgradient: for the exact prox correction `d_prox*`, `F(d)-F(d_prox*)<=||e_U||^2/[2(alpha+tau^2)]` and `||d-d_prox*||<=||e_U||/(alpha+tau^2)`. | The canonical point-source boundary scan is full because the source is seeded and far nonneighbors have negative floor score.  This certifies capped objective output, not exact support. |
| Scalar shifted-debt envelope | For nonnegative solve debt `e`, every exterior response obeys `0<=C_v(Q_UU+tau^2 I)^-1e<=sqrt((a+tau^2)/(alpha+tau^2))||e||_2`.  Visible positive batches append at correction zero, leave old scores unchanged, and have `sum_B||g_B||_2^2<=(1+tau^2)alpha`. | Leverage is needed only for the exact restricted center or zero-margin support.  A norm-trigger count requires reset-and-zero-append epochs; it is not valid for arbitrary residual-changing rent steps. |
| Deterministic group reporter | One positive inverse-square-root probe dominates every row leverage; canonical conservation and first crossing charge all group visits and exact leaves in `O_tilde(M tau/alpha)`. | The additive response summary must first be produced. |
| Rank--port balance | A charged response bank with coefficients `A,B` gives `O_tilde(M+A/tau+B tau/alpha)` and optimizer `tau=sqrt(A alpha/B)`. | Construction and persistent application of the bank. |
| Supplied laminar hierarchy | One-low-mode clusters, mean-zero gap `Omega(tau^2)`, bounded overlap, and retained state give `O_tilde(A_H/tau+B_H tau/alpha)`. | Online support-local hierarchy plus coarse Schur response. |
| Landscape hierarchy | The local potential `V_U(i)=alpha+c d_out,U(i)/d_i` identifies monotone low wells; all dyadic well forests cost `O_tilde(M)` structural work.  A supplied closure gives `O_tilde(min_tau[A_fast(tau)/tau+B_land(tau)tau/alpha])`. | A Bessel-stable frame/implicit Schur state through well entries and merges. |
| Projected two-mask NAG | Correctness, non-deadlock, lattice projection, immediate scratch readiness, held contraction, event debt, and the full-spectrum `F0` cut bank are proved. | A scale-relative publication/occupancy clock converting the additive bank into elapsed products. |
| Certified-gap adaptive NAG | For any charged `mu<=lambda_min(Q_U)`, `F_mu=(1+mu)Q-Q^2-mu aI` is Stieltjes/lattice compatible, contracts by `1-sqrt(mu)`, and keeps the exact principal-growth cut drop.  Nonincreasing dyadic gap changes are nonexpansive after physical-state rescaling, and all recenter debts sum to `O_tilde(alpha)`. | The same publication/occupancy conversion; a cheap certificate may also be loose.  At `mu=alpha` this is the original open clock. |
| Certified-gap fixed-face square function | Tuned NAG on one face obeys `sum_t||Cq_t||^2<=[(3+sqrt(5))/(8sqrt(mu))]J_mu` for every fixed exterior cut; the scalar constant is sharp. | The exact future-output Gramian acquires a shifted harmonic Schur lift when the face grows; `P4` shows zero instantaneous interface output does not pay it. |
| Quarter-scale response epochs | Exact fixed-face Gramians give full cut-square and quadratic-variation bounds.  Their moving-face term is one resolvent shifted by `Theta(tau)`, with Chebyshev radius `tau^-1/2`; `tau^(3/2)/alpha` epochs would cost `M tau/alpha`. | Output-sensitive persistence/no-reuse packing of the shifted harmonic response through face events. |
| Positive Poisson clock | `d'=A^-1/2(g-Ad)` is positive, monotone, domain ordered, and root-time convergent. | Sparse application of `A^-1/2`; universal positive walk polynomials need degree `Omega(1/alpha)`. |

These statements may be composed only when the missing operation in the last
column is explicitly supplied and charged.  In particular, neither the
positive reporter nor a spectral sparsifier makes `CenterLift` free.

## C. Strict stops and counterexamples

| Tempting inference | Witness / reason it is false |
|---|---|
| “The formed face has a narrow spectrum.” | Every diagonal is `(1+alpha)/2`, hence `lambda_max>=1/2`; a face with minimum eigenvalue `Theta(alpha)` has condition number `Theta(1/alpha)`. |
| “Measure every current gap and restart CG.” | The canonical ballasted broom has `Theta(1/sqrt(alpha))` large faces, each with gap `Theta(alpha)`, for `Omega(M/alpha)` fresh work. |
| “Warm-started short CG recurrence survives a new coordinate.” | Padded directions keep mutual conjugacy but acquire defect `P^T H_UBg_B`; exact repair is the dense Schur lift.  A three-coordinate path already breaks the unmodified recurrence. |
| “A connected landscape well has one slow scalar.” | A hub joining `r` large cliques is one well but has at least `r` eigenvalues below `alpha+c/W`. |
| “Union--find is the well response state.” | One endpoint added to a path needs the dense vector `(A^-1e_n)_i proportional sinh(i kappa)` with `kappa=Theta(sqrt(alpha))`. |
| “Dynamic terminal Schur equals the active face.” | It maintains `Q_U-Q_UWQ_W^-1Q_WU`, not `Q_U`; on one edge the two values are `alpha/a` and `a`, separated by `Theta(1/alpha)`. |
| “Future Schur energy is relatively bounded by active error energy.” | A reachable canonical two-vertex checkpoint with zero unopened residual has ratio `c^2/(2alpha)`.  The valid repair contains the spectral factor `(A-alpha I)(I-A)/alpha`. |
| “Retune the critical `F0` metric only by scalar weights and replace `sqrt(alpha)` with `sqrt(alpha+tau^2)`.” | The floor-mode energy ratio tends to two; three scalar modes rule out that natural diagonal family.  It does not rule out the proved certified-gap operator `F_mu`, which adds `-c(mu-alpha)S`; `mu` must be a safe face-gap lower bound, not a free cutoff. |
| “A deterministic dynamic hierarchy follow-up removes the small `o(1)`.” | The 2026 proper-router data structure retains `n^(o(1))` overlap/congestion/update factors and stores routes, not a Schur response. |
| “Immediate scratch readiness means the next publication occurs in one product.” | An exact `Q(sqrt(10))` canonical trace on a 34-vertex simple-unit graph has publication times `[0,1,2,3,4,38]` at `alpha=1/1000,rho=1/100000`; every exterior residual at products 5--37 is nonpositive and the final batch is strictly positive.  All lower-subsolution and early-stop tests are certified, and exact elimination proves `S*=V`.  Scratch dominance closes admission only.  This strict recurrence-specific counterexample remains compatible with a shared root clock because `34sqrt(alpha)=1.075`; it is not a lower bound for all algorithms or the target runtime. |
| “The fixed-face quadratic-variation bank splices through face growth.” | On unit `P_3`, adding the third vertex makes the exact remaining-variation Gramian jump strictly for `h=e_1,w=0`, although `Ch=Cw=Cq=0`.  Its hard term is a shifted harmonic resolvent, so no finite multiple of the instantaneous `F0` cut square pays the jump. |
| “Explore an ordinary `tau^-1/2` graph ball to implement the shifted response.” | In the canonical seed--hub--`N`-leaf tree with `rho=2/(N+1)`, the exact obstacle support is only the degree-one seed (`M=1`), while its radius-two ball touches `N+1` edges.  Hop locality alone is not output locality. |
| “One positive point-source Green reservoir dominates every raw NAG hard lift.” | An explicit canonical simple-unit tree makes a raw critical-NAG coordinate negative while both it and the exact solution exceed the publication threshold by more than 25 orders; coefficient isolation on high-degree trees rules out every universal pointwise constant under the same support/threshold hypotheses.  A 39-vertex tree makes the hard lift larger than the full reservoir increment, and at fixed `alpha=.01` high-private-degree paths make their ratio `Omega(1.22745543^t/t)`.  This also defeats payment by past/current raw cut squares on that row.  Exact maximal-batch chronology is not shown, so stopped low-band, future-tail, and chronology-specific routes remain open. |
| “Coordinate clipping restores a significant-coordinate Green upper bracket.” | A finite simple-unit tree has a fixed principal face where exact projected NAG overshoots the exact Green coordinate by `26.5766...`; canonical tiny `rho,epsilon_obj` give `S*=V` and keep both values far above the publication threshold.  The face/time is not proved to occur in the exact maximal-batch chronology. |
| “Fixed-face square functions telescope through mask growth using instantaneous cut and center charges.” | Tuned `P4` has zero old cut, zero expansion-interface output, and zero first two exterior outputs, followed by a strictly positive exterior output.  A canonical `P3` event makes the center charge arbitrarily small while a legal old packet has fixed positive future shifted-resolvent lift.  The `P3` state is not proved reachable from zero, so this is a local-payment stop rather than an algorithmic lower bound. |
| “The shifted `alpha^-1/4` depth implies only `alpha^-1/4` response builds.” | It bounds memory for one fixed load.  A unit path admits `Theta(alpha^-1/2)` significant fresh positive loads with only `O(alpha)` total square mass; independent clique modules add fresh response directions.  Load aggregation/disjoint attenuation is an additional premise. |

The counterexamples are scoped.  They refute the named proof templates or
interfaces, not every possible deterministic graph algorithm.  Paths in
particular compress their dense response by a transfer recurrence, showing
why “dense vector” is not an unconditional lower bound.

## D. General-graph decision boundary

The general target

```text
O_tilde(M/tau+M tau/alpha),
```

and hence `O_tilde(M/sqrt(alpha))`, is proved after either of the following
producer contracts, but neither contract currently has a deterministic
support-local general-graph implementation:

1. `CenterLift(tau)`: persist old-face inverse/Schur responses and emit the
   certified group summaries in `O_tilde(M/tau)` total work; or
2. `AmortizedLowerShiftedApply(tau)`: maintain a certified-lower accelerated
   shifted solve through all visibly positive zero-appends, reducing the active
   residual and rescanning until the global subgradient objective cap holds,
   with total response/rescan work `O_tilde(M/tau)`.  Exact zero-margin
   discovery additionally requires an exact solve or interval refinement.

The low-side reporting ledger `O_tilde(M tau/alpha)` is closed once those
summaries exist.  Therefore the unresolved issue is response production,
not Gaussian candidate detection, normwise solve accuracy, or advance choice
of `tau`.

For reference, the exact clipped optimizer of `A/tau+B tau/alpha` on
`sqrt(alpha)<=tau<=1` is `tau=sqrt(alpha)` when `A<=B`,
`tau=sqrt(A alpha/B)` when `B<=A<=B/alpha`, and `tau=1` when
`A>=B/alpha`.  The respective values are `(A+B)/sqrt(alpha)`,
`2sqrt(AB/alpha)`, and `A+B/alpha`.

With a common certified final-face lower bound `mu_bar`, every supplied
producer contract and the shifted-prox contraction replace the low
denominator by `mu_bar`, giving the conditional curve

```text
A/tau+B tau/mu_bar,       sqrt(mu_bar)<=tau<=1.
```

The same clipped formula holds with `alpha` replaced by `mu_bar`; in
particular `A=B=O_tilde(M)` is minimized at `tau=sqrt(mu_bar)` with value
`O_tilde(M/sqrt(mu_bar))`.  The new `F_mu` theorem makes nonincreasing
certified-gap state transport consistent with this improvement, but it does
not implement either general-graph producer contract.
