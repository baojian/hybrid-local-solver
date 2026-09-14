# A limitation of coordinatewise-safe polynomial inverse approximations

Status: proved restricted-method obstruction. This is **not** a lower bound for OP2, for deterministic local algorithms generally, or for objective-gap accuracy. All constructions below are deterministic. The only manuscript reference read for this work is `manuscript/notes/problem_definitions/main.tex`.

## Statement

Fix `0 <= q < 1`, an integer `t >= 0`, and a real polynomial

\[
p_t(z)=\sum_{k=0}^t a_kz^k.
\]

Suppose that for every finite simple regular connected graph, with normalized adjacency matrix `N`,

\[
0\leq p_t(N)\leq (I-qN)^{-1}
\tag{1}
\]

entrywise. Then

\[
0\leq a_k\leq q^k \qquad (0\leq k\leq t).
\tag{2}
\]

Consequently, on every regular graph,

\[
1-(1-q)p_t(1)\geq q^{t+1}.
\tag{3}
\]

In particular, the relative residual operator obeys

\[
\left\|I-(I-qN)p_t(N)\right\|_2\geq q^{t+1}.
\tag{4}
\]

For the PageRank normalization in the problem definitions,

\[
a=\frac{1+\alpha}{2},\qquad q=\frac{1-\alpha}{1+\alpha},\qquad Q=a(I-qN).
\]

Thus a graph-uniform polynomial lower inverse of this kind cannot attain relative residual `delta` in degree `O(alpha^(-1/2) log(1/delta))` uniformly as `alpha -> 0`. For `0 < alpha <= 1/2`, a necessary bound is

\[
t+1\geq\frac{\log(1/\delta)}{\log(1/q)}
\geq\frac{3}{8\alpha}\log(1/\delta).
\tag{5}
\]

Here `0 < delta < 1`. At `q=0` (`alpha=1`) the inverse is the identity and no nontrivial iteration lower bound is asserted.

## Deterministic hypercube test family

Let `H_d` be the `d`-dimensional binary hypercube, with vertex set `{0,1}^d`, edges joining binary vectors that differ in exactly one coordinate, and degree `d`. It is a finite simple connected regular graph. Write

\[
N_d=\frac{1}{d}\sum_{j=1}^d X_j,
\]

where `X_j` flips coordinate `j`. The matrices `X_j` commute. Fix an integer `ell >= 0`, take `d >= ell`, and choose vertices `u,v` at Hamming distance `ell`.

### Polynomial entries

For each fixed `k`,

\[
\lim_{d\to\infty}d^\ell (N_d^k)_{uv}
=\begin{cases}\ell!,&k=\ell,\\0,&k\ne\ell.\end{cases}
\tag{6}
\]

Indeed, no walk of length less than `ell` reaches `v`. Exactly `ell!` walks of length `ell` do so. If `k > ell`, the parity condition requires `k-ell` even. Any reaching walk must flip each of the `ell` prescribed coordinates an odd number of times, and every other used coordinate an even number of times. It therefore uses at most `(k-ell)/2` additional coordinate labels. For fixed `k,ell`, its number of possible label sequences is `O_{k,ell}(d^((k-ell)/2))`. Since each walk has weight `d^(-k)`, multiplying by `d^ell` gives `O_{k,ell}(d^(-(k-ell)/2))`, which vanishes. For odd `k-ell`, the entry is identically zero.

It follows that, for `ell <= t`,

\[
\lim_{d\to\infty}d^\ell p_t(N_d)_{uv}=\ell!a_\ell.
\tag{7}
\]

### Resolvent entries, including the domination check

Because the spectrum of `N_d` lies in `[-1,1]` and `q < 1`,

\[
(I-qN_d)^{-1}=\int_0^\infty e^{-s}e^{qsN_d}\,ds.
\]

Commutativity and the hypercube tensor-product structure give

\[
\bigl(e^{qsN_d}\bigr)_{uv}
=\sinh(qs/d)^\ell\cosh(qs/d)^{d-\ell}.
\tag{8}
\]

For every fixed `s >= 0`,

\[
d^\ell\sinh(qs/d)^\ell\cosh(qs/d)^{d-\ell}
\longrightarrow(qs)^\ell.
\]

For domination, use `sinh(z) <= z exp(z)` and `cosh(z) <= exp(z)` for `z >= 0`. The scaled integrand is bounded by

\[
e^{-s}d^\ell\sinh(qs/d)^\ell\cosh(qs/d)^{d-\ell}
\leq(qs)^\ell e^{-(1-q)s}.
\tag{9}
\]

The right-hand side is integrable on `[0,infinity)` for every fixed `q<1` and `ell`. Dominated convergence yields

\[
\lim_{d\to\infty}d^\ell (I-qN_d)^{-1}_{uv}
=\int_0^\infty e^{-s}(qs)^\ell\,ds
=q^\ell\ell!.
\tag{10}
\]

For `ell=0`, the integrand convention is `(qs)^0=1`, including `q=0`. For `ell>0` and `q=0`, the resolvent off-diagonal entry is zero and the displayed limit is zero directly.

## Proof of the coefficient and residual bounds

Apply (1) on `H_d` to a pair at distance `ell <= t`, multiply by `d^ell`, and pass to the limits (7) and (10). This proves `0 <= ell! a_ell <= ell! q^ell`, hence (2).

Summing (2) gives

\[
p_t(1)\leq\sum_{k=0}^t q^k=\frac{1-q^{t+1}}{1-q}.
\]

This is (3). Since `N one = one`, the vector `one` is an eigenvector of the residual operator with eigenvalue `1-(1-q)p_t(1)`, proving (4).

Finally,

\[
\log(1/q)=\log\frac{1+\alpha}{1-\alpha}
=\int_0^\alpha\frac{2}{1-u^2}\,du
\leq\frac83\alpha \quad (0<\alpha\leq1/2).
\]

Combining `q^(t+1) <= delta` with this bound proves (5).

## Point-source meaning and precise scope

On a `d`-regular graph with seed `v`, the PageRank approximation obtained from this polynomial is

\[
\widehat\pi=(1-q)p_t(N)e_v.
\]

Condition (1) makes it nonnegative and coordinatewise below exact PageRank. Its missing total probability mass satisfies

\[
\|\pi-\widehat\pi\|_1
=1-(1-q)p_t(1)\geq q^{t+1}.
\tag{11}
\]

This statement concerns unregularized inverse approximation and total mass / residual-operator accuracy. It does **not** translate by itself into an RPPR objective-gap lower bound. In particular, a mass deficit can be spread over many coordinates while its Euclidean energy is small. OP2 also permits adaptive active sets, rational methods, certificates, truncation, and nonlinear operations that are not fixed polynomial inverse maps.

## Extension: coefficients may adapt to the hypercube dimension

The fixed-coefficient statement above has a useful strengthening. Fix `q,t` and let `p_{t,d}` have arbitrary real coefficients depending on `d`, with degree at most `t`. Suppose its output on one fixed hypercube seed is coordinatewise safe:

\[
0\leq p_{t,d}(N_d)e_v\leq(I-qN_d)^{-1}e_v.
\tag{12}
\]

Then its coefficients satisfy, for every `0 <= ell <= t`,

\[
\liminf_{d\to\infty}a_{\ell,d}\geq0,
\qquad
\limsup_{d\to\infty}a_{\ell,d}\leq q^\ell,
\tag{13}
\]

and therefore

\[
\liminf_{d\to\infty}
\bigl[1-(1-q)p_{t,d}(1)\bigr]\geq q^{t+1}.
\tag{14}
\]

To prove this, work downward from `ell=t`. At distance `t`, only the leading coefficient contributes, so (12) and (10) bound `a_{t,d}` and imply (13). Suppose all coefficients with index greater than `ell` are already bounded. After multiplying the distance-`ell` entry by `d^ell`, their total contribution tends to zero by (6), while the coefficient of `a_{ell,d}` is exactly `ell!`. Applying (12) and (10) gives (13) for `ell`, closing the induction. Summing the finitely many upper-limit bounds proves (14).

This extension rules out a uniform improvement for coordinatewise-safe degree-`t` polynomial Krylov outputs even when their scalar coefficients adapt to the graph within this explicit family. It still gives neither an objective-gap lower bound nor a lower bound against nonlinear adaptive algorithms.

## Checks

- No probabilistic graph construction is used; every test graph is an explicit hypercube.
- The graph is simple, connected, unweighted, and regular, as required by the reference model.
- The degree parameter `d` is distinct from the polynomial degree `t`; limits hold with `q,t,ell` fixed.
- The infinite resolvent series is handled by an integral and an explicit integrable dominating function, rather than by interchanging an unjustified infinite sum and limit.
- The case `q=0` forces `a_0` in `[0,1]` and all higher coefficients zero; the iteration lower bound is then vacuous.
- The result is a restricted-method obstruction and cannot be cited as a negative answer to Conjecture 2.

## Supplement A: safe positive mixtures of shifted resolvents

There is also a precise limitation for one simple family of rational approximations. Set `A=I-qN`, and consider

\[
R(A)=\sum_{j=1}^J w_j(A+\sigma_jI)^{-1},
\qquad w_j\geq0,\quad\sigma_j\geq0.
\tag{15}
\]

The finite list of weights and shifts is fixed across graphs. Then

\[
0\leq R(A)\leq A^{-1}\quad\hbox{entrywise on every graph}
\quad\Longleftrightarrow\quad
\sum_j\frac{w_j}{1+\sigma_j}\leq1.
\tag{16}
\]

For necessity, apply the hypercube diagonal limit separately to each shifted resolvent: its limit is `1/(1+sigma_j)`, while the limit of `A^(-1)` is `1`. For sufficiency, expand

\[
R(I-qN)=\sum_{k=0}^\infty q^k N^k
\left(\sum_j\frac{w_j}{(1+\sigma_j)^{k+1}}\right).
\]

All coefficients are nonnegative and, under the right side of (16), the parenthesized expression is at most `1`. Comparison with the Neumann series proves the entrywise inequality.

Let `mu=1-q`, suppose `0<mu<=1/2`, and request relative inverse accuracy at the slow eigenvalue with `0<delta<=1/4`:

\[
\mu R(\mu)\geq1-\delta.
\]

Write `lambda_j=w_j/(1+sigma_j)`, so `sum_j lambda_j<=1`. With `sigma_min` the smallest shift having positive weight,

\[
\mu R(\mu)
=\sum_j\lambda_j\frac{\mu(1+\sigma_j)}{\mu+\sigma_j}
\leq\frac{\mu(1+\sigma_{\min})}{\mu+\sigma_{\min}}.
\]

The last fraction decreases in its shift. Rearranging the desired lower bound gives

\[
\sigma_{\min}\leq\frac{\mu\delta}{1-\delta-\mu}
\leq4\mu\delta.
\tag{17}
\]

Thus a universally safe mixture cannot achieve a fixed good relative accuracy using only substantially larger, easier shifts. At least one shifted system retains a condition number on the order of the original one. This statement excludes neither general rational functions nor rational powers, recursive solvers, or nonlinear certificates. It does not establish an OP2 lower bound.

