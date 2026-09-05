# Positive linear coupling and a charged volume identity

Date: 2026-09-05. Status: **Proved convergence; local work open.**

This is a separate candidate from the earlier safe-box recurrence. It allows
primal overshoot and asks whether cumulative scanned volume can be paid without
requiring exact-support containment. No randomized operation is involved.

Let `phi(x)=x^TQx/2-c^Tx` on `x>=0`, with the canonical `Q,c`, and put
`s=sqrt(alpha)`. Start `x=z=0` and use

\[
 y=\frac{x+s z}{1+s},\qquad
 x^+=[y-(Qy-c)]_+,\qquad G=y-x^+,
\]
\[
 z_{\rm raw}=(1-s)z+s y-G/s,
 \qquad z^+=\Pi_C(z_{\rm raw}).
\]

Two choices are considered:

- `C=R_+^n` (orthant projection);
- `C={z>=0: w^Tz<=1}`, where `w=sqrt(d)` (mass-constrained projection).

Both contain the unknown optimum. Euclidean projection onto the second set
is deterministic weighted thresholding, requiring a charged sort or a
deterministic selection routine on already materialized nonzero candidates.
It is never supplied as a free global operation.

## Proved here: accelerated potential contraction

For every nonnegative comparator u, the projected-gradient inequality is

\[
 \phi(x^+)\le\phi(u)+G^T(y-u)-\tfrac12\|G\|^2
                        -\tfrac\alpha2\|y-u\|^2.
\]

This follows from strong convexity of phi, its unit smoothness, and the exact
optimality condition of the orthant proximal step. Take comparators x and
`x_rho^*` with weights `1-s` and s. Expand the squared norm of `z_raw-x_rho^*`.
The terms in `||G||^2` cancel, and the remaining linear G term vanishes because

\[
 (1-s^2)y-(1-s)x-s(1-s)z=0.
\]

Projection onto C can only reduce squared distance to the optimum. Hence,
with `E(x,z)=phi(x)-phi(x_rho^*)+alpha||z-x_rho^*||^2/2`,

\[
 E(x^+,z^+)\le(1-s)E(x,z)
 -\tfrac{\alpha(1-s)}2\|y-x\|^2
 -\tfrac{\alpha s(1-s)}2\|z-y\|^2.
\]

This gives `O(alpha^(-1/2) log(alpha/eps_obj))` products on a supplied graph.
It does not yet give local work because supports may contain false activations.

### A local stopping certificate

Completing the square in the same inequality with comparator `x_rho^*` gives

\[
 \phi(x^+)-\phi(x_\rho^*)
 \le \frac{1-\alpha}{2\alpha}\|G\|^2.
\]

The residual vector G is available from the product and proximal step already
performed; outside their materialized union it is identically zero. Thus this
certificate requires no ambient graph scan. Since the projected-gradient map
is nonexpansive, `||G||<=2||y-x_rho^*||`, and convexity of the squared norm gives
`||y-x_rho^*||^2<=2E/alpha`. Consequently the displayed certificate is at most
`4E/alpha^2`. It reaches any prescribed positive objective tolerance after
`O(alpha^(-1/2) log(1/(alpha eps_obj)))` steps from the zero start. This coarse
bound is sufficient for logarithmic accuracy dependence and does not assume
a complementarity margin.

## Proved here: auxiliary support needs no additional adjacency scans

The raw update simplifies exactly to

\[
 z_{\rm raw}=\frac{x^+-(1-s)x}{s}.
\]

For either C, the projection is coordinatewise at most `[z_raw]_+`. Therefore
`supp(z^+) subseteq supp(x^+)`. Every vector whose matrix product is taken
has support inside the current primal support, because
`supp(y) subseteq supp(x)` inductively. Candidate boundary coordinates are
computed by scanning those rows, and do not need their own rows until a
subsequent product.

## Proved here: exact location of the missing volume charge

Write `X_k=w^Tx_k`, `Z_k=w^Tz_k`, and `V_k=vol(supp(x_k))`.
Since `I-Q>=0` entrywise, `w^T(I-Q)=(1-alpha)w^T`, and y is nonnegative,

\[
 \alpha\rho V_{k+1}
 \le\alpha+(1-s)(X_k+sZ_k)-X_{k+1}.
\]

Define the dropped primal mass

\[
 D_k=w^T[(1-s)x_k-x_{k+1}]_+.
\]

For orthant projection,
`s Z_(k+1)=X_(k+1)-(1-s)X_k+D_k`. Summing the previous inequality gives

\[
 \alpha\rho\sum_{k=0}^{T-1}V_{k+1}
 \le\alpha T+\sum_{k=0}^{T-1}D_k
       -\alpha\sum_{k=0}^{T-1}Z_k-s Z_T.
\]

Thus a bound `sum D_k=O_tilde(alpha T)` would imply the desired cumulative
degree work. It is an **open** lemma, not a consequence of the energy
contraction above. The weights w can be large, and an unjustified Euclidean
to weighted-L1 conversion would lose locality.

For the mass-constrained projection, define the removed auxiliary mass
`P_k=w^T([z_raw]_+-Pi_C(z_raw))>=0`. The exact right side changes from
`sum D_k` to `sum (D_k-s P_k)`. Both primal and auxiliary masses are at most
one: for the primal, the displayed inequality without its nonnegative volume
term gives `X_(k+1)<=(1-s)X_k+s` when `Z_k<=1`.

The stronger useful open interface is consequently

\[
 \sum_{k<T}(D_k-sP_k)\le\widetilde O(\alpha T)
       +\alpha\sum_{k<T}Z_k+s Z_T.
\]

No claim is made that mass capping proves this inequality. It removes an
unbounded-mass failure mode while preserving the accelerated potential.

### Proved here: a weaker fully local bound

Retaining the projection's Pythagorean decrement in the potential proof gives

\[
 \frac\alpha2\sum_{k<T}\|z_{k+1}-z_{{\rm raw},k}\|^2\le E_0.
\]

On every negative raw coordinate the projected vector is zero, and those
coordinates are contained in `supp(x_k)`. With `W=sum_(k<T) V_(k+1)` and
`sum_(k<T)V_k<=W` from the zero start, Cauchy--Schwarz therefore gives

\[
 \sum_{k<T}D_k
 \le s\sqrt{W}\sqrt{2E_0/\alpha}
 =\sqrt{2E_0 W}.
\]

Discarding the favorable mass-cap and auxiliary terms in the exact ledger,
then using Young's inequality, proves

\[
 W\le\frac{2T}{\rho}+\frac{2E_0}{\alpha^2\rho^2}.
\]

This holds for both auxiliary projections. It is independent of ambient
graph size, but its second term does **not** meet OP2. In particular the
general zero-start bound is only `E_0<=alpha/d_seed`, not the smaller
`O(alpha^2/d_seed)` that one observes on well-grounded tree quotients. The
weaker bound must not be advertised as the desired accelerated locality.

### Checked local implementation

`experiments/local_positive_coupling.py` uses only degree replies and active
row scans, in degree coordinates. It sorts and merges all contributions
deterministically; no expected-time hash-table oracle is used in its work
claim. Boundary rows are not scanned merely because their labels or degrees
are observed. Every stopping certificate is computed from already generated
coordinates. The ledger charges all such work, sorting, state, and output.

`audit_local_positive_coupling.py` passed 1,233 canonical graph-atlas cases
(all connected graphs on 2--5 vertices, every seed, nine parameter pairs).
It independently checked output objective gaps, exact neighbor/degree call
counts, and agreement with the dense recurrence at the same iteration.
The largest relative iterate discrepancy was about `2.24e-13`. Labels were
reassigned to noncontiguous integers to check that vertex-array assumptions
did not leak into the local solver.

## Deterministic computational audits (not a locality theorem)

The connected graph-atlas campaign started at
`2026-09-05T02:31:12.761992+00:00`, with a 36,000-second computation limit and
no repeated-case padding. Its source snapshots, hashes, cases, and checkpoint
are in `results/plc-atlas-campaign/`. It checks both variants on every seed,
deterministic values `alpha=1/m^2`, and points on both sides of numerical exact
regularization-path support transitions.

A separate radial-tree census completed 6,604 cases. Every quotient represents
a finite canonical unit tree; all work ledgers use original vertex counts and
ambient degrees, not the quotient's dimension. The audit tolerance was
`eps_obj=10^(-12)` times the reference initial objective gap. All cases met the
computed stopping certificate; the potential and volume identities passed to
floating-point tolerance. Exact/high-precision certification remains necessary
before treating any individual adverse history as a theorem.

The strongest observed normalized work `rho sqrt(alpha) sum V_k` was about
22.59 with the mass constraint and 1497.60 without it. The largest capped
prefix average `rho sum V_k/k` was about 21.71, on a depth-64 ten-ary tree at
`alpha=10^(-4)`. Its total normalized work was about 15.64. This distinguishes
the desired whole-run work bound from the stronger, now numerically implausible,
uniform-per-iteration bound. No graph-uniform constant or polylogarithmic
bound follows from these numbers.

## Next checks

Derive and test the cumulative volume identity on canonical point-source
histories, first on paths, stars, deep radial trees, combs, and clique chains.
Count row scans, boundary-candidate words, projection work, and certificate
work. Seek a whole-run argument for the displayed signed mass debit, or a
canonical counterexample that identifies why it fails. Finite positive tests
will not be promoted to a graph-uniform theorem.
