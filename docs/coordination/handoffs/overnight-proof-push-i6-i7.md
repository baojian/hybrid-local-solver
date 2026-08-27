# Iterations 6–7 proof-push handoff

## Assignment

- Branch: `agent/codex/overnight-proof-push-i6-i7`
- Base: `71764c15c5bc2bb92f01d9d807942acf61e4be85`
- Scope: the immutable overnight campaign snapshot, its coordination records,
  and a narrow Ruff exclusion for that snapshot.
- Status: ready for review; no result has been promoted into the active
  manuscript or the repository's accepted theorem ladder.

## Commit structure

1. `32ecd3e` — register the clean-worktree assignment and snapshot lint policy.
2. `5dbc131` — archive Iteration 6 proof-push findings, exact scripts, JSON
   evidence, and cited logs.
3. `e4592bd` — archive Iteration 7 and the Route-B closure package, restore the
   audited exact-Fraction face-cap core, and make the unified verifier
   repository-relative.
4. `974892a` — append the Iterations 6–7 report and scoreboard summary.

## Scientific status

- The campaign artifacts label new statements as `Proved-draft`,
  `Conditional`, `Measured`, `Refuted`, or open as appropriate.
- The unmodified never-triggering statement is refuted by the exact `rt22b`
  counterexample; the replacement result concerns the modified `fm-w`
  algorithm.
- The class theorem remains conditional on analytic `(PSI)` outside the
  exactly checked families.
- The graph-uniform end-to-end work bound remains open. Inflation control is
  not presented as a completed total-work theorem.
- Nothing from this snapshot is promoted into the active manuscript, the
  AESP–LOCSOR note, or `docs/research_notes.md`.

## Verification

- `python manuscript/claude-overnight-2026-08-24/i7c/verify_routeB.py`
  completed in 78.6 seconds with all gated exact checks passing:
  - fm-w `NF`, `CMP`, and `KKT`: 3,840/3,840;
  - `YPOS` and `UID`: 3,821/3,821;
  - `MOM`: 571/571 and `PROX`: 3,269/3,269;
  - `rt22b`: first unmodified-fm fire reproduced at stage 13, class `F`;
  - complete-graph spot grid: all 18 predicates pass, all cases absorb, and
    maximum `J_total = 0.36918 < log 2`;
  - class-boundary master-form checks: 48/48 for each exact identity.
- `i6c/open1_maxprinciple.py`: 90 cells, zero failures.
- `i6c/open2_scope.py`: all scope predicates pass.
- `make agent-audit`: pass.
- `make test`: 210 passed; 15 macOS temporary-directory cleanup warnings.
- `make lint`: Ruff check pass; all 89 maintained Python files formatted.
- `make reproduce`: pass; APPR smoke, figures, and the 40-page manuscript
  rebuild completed. The generated APPR code-version-only diff was restored.

The archived Route-B JSON/log retain the original run's float-only measured
diagnostics and 109.5-second timing. A local rerun produced identical exact
gates; tiny platform-dependent float changes (including 515/563 rather than
513/563 for the non-gating R-decay diagnostic) were deliberately not folded
into the historical artifact.

## Deliberate exclusions

- `_to_delete_i67.tar.gz`: scratch archive explicitly marked for deletion.
- `i4c/out/verify.json`: unrelated floating-point drift from the older
  Iteration 4 artifact.
- zero-byte `*.err` files: no evidence content.
- `w7_windowed/i6a1_out/S16.json`: empty failed output; its run terminated with
  `ZeroDivisionError`, so it is not represented as evidence.
- `w7_windowed/i7b_q4_reps.npy`: regenerable binary enumeration cache; the
  source, decision JSON, and cited log are retained.
- `manuscript/notes/class_separation_ladder/`: handled independently on
  `agent/claude/class-separation-ladder` to keep the write scopes disjoint.

The user's original checkout and all excluded files remain untouched. This
branch was assembled and verified in `/private/tmp/hls-overnight-proof-push`.
