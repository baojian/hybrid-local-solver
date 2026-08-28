# path_face_lock_warmup

This note studies whether the conservative spectral warmup in the safeguarded
changing-face momentum construction can be replaced by a sharp componentwise
post-lock certificate.  The first target is the endpoint path; the next target
is a spider obtained by coupling path arms through its center.

The exact Fable trigger has been reconstructed in the project's normalized
variables.  An exact rational screen also separates arbitrary nonnegative
entrance states from the realized RPPR face-entry profile: one, two, and
three pure-prox warmups are not cone-uniformly sufficient on full endpoint
paths, and four are insufficient on a 16-arm star.  More strongly, an exact
leaf-seeded unit-star family proves that every fixed number `J` of full-face
warmups fails on all sufficiently large stars.  In the positive direction,
one prox solve always certifies the first momentum trigger when
`alpha <= 1/5`, and

```text
J_B = max{3, 1 + ceil(log_(3/2)(8(B-1)))}
```

makes every subsequent full-star trigger kernel entrywise nonnegative.  Thus
the fixed-policy star mechanism has matching `Theta(log B)` upper and lower
warmup scale.  Under a slightly longer logarithmic warmup, every exact kernel
entry has an explicit positive finite-horizon margin.  In contrast, the same
global momentum is never permanently cone-safe on a strict connected proper
face: its Perron trigger is a damped oscillation, independent of how many
finite pure-prox warmups precede it.  This obstruction is repaired exactly by
a face-tuned momentum parameter plus a spectral-gap/Perron-spread warmup; the
result has an explicit positive kernel margin but is not graph-uniform.
Without requiring a permanent tail, a Perron-split window retains both
components of the actual common-cap correction. With face-tuned momentum,
its two observable event charges certify a half-contraction in
`ceil(2/q_face)` stages on any fixed connected face. A reachable `P3`
trajectory proves that ground-state coordinates do not preserve the common
cap, so the full-face clipped-master theorem cannot simply be transported to
a proper face.
Every rejected Perron-split window now has an exact alternative payment from
the Perron mean, but the payment is only of order
`1/(1/q_face+1/phi_min)` and therefore still allows quadratic-in-`1/q_face`
stage counts. A finite error-bar version of the accepted gate is proved;
using the safe signed-scratch Chebyshev face solver makes one accepted macro
cost `O_tilde(vol(A)/sqrt(lambda_1(A)))`, apart from charged Perron data.
Pure-prox Collatz probes give a cheaper conditional alternative: once their
Perron bracket has relative width at most `1/16`, an observable error-bar gate
certifies a fixed-face momentum window with root rate
`1-(3/8)*sqrt(1-U)`, without computing lower eigenvalues or eigenvectors.
The bracket hitting time is now bounded exactly by either Birkhoff projective
contraction or a proof-only spectral-ratio/Perron-spread estimate.  A path
family shows this probe phase can require `Omega(n^2 log n)` solves, so it is
not graph-uniform; admission replay count remains a charged open term.
For replays launched from a maintained coordinatewise lower checkpoint, a
new Schur-complement lemma pays the squared certified boundary residual from
the telescoping restricted-optimum gain.  This bounds all margin-separated
admission batches.  With volume doubling and a volume-normalized residual
margin, total replay work is at most
`2*C_res*(V+Delta_tot/eta)`; paying a discarded accelerated window requires
the stronger margin `||g||^2 >= eta*vol(A)/q`.  The theorem does not apply to
transient momentum shocks.  Without such a margin, tiny-gain admissions can
force quadratic cumulative replay volume, so small-margin admissions remain
a genuine charged obstruction.

The note gives the exact normalized center/arm coupling and the exact
ambient-volume charge for unequal arm prefixes.  The star reachability test is
settled at a matching logarithmic scale for this exact full-face policy. The
live route is a batched active-set implementation on changing faces, using
same-point replay whenever an admission is detected. A
one-admission final-full-star theorem already supplies
explicit finite-inner warmup and momentum tolerances on a finite horizon.  On
a full star, the literal repeated-solve warmup costs `Theta(B log B)`; the
three-class verifier's constant arithmetic is only a symmetry reduction.

Build with `make`.  Run the exact screen with:

```bash
python3 verify_warmup.py --sizes 4 6 8 10 12 --horizon 32
python3 verify_warmup.py --sizes 14 16 20 --horizon 64
python3 verify_warmup.py --sizes 46 --horizon 4 --max-warmup 3
python3 verify_warmup.py --spider-arms 16 --spider-length 1 \
  --horizon 2 --max-warmup 4
python3 verify_reachable_star.py
python3 verify_reachable_star.py --arms 22 --warmup 6
uv run python -m \
  experiments.proof_audits.path_face_lock_warmup.proper_perron_cap_stop
```
