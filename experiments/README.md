# Experiments

Experiment drivers live here rather than under `src/baselines/`. They may
download graph data, trigger Numba compilation, and run for a long time, so
they are not collected by pytest.

## Offline reproduction smoke

Run the lightweight reproduction path with:

```bash
make experiments
```

This runs a deterministic, center-seeded APPR star case without downloading
data. It verifies the proved strict lower bound and the classical upper bound
on degree-weighted work, then writes a validated result bundle to
`results/raw/reproduction_smoke.json`. The output records the graph, source,
`alpha`, `eps_appr`, random seed, exact stopping rule, solver parameters, work,
metrics, and code version.

`make reproduce` is the offline-friendly repository reproduction target. It
runs the tests and lint checks, the smoke experiment, the synthetic APPR figure
generation, and the manuscript build.

## Full dataset sweeps

The real-graph sweeps may download data and run for a long time. Run both with:

```bash
make full-experiments
```

The individual `make eps-sweep` and `make omega-sweep` targets remain
available for running one sweep at a time.

Both sweeps write validated, per-source JSON records by default under
`results/raw/`; pass `--output PATH` to choose another destination. Each record
contains the exact implemented queue/frontier termination rule, an
`epsilon_name`, the intended residual certificate, and whether the returned
iterate actually achieved that certificate. Rankings exclude a solver at an
epsilon unless it certifies every sampled source. This matters for legacy
accelerated baselines whose empty active frontier need not imply their intended
coordinate residual threshold. The remaining cross-method rankings are still
exploratory because the repository has not adopted conversions between APPR
and gradient-residual certificates.

The sweep configuration also records the reference-solution routine and
tolerance used for reported L1 errors, together with the coordinate conversion
applied to APPR output.

Run the epsilon sweep with:

```bash
uv run python -m experiments.run_eps_sweep \
    --dataset com-dblp --alpha 0.05 --num-sources 10 \
    --output results/raw/eps-sweep-com-dblp.json
```

Run the SOR omega sweep with:

```bash
uv run python -m experiments.run_omega_sweep \
    --dataset com-dblp --alpha 0.05 \
    --output results/raw/omega-sweep-com-dblp.json
```

Check the APPR lower-bound constructions under several legal active-vertex
orderings with:

```bash
uv run python -m experiments.check_appr_lower_bound
```

The star rows test the proved lower bound. Path and long-spider rows are
diagnostics and are not labeled as theorem verification. The checker accepts
only `0 < eps_appr <= 1/16`, the parameter regime proved by the star theorem.

Explore conjugate-direction locality on deterministic synthetic graphs with:

```bash
uv run python -m experiments.explore_evolving_cg
```

This compares exact frontier-sparse CG against CG restarted after every
boundary-driven support expansion and a factor-two variant that grows every
failed envelope by a factor of two in degree volume. The factor-two method
charges all breadth-first halo discovery. It uses the explicitly note-scoped
certificate `max_i |r[i]| / sqrt(d[i]) <= alpha * eps_ppr`; its epsilon is not
identified with `eps_appr`, `eps_obj`, or the unresolved repository-wide
residual.  The experiment records direction or active-set trajectories,
restarts, explored volume, degree-weighted edge work, and error against a
direct synthetic reference solve.

Reproduce the high-degree decoy obstruction to geometric-envelope locality
with:

```bash
uv run python -m experiments.explore_geometric_envelope_obstruction
```

The construction keeps `alpha = 0.01` and the note-scoped `eps_ppr = 0.25`
fixed while increasing the degree of a nonviolating boundary hub. Literal
violation-only restart remains at constant explored volume and work, whereas
factor-two halo growth is forced to admit the hub and incurs work linear in
its arbitrarily large degree.

Generate the manuscript figure comparing actual hard-star work with both
proved bounds using:

```bash
make figures
```

This writes the complete plotted records, including run provenance, to
`results/appr_star_work_bounds.json`. It generates PDF and PNG versions of
`manuscript/figures/appr_star_work_bounds` for actual work and
`manuscript/figures/appr_star_scaled_work` for the normalized quantity
`alpha * eps_appr * W`.
