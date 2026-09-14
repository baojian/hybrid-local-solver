# Reproduce local-graph measurements

This runner uses only the adjacent solver package and Python's standard
library. It represents large graphs implicitly; no whole graph is built.
All solver parameters, states and accuracy certificates are exact rational
values. Only clocks and descriptive timing summaries use floating point.

From the unpacked package directory, start with one small installation check:

```sh
python3 -I benchmarks/run.py --output benchmark-smoke.json
```

The default is a three-vertex path and the fast solver. To compare an optional
backend against fast in the same process, use one fixed **fast, option,
option, fast** block:

```sh
python3 -I benchmarks/run.py --case four --compare adaptive --output adaptive-abba.json
python3 -I benchmarks/run.py --case four --compare mass-grid --output mass-grid-abba.json
python3 -I benchmarks/run.py --case small-mass --compare mass-grid --output small-mass-abba.json
```

`four` selects the endpoint path, interior square grid, tree attached to a
clique, and hard-alpha path used in the accompanying paired reports. The
`small-mass` case is a three-vertex path with `alpha=1/4`, `rho=1/2^20`, and
`epsilon=1/2^50`; it exercises the optional coarser precision rule. Use
`--help` for the individual case names. A single optional-backend call uses
`--backend adaptive` or `--backend mass-grid`, without `--compare`.

Timing includes the entire solver call: deterministic AVL counting sets,
graph-oracle metering, internal stopping checks, terminal repair, and any
optional source or mass-hint work. Graph construction, pre-run garbage
collection, record serialization, and the separately recomputed final
certificate are outside the timed region. Garbage collection remains
enabled while solving. The output records actual oracle replies, repeated
cached scans, complete stage data and all additional option ledgers.
The displayed rescheduling subtotals for mass-grid are already included in
its ordinary scheduling counters and are not added twice.

An independent final certificate is recorded for every completed output.
Its `independent_certificate_meets_target` field can be false when that conservative bound is
inconclusive; the runner separately checks the solver's proved certificate.
Two measurements per backend do not establish a statistical or universal
speedup. Compare timing ratios only within the same run: the current runner
uses deterministic AVL metering and may have different overhead from the
historical research harnesses in the saved reports. It does not reproduce
their elapsed times by construction.

The default guards allow sixty seconds per solver or verifier call and one
million adjacency entries or degree replies per oracle. `--wall-seconds`
and `--oracle-limit` may adjust them. On platforms with `setitimer`, the
wall guard is preemptive; elsewhere it is checked at graph-oracle calls.
Run without Python `-O`, which is rejected because it disables checks.

Choose a new JSON output path for every run. The runner refuses to overwrite
existing measurements. It saves completed records atomically after each
call, and records `status: "incomplete"` with the failure or guard reason if
interrupted. Only a fully completed requested block has
`status: "complete"`. Source hashes and the Python/platform identity are
included in every report. This benchmark is a reproducibility aid, separate
from the mathematical proof and the exhaustive tiny-graph validation in
`validation/`.
