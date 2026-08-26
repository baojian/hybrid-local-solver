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
specializes it to spider prefixes, and gives a finite fixed-face work bound.
It then records the stronger existing response results: exact RPPR support and
solution can already be found locally on hub-rooted spiders, arbitrary rooted
trees, and graphs with bounded biconnected blocks.  Choosing the RPPR
regularization at the PPR accuracy scale converts those results into semantic
PPR guarantees.  It also distinguishes the already-proved radial two-rung
finite-spider theorem from the sharper open question of log-free semantic
damping for plain optimal SOR.  The remaining graph-uniform obstacle is not
tree geometry;
it is changing signed state and output-sensitive boundary reporting inside
large biconnected cyclic cores.

Build from this directory with:

```bash
make
python3 verify_spider.py
python3 verify_fixed_face.py
```
