# Finite-precision implications: repair certificates, tolerances, and scaling

This note does not change the completed exact-real theorem. It gives proved
end-stage certificate and tolerance statements that can guide a numerical
implementation, and distinguishes them from unresolved floating-point
convergence or work guarantees. All proposed procedures and tests are
deterministic. Only fresh task artifacts and the authorized problem definition
were used.

Write `lambda=alpha*r`, let `x*=x*_r`, and work on the nonnegative objective

    J_r(x)=x^T Qx/2-b^T x+lambda*w^T x.

The graph assumptions give `d_i>=1`, `Qw=alpha*w`, `alpha*I<=Q<=I`, and
absolute row sums one for the degree-scaled Q operator.

## 1. The existing repair tolerates a larger certified objective gap

The completed proof uses `delta=alpha*r/2` at an intermediate stage and the
conservative objective-gap target `alpha^5*r^2/8`. The **same repair**, without
another algorithmic step, is valid at

\[
 \boxed{\tau\le\alpha^4r^2/8.}                            \tag{1}
\]

More generally, for any prescribed `0<delta<=alpha*r/2`, it suffices that

\[
 J_r(\widetilde x)-J_r(x^*)\le\tau,
 \qquad \tau\le\alpha^2\delta^2/2,
 \qquad \widetilde x\ge0.                                \tag{2}
\]

Indeed, the quadratic expansion and KKT give

\[
 \|\widetilde x-x^*\|_Q\le\sqrt{2\tau},\quad
 \|Q(\widetilde x-x^*)\|_2\le\sqrt{2\tau},\quad
 \|\widetilde x-x^*\|_2\le\sqrt{2\tau/\alpha}.
\]

Thus the Q-error is at most `alpha*delta`, while the position error is at
most `sqrt(alpha)*delta<=delta`. For
`bar=[x_tilde-delta*w]_+`, the completed proof's positive-coordinate
inequality becomes

    Qbar_i<=Qx_tilde_i-alpha*delta*w_i<=Qx*_i<=b_i.

The lower-bound property and the error `0<=x*-bar<=2delta*w` hold as before.
The repaired source therefore remains in `[0,2alpha*r*w]`, giving constant
four at a following factor-two regularization decrease. Equation (1) is
just (2) with the prescribed intermediate delta.

This improvement uses a sharper Q-error bound. It does not assume that
ordinary Euclidean error is as small as the Q-error.

## 2. One end-stage projected-gradient step permits alpha-cubed tolerance

A further improvement is available if one adds a single step **after** the
accelerated stage and before repair:

\[
 y=[\widetilde x-\nabla J_r(\widetilde x)]_+,
 \qquad \bar x=[y-\delta w]_+.
\]

For `0<delta<=alpha*r/2`, it suffices that

\[
 \boxed{\tau\le\alpha\delta^2/2.}                         \tag{3}
\]

At an intermediate stage this is

\[
 \boxed{\tau\le\alpha^3r^2/8.}                            \tag{4}
\]

To prove it, let `Delta=x_tilde-y`. Projection optimality and `Q<=I` give
`J_r(x_tilde)-J_r(y)>=||Delta||^2/2`. Consequently
`||Delta||<=sqrt(2tau)`, and `y` retains objective gap at most tau.
The vector

\[
 v=(I-Q)\Delta
\]

is a valid subgradient of `J_r+I_(x>=0)` at y: add the projection normal
`Delta-grad J_r(x_tilde)` to `grad J_r(y)`. In particular, on every positive
y coordinate the normal vanishes, so `grad J_r(y)_i=v_i`. Therefore

\[
 \|v\|_2\le\|\Delta\|_2\le\sqrt{\alpha}\delta\le\lambda/2.
\]

On a positive y coordinate this implies `Qy_i-b_i<=0`; on a zero coordinate
the Stieltjes signs imply it directly. Thus `Qy<=b` globally. Also (3)
gives `||y-x*||_2<=delta`. Clipping by delta is therefore safe, preserves
`Qbar<=b`, and gives `0<=x*-bar<=2delta*w`. All source and final-gap bounds
of the completed repair follow.

This step is not inserted inside the accelerated stage. The Q-metric energy
is not claimed to survive an arbitrary change to the stage recurrence.
After the stage is complete, the separate repair invariant justifies restart.

The added step can be charged locally. Scan the full current candidate
support once; its volume is bounded by the emitted stage history and the
previous baseline. Compute projected-gradient values at the exposed neighbors,
then truncate immediately. Do not scan adjacency lists of newly positive
projected-gradient neighbors before truncation. After the certified repair,
the retained support has volume at most `1/r` and can be scanned to build
the next source. Materializing the intermediate vector itself costs only
its number of exposed entries. In particular, this argument does not grant
a free adjacency scan of its possibly much larger support volume.

## 3. An a posteriori certificate for an inexact projected-gradient step

Floating-point accelerated iterates should not be certified solely by a
floating evaluation of the exact recurrence bound `a^k`. The following
certificate applies to the actual stored candidate, independently of how
it was produced.

Let `x>=0` be that candidate. Compute an approximate gradient `gtilde` and
an approximate nonnegative projected point `y`. Let

\[
 \Delta=x-y,\qquad e_g=g_{\rm tilde}-\nabla J_r(x).
\]

Choose a valid orthant normal `n` at y: it is zero on positive coordinates
and nonpositive on zero coordinates. A convenient explicit choice is

    n_i=0                           if y_i>0,
    n_i=min(Delta_i-gtilde_i,0)          if y_i=0.

Define the projection defect

\[
 e_p=\Delta-g_{\rm tilde}-n.
\]

Then the exact identity

\[
 v:=\nabla J_r(y)+n=(I-Q)\Delta-e_g-e_p
\]

shows that v is a valid subgradient at the actual y. If directed rounding
or another rigorous computation supplies bounds

\[
 D\ge\|\Delta\|_2,\qquad E_g\ge\|e_g\|_2,\qquad E_p\ge\|e_p\|_2,
\]

put

\[
 \boxed{R=(1-\alpha)D+E_g+E_p.}                            \tag{5}
\]

Then

\[
 \boxed{
 J_r(y)-J_r(x^*)\le R^2/(2\alpha),\qquad
 \|y-x^*\|_2\le R/\alpha.
 }                                                        \tag{6}
\]

These follow directly from strong convexity and the subgradient inequality.
They certify the actual numerical point, not an unrounded ideal trajectory.
No Q-product on the newly positive y support is required to compute (5).
Only the old candidate gradient, coordinatewise projection defect, and
weighted sums of squared scalar bounds are needed.

The certificate is naturally evaluated in degree densities. If a gradient
error density is bounded by `e_i`, its contribution to `E_g^2` is
`d_i*e_i^2`; projection and displacement norms use the same rule. Directed
summation can provide an upper bound on each total. Square roots can be
upper-bounded and checked by squaring, or the conservative inequality
`R^2<=3*((1-alpha)^2*D^2+E_g^2+E_p^2)` can avoid them.

All affected gradient coordinates belong to the old candidate support,
its exposed neighbors, and the seed. An unexposed coordinate has the
symbolically known positive gradient `lambda*w_i`, zero projected value,
and zero certificate defect. It must not acquire a fictitious global error
term from pretending that this implicit value was independently rounded at
every vertex of the graph.

A raw minimal-norm subgradient test on an ordinary accelerated primal point
can be misleading operationally: an arbitrarily tiny positive ghost may
retain a gradient of order lambda until it is exactly zero. The projected
point and defect certificate avoid requiring a free adjacency scan to form
its full new gradient.

## 4. A rounded repair with explicit error margins

The certificate in Section 3 yields a convenient robust repair rule.
Choose a represented positive delta satisfying `delta<=lambda/2`. Suppose
that the certified bound satisfies

\[
 \boxed{R\le\alpha\delta/2.}                              \tag{7}
\]

Form the densitywise truncated vector by rounding **downward** from the
ideal clip, with a certified density error kappa:

\[
 0\le\bar x\le[y-\delta w]_+,
 \qquad [y-\delta w]_+-\bar x\le\kappa w,
 \qquad \boxed{\kappa\le\delta/2.}                        \tag{8}
\]

Then the actual stored repaired vector has all the required exact
mathematical properties:

\[
 0\le\bar x\le x^*,\quad Q\bar x\le b,
 \quad 0\le x^*-\bar x\le2\delta w,
 \quad 0\le b-Q\bar x\le2\lambda w.                      \tag{9}
\]

For containment, (6)--(7) give position error at most `delta/2`, and (8)
then gives total loss at most `delta/2+delta+kappa<=2delta`.
For source nonnegativity, on a positive y coordinate the chosen normal is
zero, so `grad J_r(y)_i=v_i<=R<=lambda*w_i/4`. Hence
`Qy_i-b_i<=-3lambda*w_i/4`. At a positive repaired coordinate, clipping
below a uniform shift only helps the Q-product, while the additional
nonuniform downward rounding can raise it by at most `c*kappa*w_i` through
neighbor contributions. Thus

\[
 (Q\bar x)_i\le(Qy)_i-\alpha\delta w_i+c\kappa w_i\le b_i,
\]

because `kappa<=delta/2<=lambda/4` and `c<=1/2`. At zero repaired
coordinates the Stieltjes sign argument applies. The source upper bound
follows from (9)'s position error and the degree-scaled row-sum bound.
The repaired support and final objective error consequently satisfy

\[
 \operatorname{vol}(\operatorname{supp}\bar x)\le1/r,
 \qquad J_r(\bar x)-J_r(x^*)\le2\delta^2/r.
\]

For an intermediate stage, `delta=alpha*r/2` gives the concrete tests
`R<=alpha^2*r/4` and `kappa<=alpha*r/4`. For the final stage, additionally
require `delta^2<=epsilon*r/2`.

One sufficient error-budget split in (5) is

    (1-alpha)*D<=alpha*delta/4,
    E_g<=alpha*delta/8,
    E_p<=alpha*delta/8.

These are sufficient, not necessary, thresholds. Checking their combined
bound is usually less conservative. The input parameters must be treated
as specified numbers; if they themselves are uncertain intervals, their
uncertainty must be included in the gradient-error bounds and a valid lower
bound on alpha must be used for strong convexity.

The mathematical source after (8) is nonnegative. This does not authorize
silently replacing it by an arbitrarily rounded or clipped source in the
next accelerated stage. A numerical implementation must either track source
evaluation errors, use exact arithmetic for this operation, or rely on an
independent end-stage certificate such as (5). A finite-precision version of
the exact theorem's work bound has not been established by this note.

## 5. Lazy scaling: avoid range failure without an uncharged full scan

The lazy representation uses `sigma=a^k`, `xi=sigma*X`, and normalized
response `R=(Q-mu I)xi/sigma`. Although the physical density is boxed, X,
R, and the normalized keys can become large when sigma is small. Direct
floating multiplication of sigma can underflow, and key expressions can
lose significant digits through cancellation before any underflow occurs.
The stopping bound and the physical state scale should be stored separately.

A simple exact rebase is available. Choose a positive factor q, set

    sigma_new=sigma/q,
    X_new=q*X,
    R_new=q*R,
    key_new=q*key.

The physical state, raw values, and projected vector are unchanged. Positive
scaling preserves the key ordering, and weighted key sums scale by q, so
an existing balanced tree can be updated without sorting. Choosing q to
be a power of two avoids new multiplication rounding when representability
and range permit; it does not make underflow or cancellation harmless.

It is acceptable to materialize all currently exposed records for a rebase
provided this extra work is explicitly paid. For example, rebase whenever
sigma has dropped by a fixed factor `2^-b`. A stage with
`K=O(theta^-1*log(1/tau))` needs only `O(1+log(1/tau)/b)` such rebases.
Its number of records is bounded by its charged source and kinetic history.
Hence these full scalar passes add only an allowed logarithmic factor.
They inspect no new adjacency entries. This is simpler to justify than
assuming an unbounded-precision global scale costs nothing in floating point.

Alternatively, mantissa/exponent records and lazy power-of-two scale tags
can postpone materialization. Their arithmetic, interval comparisons, and
range limits must still be specified before claiming an implementation is
numerically robust. A positive key comparison near the threshold cannot
be decided reliably by adopting a fixed ad hoc zero tolerance.

For clipped waterfilling, evaluating the mass as the difference of two large
positive tails may cancel badly. A better numerical form partitions keys
into an interior interval and a saturated tail:

    mass = sigma*sum_(tau<K_i<tau+U/sigma) d_i*(K_i-tau)
           +U*sum_(K_i>=tau+U/sigma) d_i.

The terms are nonnegative. Centered subtree sums or directed intervals can
reduce or certify the remaining subtraction error. Saturation and zero ties
still require a specified comparison/error policy. The exact-real reporter's
correctness does not automatically resolve floating ambiguous comparisons.

## 6. Meaningful deterministic verification

A numerical verification should record, separately at each stage:

* the source nonnegativity and density cap for the actual repaired baseline;
* the gradient, projection-defect, and norm-summation bounds entering (5);
* the repair direction and certified maximum density rounding loss in (8);
* the number and cost of scale rebases, source refreshes, emitted support scans,
  and final materializations;
* any ambiguous waterfill comparison and the precision used to resolve or
  bound it; and
* the final certified objective-gap bound, not just agreement of a few digits.

Small paths, cycles, stars, cliques, and fixed tree/chamber families can be
checked against exact rational or directed high-precision calculations.
Include exact threshold ties, simultaneous box and mass constraints, sources
close to the density cap, and parameter values near a dyadic-momentum change.
These are deterministic tests. A dense reference solve is useful for testing
but is not part of the local algorithm or its charged theorem.

If the certificate fails, the implementation may increase precision or
continue/refine the candidate deterministically. This note proves what a
passing certificate means; it does not prove that a particular fixed-precision
acceleration implementation will always obtain one in the exact theorem's
work bound. Bit growth, rounding accumulation during many stages, and
precision-dependent running time remain separate questions.
