# Independent audit of the optional singleton precheck

Audited source: `singleton_precheck_rppr.py`, SHA-256
`54d4f30160034f27aac40d947353919b4c41d7163d820ab096d20bc1087efcbc`.
The source was unchanged across this audit. No existing solver or package
file was edited. I independently derived the condition, inspected all
branches, and ran a separate bounded diagnostic rather than rerunning the
implementation author's exhaustive suite. **No defect found.**

## Mathematical equivalence

Write `q0=(1+alpha)/2`, `c=(1-alpha)/2`, and `lambda=alpha*rho`.
In degree density coordinates, the nonnegative objective has Hessian
`H=q0 D-c A`, linear term `-alpha e_seed`, and regularizer
`lambda sum_i d_i f_i`. This is the original objective with
`x_i=sqrt(d_i) f_i`. Its Hessian is positive definite for positive degrees
and `alpha>0`. The restriction to nonnegative coordinates loses no
optimum: replacing a vector by its entrywise absolute value cannot
increase its Stieltjes quadratic, cannot increase the negative point-source
linear term, and leaves the weighted absolute-value regularizer unchanged.

Let `d=d_seed`. If `rho*d>=1`, the gradient at zero is nonnegative in every
coordinate, so zero is the unique optimum. This includes equality. Source
lines 63–64 implement precisely this branch before the alpha-one branch.
If `alpha=1` and `rho*d<1`, the Hessian is diagonal and only the seed is
positive, with density `1/d-rho` (lines 65–68). Both branches require only
the seed degree.

In the remaining case, seed stationarity uniquely determines the positive
seed-only candidate

`f = alpha(1-rho*d)/(q0*d)
   = 2 alpha(1-rho*d)/(d(1+alpha))`.

Its inactive gradient is `lambda*d_i-c*f` at a seed neighbor, and
`lambda*d_i>0` at every other coordinate. Hence it is the exact unique
optimum if and only if every encountered neighbor satisfies

`(1-alpha)(1-rho*d) <= rho*d*(1+alpha)*d_i`.

For `alpha=A/D` and `rho=P/R`, clearing positive denominators gives

`(D-A)(R-P*d) <= P*d*(D+A)*d_i`.

This is exactly the precomputed comparison in lines 73–74 and 86. Strict
failure is correct: equality gives a valid zero-coordinate KKT condition
and must be accepted. Lines 94–97 return the same stationary density, with
zero objective gap. A failing inequality means the unique stationary
seed-only candidate is not optimal, so the fallback branch is necessary.
No numerical tolerance or minimum support margin enters the test.

The returned singleton is a valid sparse final answer: it is positive,
has support volume `d<1/rho`, and has the specified density representation
without requiring a square-root primitive. Its density need not be dyadic;
the helper correctly treats it as a final output, not as an intermediate
dyadic continuation baseline. A singleton automatically meets the common
density denominator contract of the independent sparse certificate.

## Streaming locality, accounting, and interface

The input contract remains a finite simple undirected graph with positive
integer degrees. The wrapper is not a global validator of this contract;
in particular it does not discover duplicate edges, self-loops, or
inconsistent unqueried reverse rows. That is the same valid-input graph
assumption as the underlying theorem, not an additional algorithmic gap.

After one seed degree reply, the default cutoff permits a row trial only
at degree at most 32. Lines 77–89 consume one entry, request exactly that
neighbor's degree, and test it before requesting another entry. No boundary
adjacency row is read. On success the completed row length is checked
(lines 90–93); on failure the loop stops immediately. The independent
diagnostic uses a generator that raises if a second entry is requested
after the first failing neighbor, so it checks actual streaming rather
than merely a retrospective entry counter.

For valid input, a tried row costs at most `d` entries, `d+1` degree replies,
and `O(d+1)` arithmetic/comparison/stored-state operations. There is only a
constant number of live numeric records and no label dictionary or set.
With the default cutoff this is constant extra word work. Even a supplied
larger cutoff cannot create an asymptotic locality problem: a row is tried
only after the direct zero test failed, so `d<1/rho`; thus its whole trial
cost is `O(1/rho)`. A cutoff skip costs one degree reply and constant scalar
work. These bounds presume the stated oracle model; the implementation
does not make construction of an oracle-owned row object free.

The named metric fields count logical operations, not every Python
instruction. The remaining validation, arithmetic and metric updates are
constant per consumed neighbor, so they fit the same bound. Successful
nonempty output has three emitted words. A fallback's output is not copied
or rematerialized: lines 100–102 preserve the exact `fallback_result`
object, its exact `output` object, and its exact gap-bound object. The
fallback receives the original oracle, the original seed, and normalized
exact input parameters. It may repeat the earlier seed or row reads;
those are real additional accesses in its untouched ledger. Therefore
total cost is the trial ledger **plus** all supplied fallback ledgers.
The wrapper itself acquires no certificate for an arbitrary callback; the
supplied fallback must obey the advertised certified-solver contract.

## Bit costs

Let `B` bound the encoding lengths of the normalized rational parameters,
cutoff, encountered degrees and labels. At the nontrivial branch,
`P*d<R`; consequently the stored `weighted_rho` and `R-weighted_rho` each
have at most `B` bits, even though their multiplication can have up to
`2B` temporary bits. The left comparison operand has at most `2B` bits,
the precomputed coefficient at most `2B+1`, and multiplication by a
neighbor degree at most `3B+1`. The final density numerator has at most
`2B+1` bits and its unnormalized denominator at most `3B+1`. All are
constant multiples of `B`. Direct alpha-one subtraction and parameter
normalization likewise use a fixed number of bounded-length rational
operations. The loop performs integer arithmetic only; there is no sum of
reciprocals, accumulating denominator, sorting, or randomized balancing.

Thus a conservative elementary bit bound is `O((d+1) B^3)` for a tried
row, inclusive of normalization and the final gcd, and `O(B)` auxiliary
bit storage apart from input/output and the oracle's own iterator. The
exact algebraic-word bound is `O(d+1)`. The claim is about exact rational
inputs and their normalized encoding; passing a binary float asks Python
to use that float's exact binary rational value, not an unprovided decimal
value. General fallback bit costs remain separate and unchanged.

## Independent evidence

Run:

```
python3 -B audit_singleton_precheck_independent.py
```

`singleton_precheck_independent_verification.json` records a passing run:

- 15 exact threshold cases on independently defined virtual spoke graphs,
  with seed degrees 1, 2, 7, 32, and 33. Each minimum neighbor degree is
  tested at its exact KKT threshold and at both sides separated by a
  relative `2^-257` perturbation. Other boundary degrees are much larger.
- 10 successful singleton outputs independently re-certified with exact
  zero subgradient norm and zero objective-gap bound; equality is checked
  by a separately evaluated rational KKT residual.
- Five failed-trial cases preserve all fallback field/object identities;
  original oracle/seed delivery and exact normalized parameters are checked.
- Three direct branches, including zero at exact equality and alpha-one
  with a zero cutoff; two cutoff skips; an immediate-failure generator
  guard; and rejection of a completed row with an incorrect length.
- Hash-forbidden signed labels longer than 4099 bits, rational parameter
  components up to 785 bits, and encountered degrees up to 181 bits.

The virtual spoke degrees are realized by attaching private leaves to
each seed neighbor. Those leaves and boundary rows are never constructed
or read. The diagnostic uses no randomized generation and makes no
performance or general convergence inference from the finite tests.
