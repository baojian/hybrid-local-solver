# Averaged positive coupling and a deterministic threshold reporter

Date: 2026-09-05. Status: **Proved rate and local algebra; work bound open.**

This candidate differs from the primal-PG/postprojected-auxiliary method in
`positive-linear-coupling.md`. Do not transfer one candidate's volume ledger
to the other.

## A moving-domain accelerated update

Let `s=sqrt(alpha)`, `q=1-s`, `K=Q-alpha I`, and
`C={z>=0:w^Tz<=1}`. From `x=z=0` perform

\[
 y=(x+s z)/(1+s),\qquad
 z^+=\Pi_C\big(qz+s y-(Qy-c)/s\big),\qquad
 x^+=q x+s z^+.
\]

Both x and z remain in C. The raw auxiliary vector also equals
`qz-Ky/s+c/s`. The primal update is the Euclidean projection of
`y-(Qy-c)` onto the moving convex set `q x+s C`.

### Proved here: the same accelerated potential

The comparator `u=q x+s x_rho^*` belongs to that moving set. Applying the
projected-gradient inequality to u, and then strong convexity to its convex
combination, gives exactly the weighted-comparator inequality used in the
other candidate's proof. Explicitly, the quadratic terms combine by

\[
 \|y-u\|^2+s q\|x-x_\rho^*\|^2
 =q\|y-x\|^2+s\|y-x_\rho^*\|^2.
\]

With `G=y-x^+`, the exact identity
`z^+=qz+s y-G/s` holds. Expansion therefore yields

\[
 E(x^+,z^+)\le q E(x,z)
 -\frac{\alpha q}{2}\|y-x\|^2
 -\frac{\alpha s q}{2}\|z-y\|^2,
\]

where `E=phi(x)-phi(x_rho^*)+alpha||z-x_rho^*||^2/2`.
The proof does not require the optimum itself to belong to the moving set.

For output, take the ordinary orthant PG point `p=[y-(Qy-c)]_+`.
Its computable certificate is
`(1-alpha)||y-p||^2/(2alpha)`, at most `4E/alpha^2`. A fixed horizon
`O(alpha^(-1/2) log(1/(alpha d_seed eps_obj)))` suffices from zero because
`E_0<=alpha/d_seed`. Output and certification must be charged; the cached
identity below removes the need for an additional matrix product.

## Proved here: sparse score updates with a common scalar decay

Use degree densities `u=D^(-1/2)x`, `v=D^(-1/2)z` and
`K_d=(1-alpha)(I-D^(-1)A)/2`. Define the prethreshold score

\[
 h_k=q v_k-\frac{K_d(u_k+s v_k)}{s(1+s)}
              +s D^{-1}e_{seed}.
\]

The next auxiliary density is

\[
 v_{k+1,i}=[h_{k,i}-s\rho-\lambda_k]_+,
\]

where `lambda_k>=0` enforces `sum_i d_i v_(k+1,i)<=1` with the usual
complementary condition. Direct substitution of `u_(k+1)=q u_k+s v_(k+1)` gives

\[
 h_{k+1}=q h_k+q v_{k+1}-q^2v_k
 -\frac{K_d(2v_{k+1}-q v_k)}{1+s}
 +\alpha D^{-1}e_{seed}.
\]

Every non-decay correction is supported on the seed, the two auxiliary
supports, and their neighbors. Unmaterialized scores are exactly zero and
cannot pass the positive threshold `s rho+lambda_k`.

### Deterministic data structure interface

Maintain the global multiplier `q^k` and a balanced search tree of normalized
scores `h_(k,i)/q^k`, with subtree sums of degrees and degree times score.
A second balanced tree maps vertex labels to their current entries and
degree densities. All balanced-tree operations are worst-case logarithmic;
an expected-time hash table is not part of this claim.

The weighted threshold is found by prefix sums in score order. A binary
search over ranks, with logarithmic prefix queries, costs `O(log^2 N)`;
reporting strictly surviving entries costs their count plus `O(log N)`.
Each local score correction costs `O(log N)`. The auxiliary vectors can be
merged in deterministic vertex order before their adjacency scans.
Mass capping can reactivate previously suppressed scores without fresh
neighbor input; the ordered reporter handles this explicitly. Merely looking
at the newest boundary would be incorrect.

Maintain u with the same common multiplier and sparse additions. Its final
support is the union of past auxiliary supports. In finite
precision, periodic rebasing of the common multiplier is charged, with at
most logarithmically many rebases over the stated horizon. These algebraic
claims do not supply a coefficient-bit stability theorem.

Consequently, if

\[
 W_z=\sum_{k=0}^{T}\operatorname{vol}(\operatorname{supp}(z_k)),
\]

then this interface has fully charged `O_tilde(T+W_z)` work, including score
maintenance, scalar arithmetic/state, degree replies, projection, output,
and certification. It does not require scanning all historical rows
at every iteration.

### Proved here: cached ordinary-PG output and certificate

The definition of h implies the exact degree-coordinate identity

\[
 p_i=[q u_i+s h_i-\alpha\rho]_+.
\]

Consequently the ordinary-PG certificate is computed by summing
`d_i ((u_i+s v_i)/(1+s)-p_i)^2` over stored labels. Every omitted label has
`u_i=v_i=h_i=0` and contributes zero. This requires no adjacency inspection.
The number of stored labels is at most one plus cumulative auxiliary neighbor
inspections. Checking at iterations `1,2,4,...` and at the guaranteed final
horizon costs `O(W_z log T)` scalar/state work, which is within the claimed
soft-O interface. A direct sum of squared coordinate differences avoids the
numerically worse subtraction of three global quadratic moments.

### Checked implementation

`local_averaged_coupling.py` implements the score recurrence, weighted rank
threshold, two AVL maps, common decay, sparse corrections, and charged
rebasing. `deterministic_avl.py` supplies the deterministic ordered map.

The first audit passed all 720 insertion permutations of six keys with
deletions and augmented-prefix queries, and 822 graph/parameter cases with
131,520 step-by-step comparisons against a direct matrix implementation.
It also checked 822 actual rebases. The largest optimum-scaled iterate
discrepancy was about `1.59e-13`. A follow-up audit independently compares the
cached certificate output to an ordinary full-matrix PG step and verifies
zero additional neighbor inspections during certification. These are
floating-point implementation checks, not a general coefficient-bit proof.

## Open target

### Proved here: the auxiliary-volume identity

Write `Z_k=sum_i d_i v_(k,i)`,
`H_k=sum_i d_i[-h_(k,i)]_+`, and
`V_(k+1)=vol(supp(v_(k+1)))`. The exact score definition gives
`sum_i d_i h_(k,i)=q Z_k+s`, since `sum_i d_i(K_d y)_i=0`.
On the reported set, `v_(k+1,i)=h_(k,i)-s rho-lambda_k`. Hence

\[
 Z_{k+1}+(s\rho+\lambda_k)V_{k+1}
 \le q Z_k+s+H_k.
\]

Summing from the zero start yields

\[
 s\rho W_z
 \le sT-s\sum_{k<T} Z_k-Z_T
       +\sum_{k<T}(H_k-\lambda_k V_{k+1}).
\]

All terms in this bound are locally computable from the ordered reporter.
In particular, H is obtained by a weighted score-prefix query, and the
threshold multiplier and reported degrees give `lambda V`. This does not
make a bound on their sum automatic. The useful open sufficient condition is

\[
 \sum_{k<T}(H_k-\lambda_k V_{k+1})
 \le \widetilde O(sT+s).
\]

Subtracting total removed auxiliary mass in place of `lambda V` would give
a smaller expression and is not justified by this inequality: removed mass
also includes suppressed coordinates that are not reported. Likewise, an
unweighted quotient count cannot replace V.

Prove `W_z=O_tilde(1/(rho sqrt(alpha)))` on canonical point-source histories,
or give a canonical counterexample. The mass bound alone does not prove it.
Strict support containment already fails in small radial tests; only a
whole-run bound could complete this route. Initial quotient experiments are
encouraging but neither extensive nor certified, and some reached their
experimental 1,000-iteration cap before the stopping certificate.

Next: test the auxiliary-volume ledger on long-holding-time cell graphs and
on deterministic branching-sequence searches. Seek a graph-uniform flux or
projection-debit argument; do not infer it from the mass cap or these tests.
