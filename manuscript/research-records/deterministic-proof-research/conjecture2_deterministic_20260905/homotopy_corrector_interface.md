# Whole-component truncation and the cost of homotopy responses

This note develops a corrector interface from the exact positive,
`Q`-orthogonal derivative jumps proved in `homotopy_geometry.md`. It does
not supply the missing persistent response data structure or prove OP2.

Use increasing homotopy time `t=-rho`. Start above the first activation,
where the optimizer and derivative are zero. If the derivative jumps are
`p_j=Delta g_j>=0` at times `s_j`, then

\[
 x(t)=\sum_{s_j<t}(t-s_j)p_j,\qquad
 \langle p_i,p_j\rangle_Q=0\ (i\ne j),\qquad
 \|p_j\|_Q^2=\alpha m_j,\quad m_j=w^Tp_j.
\]

## 1. Exact energy accounting for whole-component omission

For any coefficients `0<=zeta_j<=1`, let

\[
 \widetilde x(t)=\sum_{s_j<t}\zeta_j(t-s_j)p_j.
\]

Then `0<=xtilde<=x(t)`, its support lies in the true support, and

\[
 \boxed{\quad
 J_{-t}(\widetilde x)-J_{-t}(x(t))
 =\frac\alpha2\sum_{s_j<t}(1-\zeta_j)^2(t-s_j)^2m_j.
 \quad}
\]

The linear KKT term vanishes because the approximation is supported inside
the true support, and orthogonality gives the displayed sum. No cross
terms appear. This is the precise advantage of omitting whole derivative
components rather than truncating their coordinates independently.

## 2. An age cutoff also preserves exact stationarity on the retained core

For a cutoff age `tau>0`, retain precisely the jumps with `s_j<t-tau`.
Then

\[
 \widetilde x(t)=x(t-\tau)+\tau g((t-\tau)^-),
 \qquad 0\le\widetilde x(t)\le x(t).
\]

Here the left derivative omits any newly entering zero coordinate at the
cutoff itself. Including an admission exactly at the cutoff instead uses
the right derivative and adds its whole component consistently.
The retained support is the support immediately after the last retained
admission. On that support the current residual is exactly zero, because
`Qp_j` vanishes on every earlier support for each omitted jump.

Writing `e=x(t)-xtilde(t)` and
`Delta g_young=g(t)-g((t-tau)^-)`, one also has

\[
 0\le e\le\tau\Delta g_{\rm young}\le\tau w,
 \qquad
 \|e\|_Q^2\le\alpha\tau w^Te
                 \le\alpha\tau^2w^T\Delta g_{\rm young}.
\]

Thus an age cutoff gives a safe, exactly stationary predictor on its
retained core, together with a box and an energy certificate expressed in
the omitted derivative mass. If only the universal bound
`w^T Delta g_young <= 1/rho` is used, choosing
`tau=O(sqrt(alpha)*rho)` reaches the late-phase energy scale
`O(alpha^2*rho)`.

This is an exact representation theorem. It is not an algorithm that can
identify or evaluate all jumps older than the cutoff without paying for
their discovery and responses.

## 3. Arbitrary component masks need not preserve the subsolution residual

Although every componentwise mask above remains below the true optimizer,
it need not have nonpositive gradient on its own positive support. For
example, retain a later component `c2*p2` but omit an earlier `c1*p1`.
On the later admission set `B2`, the missing component contributes

\[
 \nabla J(\widetilde x)_{B_2}=-c_1(Qp_1)_{B_2}.
\]

When `B2` is adjacent to the earlier support, the right side is strictly
positive. An algorithm that requires a subsolution cannot silently use an
arbitrary energy-based component mask. Retaining an age prefix avoids
this problem.

## 4. Explicit harmonic-response output cannot be charged only to jump mass

Suppose one new vertex `i` is admitted to a connected old support `S`, and
it has an edge into `S`. The derivative jump has the block form

\[
 p_i=\beta>0,\qquad
 p_S=-\beta Q_{SS}^{-1}Q_{Si}.
\]

The inverse of the irreducible principal Stieltjes matrix is strictly
positive. Therefore **every coordinate on the old support changes**.
Materializing the exact response requires at least `|S|` scalar writes,
even if the response decays rapidly and its total mass is small.

For example, on a path with a fixed `alpha` bounded away from zero, a
single-vertex admission has uniformly bounded derivative-jump mass. Indeed,
the jump's positive residual is supported only at the new vertex, and

\[
 \alpha w^Tp=\|p\|_Q^2=p_i(Qp)_i
 \le Q_{ii}p_i^2\le Q_{ii}d_i=O(1).
\]

Nevertheless, the response is strictly positive on an arbitrarily long
connected old prefix. Consecutive admissions can thus demand quadratic
explicit response output while their total derivative mass is linear in
the final support volume.

This is an obstruction to a response oracle charged solely to derivative
mass or positive source mass. It is not a lower bound on OP2: on such a
path the relation between `rho` and the final support may leave a much
larger allowed `1/rho` budget, and a lazy representation can avoid these
explicit writes.

An implicit record consisting of a new admission block, its local source,
and a pointer to the old restricted operator is small, but answering a
coordinate response or boundary-threshold query from that record still
requires an actual algorithm. Declaring the response implicit does not
make those solves or queries free.

## 5. Precise remaining interface

A useful deterministic corrector must jointly provide:

1. A representation of retained whole components, or certified
   approximations to them, that preserves their energy accounting.
2. Paid boundary queries sufficient to discover components whose age is
   above the chosen cutoff.
3. A total read, update, and output bound tied to the new support volume
   and to the positive curvature/source budgets, rather than to all old
   response coordinates on every admission.

The exact component energy theorem and the age-prefix stationarity theorem
are proved above. Such a fully charged persistent corrector remains open
in this work.
