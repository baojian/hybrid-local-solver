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
Pure-prox Collatz probes give a cheaper conditional alternative: once their
Perron bracket has relative width at most `1/16`, an observable error-bar gate
certifies a fixed-face momentum window with root rate
`1-(3/8)*sqrt(1-U)`, without computing lower eigenvalues or eigenvectors.
The bracket hitting time and admission replay count remain charged open terms.

The note gives the exact normalized center/arm coupling and the exact
ambient-volume charge for unequal arm prefixes.  The star reachability test is
settled at a matching logarithmic scale for this exact full-face policy.  The
live route is a restart/window implementation of the face-tuned rule on
changing faces, using same-point replay whenever an admission is detected. A
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
```
