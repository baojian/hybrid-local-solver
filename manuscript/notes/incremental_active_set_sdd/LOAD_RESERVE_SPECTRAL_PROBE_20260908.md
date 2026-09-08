# Does a constant load reserve repair coarse spectral support discovery?

Next falsifiable target, **Open until formally checked**. A natural attempt
to avoid accuracy-squared matrix approximation is to solve a constant-quality
M-matrix approximation at a smaller obstacle penalty lambda/C. Could its
larger support then enclose the original significant region? The following
bounded-degree tree construction appears to refute this for every fixed
reserve C. It is a rule-specific obstruction, not an OP3 work lower bound.

## Original finite tree and a rational subsolution

Let G be the complete binary tree of depth D=4R, rooted/seeded at depth 0.
Use physical t=1/2, gamma=1/2, lazy alpha=1/3, and original unweighted
degrees: two at root, three at internal nonroot vertices, one at leaves.
Set q=3/17, K=17/31, lambda=K*q^R/4, e=2lambda, delta=e/8=lambda/4.
For R>=2, vol(G)=2^(4R+2)-4 >4/e; no small-component shortcut applies.

The depth-dependent vector x_i=(K*q^depth(i)-2lambda)_+ has support the
ball of radius R and value 2lambda at every depth-R vertex. On positive
nonroot rows the homogeneous coefficient is

3 - (1/2)/q - q = -1/102 <0.

The constant term contributes -3lambda, so Mx<=b=e_root-lambda*d
on those rows. Clipping negative values to zero only decreases the
boundary rows of Mx. At the root, K(2-q)=1 makes Mx=b exactly.
The maximum principle therefore gives x<=u, the original obstacle.
Every depth-R coordinate has u_i>=2lambda>delta.

## Perturbed matrix with the same row sums

Let L_right be the unit Laplacian of all edges joining a parent to its
right child. Define M_hat=M+(1/4)L_right. Then

M <= M_hat <= (3/2)M,  M_hat*1=M*1=(1/2)d,

since M=(1/2)L+(1/2)D and L_right<=L. The perturbed conductances
are 1/2 on left edges and 3/4 on right edges. Grounding is unchanged.
The graph remains an M-matrix with original-degree nonnegative row sums.

Let g=M_hat^-1 e_root. On a descendant subtree, H denotes its effective
ground conductance, excluding its incoming edge. At a leaf H=1/2.
At internal vertices with children of equal depth it obeys

F(H)=3/2 + (1/2)H/(1/2+H) + (3/4)H/(3/4+H).

One step gives H1=41/20. Two steps give
H2=3/2+41/102+123/224 >83/34. F is increasing and H1>H0, so all
subtrees of depth at least two satisfy H>=H2. The potential transfer
on a left edge is (1/2)/(1/2+H) <17/100. The root grounding is one,
so g_root<=1. Hence at the all-left depth-R vertex w (R<=D-2),

g_w <=(17/100)^R.

This is a finite-tree Schur/flux identity and bound, not an infinite-tree
Green-function import. Check the degree-one leaves and root grounding.

## Why any fixed penalty reserve can still miss w

For C>=1 let u_hat minimize the M_hat obstacle at ORIGINAL-degree load
e_root-(lambda/C)*d. Since u_hat<=g, positivity at w would require

(M_hat)ww * u_hat_w
 = sum_j c_wj*u_hat_j -3lambda/C
 <= (13/4)*g_w -3lambda/C.

Here w has a left incoming edge, two children, and original degree three,
so (M_hat)ww=13/4. Thus u_hat_w=0 whenever

(289/300)^R <=51/(403C).

This follows for large R for every fixed C. An entirely rational choice
is C=2^k, R=64(k+1): verify 8*289^64<300^64 and 403<408, which imply
the displayed inequality for every k>=0. A general C is bounded above
by the next dyadic reserve; increasing the penalty only shrinks support.
Therefore the perturbed, penalty-reserved support can omit an original
significant coordinate despite constant spectral quality, identical row
sums, fixed positive target alpha and original degree at most three.

The support of an exact solve on M_hat at lambda/C is a comparison object,
not a proposed efficient construction. This would refute only the automatic
matrix-replacement-plus-constant-reserve envelope claim. Trees themselves
already have near-linear local algorithms in this note.

## Audit plan

Check the rational coefficient, volume, message lower bound, transfer and
dyadic-reserve inequalities exactly without materializing enormous trees.
For small finite depths, independently solve the original and perturbed
Dirichlet/Green systems and compare the actual left-edge transfer to the
Schur recursion. Keep these finite checks separate from the uniform proof.
Do not run exact rational messages through thousands of levels: their
denominators grow rapidly; the two-step invariant is the certificate.
