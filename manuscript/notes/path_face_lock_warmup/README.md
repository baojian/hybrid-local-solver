# path_face_lock_warmup

This note studies whether the conservative spectral warmup in the safeguarded
changing-face momentum construction can be replaced by a sharp componentwise
post-lock certificate.  The first target is the endpoint path; the next target
is a spider obtained by coupling path arms through its center.

The exact Fable trigger has been reconstructed in the project's normalized
variables.  An exact rational screen also separates arbitrary nonnegative
entrance states from the realized RPPR face-entry profile: one, two, and
three pure-prox warmups are not cone-uniformly sufficient on full endpoint
paths, and four are insufficient on a 16-arm star.  More strongly, the
literal leaf-seeded obstacle trajectory on that star fails after every one
through five full-face warmups.  In the positive
direction, one prox solve always certifies the first momentum trigger when
`alpha <= 1/5`, on every graph face.  This does not certify the momentum tail
or determine the asymptotic minimal warmup.

The note gives the exact normalized center/arm coupling and the exact
ambient-volume charge for unequal arm prefixes.  The star reachability test is
settled negatively; the live questions are the actual endpoint-path profile
and the asymptotic warmup required by spider families.

Build with `make`.  Run the exact screen with:

```bash
python3 verify_warmup.py --sizes 4 6 8 10 12 --horizon 32
python3 verify_warmup.py --sizes 14 16 20 --horizon 64
python3 verify_warmup.py --sizes 46 --horizon 4 --max-warmup 3
python3 verify_warmup.py --spider-arms 16 --spider-length 1 \
  --horizon 2 --max-warmup 4
python3 verify_reachable_star.py
```
