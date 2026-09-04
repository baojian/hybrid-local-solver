# Exact beta=.483 edge-graft clock cell

## Scope

This is a scoped exact companion result for the canonical zero-start,
one-push-maximal chronology in the stopped masked-input-residual reduction. It
is not an atlas row and should be integrated only after independent replay.

## Graph and parameters

Start from BETA_0482_RETIMED_EDGES and add the two nonsource unit edges

\[
 (8,11),\qquad (3,11).
\]

The graph is simple, undirected, connected, has \(27\) vertices and \(64\)
edges, and retains the point source at vertex \(0\). Use

\[
 s=\frac1{224},\qquad
 \alpha=\frac1{100351},\qquad
 \rho_{\rm scale}=\frac{311}{20000},\qquad
 \beta=\frac{483}{1000}.
\]

## Exact replay result

The fraction-exact tracer executes a strict empty-input-batch failure at
phase \(24\), product \(8\), vertex \(15\). Numerically only for readability,

\[
 \frac{\xi_{15}}{W_{24}}
   =-2.0614868460881893\ldots\times 10^{-8}<0,
\]

while the immediately preceding width ratio is

\[
 0.4847047125745568\ldots>0.483.
\]

The exact same-chronology beta cell is

\[
 [\,0.4792472459633430\ldots,
      0.4833996795139087\ldots\,).
\]

The lower endpoint is attained at phase \(23\), product \(1\), row \(9\); the
upper endpoint is attained at phase \(24\), product \(3\), row \(26\).

The seven stop ratios in the failure phase are approximately

\[
 0.48866557,\ 0.48648476,\ 0.48339968,\
 0.48692307,\ 0.49151859,\ 0.49034408,\ 0.48470471.
\]

Products \(1\)--\(3\) are maximized at row \(26\), and products \(4\)--\(7\)
at row \(25\). Thus the new edge raises the former product-\(7\) bottleneck,
but product \(3\) becomes the unique limiting clock event. This is evidence
for a two-clock equioscillation design problem rather than a monotone
single-leaf improvement mechanism.

## Verification

Run

~~~bash
python3 manuscript/notes/spectral_balance_threshold_batch/stopped_masked_input_residual_beta_0483_edge_graft_exact.py
~~~

The wrapper asserts the graph, failure chronology, empty input batch, strict
negative residual, exact chronology cell, endpoint attainments, and all seven
failure-phase clock maximizers.

## What this does and does not prove

This is a rigorous finite witness throughout its exact half-open beta cell. It
does not supply a family reaching every fixed \(\beta<1/2\). In particular,
bounded searches with one pendant leaf or one length-two pendant path are only
computational evidence and are not an obstruction theorem.
