# Audit: mass-scaled perturbation and a coarser representable grid

Status: proved for the existing rounded recurrence with the exact correction
mass cap. This is a mathematical refinement; this audit changes no stable
implementation or proof file. A coarser grid changes the numerical trajectory,
although the recurrence, directed rounding, reporter, and repair rules remain
the same. Only the current team's proof artifacts were used.

## 1. Stage assumptions and the two-energy lemma

Let 0<alpha<1, 0<r<1/d_seed, lambda=alpha*r,
theta<=1/2, mu=theta^2<=alpha<4*mu, and
a=1-theta. A valid stage has

    0 <= bar <= x*_r,
    s=b-Qbar in [0,4 lambda w],
    eta = w^T s / alpha = 1-w^T bar.

Use the set C_eta={v: 0<=v<=4*r*w, w^T*v<=eta}.
The analytical vectors e=x*_r-bar and t=Q^(-1)s satisfy
0<=e<=t<=4*r*w, with w^T*t=eta. All stored primal and mirror
states lie in this same set.

For one iteration use the established error interface

    p0 = Proj_Ceta(raw+u),       p=p0+ep,
    xplus = a*x+theta*p+ex,
    |u| <= kappa_r*w,
    -kappa_p*w <= ep <= 0,      -kappa_x*w <= ex <= 0,
    p,xplus >= 0.

Write

    J(x)=x^T Qx/2-(s-lambda*w)^T x,
    A(x)=||Qx-s||^2/2+alpha*lambda*w^T x,
    E=J(x)-J(e)+mu*||z-e||^2/2,
    B=A(x)-A(t)+mu*||z-t||_Q^2/2.

Then, with exactly the original error coefficients,

    Eplus <= a*E + eta*zeta,
    Bplus <= a*B + eta*zeta,
    zeta = 2*mu*kappa_r
         + (5/2)*kappa_x + (5/2)*(theta+mu)*kappa_p.       (1)

Proof. The projection Q-sector remains valid at the single comparator t.
At an active mass face its normal contribution is
gamma*(alpha*eta-w^T s)=0; the box-face signs are unchanged.
Consequently the raw-error sector terms cost at most
2*eta*kappa_r in either metric, because both compared vectors have mass
at most eta and |Qu|<=kappa_r*w. Their energy cost is
2*mu*eta*kappa_r.

Put x0plus=a*x+theta*p0 and d=xplus-x0plus. This is a downward change with
|d|<=kappa_d*w, kappa_d=theta*kappa_p+kappa_x. Its lost mass is at most
eta, so ||d||^2<=kappa_d*eta. Moreover

    w^T|Q*x0plus-s| <= eta+alpha*eta <= 2*eta.

The nonnegative linear mass penalties decrease. Exact quadratic expansion,
|Qd|<=kappa_d*w, and ||Qd||<=||d|| bound the increase of each primal
objective J and A by (5/2)*eta*kappa_d.
Likewise the mirror mass loss is at most eta, its squared norm is at most
kappa_p*eta, and the weighted absolute mass of either comparator
difference is at most 2*eta. Either mirror-distance increase is at most
(5/2)*mu*eta*kappa_p. Adding these estimates proves (1).
No assumption that B is nonnegative is used.

For a uniform error budget define the effective additive floor

    Gamma_eta = eta*zeta/theta.                         (2)

Thus E_k<=a^k E_0+Gamma_eta and B_k<=a^k B_0+Gamma_eta.
For nonuniform errors replace this floor by the convolution with
increments eta*zeta_k; eta is fixed throughout one stage.

## 2. Auxiliary initialization, response, and work

Let m_s=alpha*eta. The unchanged source inequalities give

    ||s||^2<=4*lambda*m_s,  A(t)=lambda*m_s,
    t^TQt<=4*r*m_s.

At the zero correction initialization,

    B_0 <= (1+2*mu/alpha)*lambda*m_s <=3*lambda*m_s.

Therefore A(x_k)<=4*lambda*m_s+Gamma_eta and
||Qx_k-s||^2<=8*lambda*m_s+2*Gamma_eta.
The true residual q=s-Qe satisfies
0<=q<=lambda*w, w^Tq<=m_s, hence ||q||^2<=lambda*m_s.
It follows that

    ||Q(x_k-e)||^2 <=18*alpha^2*r*eta+4*Gamma_eta.        (3)

This argument remains valid if the auxiliary energy happens to be negative.

For the existing scalar-only rebase realization, the already proved
interface is kappa_r=2h/theta, kappa_p=h, kappa_x<=10h.
Substitution in (1) gives

    Gamma_eta <=29*eta*h/theta.                         (4)

The exact selected-flow proof now uses the same raw forcing
nu=theta*kappa_r=2h, and the analytical core has volume at most 2*eta/r.
Consequently, if nu<=lambda/4 and Gamma_eta<=alpha^2*r*eta, its unchanged
algebra gives the fully repeated kinetic volume bound

    W_K <=360*eta*K/r.                                 (5)

The support records, baseline/source formation, materializations,
checkpoints, and scalar rebases inherit this factor exactly as in the
same-grid mass-deficit audit. This is not only a bound on distinct support.

## 3. The relaxed ceiling implies the other default ceilings

Take the actual stage tolerance and repair parameter to be

    tau=alpha*delta^2/8,       0<delta<=alpha*r/2.

The stage is nontrivial, so x*_r has nonempty support containing the seed.
Its mass/support inequality implies

    1 >= eta >= eta_*(r) >= r*d_s >= r > 0.             (6)

Define psi=theta*tau/(256*eta). It suffices to choose h<=psi,
together with the requirement that the dyadic grid contain the old baseline.
Indeed,

    psi <= theta*alpha^3*r^2/(8192*eta)
         <= theta*alpha^3*r/8192.                      (7)

Thus psi is less than 1/8, theta, and theta*alpha^2*r/29.
Also

    psi/(lambda/8) <= theta*alpha^2/1024 <1,
    psi/(delta/2)  <= theta*alpha^2/2048 <1.

These verify all previously explicit guards: 2h<=lambda/4,
h<=lambda/4, h<=delta/2, and the response ceiling.
Equations (4) and (7) give

    Gamma_eta <=29*tau/256 <tau/8,
    Gamma_eta <=alpha^2*r*eta.                          (8)

The original objective gap schedule, source-energy schedule, binomial
blocks, and accepted exact stopping certificates retain their ACTUAL target
tau. Only their additive rounding floor changes to (4).
Initializing a constructor with tau/eta solely to choose a grid must not
silently change its stopping target or leave the unscaled rounding floor
in a reported certificate.

The exact terminal PG scan, clipping, grid rounding, and maximum with the
old baseline need no modification: their h<=delta/2 and h<=lambda/4
hypotheses hold. No approximate response is substituted in that PG scan.

## 4. Exact baseline representation and the final target clamp

This section concerns the default choice of the largest reciprocal
power-of-two grid permitted by the numerical ceilings and exact
representation of the incoming baseline. Strict nesting h_j<=h_(j-1)
is sufficient but is not required: the implementation may coarsen a grid
when all retained baseline fractions reduce. An arbitrarily supplied
finer grid is outside the lower-bound assertion.

Every baseline denominator divides the preceding H. If g_base is the
reciprocal of the largest reduced baseline denominator (take g_base=1
for an empty baseline), then g_base>=h_old. Let g_num be the largest
reciprocal power of two at most psi_new. The actual default choice is
min(g_base,g_num), subject to the already redundant numerical guards.
In particular,

    h_new >= min(h_old,g_num).                         (9a)

No unused bits of the previous grid must be retained.

A diffuse baseline has eta_before<=4*eta_*(r). For completeness,
e=x*_r-bar obeys Qe<=3*alpha*r*w: on e_i>0 use KKT and s<=4*alpha*r*w;
on e_i=0 use the Stieltjes signs. Inverse positivity gives e<=3r*w,
and the support/mass inequality yields the stated deficit comparison.
Any safe repaired baseline has eta_after>=eta_*(r). Therefore

    eta_(j+1) >= eta_j/4.                              (9)

For either fixed dyadic continuation or the audited adaptive source
continuation, every transition to another NONFINAL stage satisfies
r_(j+1)<=r_j/2. Its tolerance is tau_j=alpha^3*r_j^2/32, so (9) implies
psi_(j+1)<=psi_j. These relaxed ceilings are nonincreasing before the
final target clamp. Induction in (9a), starting with the zero baseline,
therefore gives h_j>psi_j/2 there.

A final clamped parameter can be closer than a factor two to its predecessor.
Nevertheless tau_final<tau_previous, while (9) still holds; hence
psi_final<4*psi_previous. Final epsilon-driven extra halvings of delta only
decrease psi_final. The final representable choice therefore satisfies
h_final>psi_final/8. A single-stage continuation has the stronger factor two.
Uniformly,

    h_j > theta*tau_j/(2048*eta_j).                    (10)

It would be incorrect to assert the factor-two lower bound at every
arbitrary final target clamp.

There is also a simpler bound that directly preserves the old bit theorem.
Because eta<=1, every relaxed ceiling is at least theta*tau_j/256.
The actual tau_j are nonincreasing. Inductively (9a) gives
h_new>=min(h_old,g_num)>theta*tau_new/512. Equivalently, the old
unit-mass default nested grid is feasible for every relaxed ceiling and
the incoming baseline. There is no extra historical denominator factor.
In particular,

    H_j=1/h_j <512/(theta*tau_j).                       (11)

All existing parameter-bit and arithmetic-word envelopes therefore hold
without enlargement. In particular log H is
O(log(1/alpha)+log(1/rho)+log_+(1/epsilon)).
Computing eta from a dyadic baseline uses the integer sum of d_i times
baseline grid counts. Forming psi adds one bounded rational scalar
operation; it introduces neither a degree-denominator least common
multiple nor a product of all previous stage denominators.
The previous grid denominator is already within (11), and eta>=rho
introduces no new precision parameter. The scalar rebase count and
reporter-root bit bounds remain those of the existing realization.

## 5. Zero cap and scope

The eta=0 case cannot occur in any valid nontrivial continuation stage,
by (6). Abstractly eta=0 forces C_eta={0}, s=0, and both comparison vectors
and all feasible stored states equal zero; (1) then holds with zero
additive error. A generic grid-selection interface should return that
zero correction before dividing by eta. The existing zero-solution and
alpha=1 direct branches retain their separate qualifications.

The refinement proves a safe coarser default grid and the same asymptotic
work/bit guarantees. It does not prove strictly smaller total graph work:
changing the grid can change support decisions and repaired baselines.
