# From signed stars to spiders and broader graph classes

This independent note answers two questions that should not be conflated.
First, it explains exactly in what sense the unregularized signed-SOR theorem
and the regularized FISTA locality obstruction can be compared.  They share
the PageRank operator and degree-work model, and RPPR is a controlled-bias
surrogate for PPR, but the published star examples do not use the same
objective, seed, or accuracy namespace and therefore do not rank SOR against
FISTA end to end.

Second, the note develops a graph-family ladder.  It proves the optimal
red--black SOR spectral factor on every fixed exposed bipartite face,
specializes it to spider prefixes, scopes the sharp rate to supplied spectral
tuning, and gives a generic finite fixed-face work bound using one
graph-global parameter.  A certified face-specific upper spectral bound also
gives a fully charged tuning formula: its estimation cost is added explicitly,
and constant-relative tuning needs squared-radius accuracy at the
`1-rho_J^2` scale.  A raw Rayleigh estimate from below is not a safe
certificate.
The note also gives a concrete a-posteriori implementation of that safe
upper certificate.  Componentwise Collatz bounds are aggregated and scaled,
one full face scan is charged per estimator product, and a checkable
relative-gap inequality licenses a frozen SOR parameter.  There is no uniform
bound on the number of estimator scans: a fixed scan budget falls back to the
graph-global parameter, and a complete face receives exactly that global
advice with no sweep improvement.
On complete equal-arm hub-seeded spiders, it proves a new dimension-free
maximum-norm theorem: plain optimal SOR reduces semantic error by
`lambda^(2k) (1 + 2k(1-lambda^2))`, giving log-free
`O(1/(sqrt(alpha) eps_ppr))` output-scale work.  An exact two-vertex witness
shows why the source color must be swept first.

The radial maximum-norm result cannot be promoted to all bipartite graphs.
An exact layered counterfamily with geometrically decreasing channel
multiplicities keeps a far semantic error almost unchanged through any fixed
multiple of `1/sqrt(alpha)` source-first full sweeps.  It rules out every
graph-universal constant exponential envelope and, because the seed output is
at inverse-volume scale, rules out graph-uniform
`O(1/(sqrt(alpha) eps_ppr))` work for this literal complete-face full-sweep
plain-SOR primitive.  This does not lower-bound other local or response-based
algorithms.  The finite-propagation stop does, however, survive arbitrary
finite scalar relaxation schedules that retain source-first color blocks, and
it survives zero-start Chebyshev, CG/Krylov, heavy-ball, and Richardson
recurrences built only from scalar combinations and complete sparse PageRank
matvecs.  Exact eigenvalues used as scalars do not break locality; eigenvector
transforms, inverse/Green responses, global warm starts, and nonlocal
preconditioners are explicitly outside the theorem.

For nested bipartite faces, the note also proves exact nonsettled
face-shock Pythagoras and a conditional continuation theorem under supplied
geometric volume growth.  It then records the stronger existing response
results: exact RPPR support and solution can already be found locally on
hub-rooted spiders, arbitrary rooted trees, and graphs with bounded
biconnected blocks.  Choosing the RPPR regularization at the PPR accuracy
scale converts those results into semantic PPR guarantees.  The remaining
graph-uniform obstacle is not tree geometry or numerical state transport;
it is avoiding repeated face scans and maintaining an output-sensitive
boundary reporter inside large biconnected cyclic cores.

Build from this directory with:

```bash
make
python3 verify_spider.py
python3 verify_fixed_face.py
python3 verify_adaptive_spectral.py
```
