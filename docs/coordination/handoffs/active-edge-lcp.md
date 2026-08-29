# Handoff: active-edge-lcp

- Agent family: codex
- Role: direction
- Branch: `agent/codex/active-edge-lcp`
- Base commit: `df0725fcf68797c5bf53527eabb6ae2dd64b9f33`
- Assignment state: ready for review
- Proof milestone: `3fa84554b8f7599734db3e38447797e81f8cc8fc`
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/active-edge-lcp.md`
  - `docs/literature/index.md`
  - `docs/literature/lcp-solvers.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/active_edge_lcp/`
- Permitted shared files: exactly the write scope above.

## Outcome

- Requested result: pursue a complete proof of OP2 through the exact
  obstacle/symmetric M-matrix LCP formulation, with primary-source auditing,
  fully charged support discovery, a projected-CG verdict, reproducible proof
  audits, and no automatic manuscript promotion.
- Strongest proved result: Theorems `thm:batch-depth` and `thm:op2` prove OP2
  in the canonical exact-real randomized word model.  Threshold-certified safe
  admission batches satisfy
  `face_gap(J) <= 8 q_alpha^(2J) + theta^2/(alpha rho)`, where
  `q_alpha=(sqrt(2/alpha)-1)/(sqrt(2/alpha)+1)`.  Choosing
  `theta=(1/8)sqrt(alpha rho eps_obj)` bounds the number of complete exposed
  faces by `O(alpha^(-1/2) log(1/eps_obj))`.
- Algorithmic result: each exposed degree-scaled SDD face is solved from
  scratch in nearly-linear local work.  Exact active-residual certification
  accepts only vectors with the required absolute energy error; capped
  independent constant-success Koutis--Miller--Peng trials give declared
  failure probability.  Only certified positive residual batches are exposed,
  so every execution prefix stays inside the true support and has volume at
  most `1/rho`.  All construction, state, retries, scans, batch exposure,
  materialization, projection, and output are charged.  Expected work is
  `O_tilde(1/(rho sqrt(alpha)))` with polylogarithmic dependence on
  `1/eps_obj` and inverse failure probability.
- Projected-CG verdict: the existing exact four-vertex rational example still
  refutes coordinatewise one-sided monotonicity for ordinary/projected face
  CG; this is not a lower bound for all obstacle algorithms.
- Stronger open targets: deterministic coefficient-bit complexity and a
  persistent changing-face response implementation.  Neither is an OP2
  dependency in the repository baseline model.
- Deliberately unchanged: the canonical problem-definition note, active
  manuscript, `docs/literature/local-solvers.md`, every other direction,
  source/experiment/provider code, and the paper library.

## Evidence

- Exact rational audits passed:
  - `verify_counterexample.py` (four-vertex CG obstruction);
  - `verify_threshold_dichotomy.py` (720 threshold cases and 36 telescopes);
  - `verify_path_ldl.py` (580 endpoint-path instances).
- New theorem audits passed:
  - `verify_batch_depth.py`: 1,152 structured/random graph cases;
  - `verify_batch_depth_high_precision.py`: 216 dependency-free 100-digit
    Decimal path/star cases, including inverse ordering, singular values,
    causal forcing, face-gap identity, and theorem bound.
- Three independent hostile read-only audits found no fatal defect after
  repairing the `J=0` Chebyshev base case, two-face batch indexing, explicit
  Cholesky inverse ordering, degree-scaled SDD conversion, randomized source
  interface, and unconditional exposure ledger.
- Koutis--Miller--Peng was rechecked at arXiv:1102.4842v4, PDF p. 10,
  Theorem 4.6, with BuildChain/Lemma 4.5 for constant success.  The note does
  not attribute an arbitrary failure parameter to Theorem 4.6; it obtains one
  by exact residual certification and capped retries.

## Checks

- Focused note build: passed; 24-page PDF, resolved references/citations, no
  fatal, undefined-reference, or overfull-box diagnostics.
- Visual PDF QA: all 24 pages rendered and inspected; no clipping, overlap,
  broken equation, or unreadable table found.
- Note inventory and `git diff --check`: passed.
- Owned Python: `ruff check` and `ruff format --check` passed.
- Full `make test`: passed 213/213, with 15 pytest temporary-directory cleanup
  warnings.
- Full `make lint`: `ruff check .` passed.  Format checking remains red only
  for nine pre-existing files under
  `experiments/proof_audits/aesp_cd_l1_rppr/`, owned by the simultaneous
  `windowed-spectral-lyapunov-7h` assignment; those files were not touched.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: only the explicitly permitted coordination,
  literature, registry, index, and owned note paths.
- Worktree exception: the Codex worktree manager kept the checkout on a
  detached HEAD.  The checkout was not switched or reset.  Coherent detached
  commits are listed here for review; the logical branch label at the starting
  point remains `agent/codex/active-edge-lcp`.
- Coordination transition: while this assignment was active,
  `make agent-audit` correctly reported overlap on the shared assignment file
  with the simultaneous controller assignment.  This direction alone was
  moved to `ready_for_review` before the final audit; no other assignment was
  changed.  Final `make agent-audit` passed.
- Promotion decision: no automatic promotion.  The controller should
  independently review `thm:batch-depth`, the certified SDD retry wrapper, and
  the fully charged work ledger before changing the active manuscript or
  shared results ledger.

## Commits

- Prior resumed-direction marker: `b7ffdfa040554c08cae9d0fc6d560e4fdce5297d`.
- Complete OP2 proof and evidence: `3fa84554b8f7599734db3e38447797e81f8cc8fc`.
- Review-ready coordination/check state: the commit containing this handoff.
