# A total-Laplacian-flow obstruction for zero-started lazy capped acceleration

Status: a proved asymptotic counterexample to the stronger total-flow
sufficient condition proposed in `capped_positive_error_flow_ledger.md`.
This is **not** a counterexample to OP2, to the cumulative auxiliary-support
bound, or to the selected signed-flow ledger in that note. In particular,
the lower bound below counts divergence at stopped position coordinates.

Only the original authorized problem definition and the fresh notes
`lazy_capped_acceleration.md` and `capped_positive_error_flow_ledger.md`
were consulted. Everything here is deterministic. No experiment is used
in the proof.

## 1. Family and statement

Let `n>=7`, `L=2^n`, and choose

    theta=1/L, alpha=1/L^2, a=1-theta,
    rho=L^(-128), lambda=alpha*rho=L^(-130),
    H=132*n, Kiter=8*L, c=(1-alpha)/2.

The graph is the complete rooted binary tree of depth H, with its root
as seed. Its layer j contains `2^j` vertices. Degrees are 2 at the root,
3 at interior vertices, and 1 at leaves. It has `O(L^132)` vertices, so
all logarithms of graph size, exposed size, inverse alpha, and inverse
rho are `O(log L)`.

Run the ordinary lazy capped iteration from zero. In mass coordinates
`u=D^(1/2)x`, `V=theta*D^(1/2)z`, its update is

    q = a/2 * [P*(u+V)-(u-V)] + alpha*e_seed-lambda*d,
    Vnew_i = [q_i-eta*d_i]_+,
    unew = a*u+Vnew,                                  (1)

where eta is the nonnegative weighted-simplex multiplier making
`sum Vnew<=theta`, with equality whenever eta is positive.

The actual initialized trajectory satisfies

    c * sum_(k=0)^(Kiter-1) ||(I-P)u_k||_1
        >= 1/(2376*n).                               (2)

Consequently no bound of the form

    c * sum_k ||(I-P)u_k||_1
        <= theta * polylog(1/alpha,1/rho,graph size)

can hold universally over `O(1/theta)` initialized iterations. For any
fixed polynomial in these logarithms, its right side is
`O(polylog(L)/L)`, whereas (2) is `Omega(1/log L)`.

## 2. Basic invariants and radial symmetry

The simplex cap and the convex-combination primal update imply

    u>=V>=0, sum u<=1, sum V<=theta.                   (3)

The coordinatewise inequality follows immediately from
`unew=a*u+Vnew`. Since the seed, degrees, and projection are invariant
under every rooted-tree automorphism, the unique projected iterate is
constant on every layer. We use `u_j,V_j` for total layer masses below.

Starting from zero, `u_k,V_k` are supported on layers at most `k-1`.
Indeed one update propagates through at most one graph edge, and a
coordinate with zero input, zero seed term, and no incoming neighbor
mass has a strictly negative raw value.

If the cap binds on a transition, `sum Vnew=theta`; hence the next
position has total mass at least theta. This observation will allow
an uncapped lower recurrence to force an early theta-mass hitting time.

## 3. A weighted moment forces mass theta by time 64*n

Put

    gamma=11/10, b0=2*gamma=11/5,
    beta=(gamma^(-1)+2*gamma)/3=57/55,
    h=2/15, r=23/20, t=a*r.

Let

    U_k=sum_j gamma^j*u_(k,j),
    W_k=sum_j gamma^j*V_(k,j).

For the radial weight `phi_j=gamma^j`, a nonroot nonleaf vertex has
`(P^T phi)_j=beta*phi_j`. At the root the multiplier is gamma, which
exceeds beta. Thus `P^T phi>=beta*phi` on all nonleaf layers.

Suppose for contradiction that `sum u_k<theta` for every
`1<=k<=k0=64*n`. Every cap used to produce these iterates is then
nonbinding. Also `k0<H`, so finite propagation avoids all leaves.
For a transition `k -> k+1` with `1<=k<k0`, sum the inequality
`[q_i]_+>=q_i` only over layers up to k, which contain the old support
and its neighboring layer. This avoids charging negative regularization
terms at unreachable vertices. The weighted degree in these layers is

    2+3*sum_(j=1)^k b0^j <= 6*b0^k.                  (4)

Dropping the nonnegative seed input after the first step gives

    [U_(k+1)]      [(beta+1)/2  (beta+1)/2] [U_k]
    [W_(k+1)] >= a*[(beta-1)/2  (beta+1)/2] [W_k]
                   -6*lambda*b0^k*[1,1]^T.           (5)

All matrix entries in (5) are nonnegative. If its displayed matrix is
M, direct rational arithmetic gives

    (M*[1,h]^T)_1 = 952/825 > 23/20 = r,
    (M*[1,h]^T)_2/h = 127/110 > 23/20 = r.           (6)

Set `m_k=min(U_k,W_k/h)`. Equations (5)-(6) imply

    m_(k+1) >= t*m_k-45*lambda*b0^k.                 (7)

At the first step, the only nonzero coordinate is the root and
`u_1=V_1=alpha*(1-2*rho)` there. The cap is nonbinding, since this is
smaller than theta. Thus `m_1>=alpha/2`. Unrolling (7), and using
`b0-t>=b0-r=21/20`, yields the convenient loose estimate

    m_k >= (alpha/2)*t^(k-1)-60*lambda*b0^k.          (8)

Because all position mass lies at depth at most k-1,
`U_k<=gamma^k*sum u_k`. As `U_k>=m_k`, equation (8) gives

    sum u_k >= alpha/(2*t)*(t/gamma)^k
                       -60*alpha*rho*2^k.           (9)

For L at least 128,

    t/gamma = a*(23/22)
        >= (127/128)*(23/22) > 33/32.                (10)

The binomial theorem gives `(33/32)^32>2`; therefore
`(33/32)^(64*n)>L^2`. At `k=k0`, the first term in (9) exceeds
`1/(2*t)>=10/23`, and the second equals `60*L^(-66)`.
Thus `sum u_k0>1/3>theta`, contradicting the supposition.

We have proved that some index `k_*<=64*n` satisfies

    sum u_(k_*) >= theta.                            (11)

Notice that the proof did not assume that a cap actually binds: either
a cap produces theta mass, or the uncapped weighted-moment growth
forces a theta-mass crossing first.

## 4. Leaves never activate

At the leaf layer, (3) bounds the aggregate raw value by

    q_H <= a/2 * (P*(u+V))_H-lambda*2^H
        <= a*(1+theta)/2-lambda*2^H
        = c-L^2 < 0.                                (12)

Here the nonpositive term `-a*(u_H-V_H)/2` was dropped, and the seed is
not a leaf. Radial symmetry makes every individual leaf raw value
equal; therefore the negative aggregate implies that every leaf is
clipped to zero. The additional cap subtraction can only decrease it.
Induction from zero now shows `u_H=V_H=0` at every iteration.

This claim is about the algorithm's actual trajectory, not a choice
to delete vertices or replace the graph by an infinite tree.

## 5. Distance drift turns persistent mass into total flow

Let `psi_i` be distance from the root, so `0<=psi_i<=H`. Its one-step
outward drift under P is 1 at the root, 1/3 at every interior vertex,
and -1 at the leaves. The leaves carry zero position mass by (12).
Consequently

    <psi,(P-I)u>
       =u_0+(1/3)*sum_(j=1)^(H-1)u_j
       >= (1/3)*sum u.

Holder's inequality implies

    ||(I-P)u||_1 >= (sum u)/(3*H).                   (13)

The lazy primal update is coordinatewise at least `a*u`. Hence for
`0<=j<L`, equation (11) implies

    sum u_(k_*+j) >= theta*a^j.

Summing this geometric lower bound gives

    sum_(j=0)^(L-1) sum u_(k_*+j)
       >= 1-a^L > 1/2.                              (14)

For example, the last strict inequality follows from the binomial
theorem applied to `(1+1/(L-1))^(L-1)>=2`, which implies
`a^(L-1)<=1/2` and `a^L<1/2`.

Since `c>=1/3`, equations (13)-(14) yield

    c*sum_(j=0)^(L-1) ||(I-P)u_(k_*+j)||_1
       > 1/(18*H)=1/(2376*n).

Finally, `64*n+L<=8*L` for every `n>=7`, so the entire interval is
included among indices `0,...,Kiter-1`. This proves (2).

## 6. What this rules out, and what it leaves open

This result rules out funding the ordinary lazy capped algorithm by a
universal small bound on **all** accumulated Laplacian variation. It
also rules out proving that particular bound using entropy or a
spectral argument without additional restrictions, since the bound
itself is false for an initialized deterministic trajectory.

The argument supplies no lower bound of the forbidden order on

    rho*theta*sum_k vol(supp V_k).

The lower-bound mass can persist after its auxiliary coordinates stop,
and the total divergence can occur where no new auxiliary coordinate
is selected. The selected signed-flow ledger explicitly discards such
unselected forcing and retains helpful cap and killed-transport terms.
It is therefore not contradicted. Nor does this proof directly apply
to the monotone segment-search primal rule: that rule retains the
weaker persistence `unew>=a*u`, but it loses `u>=V` and the implication
that a binding auxiliary cap produces primal mass at least theta.
Those two properties are used in sections 3 and 4.

There is also a direct obstruction to the unselected positive-error
forcing bound, not merely to its total-flow relaxation. In the notation
of `capped_positive_error_flow_ledger.md`, let

    f_k=[a/2*(P-I)*(u_k-u*)]_+.

Every Laplacian vector has zero total sum, so

    ||f_k||_1 = a/4*||(P-I)*(u_k-u*)||_1
      >= [c*||(I-P)u_k||_1/2-alpha]/(1+theta),        (15)

where the optimum bound `c*||(I-P)u*||_1<=2*alpha`
was used. Summing (15) over `Kiter=8*L` and using (2) yields

    sum_k ||f_k||_1
       >= [1/(4752*n)-8/L]/(1+theta).                (16)

For every `n>=21`, `2^n>=76032*n`; hence the right side is at least
`1/[9504*(1+theta)*n]>=1/(19008*n)`. Thus a universal
`sum ||f_k||_1 <= theta*polylog(parameters)` is false as well.
Only the further selection and cancellation in the signed-flow ledger
escape this counterexample.

## 7. Separate deterministic numerical diagnostics

`binary_tree_flux_probe.py` implements the exact radial quotient formulas
with floating-point arithmetic. Its outputs are observations, not exact
support certificates or ingredients of the proof. The script explicitly
rejects parameters beyond its floating exponent range.

For the less conservative empirical family `rho=L^-4`, `H=8*log2(L)`,
and `Kiter=8*L`, the saved file `binary_tree_flux_rho4.json` reports:

| L | cumulative c-total-flow | rho*theta*sum vol(Z) | binding caps |
|---:|---:|---:|---:|
| 32 | 0.81808 | 4.64364 | 0 |
| 64 | 0.79246 | 5.16062 | 0 |
| 128 | 0.81968 | 5.37121 | 7 |
| 256 | 0.80545 | 4.90479 | 11 |
| 512 | 0.79470 | 4.42023 | 12 |
| 1024 | 0.78946 | 3.92501 | 14 |

The final auxiliary support is nonempty in all these runs, with
`rho*vol(Z_final)` approaching 0.75. Thus these finite diagnostics show
large total flow alongside moderate normalized support work.

For the exact theorem's family at `L=128`, the saved file
`binary_tree_flux_rho128.json` reports total flow 6.77578, 987 binding
caps, nonempty final auxiliary support, and normalized support work
about `6.46e-178`. The final auxiliary mass equals its cap up to
floating arithmetic. This small normalized-work value results from
the extremely small rho chosen to make the proof simple; it is not
an asymptotic assertion about support work.
