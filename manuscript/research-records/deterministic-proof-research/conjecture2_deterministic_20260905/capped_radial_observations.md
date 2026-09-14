# Deterministic radial diagnostics: caps, flux, and outside mass

These are fresh finite numerical experiments, not a proof of OP2 or of an
asymptotic work bound. They use no randomness. The radial reduction uses a
fully prescribed hypercube and is **not** itself a local graph algorithm.
Support signs in these particular files use 100-digit Decimal arithmetic;
they are not exact certificates. Separate Fraction tests certify the small
local implementations, and the earlier uncapped integer experiment is exact.

The prescribed family is the d-dimensional hypercube, theta=1/d,
alpha=theta^2, rho=2^(-7d/8)/d (integer exponents in the sampled dimensions),
with 3d accelerated steps. The ordinary lazy capped recurrence and the
monotone segment-search recurrence are both tested from zero.

`capped_radial_probe_results.jsonl` records the initial cap/work experiment.
Through d=512, rho*theta times the cumulative kinetic-support volume is
approximately 2--6 in these samples. Peak rho times kinetic-support volume
is much larger, reaching about 266 for d=512 in the ordinary variant.
This distinction motivates cumulative accounting; it is not a uniform bound.

`capped_radial_flux_results.jsonl` adds c*||(I-P)u||_1 measurements. For the
ordinary recurrence, sampled maximum values divided by alpha are

| d | 16 | 32 | 64 | 128 | 256 |
|---|---:|---:|---:|---:|---:|
| maximum flux / alpha | 3.73 | 14.25 | 70.40 | 224.50 | 666.21 |
| mean flux / alpha | 2.26 | 5.36 | 23.63 | 78.14 | 230.23 |

The monotone recurrence gives similar values. Since log(1/rho)=Theta(d)
here, polynomial growth in d does not by itself contradict a bound hiding
parameter polylogarithms. An independent binary-tree investigation targets
that distinction more sharply; no result from it is presumed in this note.

`capped_radial_outside_results.jsonl` additionally solves successive radial
principal prefixes at rho/2 to identify the comparison core. This is a
separate numerical diagnostic, not a supplied-support oracle for the local
solver. For the ordinary recurrence:

| d | last core layer | max outside position mass / theta | sum of outside coordinate maxima / theta |
|---|---:|---:|---:|
| 32 | 12 | 2.26 | 2.37 |
| 64 | 21 | 9.04 | 9.25 |
| 128 | 41 | 10.59 | 10.62 |
| 256 | 79 | 14.50 | 14.56 |

The sum of coordinate maxima includes layer multiplicities and degrees.
It suggests a possible outside-reservoir potential worth investigating.
Neither a position-mass bound nor coordinate-maxima bound alone counts
arbitrarily small emitted kinetic coordinates. A threshold/lifetime
argument would still be required, even if such a bound were proved.

The probe now accepts a separate theta denominator for future deterministic
checks. All input choices and precision are saved with each result.
