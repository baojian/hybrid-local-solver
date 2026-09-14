# The convex information contained in the RPPR mass/support identity

This is a proved deterministic geometric observation. It does not establish
the missing support-work theorem for capped acceleration.

Let `w_i=sqrt(d_i)` and use mass coordinates `u_i=w_i*x_i`. The RPPR
optimum obeys

    sum_i u_i + rho*sum_(u_i>0)d_i <= 1.             (1)

Thus vertices with `rho*d_i>=1` cannot belong to a nonzero optimum.
Put `c_i=1-rho*d_i` for the remaining vertices.

## Exact closed convex hull without the mandatory seed

The closed convex hull of all nonnegative vectors satisfying (1) is

    u_i=0 when c_i<=0,
    sum_(c_i>0) u_i/c_i <= 1.                       (2)

To prove inclusion, let S be the support of a feasible vector and
`c_S=1-rho*vol(S)`. If the vector is nonzero, c_S>0. For i in S,
`c_i>=c_S`, whence

    sum_i u_i/c_i <= (sum_i u_i)/c_S <=1.

Conversely, the origin and each axis vertex `c_i*e_i` satisfy (1).
Every vector in (2) is their convex combination. This proves equality,
and in the finite graph setting the hull is already closed.

In x coordinates the resulting valid convex cap is

    sum_i w_i*x_i/(1-rho*d_i) <=1.                  (3)

The cap is strictly stronger than `w^T x<=1`, and automatically yields
the degree exclusion. It is the strongest convex consequence of (1)
alone; any stronger universal convex set must use additional information.

## Including the known seed support

In the nonzero RPPR regime the seed s is positive. Define

    c_s=1-rho*d_s,
    c_i=1-rho*(d_s+d_i),  i!=s.

Every optimum is zero at a nonseed coordinate with c_i<=0. This gives
the stronger safe degree guard `d_i<1/rho-d_s` for nonseed admissions.
The same argument proves the valid cap

    u_s/c_s + sum_(i!=s,c_i>0)u_i/c_i <=1.           (4)

Indeed, for a support S containing s, each denominator in (4) is at
least `1-rho*vol(S)`, and (1) applies. Formula (4) is the closed convex
hull obtained from (1), the positive-seed requirement, and the origin.
For each nonseed i with c_i>0, points supported on {s,i} with
`u_s=epsilon`, `u_i=c_i-epsilon` tend to the axis vertex `c_i*e_i`.
The seed axis vertex is feasible directly. These vertices generate (4).

The word “closed” matters for the mandatory-seed version: the limiting
nonseed axis vertex itself has zero seed coordinate.

## Algorithmic limits of this observation

These weighted simplexes are convex and downward closed, so either can
replace the ordinary mass cap in the previously proved averaging or
aligned acceleration convergence proof. One may also intersect them
with other certified coordinate bounds.

This does not grant the same lazy threshold reporter at no cost. For
the modified cap, the projection weights are `w_i/c_i`, whereas the
linear regularization weights remain w_i. After division by the new
projection weights, the additive regularization offset becomes
`theta*rho*c_i`, which differs between degrees. The single shared affine
key ordering used for the original cap therefore requires a new argument
or a different deterministic data structure. A full sort of all old
exposed records each iteration cannot be hidden.

The degree guards themselves only require the already charged degree
reply when a neighbor is first exposed. They do not require scanning
that neighbor's adjacency list. On bounded-degree graphs with small rho,
the denominators are close to one, so this improvement alone does not
resolve the observed broad, short-lived auxiliary waves.
