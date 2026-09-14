# Worked example: an endpoint-seeded three-vertex path

Consider the path `1 — 2 — 3`, with seed 1, degrees `(1,2,1)`,
`alpha=1/4`, final regularization `rho=1/16`, and requested additive
objective accuracy `epsilon=10^-6`. This example derives the entire exact
solution path and compares it with one run of the packaged `solve_fast`.
It illustrates the proved guarantees; a three-vertex calculation is not
evidence for a graph-uniform complexity theorem.

All mathematical checks and solver computations below use exact rational
arithmetic. Decimal numbers in tables are display approximations. The
complete exact values, package hashes, stage summaries, and oracle counts
are saved in `worked_three_vertex_example.json`.

## Exact solution path and its activation thresholds

Use degree densities `f_i=x_i/sqrt(d_i)`. Thus the normalized optimization
vector is `x=(f_1,sqrt(2)f_2,f_3)`, and its mass is
`m=f_1+2f_2+f_3`. On the nonnegative orthant the objective is

$$
F_r(D^{1/2}f)=\frac1{16}f^T
\begin{pmatrix}5&-3&0\\-3&10&-3\\0&-3&5\end{pmatrix}f
-\frac14f_1+\frac r4(f_1+2f_2+f_3).
$$

Replacing a vector by its coordinatewise absolute value cannot increase
the original objective: the cross terms are nonpositive, the seed term
favors a nonnegative first coordinate, and the absolute-value penalty is
unchanged. Strict convexity then gives a unique nonnegative optimum.

For a proposed nonnegative density vector define the scaled KKT slack

$$
k=\begin{pmatrix}
5f_1-3f_2-2+2r\\
-3f_1+10f_2-3f_3+4r\\
-3f_2+5f_3+2r
\end{pmatrix}.
$$

Here `k_i=8 sqrt(d_i) grad_i J_r(x)`. The necessary and sufficient
conditions are `f>=0`, `k>=0`, and `f_i k_i=0` for every coordinate.

1. For `r>=1`, `f=0` has slack `(2r-2,4r,2r)>=0`.
2. With only vertex 1 positive, stationarity gives
   `f_1=2(1-r)/5`. The second slack is `(26r-6)/5`, so vertex 2 remains
   inactive down to `r=3/13`.
3. With vertices 1 and 2 positive, solving their two stationarity equations
   gives `f_1=(20-32r)/41`, `f_2=(6-26r)/41`. The third slack is
   `(160r-18)/41`, so vertex 3 remains inactive down to `r=9/80`.
4. With all vertices positive, solving the three equations gives the
   unregularized density `(41/80,3/16,9/80)` minus `r(1,1,1)`.

Consequently,

$$
f^*(r)=
\begin{cases}
(0,0,0), & r\ge1,\\[2pt]
\bigl(2(1-r)/5,0,0\bigr), & 3/13\le r\le1,\\[2pt]
\bigl((20-32r)/41,(6-26r)/41,0\bigr),
     & 9/80\le r\le3/13,\\[2pt]
\bigl(41/80-r,3/16-r,9/80-r\bigr), & 0\le r\le9/80.
\end{cases}
$$

The formulas agree at every shared endpoint. At an activation threshold,
the newly admitted coordinate is still zero; it becomes positive
immediately below that threshold. The complete symbolic KKT check is:

| Regularization interval | Scaled slack `k` | Positive support in the interval interior |
|---|---|---|
| `r>=1` | `(2r-2,4r,2r)` | empty |
| `3/13<=r<=1` | `(0,(26r-6)/5,2r)` | `{1}` |
| `9/80<=r<=3/13` | `(0,0,(160r-18)/41)` | `{1,2}` |
| `0<=r<=9/80` | `(0,0,0)` | `{1,2,3}` |

The affine density and slack coefficients were independently substituted
into the matrix equations. Their endpoint signs prove nonnegativity over
each whole interval, and the products are identically zero. As an additional
check, exact KKT tests passed at 184 rational values, including every
threshold and points on both sides. These samples are supplementary to
the interval calculation.

The optimal masses in the three nonzero regimes are respectively
`2(1-r)/5`, `(32-84r)/41`, and `1-4r`. At the requested final parameter,

$$
f^*(1/16)=\left(\frac9{20},\frac18,\frac1{20}\right),\qquad
x^*_{1/16}=\left(\frac9{20},\frac{\sqrt2}{8},\frac1{20}\right),
$$

with mass `3/4`, deficit `1/4`, support volume `4`, and objective
`F_(1/16)(x*)=-129/2560`.

## The four packaged continuation stages

The solver starts with the exact zero baseline at `r_0=1` and uses
`r=1/2,1/4,1/8,1/16`. Its dyadic momentum is `theta=1/2`. The repaired
baselines returned by the four stages are:

| `r` | Exact optimum density | Repaired density, approximately | Accelerated steps | Repaired support |
|---|---|---|---:|---|
| `1/2` | `(1/5,0,0)` | `(0.138671875,0,0)` | 4 | `{1}` |
| `1/4` | `(3/10,0,0)` | `(0.269695282,0,0)` | 4 | `{1}` |
| `1/8` | `(16/41,11/164,0)` | `(0.374761850,0.051549241,0)` | 8 | `{1,2}` |
| `1/16` | `(9/20,1/8,1/20)` | `(0.449870922,0.124870922,0.049870923)` | 16 | `{1,2,3}` |

All four stages terminated at an accepted independent checkpoint. The
coarse intermediate baselines intentionally lie visibly below their
optima: terminal clipping supplies a safe next-stage source. Their shifts
are `1/16`, `1/32`, `1/64`, and finally `1/8192`, where the final shift is
reduced to meet the requested output accuracy.

| `r` | Actual repaired objective gap | Proved repair bound `2 delta^2/r` |
|---|---:|---:|
| `1/2` | `1.175355911e-3` | `1/64` |
| `1/4` | `2.869924794e-4` | `1/128` |
| `1/8` | `1.353962469e-4` | `1/256` |
| `1/16` | `8.330525610e-9` | `1/2097152` |

The independent checkpoint bound certifies the candidate **before**
terminal repair. The table reports the repaired vector's gap, which can be
larger after clipping. Confusing those two vectors would give an incorrect
comparison; the separate repair bound is the relevant one here.

## Source, mass, support, and locality checks

For a baseline density `bar f`, the residual source densities are explicitly

$$
\frac{s_1}{w_1}=\frac14-\frac58\bar f_1+\frac38\bar f_2,
\qquad
\frac{s_2}{w_2}=-\frac58\bar f_2+\frac3{16}(\bar f_1+\bar f_3),
\qquad
\frac{s_3}{w_3}=-\frac58\bar f_3+\frac38\bar f_2.
$$

At every stage the exact checks verified:

- The old baseline is coordinatewise below the repaired baseline, which
  is below `f*(r)`.
- Every input source density lies in `[0,4 alpha r]=[0,r]`.
- Every repaired source density lies in `[0,2 alpha r]=[0,r/2]`, giving
  the next factor-two stage its input interval.
- The correction cap is exactly `eta=1-(bar f_1+2 bar f_2+bar f_3)`, and
  the source mass is exactly `sum_i d_i(s_i/w_i)=alpha eta`.
- Repaired support is contained in the exact optimum's support; its volumes
  are `1,1,3,4`, each at most `1/r`.

Some of these numbers can be inspected directly:

| Stage `r` | Input correction cap `eta` | Largest repaired source density | Allowed upper bound `r/2` |
|---|---:|---:|---:|
| `1/2` | `1` | `0.163330078` | `0.25` |
| `1/4` | `0.861328125` | `0.081440449` | `0.125` |
| `1/8` | `0.730304718` | `0.038049571` | `0.0625` |
| `1/16` | `0.522139668` | `0.015657270` | `0.03125` |

For example, the first repaired baseline is exactly `(71/512,0,0)`.
Its source density is `(669/4096,213/8192,0)`, whose degree-weighted sum
is `(1/4)(1-71/512)`. Thus the next cap `441/512` comes from the actual
baseline, not from the exact optimum's mass.

The four kinetic volumes are `4,4,24,64`. The implementation records
9 first adjacency-entry reads, 101 corrector cached-entry inspections
(including source setup), 29 checkpoint cached-entry inspections, and
9 terminal-PG inspections: 148 entry inspections in all. The final
independent validation below uses a separate oracle and reads four more
entries. Checkpoints make no new external graph queries. These counts
illustrate repeated-scan accounting; they do not establish an asymptotic
bound from this small graph.

## Final exact output and independent accuracy check

The returned density vector is exactly

$$
\widehat f=
\left(
\frac{494638309763}{1099511627776},
\frac{68648515523}{549755813888},
\frac{54833659273}{1099511627776}
\right).
$$

Its actual objective gap, computed from the explicit quadratic and exact
optimum, is

$$
\frac{402839500036915121}{48357032784585166988247040}
\approx8.3305256100\times10^{-9}.
$$

The solver's final repair certificate is `1/2097152`, approximately
`4.768371582e-7`, below the requested `10^-6`. A separately recomputed sparse
subgradient certificate gives approximately `8.3305256101e-9`, independently
confirming the requested accuracy. Its slight excess over the actual gap
comes from the conservative subgradient inequality and integer upward
rounding, not from numerical evaluation of the optimum.

The standard plot shows the exact solution curves and the four repaired
stage baselines. Its horizontal axis is reversed so continuation proceeds
from left to right. All plotted coordinates come from the exact data; only
rendering converts them to floating point.

![Exact density curves and repaired continuation stages](worked_three_vertex_example.png)

Reproduction: `build_worked_three_vertex_example.py` generates the exact
JSON and standalone PNG/PDF plot using the packaged solver and a fresh
three-row oracle. No package, main TeX, or manuscript source was modified.
