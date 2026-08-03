# Experiments

Experiment drivers live here rather than under `src/baselines/`. They may
download graph data, trigger Numba compilation, and run for a long time, so
they are not collected by pytest.

Run the epsilon sweep with:

```bash
uv run python -m experiments.run_eps_sweep \
    --dataset com-dblp --alpha 0.05 --num-sources 10
```

Run the SOR omega sweep with:

```bash
uv run python -m experiments.run_omega_sweep \
    --dataset com-dblp --alpha 0.05
```

Check the APPR lower-bound constructions under several legal active-vertex
orderings with:

```bash
uv run python -m experiments.check_appr_lower_bound
```

The star rows test the proved lower bound. Path and long-spider rows are
diagnostics and are not labeled as theorem verification.

Generate the manuscript figure comparing actual hard-star work with both
proved bounds using:

```bash
make figures
```

This writes the complete plotted records, including run provenance, to
`results/appr_star_work_bounds.json` and generates PDF and PNG versions of
`manuscript/figures/appr_star_work_bounds`.
