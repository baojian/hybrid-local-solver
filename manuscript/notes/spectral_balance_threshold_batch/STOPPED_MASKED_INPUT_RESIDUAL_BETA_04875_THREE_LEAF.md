# Exact beta=.4875 three-leaf extension

Date: 2026-09-04

This unregistered companion freezes a Fraction-exact finite positive-root
witness. Start from the two-leaf graph in
STOPPED_MASKED_INPUT_RESIDUAL_BETA_048659_TWO_LEAF.md and add

\[
 (1,29).
\]

The resulting graph is simple, connected, undirected, unit weighted, and has
30 vertices and 67 edges. Use

\[
 s=\frac1{65536},\qquad
 \rho_{\rm scale}=\frac{2879}{200000},\qquad
 \beta=\frac{975}{2000}.
\]

The exact run first violates the active input cone at phase \(25\), product
\(8\), at leaf \(28\), with an empty input batch:

\[
 \frac{\xi_{28}}{W_{25}}
 =-1.0153101969295677\ldots\times10^{-12}<0.
\]

Its exact same-chronology beta cell is

\[
 [\,0.48675686401696866\ldots,\,
    0.4875724218291617\ldots\,).
\]

The lower endpoint is phase \(24\), product \(1\), row \(7\). The upper
endpoint is phase \(25\), product \(3\), row \(26\). The seven continued
ratios in the failure phase are approximately

\[
 .49144102,\ .48971467,\ .48757242,\ .49034411,\
 .49368583,\ .49252294,\ .48773412.
\]

Products \(1\)--\(3\) are maximized at row \(26\), and products \(4\)--\(7\)
at row \(25\). The third leaf shifts the strict leaf-28 failure one phase
later and raises the clock relay without becoming a stopping maximizer.

Run

~~~bash
python3 manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_04875_three_leaf_exact.py
~~~

The wrapper asserts the graph, strict failure, empty input batch, exact cell,
endpoint attainments, failure face, and failure-phase maximum-row relay. A
separately audited zero-root growing-family cell may dominate this finite
upper endpoint; this witness remains useful as a direct finite graph and as
evidence for the repeated-leaf retiming mechanism.
