# Resolution recorded at 07:42 UTC

**Proved here:** The graph-limit statement is now proved in
`sections/12_ramp_obstruction.tex`, under the stable labels
`lem:revisit-level-scales`, `lem:revisit-activation-separation`,
`lem:revisit-current-front`, and `thm:revisit-front-limit`.
The earlier open route below is preserved as research history.

The missing observation was to group the global energy by automorphism
orbits. For level volume W_l, both primal and kinetic density errors are
at most 2 sqrt(r/W_l). Exact static ratio elimination gives pair-i PPR
scale h_i=(alpha/b)(gamma/b)^i and W_l of order b^(i+1).
This proves old kinetic positivity after a fixed offset from iK, and proves
future inactivity by induction from time zero. The current front then
converges on every fixed window by continuity of the actual projection.

For all older normalized error maxima M_i up to a fixed front window,
uniformly stable two-coordinate impulse kernels give

    M_i <= A_i + L M_(i+1) + (L/b) M_(i-1).

The finite nonnegative coupling matrix tends to a strictly upper triangular
matrix. Its inverse is therefore uniformly bounded for large b. This
bounds every old normalized error, and makes reverse couplings vanish.
The homogeneous terms decay from each pair's own activation time.
Dominated convergence of causal kernels then gives the separated-front
limit. Combined with the proved cascade gain, it rules out every universal
constant ramp-tracking bound at the fixed alpha=1/4096.

A separate exact finite audit checked the sign separation on 12 trees with
j in {1,2,4,8} and K in {4000,6000,8000}, through 65,000 steps.
It is supporting evidence, not the graph-limit proof.

---

# Working route toward an asymptotic ramp-tracking obstruction

Status at 06:30 UTC: **Open / under development.** The fixed finite
counterexamples are already certified. The argument below is not yet part
of the proved theorem ledger. Its central new obligation is the matched
front limit; numerical checks of that limit are planned.

## Two-vertex block limit

Fix theta=1/64, alpha=theta^2, chi=1-theta, eta=1-theta/2,
beta=chi/(1+theta), and c=(1-alpha)/2. Consider the rooted unit tree
T(b,2,2j+4): b children at even levels, one child at odd levels. Group
levels (2i,2i+1). As integer b tends to infinity, the degree-density
operator on every nonterminal pair has diagonal block

    Q_B = [[(1+alpha)/2, -c], [-c/2, (1+alpha)/2]],
    C_B = I-Q_B = c [[1,1],[1/2,1]],

with coupling from the next pair's first coordinate to this pair's second
coordinate c/2 in I-Q. Reverse coupling is O(1/b). The limiting chain is
upper triangular in these two-coordinate blocks. It is a limit of canonical
unit graphs; the proposed solver is still run on those finite graphs.

Define the static transmission coefficient

    gamma = c^2 / (2*((1+alpha)/2)^2 - c^2).

The effective PPR source entering block i is asymptotic to
(alpha/b)*(gamma/b)^i. Choose integers b_K nearest to gamma*eta^(-K).
Then its activation scale aligns with time i*K because
(alpha/b)*eta^(i*K) is asymptotic to that effective source.

For every fixed j, let K tend to infinity first. Around time j*K+tau,
block j should converge, after scaling by its effective source, to an
isolated Q_B orthant-continuation profile with source e_1 and regularizer
lambda_tau=eta^tau. It is identically zero for tau<=0. Older blocks are
strictly positive by then; their nonlinear floors are inactive. Later
blocks remain zero on every fixed tau window. The extra pair before the
leaves is essential: otherwise leaf degree 1 changes the limiting source
at the last active pair.

## Why old transients should disappear

The limiting diagonal block dynamics has poles of modulus at most
sigma=sqrt(beta*c*(1+1/sqrt(2)))<eta. For each fixed number of blocks,
finite-b matrices converge to a block triangular matrix with those poles.
A resolvent contour gives a power bound C_j*sigma_bar^k, uniformly for
large b, for any sigma<sigma_bar<eta; diagonalization with a b-dependent
condition number is unnecessary.

A transient created i epochs before the current front has initial size
larger by b^i, but has decayed for i*K steps. Its relative size is bounded
by a fixed polynomial in K times (b*sigma_bar^K)^i, which tends to zero.
The exponent is i in both factors; there is no need to require
sigma_bar<eta^j. An induction over the finitely many front epochs should
establish sign separation and convergence on every fixed tau window.
Reverse coupling of an O(r) error into the new pair is only O(r/b).

## A transfer function with gain above one

Let E_i(tau) be the block's PPR density error divided by the current r.
For an old positive block,

    E_next = ((1+beta)/eta) C E
             - (beta/eta^2) C E_prev + (alpha/eta) one,

including the next-block coupling. Taking temporal differences removes
the constant forcing. At temporal frequency zeta on the unit circle put
z=eta*zeta and A(z)=c*(1+beta-beta/z). The transfer from the next pair's
first coordinate to this pair's first coordinate is

    H(z) = A(z)^2 / (2*(z-A(z))^2 - A(z)^2).

For zeta=(12+5i)/13, direct calculation at theta=1/64 gives |H|>3.
This should be checked with exact complex rational arithmetic. The pole
radii after normalization are below one.

The isolated front profile is eventually linear: the response-energy bound
forces x,z to its strictly positive unregularized optimum, after which the
floor is inactive. If U(tau)=alpha*eta^(-tau)*(Q_B^(-1)e_1-x(tau)), then
its temporal difference D(tau) decays exponentially in both time directions.
For negative tau, U is a constant times eta^(-tau); for positive tau its
nonconstant part has decay sigma/eta. D is not identically zero, since
U tends to zero in the remote past and to a positive particular response
in the future. Its Fourier transform is analytic on an annulus and cannot
vanish on the entire frequency interval where |H|>3.

Consequently the j-fold cascade should have L2 norm at least c0*M^j for
some M>1. Cauchy coefficient bounds on a slightly larger annulus confine
all but an exponentially smaller tail to O(j) time indices. Hence its
maximum is at least c1*M^j/sqrt(j). A large temporal difference implies
one adjacent normalized error has at least half that magnitude.
Combining this with the matched-front limit would prove that no graph-
uniform constant C bounds ramp error by C*r, even at this fixed alpha.

## Exact initialization for a limit-profile audit

The old-pair error chain has a constant particular A and a past exponential
part B*eta^(-tau). For the j old pairs, with block-upper-triangular matrix
C_old, set

    A = (eta I - g(eta) C_old)^(-1) alpha*one,
    B = (I-C_old)^(-1) (alpha*(c/2)*t_front[0]*e_last),
    g(eta)=1+beta-beta/eta,
    t_front=Q_B^(-1)e_1.

Then E_old(0)=A+B and E_old(-1)=A+eta*B exactly. The front has
x=z=0 at tau=0, U_front(0)=alpha*t_front and
U_front(-1)=alpha*eta*t_front. Evolve the front with its actual projected
recurrence and the old pairs with the displayed linear error recurrence.
This avoids truncating an infinite past. Compare finite-b root error/r at
j*K+tau to this profile for several K and fixed j, using high precision.

## What remains before promotion

1. Check the transfer algebra and strict gain exactly.
2. Implement and audit the finite-graph-to-limit comparison.
3. Write a complete matched-front induction, including the normalization
   of the exact PPR source and the strict inactivity/positivity claims.
4. Prove the analytic-cascade concentration lemma with all constants
   allowed to depend on fixed alpha and the front profile, but not j.
5. If any of these is unresolved, retain this as an open proof route.
