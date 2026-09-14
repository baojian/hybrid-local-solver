# Tighter dyadic block schedule: derivation and implementation audit

The proposed bound is valid. `binomial_block_dyadic_rppr.py` implements it
separately through `BinomialBlockDyadicCorrector` and
`solve_rppr_binomial_blocks`. Existing integer, source-energy, and package
modules remain unchanged. The recurrence, grid, source cap, terminal repair,
and selected-work proof are exactly the same; only the prescribed endpoint
and reported contraction bound change.

## 1. A constant-degree bound for one block

Let T=1/theta>=2 be an integer, a=(T-1)/T, and m=min(6,T). Define

    S = sum_(k=0)^m binom(T,k)/(T-1)^k.

The binomial theorem and nonnegative omitted terms give

    1/a^T = (1+1/(T-1))^T >= S,
    a^T <=1/S.

There are always at least three terms, and these already sum to

    1 + T/(T-1) + T/[2(T-1)]
      = 1 + 3T/[2(T-1)] >5/2.

For B0=2^16, put U=ceil(B0/S) and beta=U/B0. The ceiling inequality implies

    a^T <=1/S <=beta <1/S+1/B0 <2/5+1/65536 <1/2.   (1)

At equality of B0/S with an integer the upper ceiling comparison can be
replaced by equality there; the displayed strict final bound still holds.
No sign or rounding-direction ambiguity occurs: U is an upward bound.

For T=2 the full binomial sum is 4 and beta=1/4. For T=4 it is 256/81,
and B0 is divisible by 256, giving beta=81/256 exactly. At these two values
beta equals a^T. For T>6 the omitted terms are positive, so the truncated
inverse bound is strictly above a^T before or after upward rounding.

As T tends to infinity, S tends to sum_(k=0)^6 1/k!=1957/720. The limiting
upward-rounded value is 1507/4096. This is close to the limiting exact block
contraction exp(-1), but neither an exponential nor a logarithm is evaluated
by the algorithm.

## 2. Setup uses only bounded-degree integer expressions

The code represents S over the common denominator (T-1)^m:

    S_num = sum_(k=0)^m binom(T,k)*(T-1)^(m-k),
    S_den = (T-1)^m.

Binomial coefficients are formed by the exact integer recurrence
choose_(k+1)=choose_k*(T-k)/(k+1). Finally

    U = (B0*S_den+S_num-1)//S_num.

There are at most seven summands and seven integer divisions in total. Every
power of T-1 has exponent at most six. Since binom(T,k)<=T^k, the sum
numerator is at most 7*T^6; the extra B0 factor adds only sixteen bits.
Thus setup operands and temporary results use O(log T) bits, with a fixed
constant independent of T. In particular, the code never forms either
T^T or (T-1)^T.

The implementation records the truncation degree, fixed-grid numerator and
denominator, setup division count, and maximum setup integer size. B0 is a
fixed denominator with **sixteen fractional bits**; its integer encoding
has seventeen bits.

## 3. Schedule and every-prefix energy certificate

Keep the audited initial bound Ebar and rounding floor Gamma from the
source-energy implementation. The inherited rounded trajectory satisfies

    E_k <=a^k E0+Gamma,  E0<=Ebar,
    Gamma=29h/theta<tau/8.

Choose the smallest q>=0 such that

    Ebar*beta^q <=tau/2,

and run K=Tq steps. At any positive iteration k, with c=floor(k/T),

    a^k <=(a^T)^c <=beta^c,
    E_k <=Ebar*beta^c+Gamma.                         (2)

This includes non-block endpoints. At the prescribed final endpoint the
right side is below tau. Equality beta=a^T at T=2 or T=4 causes no problem:
strict final accuracy comes from tau/2+Gamma<tau, not a strict contraction
comparison in (1).

At zero steps, report Ebar alone because no perturbation has occurred. A
zero-step stage has Ebar<=tau/2; if Ebar=0, its baseline is already exactly
optimal by positive definiteness. The inherited exact PG/grid/max repair is
safe for both zero-energy and positive-energy zero-step cases. Initialization,
source computation, candidate materialization, and terminal work remain
charged.

For the same stage parameters and the same baseline, beta<1/2 ensures this
schedule is no longer than the previous source-energy schedule. When T=2,
its block count is exactly ceil(q_half/2). This does not prove that every
complete continuation has fewer total entries or steps than another
schedule: changed endpoints can change later baselines. The comparison
below is explicitly a measured finite comparison.

## 4. Power representation and operation accounting

The implementation stores the current block power as U^c/2^(16c), updating
its integer numerator by multiplication with U and its denominator by a
sixteen-bit shift only when a block is completed. Its numerator has at most
16c+1 bits and its denominator has exactly 16c+1 bits. The same representation
is used in the schedule-selection loop. Thus powers use O(q) bits, with no
q*log T or Tq dependence.

The stopping comparison is done by exact cross multiplication against Ebar
and tau; it does not require evaluating a convergence diagnostic or scanning
a vector. Fractions are constructed only for scalar reported bounds, after
which ordinary exact reduction applies. The numerical vectors never contain
these power denominators.

The base constructors still perform the prior unit-bound and source-half
schedule loops, and the base step still maintains its unused power-of-two
block denominator. Those operations remain counted. The new loop adds O(q)
scalar operations and its own counters; the new completed-power update adds
O(1) scalar operations per block. This preserves the word/bit bounds in
`integer_source_complexity_corollary.md`, changing constants only. Default
metadata reads a fixed number of integer sizes; it adds no full-state scan.

The subclass calls the unchanged parent step, then updates its power before
returning a completed block. Its reported bound therefore always agrees
with the current completed-block count. The continuation uses an isolated
corrector-class binding and the identical stable wrapper/repair code. No
original module global is patched.

## 5. Exact verification

`test_binomial_block_dyadic_rppr.py` passes all six test groups. Results are
saved in `binomial_block_dyadic_verification.json`.

* Sixty-five scalar cases compare beta against the fully expanded exact
  a^T and independently formed binomial sums. They check the upward ceiling,
  strict half bound, setup size bound, and exact T=2 and T=4 values.
* Six larger scalar cases extend to T=2^256 without constructing a^T. They
  verify both exact ceiling inequalities and the constant-degree size bound.
  At T=2^256 the largest recorded setup integer has 1,553 bits and
  beta=1507/4096.
* Six stage fixtures give 154 step-by-step exact trajectory matches with the
  preceding source-energy implementation. They include T=2,4,16,32,
  nonsquare rational alpha, positive baselines, a tree, and a star.
* Complete acceleration energy is independently computed against exhaustive
  dense KKT optima at 788 prefixes, including intermediate non-block
  endpoints. Every energy lies below the reported bound. Stored powers are
  checked against their exact mathematical values and linear-in-block bit
  bounds at each prefix.
* Eight complete deterministic solves cover fourteen stages. Every repaired
  stage satisfies independent optimum-order, source, and monotone-baseline
  checks; each final objective gap satisfies its exact certificate. Oracle
  access counts are reconciled. Zero-solution equality and alpha=1 use their
  unchanged direct branches.
* Three zero-step cases include an exact optimum baseline, a positive-energy
  stage, and a full zero-step continuation. Source/setup work remains
  observable and the bound is Ebar without a fictitious rounding term.

Across the eight complete fixtures, the new schedule uses 612 iterations
versus 954 and 1,168 corrector adjacency entries versus 1,800. These are
finite test measurements, not a graph-uniform strict reduction assertion.

## 6. Bounded timing and work comparison

`benchmark_binomial_block_dyadic.py` compares the old source-energy half-block
schedule with the new bound in ABBA order. The input is an implicit path
with 10^9 vertices, endpoint seed0, alpha=1/100, rho=1/16, and
epsilon=1/1,000,000. Full records are in
`binomial_block_dyadic_benchmark.json`.

| Measurement | Half-block bound | Binomial block bound |
|---|---:|---:|
| Iterations | 1,344 | 912 |
| Corrector adjacency entries | 7,787 | 5,211 |
| Terminal PG adjacency entries | 24 | 24 |
| Total counted adjacency entries | 7,811 | 5,235 |
| Median process CPU seconds | 0.7869 | 0.5255 |
| Median wall seconds | 0.7903 | 0.5276 |

Both runs use eleven source-statistic visits, nineteen degree replies,
twenty-four first adjacency entries, and six output records. Both final
certificates are exactly 1/1,280,000. Their exact endpoints differ as
expected. Each variant repeats its own exact endpoint and stage summaries
in its second run.

The measured CPU and wall speedups are both approximately 1.50x. Timing
clocks alone use floating values; all solver arithmetic, comparisons,
projection decisions, and outputs remain exact and deterministic. No
optional arithmetic dependency or implementation edit outside this separate
module was needed.
