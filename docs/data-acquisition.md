# Data acquisition

Normal solver execution is local-only. Code under `src/` accepts an explicit
data directory, validates the selected file against the repository manifest,
and never retrieves a missing file or writes to a user cache.

The ten full-experiment graph files come from the revision-pinned dataset
declared in `experiments/data_acquisition/fetch_graphs.py`. Retrieval is a
separate, user-invoked experiment preparation step:

```bash
make fetch-graphs DATA_DIR=/absolute/path/to/graphs
```

To retrieve only selected files, invoke the module directly:

```bash
uv run python -m experiments.data_acquisition.fetch_graphs \
    --data-dir /absolute/path/to/graphs \
    --graph com-dblp --graph wiki-talk
```

Files are stored as `<data-dir>/<graph>/<graph>_csr-mat.npz`. Each completed
transfer must match both the byte count and SHA-256 value in `src/graphs.py`
before it replaces the temporary partial file. A valid existing file is reused.
An invalid existing file is preserved unless `--force` is supplied explicitly.

Source papers are separate from experiment data. Keep them under `papers/`
according to `papers/README.md`; read only the papers needed for the active
research question.
