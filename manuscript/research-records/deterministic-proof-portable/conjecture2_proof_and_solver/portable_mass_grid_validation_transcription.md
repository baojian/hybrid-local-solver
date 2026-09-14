# Portable mass-grid validation transcription

The standalone package validator now accepts `--backend mass-grid`, dispatching to the packaged `solve_mass_scaled_grid`. Only `validation/run_full.py` and `validation/README.md` changed. The manifest, numerical modules, existing tests, and default `fast` alias are unchanged.

The added branch uses the fixed halving schedule and unwraps the unchanged `SolverResult`. It checks the weighted perturbation budget `Gamma = 29 eta h/theta < tau/8`, the ceiling `h <= theta tau/(256 eta)`, and `Gamma <= alpha^2 r eta`. It verifies exact baseline representation on the current grid without incorrectly requiring arbitrary historical grids to remain nested. Each factory hint is compared with the independently computed exact baseline mass deficit. The same source, support, kinetic-work, repair, exact optimum KKT, additive objective, independent final subgradient, and label/reversed-row checks apply.

An observer runs the already-audited initialization assertions before the first step: actual and relaxed tolerances, zero-step state, all three restored horizons and exact binomial powers, and schedule-counter decomposition. This `initial_checks` function is AST-identical to the independently validated prototype check. Hint construction and final reference release are separately observed to make no extra external graph calls. All hint scalar work remains in the additive mass-hint ledger; retargeting loop counters remain subsets of the ordinary accumulated schedule counters and are not added twice. The checkpoint checks also verify reclamation of all six temporary containers per checkpoint.

## Evidence

- Read-only replay of all **183 saved prototype outputs and 520 stages** through the portable stage/final assertions passed. Exact horizon reconstruction and all eight saved label/reversed-row comparisons passed. All final independent certificates meet the requested epsilon. This replay never invokes a numerical solver: the saved graph-access observations remain historical evidence, not newly measured access.
- A temporary isolated bundle containing only `deterministic_rppr`, bundled `tests`, and `validation`, run with Python's `-I` flag, passed the existing fixed **five-case smoke subset**. It covers an ordinary solve and its label/reversed-row counterpart, zero and alpha-one branches, and the analytic million-leaf star. Its entire returned results match the saved prototype results exactly: 14 stages, 416 iterations, 70 external adjacency entries, and 57 degree replies. The optional factory recorded 14 calls/releases and 27 cached degree lookups.
- A separate forced guard rejects the first attempted numerical step. It returns exit code 1, preserves `status: incomplete`, records no completed case, and observes final factory reference release. **Zero numerical steps** execute in this guard check.
- No complete solver suite was rerun, and no fast/adaptive solver case was rerun. Numerical modules and existing tests have identical before/after SHA-256 hashes.

The manifest's canonical SHA-256 remains `e02485273de4bc1b615530518ac9db60ae5d7beee0140e0e787f6f4320ed0434`; its actual file hash remains `d05538fd59877d6da94bb6477d780fdbdd930ac3a276a987ee46481e0b63681b`.

| Artifact | SHA-256 |
|---|---|
| `validation/run_full.py` | `1752cec8b106f36e300d6d2738502a09e633686b38fc3fca397fcd48c00e3b11` |
| `validation/README.md` | `c53f0ca3ec849ec6a9a9502507205d62040442422435bffe29fd31057ad3450a` |
| `audit_portable_mass_grid_validation.py` | `6dcd5f5e988f721e8797410c1f705346ad9555a5b8d66b35b30372e45fd65ba1` |
| `portable_mass_grid_validation_transcription.json` | `01ff7dbec5d64aa0ffec30f3033aeca45e75d8cfa3865c76cbe16fc44f464821` |
| `portable_mass_grid_validation_smoke.json` | `f85defd6d5f4beb80cba1eb0b18eb189eb65ad836463d98ce8ba46d2c1b3425f` |
| `portable_mass_grid_validation_forced_guard.json` | `471159872f13f42f3f35f118ef7126e91d4ed0a95b92c00531e6618e64315235` |

From the unpacked source package, users can run the full suite themselves:

```sh
python3 -I validation/run_full.py --backend mass-grid --output mass-grid-validation.json
```

Add `--smoke` for the fixed five-case installation check. Fixed resource guards, atomic persistence, complete/incomplete semantics, and all other backend commands are documented in `validation/README.md`. The runner has no research-directory imports or third-party runtime dependencies. These deterministic checks supplement the proof and the earlier full prototype validation; they do not provide a new timing claim or imply that the full packaged suite was rerun.
