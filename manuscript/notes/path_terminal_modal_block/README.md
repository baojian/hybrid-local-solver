# path_terminal_modal_block

This note proves an asymptotic logarithmic terminal block for one named
transported-center endpoint-path execution.  The model is the path `P_m` with
`q=1/(16m)`, `alpha=q^2`, `rho=tau=q/5`, exact-real zero start, complete
all-violations admission, ambient degrees, and the literal projected and
safe-envelope recurrence.  The terminal-block result is unconditional for all
sufficiently large `m`.  Its static and nonlinear regime subtheorems have the
conservative explicit cutoff `m>=8192`; uniformity on `64<=m<8192` remains
open, and the separate modal-band theorem retains asymptotic scope.

The proof has four layers.

1. Proper-prefix chronology is uniform for every `m>=64`: projection is
   inactive, safe correction is zero, and exactly the next singleton is
   admitted.  This follows from the exact prefix optima, the transported
   displacement, a reflected ideal/correction split, and a finite-`q`
   stopped-kernel ledger with margin `179/14400`.
2. The full-entry position and velocity profiles are proved on the required
   growing modal band.  The ideal packet splits into two nonpositive directed
   binomial waves, while the literal entry correction satisfies
   `c(j)<-13q^3/100` on every row for `m>=64`.
3. The static directed remainder is deconvolved exactly as `u=Ld`.  A uniform
   folded-source theorem proves the two-step cone on rows `0<=j<=m-6` for
   every `m>=64`.  Exact first-order formulas give positive limits on the
   five frontier rows.  An exact causal-transfer and transient ledger makes
   their common cutoff explicit at `m>=8192`.  Hence all local half-ratios,
   `d>=h`, and `||(Ld)_+||_(1,D)<21q^3/80` hold in that range.
4. A correlated finite-`q` stopped ledger closes the early interval
   `qk<3/50` with margin `1807/115200`.  The static bound and an exact
   position comparison close `qk>=3/50`.  The integer handoff has no gap, so
   the literal nonlinear regime persists through
   `K_m=floor((8q)^-1 log(1/q))`; the proved modal band then excludes the
   note-scoped terminal certificate through those steps.

The stronger separate inequality `L_k u<=13q^3/200` is still unproved and is
not needed.  The former `q^3/16` claim through `17/200` is false.  A global
quarter-mass shortcut is also false: at `k=2`, reflection gives the
degree-normalized coefficient `3/8` from path source one to target zero.  The
proof instead preserves source location, reflection, and the literal endpoint
group.

The theorem is deliberately narrow.  It is not a lower bound for arbitrary
local algorithms, alternate face schedules, nonlocal response primitives, or
exact-spectrum Krylov methods.  In particular, exact CG on this `(m+1)`-
dimensional path terminates in at most `m+1=Theta(q^-1)` matvecs, so the named
recurrence's logarithmic block cannot be transferred to arbitrary Krylov
iteration.

For the named implementation's prescribed certification runtime, each
terminal full-face scan costs `vol(P_m)=2m=1/(8q)`.  The terminal block
therefore yields
`W_terminal >= (64q^2)^-1 log(1/q)-(8q)^-1`.  With the note-scoped
`eps_ppr=rho+tau=2q/5`, this is
`Omega(eps_ppr^-2 log(1/eps_ppr))`.  This is a charged implementation ledger,
not a semantic-error lower bound, an eleven-resource lower bound, or a claim
that the iterate cannot already be accurate.

Exact preflights cover chronology, source identities, entry profiles,
directed kernels, the static cone, the five frontier limits, the stopped
baseline, the finite-`q` early ledger, and the early/late implication chain.
Floating screens are labeled measured and are not proof inputs.

Build the note with:

```bash
make
```

Run the consolidated and focused checks with:

```bash
python3 verify.py 128 256 512 1024
python3 verify_static_frontier.py
python3 verify_static_frontier_cutoff.py
python3 verify_finite_stopped_ledger.py
python3 verify_asymptotic_closure.py
```
