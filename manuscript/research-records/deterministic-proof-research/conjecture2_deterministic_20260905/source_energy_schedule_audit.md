# Independent audit of the source-energy schedule

The source-energy bound and shorter fixed-block schedule in
`source_energy_schedule.md` are sound. The separately derived implementation
is `source_energy_dyadic_rppr.py`, exposing `SourceEnergyDyadicCorrector` and
`solve_rppr_source_energy`. The stable integer core and its wrapper are
unchanged. The implementation uses an upward-rounded squared statistic to
preserve bounded scalar denominators.

## Initial-energy proof

Let e=x*_r-bar, h=s-lambda*w, mu=theta^2<=alpha. Because bar<=x*_r and the
original optimum satisfies complementarity,

    r*=Qe-h >=0,       e>=0,       e^T r*=0.

Indeed, every positive coordinate of e is a positive coordinate of x*_r, on
which the original residual vanishes. Thus the correction objective at zero
exceeds its minimum by e^T Qe/2. Starting primal and kinetic correction at
zero gives

    E0 = e^T Qe/2 + mu*||e||^2/2
       <= ((1+mu/alpha)/2) e^T Qe.

Write g_i=(s_i/w_i-lambda)_+, and define
H1=sum d_i*g_i, H2=sum d_i*g_i^2, Hinf=max g_i. Unstored source coordinates
have g_i=0, so these sums need only the already exposed source records.
The stage box and mass conditions yield

    e^T Qe = e^T h <=4r H1,
    e^T Qe <=eta Hinf.

Also e^T Qe<=||e|| sqrt(H2) and alpha||e||^2<=e^T Qe. If the energy is
positive, divide by its positive square root to obtain e^T Qe<=H2/alpha;
the zero case is immediate. Each of the three terms is therefore a valid
upper bound independently.

The cap at 1 in the proposed Ebar is also safe without any new global
information. Nonnegative source and w^T s=alpha*eta imply
s_i/w_i<=alpha*eta/d_i<=alpha*eta, since d_i>=1. Consequently
eta*Hinf<=alpha*eta^2<=1. The earlier estimate E0<=1 is thus already implied
by a retained term. Finally Hinf<=3*alpha*r proves Ebar<=3*alpha*r*eta.

## Bounded-denominator implementation

An exact sum H2 would accumulate degree denominators, potentially producing
a large least common multiple on many coprime degrees. This does not affect
the real-arithmetic inequality but is unsuitable for the intended bounded
integer-state implementation.

Use alpha=A/D, rho=P/R, h_grid=1/H and the existing integer source numerator
N_i, whose density is N_i/(2*D*H*d_i). Set

    C=2*D*H*R,
    G_i=max(R*N_i-2*A*H*P*d_i,0).

Direct common-denominator arithmetic gives g_i=G_i/(C*d_i), hence

    H1 = (sum G_i)/C,
    Hinf = max_i(G_i/d_i)/C,
    H2 = (sum G_i^2/d_i)/C^2.

The implementation accumulates

    H2_upper = (sum ceil(G_i^2/d_i))/C^2.

Its excess over H2 is nonnegative and strictly below n_positive/C^2 when
n_positive>0; both are zero when n_positive=0. Per-record operations are
integer additions, products, comparisons, and one integer division. The
maximum retains only one degree denominator. The two sums have fixed common
denominators, so their bit lengths grow only logarithmically with source
record count and degrees, in addition to the input/grid bit lengths.

Replacing H2 by H2_upper keeps the initial-energy bound valid. The unchanged
eta*Hinf term still gives Ebar<=3*alpha*r*eta even if this upward rounding is
coarse. The implementation reports H1, Hinf, H2_upper, its excess bound, C,
Ebar, and all source-record/division counts. Exact H2 appears only in the
independent small test oracle.

## Schedule, zero steps, and locality

The grid remains selected from the original tolerance tau. In particular,
Gamma=29h_grid/theta<=29tau/256<tau/8. The existing perturbed trajectory bound
is E_k<=a^k E0+Gamma. With T=1/theta and a^T<1/2, choose the least q>=0 with
Ebar/2^q<=tau/2 and run K=Tq steps. For q>0 the final objective gap is at most
Ebar/2^q+Gamma<tau. After any positive number of steps, using the completed
block count in place of q remains a conservative bound.

At zero steps, report Ebar itself, because there has been no rounding error.
If q=0 this is already <=tau/2. In particular Ebar=0 forces e=0 by positive
definiteness, so the baseline is exactly optimal for this stage. The unchanged
exact PG/grid/max repair remains safe in either zero-step case. Source
initialization, baseline scans, candidate materialization, and terminal repair
remain charged even if K=0.

Since Ebar<=1, this schedule is never longer than the original one on the
same stage parameters. The numerical recurrence and auxiliary-energy proof
are untouched, so the existing selected-work theorem applies to this shorter
prefix. Endpoint equality with the longer schedule is neither needed nor
generally true. The same objective and final repair certificates apply.

The prototype derives its continuation by reusing the stable wrapper code
with an isolated corrector-class binding. Original module globals are never
patched. The extra source pass is counted explicitly. The base constructor
still performs its original small schedule-setup loop before replacement;
those original setup operations remain in its counters, and new schedule
checks/doublings are separately recorded.

## Exact tests

`test_source_energy_dyadic_rppr.py` passes all four groups. Results are saved
in `source_energy_dyadic_verification.json`.

* Twenty-one independent exact initial-energy and final stage-gap checks use
  exhaustive dense KKT solutions. The initial objective identity, all source
  statistics, rounded H2 upper bound, Ebar domination, least-block condition,
  and final objective bound are verified.
* Shortened stages match the stable integer recurrence exactly at every step
  of their common prefix. Grids are identical.
* A degree-three source fixture gives strict upward rounding in H2_upper;
  its denominator divides C^2 and its excess obeys the stated bound.
* An exact optimum baseline produces Ebar=0 and zero steps, but still pays
  for baseline/source and terminal work. A separate positive-Ebar stage also
  needs zero steps. A full continuation with rho=1023/1024 exercises the
  zero-step wrapper branch with a positive final error allowance.
* Eight full deterministic cases cover fourteen stages, arbitrary rational
  alpha, non-dyadic final rho, a tightened final tolerance, a tree, triangle,
  star, zero-solution equality, and alpha=1. Every repaired stage satisfies
  monotone baseline, source, and safe-order conditions against dense KKT;
  every final exact objective gap meets its certificate. Graph accesses are
  reconciled with the logical counters.

Across those eight fixtures the new schedules use 954 iterations versus
1,478, and 1,800 corrector adjacency-entry reads versus 2,818. These totals
are finite verification measurements, not a universal strict improvement
claim for adjacency work on every possible input: changing an endpoint also
changes the next baseline and may change individual materialization costs.

## Bounded measured comparison

`benchmark_source_energy_dyadic.py` uses the same implicit path fixture as
the integer-core comparison: 10^9 vertices, endpoint seed0, alpha=1/100,
rho=1/16, epsilon=1/1,000,000. It compares the unit initial bound against the
source bound in ABBA order. Full records are in
`source_energy_dyadic_benchmark.json`.

| Measurement | Unit bound | Source bound |
|---|---:|---:|
| Accelerated iterations | 2,016 | 1,344 |
| Corrector adjacency entries | 11,755 | 7,787 |
| Terminal PG adjacency entries | 22 | 24 |
| Total counted adjacency entries | 11,777 | 7,811 |
| Median process CPU seconds | 1.2180 | 0.8269 |
| Median wall seconds | 1.2356 | 0.8451 |

The new schedule adds eleven charged source-statistic visits. Both variants
use nineteen degree replies, twenty-four first adjacency entries, and six
output records; both final certificates equal 1/1,280,000. Their exact
endpoints differ as expected. Repeated runs of each variant reproduce their
own exact endpoint and stage summaries.

The measured CPU speedup is 1.47x (wall 1.46x), with one-third fewer iterations.
These clocks alone use floating values. All algorithmic arithmetic,
comparisons, outputs, and certificates remain exact and deterministic.
