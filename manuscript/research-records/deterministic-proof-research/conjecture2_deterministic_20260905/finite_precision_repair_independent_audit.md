# Independent audit of the numerical repair certificates

Reviewed Sections 1--4 of the fresh
`finite_precision_repair_and_scaling.md`. The note does not change the
exact-word theorem or assert a finite-precision work bound. All four
sections pass this independent mathematical audit.

## 1. Sharper direct-repair tolerance

For e=xtilde-x*, nonnegative feasibility and obstacle KKT give

    J(xtilde)-J(x*)=.5 e^TQe+r*^T xtilde >=.5 e^TQe.

Because Q²<=Q, gap tau bounds the Euclidean Q-error by sqrt(2tau), while
strong convexity bounds the position error by sqrt(2tau/alpha).
Thus tau<=alpha²delta²/2 gives Q-error<=alpha*delta and position error
<=sqrt(alpha)*delta<=delta, exactly the two estimates direct repair needs.
The resulting intermediate tolerance alpha^4*r²/8 is correct.

## 2. One exact end-stage projected-gradient step

For y=[x-grad J(x)]_+ and Delta=x-y, projection optimality against the
feasible x gives grad J(x)^T Delta>=||Delta||². One-smoothness therefore
implies J(x)-J(y)>=||Delta||²/2, so ||Delta||<=sqrt(2tau) when x's gap is
tau, and y's gap remains at most tau.

The projection normal is n=Delta-grad J(x), nonpositive on zero y
coordinates and zero on positive ones. Therefore

    grad J(y)+n=(I-Q)Delta.

On positive y coordinates the gradient equals this subgradient. With
`tau<=alpha*delta²/2` and `delta<=lambda/2`, its magnitude is at most
`sqrt(alpha)*delta<=lambda/2`. Thus Qy<=b on positive coordinates;
Stieltjes signs prove it on zero coordinates. Strong convexity also gives
||y-x*||<=delta. Uniform density clipping by delta is therefore safe and
preserves source nonnegativity. The intermediate tolerance
alpha^3*r²/8 and final error bound 2delta²/r are correct.

This is an end-stage operation, so it need not preserve the auxiliary
accelerated energy. Restart uses the separately proved repaired-source
invariant.

## 3. Inexact projected-step certificate

For the actual represented x,y and approximate gradient gtilde, let

    eg=gtilde-grad J(x),
    ep=Delta-gtilde-n,

where n is any valid orthant normal at y. The note's coordinatewise
choice of n has the correct sign. Substituting these definitions gives
exactly

    grad J(y)+n=(I-Q)Delta-eg-ep.

No gradient evaluation at y is implicit in this identity. Therefore
`R=(1-alpha)D+Eg+Ep` bounds a valid subgradient norm at y. Strong convexity
then gives both `gap(y)<=R²/(2alpha)` and `||y-x*||<=R/alpha`.

In degree densities, the norm weights are d_i, not 1/d_i. All displacement,
gradient-error, and projection-defect norms can be formed over the old
candidate, its one-hop neighbors, and the seed, provided the implementation
keeps y zero at unexposed coordinates. Outside that region, the exact
symbolic positive gradient lambda*w is canceled by an equally symbolic
valid lower normal. It does not introduce a global error norm.

This symbolic treatment is necessary: independently rounding an implicit
gradient on every unseen vertex would introduce an unjustified graph-wide
error term. The note explicitly avoids doing so.

## 4. Rounded repair

The hypotheses `R<=alpha*delta/2`, `delta<=lambda/2`, and a downward density
rounding loss `kappa<=delta/2` imply position error at most delta/2 before
repair. Consequently the represented repaired vector is below x* and loses
at most 2delta in density.

On a positive y coordinate, the normal is zero, so

    grad J(y)_i<=R<=lambda*w_i/4,
    (Qy-b)_i<=-3lambda*w_i/4.

For the ideal clip u=[y-delta*w]_+ and actual bar=u-h, with
0<=h<=kappa*w, a positive bar coordinate satisfies

    (Qbar)_i <= (Qy)_i-alpha*delta*w_i+c*kappa*w_i.

The possible increase comes only from negative off-diagonal neighbor
terms; the diagonal contribution -q0*h_i is nonpositive. Since
`c*kappa<=lambda/8`, the existing margin is more than sufficient for
Qbar<=b. Zero bar coordinates are covered directly by Stieltjes signs.
The source upper bound and quadratic final gap follow from the 2delta
density error. All stated constants are valid, with slack.

## 5. Local charge and unproved scope

Computing the extra gradient requires one scan of the old candidate's
support. That support is contained in the old baseline plus the accumulated
emitted correction supports, whose degree volume is already charged.
Forming y and its coordinatewise defect requires only exposed scalar
records. Newly positive y vertices must be truncated before any scan of
their adjacency lists. After a passing repair their retained degree volume
is at most 1/r, making the next source scan local.

The note proves the consequences of a passing certificate. It does not
prove that fixed-precision acceleration reaches one in the target number
of iterations, that the exact second energy survives roundoff, or that
precision retries preserve the exact theorem's complexity. Those gaps
are correctly left explicit rather than treated as consequences of these
end-stage lemmas.
