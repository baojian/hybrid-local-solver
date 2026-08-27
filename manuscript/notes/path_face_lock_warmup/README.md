# path_face_lock_warmup

This note studies whether the conservative spectral warmup in the safeguarded
changing-face momentum construction can be replaced by a sharp componentwise
post-lock certificate.  The first target is the endpoint path; the next target
is a spider obtained by coupling path arms through its center.

The exact Fable trigger has been reconstructed in the project's normalized
variables.  An exact rational finite-horizon screen also separates arbitrary
nonnegative entrance states from the realized RPPR face-entry profile: one
and two pure-prox warmups are not cone-uniformly sufficient on full endpoint
paths.  This does not yet refute a constant warmup for the actual
endpoint-seeded chronology.

Build with `make`.  Run the exact screen with:

```bash
python3 verify_warmup.py --sizes 4 6 8 10 12 --horizon 32
python3 verify_warmup.py --sizes 14 16 20 --horizon 64
```
