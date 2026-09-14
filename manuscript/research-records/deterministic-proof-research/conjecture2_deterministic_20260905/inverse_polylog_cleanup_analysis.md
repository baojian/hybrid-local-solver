# Inverse-polylogarithmic relative cleanup: proved bounds and limitations

Status: no general initial kinetic-work theorem, and no initialized asymptotic
counterexample, is proved here. The results below are deterministic. They give
(i) the explicit cleanup cost, (ii) a barrier to the simplest unsubdivided-tree
amplification, (iii) a quantitative obstruction to extending that barrier after
edge subdivision, and (iv) a connected feasible-state counterexample to bounds
using only the cleanup, cap, and nonpositive-objective invariants. The last
result starts from an expensive supplied state and is NOT an OP2 lower bound.

Use degree densities f_i=x_i/sqrt(d_i), theta=sqrt(alpha), a=1-theta,
c=(1-alpha)/2, q0=(1+alpha)/2, lambda=alpha*rho, and tau=lambda/8. The normalized
Laplacian acting on densities is L=I-D^(-1)A. At every positive coordinate after
cleanup,

    alpha*f_i+c*(Lf)_i-alpha*1{i=s}/d_i+lambda
        <=beta*q0*f_i+tau.                            (1)

Write kappa=beta*q0-alpha when this quantity is positive.

## 1. What inverse-polylog beta does prove about cleanup cost

A cleanup that leaves a coordinate positive satisfies

    fnew <= (1-beta)*f-tau/q0.

A final zeroing contributes at most one additional event per epoch between
positive kinetic additions. Thus the total cleanup volume is at most

    O(1+beta^(-1)*log(1+beta*q0/tau))

 times the initial support volume plus cumulative kinetic-support volume.
For beta=log^(-C)(1/(alpha*rho*epsilon)) with fixed C, this overhead is
polylogarithmic in the displayed parameters. This verifies the implementation
reduction but does not bound the kinetic-support volume being multiplied.

A direct global mass/flow relaxation still leaves a term of order
kappa*sum_k mass(u_k). Choosing inverse-polylog beta does not by itself make
this term of order theta times polylogarithms. A trajectory argument with
additional cancellation or propagation information is needed.

## 2. A static barrier on an unsubdivided binary prefix

Consider a complete binary prefix of depth h>=1, each leaf joined to the port
of a clique with R vertices. The port has degree R, the prefix leaf degree2,
and the other R-1 clique vertices degree R-1. Suppose a cleaned primal point
has zero density on all nonport clique vertices. It may have arbitrary support
on the prefix and ports. Put

    s=max(beta*q0-alpha,0)/c,
    s'=s+1/R <=1/32.

Let r be the smaller root of

    r^2-3*(1-s')*r+2=0.

Then 1<=r<=1+4s'. For the upper bound, evaluate the polynomial at 1+4s':
its value is s'*(28s'-1)<=0, so this point lies between the roots. Define

    F_j=(2*alpha/c)*(r/2)^j on prefix level j,
    F_port=F_h/[R*(1-s)].                             (2)

This is a positive supersolution for the shifted density operator c*L-c*s*I
on the prefix-plus-port principal system, with the seed source alpha/2.
Interior prefix residuals equal c*(s'-s)*F_j>=0. At a degree2 prefix leaf,
after dividing by c*F_h, the residual is

    (1-s)-1/r-1/[2*R*(1-s)]
      =(r-1/r)/3+1/R-1/[2*R*(1-s)] >=0.

The port residual is zero. At the root the residual is at least

    c*F_0*(1/2-s-2*s') >=13*alpha/16 >alpha/2.

The actual operator has at least this diagonal when beta*q0<alpha. Dropping
the positive regularization remainder lambda-tau in (1), the maximum-ratio
principle consequently gives f<=F. To justify the comparison without assuming
invertibility for free: a maximum ratio f_i/F_i>1 at a positive coordinate
propagates along nonzero off-diagonals through every zero-residual row until
it reaches a strict supersolution row, where it contradicts (1).

In particular the aggregate port mass q obeys

    q <= (2*alpha/[c*(1-s)])*r^h
       <= (2*alpha/[c*(1-s)])*exp(4*s'*h).             (3)

A port mass comparable to theta therefore requires s'*h at least a constant
multiple of log(1/alpha), apart from fixed constants. This makes precise why
increasing prefix depth can defeat a fixed beta, but does not automatically
defeat a beta tied to log(1/rho).

For completeness the auxiliary vector can also be bounded while no bulk
coordinate has ever been activated. Put

    Abar=(2*alpha/c)*r^h, B=12*Abar,
    G_j=B*(j+2)*2^(-j) on the prefix,
    G_port=[B*(h+2)+Abar]*2^(-h)/R.                   (4)

Assume R>=h+3. In scaled kinetic degree densities v_i=theta*z_i/sqrt(d_i),
the update, after dropping negative terms and the cap subtraction, is at most

    vnew <= a*(I+P_density)*v/2 + a*P_density*f/2
             +alpha*e_s/d_s.

The vector G is a supersolution of this affine recurrence. On an interior
prefix vertex LG=B*2^(-j)/3; at the root LG=B/2; at a degree2 prefix leaf
LG>=B*2^(-h)/2; and at a port LG=Abar*2^(-h)/R. These inequalities dominate
the forcing from f<=F<=Abar*2^(-j), with the source included. Starting from
zero, comparison gives aggregate kinetic port mass at most Abar*(12*h+25).
Together with (3),

    q+v_port <= Abar*(12*h+27).                      (5)

For the familiar family rho=gamma0*L/Cvol, theta=1/L, R=L^2, and fixed
gamma0>0, bulk raw values are nonpositive whenever

    Abar*(12*h+27) < 2*gamma0*theta/3,                 (6)

since bulk volume/Cvol>1/3. This closes an induction: no bulk activation
implies the primal support condition, which gives (3)-(5), which prevents the
next activation. The argument applies to the ordinary or monotone primal
update followed by cleanup; it does not use theta*z<=x.

For h=O(log L) and beta inverse-log^C in the full parameters with C>=1,
s'*h stays bounded and (6) holds for all sufficiently large L. Thus the
unsubdivided fixed-depth-exponent construction is not an initialized
asymptotic obstruction at that beta. This is a family-specific result.

## 3. Edge subdivision destroys the positive-inverse comparison

Let one prefix edge be replaced by an even-length path ell=2m. Restrict to its
ell-1 new internal vertices and set endpoint densities to zero. The rational
tent f_j=min(j,ell-j) has Laplacian energy ell and degree-weighted squared
norm (4m^3+2m)/3. Its exact normalized-Laplacian Rayleigh quotient is

    6/(ell^2+2).

Consequently the shifted principal matrix Q-beta*q0*I has a negative Rayleigh
quotient as soon as

    ell^2 >=12*c/(beta*q0-alpha),                     (7)

provided beta*q0>alpha. In particular ell=Theta(beta^(-1/2)) suffices. A
symmetric Z-matrix with a negative eigenvalue cannot have the nonsingular
M-matrix comparison property used in Section2.

For beta an inverse fixed power of the parameter logarithm, ell is itself
polylogarithmic. Subdividing a prefix of depth O(log L) therefore leaves total
travel distance polylogarithmic in L, much smaller than 1/theta=L. This is a
real obstruction to extending Section2 merely by replacing prefix depth by
its original branching depth. It does not prove that the initialized
accelerated trajectory supplies the necessary mass or activates clique bulk.

## 4. A connected cleaned state with a very expensive next projection

This construction shows why (1), a mass cap, and J<=0 do not alone control
initial-phase support work, even at inverse-polylog beta. Connectivity of the
positive primal support does not repair this example.

Fix an integer C>=1. For sufficiently large integer n, take

    alpha=2^(-2n), theta=2^(-n), rho=alpha^2,
    epsilon=alpha^4, beta=(14*n)^(-C).

Thus beta=log_2^(-C)(1/(alpha*rho*epsilon)) exactly, and all parameters are
rational. Increase n so beta<=1/16 and alpha<=beta/1024. Then

    3*beta/8 <=kappa=beta*q0-alpha <=beta,
    alpha<=kappa/3.

Choose ell to be the smallest power of two with ell^2>=16*c/kappa. It is even,
ell>=8, and ell^2<32/kappa. On the interior of an ell-edge path define

    H_j=j^2*(ell-j)^2/(ell-1)^2, 1<=j<=ell-1,
    H_0=H_ell=0,
    fbase=(lambda-tau)/kappa,
    t=2*fbase,  bump_j=t*H_j.                         (8)

The minimum H_j is one. A direct second difference gives

    (L H)_j=[6*j*(ell-j)-ell^2-1]/(ell-1)^2
       <= (8/ell^2)*H_j.

Indeed, with z=j*(ell-j)<=ell^2/4, the ratio (6z-ell^2-1)/z^2 is increasing
on this interval wherever positive and is at most 8/ell^2. Thus on positive
bump coordinates,

    c*L(bump)-kappa*bump <=-kappa*bump/2.             (9)

At a zero endpoint the same left side is nonpositive because incoming bump
mass is nonnegative.

Let mpath be one bump's degree mass. The exact identity

    2*sum_(j=1)^(ell-1) H_j
       =ell*(ell^4-1)/[15*(ell-1)^2]

implies ell^3/15 <= mpath/t <=ell^3/4. Choose N to be the largest power of two
at most 1/(16*mpath); for sufficiently large n, N>=4. Build a complete binary
tree with N leaves, and attach a separate ell-edge path at every leaf. Its root
is the seed. Set density fbase on EVERY vertex, add the bump (8) on each path
interior, and add the seed peak

    p=alpha/(2*q0).

Set z=0. The entire positive primal support is connected; all graph degrees
are at most3. No isolated positive component is available for deletion.

The bump mass is at most1/16. Total graph volume is at most2*N*(ell+2), so the
uniform-background mass is at most the bump mass for ell>=8. The seed peak
adds at most2*alpha. Hence total mass is at most1/4 for large n.

The cleanup test is satisfied everywhere. For the background,

    c*L(fbase)-kappa*fbase+(lambda-tau)=0.

Adding bumps preserves the inequality by (9), including their endpoints.
At the seed the added peak contributes
(c-kappa)*p-alpha/2=-beta*alpha/2<0; at its neighbors its contribution is
nonpositive. Thus no cleanup coordinate is eligible. Since degrees are bounded
and rho tends to zero, the strict degree guard and even the unrounded stronger
weighted mass cap also retain this state (their weights are eventually<2).

The nonpositive-objective condition also holds. Let y denote background plus
bumps. Its mass is at most1/8 and its maximum density is at most17*lambda/kappa^2.
The pointwise shifted inequality gives

    J(y) <= (beta*q0*max(y)/2+lambda)*mass(y)
          <=13*lambda/(8*kappa) <5*alpha^3/beta.

Here the negative seed linear term was discarded. Bumps are separated from the
seed peak by zero bump coordinates. Adding the peak changes the objective by

    -alpha^2/(4*q0)+alpha*(lambda+alpha*fbase)/q0
        <=-alpha^2/8

for the chosen sufficiently large n. Therefore J(f)<0.

Nevertheless the NEXT kinetic projection selects all N terminal leaves. With
z=0, the uniform background has zero Laplacian and contributes no raw kinetic
term. Each terminal leaf has degree1 and the identical raw value

    T=a*t/2-lambda>0.                                (10)

Every path-interior raw value divided by its degree is strictly smaller than
T: the displayed second difference satisfies L H_j>-1. Each path's attachment
vertex also has a smaller raw ratio, a*t/4-lambda. Other connector vertices have
ratio -lambda, except the root and its two neighbors affected by the peak.
Their TOTAL positive raw mass is at most alpha+a*p<=2*alpha<theta.

Thus the weighted raw tail evaluated at threshold T is strictly below the cap
theta. The exact projection multiplier is strictly below T, whether the cap
binds or not. Every terminal leaf is therefore positive in the projected
kinetic vector. This conclusion is independent of the subsequent monotone
line fraction or cleanup.

Since N>=1/(32*mpath)>=kappa/(14*lambda*ell^3), its normalized one-step work is

    rho*theta*N >= kappa/(14*theta*ell^3)
       =Omega(beta^(5/2)/theta)
       =Omega(2^n/n^(5C/2)).                         (11)

The graph has O(N*ell) vertices, so all graph and parameter logarithms are
O(n). The right side exceeds every fixed polylogarithmic factor.

## 5. Exact scope of the obstruction

Section4 is a feasible-state counterexample for the specified cleanup rule,
including connected support and a nonpositive objective. It invalidates an
instantaneous support bound deduced solely from those invariants. It is not a
cold-start counterexample: its preexisting support is large and expensive,
and its construction is not a proof that the local recurrence reaches it.
The support preparation and eventual output cannot be omitted from a work
ledger. In particular this result does not establish an OP2 lower bound or a
failure of a cumulative bound that fully charges how the state was obtained.

The remaining constructive question is precisely whether zero-started
propagation and the paid cleanup history rule out such reservoirs. Section3
shows that the easiest positive-inverse comparison does not settle that
question on subdivided prefixes. No randomized argument or uncharged solver
primitive is assumed in this note.
