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
