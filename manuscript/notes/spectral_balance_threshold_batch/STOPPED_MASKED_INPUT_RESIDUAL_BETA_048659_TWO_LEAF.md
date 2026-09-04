# Exact beta=.487 two-leaf extension

Date: 2026-09-04

This unregistered companion freezes a Fraction-exact positive-root witness.
It should enter the global atlas only after independent replay.

Start from BETA_04864_CLOCK_REWIRE_EDGES, replace edge \((1,11)\) by
\((1,4)\), and add the two pendant leaves

\[
 (4,27),\qquad (15,28).
\]

The resulting graph is simple, connected, undirected, unit weighted, and has
29 vertices and 66 edges. Use

\[
 s=\frac1{65536},\qquad
 \rho_{\rm scale}=\frac{367530301}{25000000000},\qquad
 \beta=\frac{487}{1000}.
\]

The exact run first violates the active input cone at phase \(24\), product
\(8\), at the new leaf \(28\), with an empty input batch:

\[
 \frac{\xi_{28}}{W_{24}}
 =-1.5293003742606772\ldots\times10^{-12}<0.
\]

The same-chronology beta cell is

\[
 [\,0.4861893592528099\ldots,\,
    0.4870256869778903\ldots\,).
\]

Its lower endpoint is phase \(23\), product \(1\), row \(7\). Its upper
endpoint is phase \(24\), product \(7\), row \(25\), and is also the
predecessor ratio immediately before the failure. The seven continued ratios
in the failure phase are approximately

\[
 .49111145,\ .48927502,\ .48702569,\ .48980820,\
 .49315458,\ .49192934,\ .48702569.
\]

Products \(1\)--\(3\) are maximized by row \(26\), and products \(4\)--\(7\)
by row \(25\). The two new leaves do not themselves supply the stopping
maximum. Instead, their joint retiming preserves the old two-clock relay and
makes the second new leaf the strict failing row. This explains why every
single-leaf scan can fail while a two-leaf construction succeeds.

Run

~~~bash
python3 manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_048659_two_leaf_exact.py
~~~

The wrapper asserts the full graph, strict failure, empty input batch, exact
cell equality, endpoint attainments, failure face, and complete sequence of
failure-phase maximum rows.
