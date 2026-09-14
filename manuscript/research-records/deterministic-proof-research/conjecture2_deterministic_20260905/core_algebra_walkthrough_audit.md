# Audit of the core algebra walkthrough

Status: equations, signs, and constants pass against the frozen proof.
No new analytical gap or algorithmic requirement was found. Two short
scope clarifications were suggested, applied by the author, and checked.
No experiment was run and no proof/package source was edited.

Initial reviewed walkthrough SHA-256:
77958037c8433815b4bffe33de4ab84dfc1cbc2af5a23cd2d935b56011355cd7.
Final corrected walkthrough SHA-256:
49ff72330eb6189d9fdb4ecab620750f27efe302cc04710ec9f5e7b399f0c488.
The auditor did not edit the walkthrough; the author applied the two
exposition changes described below. Proof/PDF/package sources are unchanged.

## 1. Accelerated comparison

The sector sign gives the displayed squared-distance inequality. In the
smoothness calculation the gradient/correction cross terms cancel exactly,
leaving -||g||^2/2+mu||p-q||^2/2. Adding the sector inequality and expanding
q-t=A-g/theta yields the stated -theta<A,g> term because mu=theta^2.
The weighted strong-convexity identity is correct, including
a(x-y)+theta(t-y)=-theta*A and x-y=theta(y-z).
The remaining term is
-mu*a*theta*(1+theta)||z-y||^2/2
=-mu*theta*(1-mu)||z-y||^2/2.

This derivation requires neither optimality of the comparator nor
nonnegativity of the energy. In the Q metric, the auxiliary gradient and
metric Hessian are exactly the ones stated. The proof's single-comparator
sector signs, rather than an unjustified general Q-nonexpansiveness claim,
are the needed projection hypothesis.

## 2. Actual-state raw identity and selected telescope

The coefficient of the kinetic state in equation (3) simplifies using
a(1+theta)+mu=1. The similarity transform of normalized adjacency is
AD^(-1), which is column stochastic; row stochasticity is not substituted.
Since alpha>=mu, beta=(1-alpha)/(1+theta)<=a.

At the formal comparator state the raw vector is xi*-r*/theta, so its mass
form is V*-R*. Subtracting this identity gives equation (4) with the stated
negative slack -R* and negative response operator -(Q-mu I)/(1+theta).
It is valid at arbitrary actual feasible primal/mirror states; it does not
require lower approximation or an unconstrained linear trajectory.

Selection implies positive projected mirror values, so lower normals vanish
and upper/cap normals only subtract mass. Dropping the negative kinetic
part is legitimate. The telescope has exactly the terminal positive error
plus (1-beta) times the intervening errors, because its initial error is
zero. Outside the analytical core, positive kinetic support equals selection,
and the slack contributes lambda*d_i/2.

## 3. Constants and rounded forcing

Weighted Cauchy counts selected degree-volume, not distinct vertices or
unselected absolute flux. The commuting spectral bound gives the claimed
response norm. Splitting D_out>B_core and its complement proves
W<=8H2/lambda^2+2B_core, hence 144K/r+4K/r=148K/r.

For rounded states equation (4) describes the exact raw formula evaluated
at those actual states. The approximate raw evaluation adds its separate
error; after mass scaling its magnitude is at most nu*d_i, with
nu=theta*kappa_r. If the stored rounded mirror exceeds the comparator, the
ideal projected mirror does too, so the lower-normal sign remains valid.
Downward primal rounding changes the current response H, already covered
by the two-energy estimate; it adds no independent historical term.

With the proved effective floor at most alpha^2*r*eta, one has
H2<=22*alpha^2*r*eta*K. Absorbing nu<=lambda/4 gives
W<=2B_core+4*sqrt(W*H2)/lambda.
The displayed Young inequality yields
W<=4B_core+16H2/lambda^2<=(8+352)*eta*K/r=360*eta*K/r.
All coefficients and signs agree with the appendices.

## 4. Completed standalone clarifications

The walkthrough inherits valid stage parameters and the certified rounding
budget from the linked proof. For clarity, the author was asked to state
0<theta<=1 in the generic comparison paragraph (actual stages use theta<=1/2),
and explicitly mention the effective-floor bound before the rounded
22*alpha^2*r*eta*K estimate. Both changes are now present and were checked.
They are reminders of existing premises, not corrections to the derived
identities or new solver assumptions. No further change is requested.

Frozen source hashes checked during this audit:

- deterministic_conjecture2.tex:
  d5425bc5aec84166adf6ffbda7bb1738bed26eab458df1b1b40e565410a3f2fa
- practical_refinements_appendix.tex:
  dfa059bf8ab9631d4881818f5e10ac1511b5877daa3dd8af0e65547f4431d4e8
- practical_schedules_appendix.tex:
  3fb6d6d901d5c7c3e2105bb31e94e2827d031d1c27b5d610324a4cca2a25b559
