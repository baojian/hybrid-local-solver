# Verification manifest

This manifest records what the executable checks certify.  A passing script
is evidence only for the statement listed here; it must not be promoted to a
stronger end-to-end claim.

| Artifact | Certified statement | Deliberate scope limit |
|---|---|---|
| `exact_delayed_clock.py` | Exact `Q(sqrt(10))` moving projected-NAG trace with events `0,1,2,3,4,38`; finite threshold, lower-subsolution, early-stop, connectedness, and `S*=V` checks. | Refutes immediate next-product publication for this recurrence only; not a target-runtime lower bound. |
| `gap_adaptive_fmu_exact.py` | Tensor-Bernstein held-step LMI for `F_mu`, nonexpansive decreasing-gap transport, and the stale-gap triangle obstruction. | Algebraic state transport; not publication occupancy or a response implementation. |
| `adaptive_square_function_exact.py` | Sharp fixed-face constant `(3+sqrt(5))/8` and the `P4` delayed exterior output. | Fixed-face observability does not telescope through mask growth. |
| `f0_lmi_exact.py` | Critical `F0` held contraction and positivity certificates. | Gives an additive cut bank, not a count of held products. |
| `moving_face_smoothing_exact.py` | Fixed-face Gramians, shifted harmonic jump, and canonical `P2/P3` local-payment stops. | The legal `P3` packet is not proved to arise in exact zero-start chronology. |
| `path_gap_certificate_exact.py` | Path-Poincare lower certificate and exact ballasted-broom congestion formula. | Stops fresh per-face relaxation, not retained tree/Schur state. |
| `green_bracket_exact.py` | Exact threshold-significant raw Green-bracket counterexample. | Principal-face/raw-state statement; not exact maximal-batch chronology. |
| `green_lift_exact.py` | Exact hard-lift/source-reservoir ratio `1.126299...`. | Does not rule out a stopped low-band or future-tail reserve. |
| `projected_green_overshoot_exact.py` | Exact fixed-face projected-NAG/Green ratio `26.576618...`. | The face/time is not proved to occur in canonical chronology. |
| `cycle_rank_response_verify.py` | Tree cavity Green formula, `Q=B+cZZ^T`, and Woodbury solution identity on random small graphs. | Numerical identity audit; the `k^omega_mat` recursive-block-solve work theorem is algebraic and proved in `README.md`, including exact ordered-field and capped-output scope. |
| `shifted_debt_envelope_verify.py` | Scalar Schur envelope, global capped objective/distance bounds, zero-append block residual identity, exact packet orthogonality, and source-square bank on random small normalized graph faces. | Numerical normalization audit; these identities and the global capped subgradient stop are proved algebraically in `README.md`, and the script does not implement the missing shifted-response producer. |
| `witnesses.py` | Numerical regression collection for the remaining finite witnesses. | Floating-point diagnostics, not theorem certificates. |
| `two_mask_experiments.py` | Structured/random chronology and Lyapunov regression. | Floating-point evidence for a shared clock, except for the separate exact 34-vertex verifier. |

The exact symbolic suite was rerun with cached isolated dependencies as

```text
uv run --with sympy --with numpy --with scipy python <script>
```

and the exact delayed-clock verifier uses only the Python standard library.
The scalar shifted-debt envelope/local-append theorem is a direct
Schur-complement and block-multiplication proof; its numerical regression is
not treated as authority.  Likewise, the fast dense-core exponent is not
inferred from timing `cycle_rank_response_verify.py`.
The complete `witnesses.py --alpha 1e-4` JSON regression and a 120-random-run
two-mask regression passed.  A separate `alpha=3e-5` stress run was stopped
without a result after entering a 16.6GB dense SVD; it is not counted as a
test pass or as mathematical evidence.

## Repository gate status

The direction-local `ruff check`, `ruff format --check`, `compileall`, and
`git diff --check` pass.  `make agent-audit` also passes.  The repository-wide
gates are not green because of files outside this unregistered working
companion:

- `make lint` has one unused import in
  `problem_definitions/verify_exact_batch_cholesky.py`;
- `make note-audit` reports two over-limit sections in `aesp_cd_l1_rppr`;
- `make test` passes 209 of 213 tests and fails on those two inventory findings
  plus pre-existing notation findings in `related_work.tex` and
  `aesp_cd_l1_rppr`.

Those unrelated owned files were not modified.  The working companion is not
registered and therefore does not claim a controller-approved inventory or
promotion status.  `make reproduce` was also invoked and stopped at the same
four repository-wide pytest failures before reaching its experiment, figure,
and manuscript stages.
