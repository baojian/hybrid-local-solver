## Crossover eps*(alpha) where W_push = W_WY (dense grid)

Fit: log2 eps* = log2 kappa + (theta/2) * log2 alpha, i.e. eps* = kappa * alpha^(theta/2) = kappa * sqrt(alpha)^theta.
theta = 1 would be the sqrt(alpha) line; the constant-free algebra 1/(alpha*eps) = 1/eps^2 predicts theta = 2 (eps* = alpha).

| graph | theta | kappa | rms(log2) | #alphas | eps* range |
|---|---|---|---|---|---|
| star | n/a (0 crossings in-grid) | | | | |
| spider | n/a (0 crossings in-grid) | | | | |
| spider2 | n/a (2 crossings in-grid) | | | | |
| caterpillar | n/a (1 crossings in-grid) | | | | |
| btree | n/a (1 crossings in-grid) | | | | |
| grid | 2.36 | 0.509 | 0.74 | 8 | 2^-11.8 .. 2^-4.0 |

Crossing points (alpha_log2 -> eps*_log2): spider2: -5->-4.9, -4->-3.2; caterpillar: -5->-12.8; btree: -3->-12.2; grid: -9->-11.8, -8->-11.4, -7->-7.8, -6->-8.6, -5->-6.6, -4->-5.1, -3->-4.5, -2->-4.0

### Crossover vs the self-certified WY bracket (cert < alpha*eps, deterministic guarantee)

| graph | theta | kappa | rms(log2) | #alphas | points |
|---|---|---|---|---|---|
| star | n/a (0 crossings) | | | |  |
| spider | n/a (0 crossings) | | | |  |
| spider2 | n/a (0 crossings) | | | |  |
| caterpillar | n/a (0 crossings) | | | |  |
| btree | n/a (0 crossings) | | | |  |
| grid | n/a (0 crossings) | | | |  |

## Empirical wedge boundary eps_dagger(alpha) where min(W_push,W_WY) = W_target

Below this eps the target oracle beats both measured contenders (theory line: eps = sqrt(alpha), i.e. theta=1, kappa=1).

| graph | theta | kappa | rms(log2) | #alphas |
|---|---|---|---|---|
| star | n/a (0 crossings) | | | |
| spider | n/a (0 crossings) | | | |
| spider2 | 0.91 | 0.183 | 0.15 | 5 |
| caterpillar | n/a (1 crossings) | | | |
| btree | n/a (0 crossings) | | | |
| grid | 1.69 | 0.303 | 0.29 | 7 |

## Measured constants (non-trivial cells, eps <= 2^-5)

| graph | W_push*alpha*eps med [min,max] | W_WY*eps^2 med [min,max] | W_WY*eps^2 at eps=2^-13 (per alpha range) |
|---|---|---|---|
| star | 0.367 [0.312, 0.368] | 0.0148 [0.000549, 0.41] | 0.000549 .. 0.00128 |
| spider | 0.156 [0.125, 0.250] | 0.00149 [9.16e-05, 0.0293] | 9.16e-05 .. 9.16e-05 |
| spider2 | 0.207 [0.066, 0.244] | 0.0298 [0.000183, 0.926] | 0.000238 .. 0.0298 |
| caterpillar | 0.162 [0.009, 0.254] | 0.0479 [1e-05, 1.93] | 1e-05 .. 0.0171 |
| btree | 0.062 [0.001, 0.211] | 0.000534 [1.79e-07, 0.0703] | 1.79e-07 .. 0.000181 |
| grid | 0.135 [0.021, 0.215] | 0.0131 [2.86e-06, 0.0806] | 2.77e-05 .. 0.0628 |

## Fitted scaling exponents log2 W = c + pe*log2(1/eps) + pa*log2(1/alpha)  (non-trivial cells, eps<=2^-5, n>=30)

| graph | push: pe, pa, c | WY: pe, pa, c |
|---|---|---|
| star | 1.00, 1.01, -1.6 | 0.99, 0.10, 2.2 |
| spider | 1.00, 0.50, -1.1 | 0.97, -0.00, -0.0 |
| spider2 | 1.07, 0.95, -2.7 | 1.18, 0.45, -1.2 |
| caterpillar | 0.67, 1.16, -1.3 | 0.62, 0.72, 1.5 |
| btree | 0.91, 0.48, -0.5 | 0.96, -0.56, 2.6 |
| grid | 0.97, 0.95, -2.6 | 1.45, 0.17, -3.0 |

## WY expansion counts E (rounds incl. tightenings) vs the 1/eps pessimism

| graph | E at eps=2^-13 (over alpha) | fitted slope dlog2 E / dlog2(1/eps) (at alpha=2^-10) | tightenings max |
|---|---|---|---|
| star | 2 .. 14 | 0.00 | 12 |
| spider | 1 .. 1 | 0.00 | 0 |
| spider2 | 2 .. 140 | 0.63 | 7 |
| caterpillar | 7 .. 409 | 0.31 | 12 |
| btree | 1 .. 10 | 0.43 | 2 |
| grid | 7 .. 137 | 0.99 | 6 |

## Prize map: potential speedup of the target oracle

LO bracket = min(W_push, W_WY_oracle)/W_target (oracle-stopped WY, generous incumbent); HI bracket = min(W_push, W_WYcert)/W_target (self-certified WY, conservative incumbent). Real WY with whp certification lies between.

LO bracket, cells with speedup >= 10:
- none in grid

LO bracket, cells with speedup >= 100:
- none in grid

HI bracket, cells with speedup >= 10:
- spider2: (2^-14,2^-9):14x

HI bracket, cells with speedup >= 100:
- none in grid

| graph | max LO speedup (at) | max HI speedup (at) |
|---|---|---|
| star | 1.5x (2^-5,2^-3) | 1.4x (2^-4,2^-3) |
| spider | 0.2x (2^-2,2^-3) | 0.5x (2^-2,2^-3) |
| spider2 | 2.1x (2^-8,2^-7) | 14.1x (2^-14,2^-9) |
| caterpillar | 2.6x (2^-10,2^-8) | 8.3x (2^-12,2^-9) |
| btree | 0.4x (2^-4,2^-8) | 0.7x (2^-6,2^-9) |
| grid | 4.3x (2^-11,2^-13) | 9.0x (2^-12,2^-13) |

### Self-certified WY: W_WYcert*eps^2 (coarse grid, non-triv, eps<=2^-5) and expansions

| graph | W_WYcert*eps^2 med [min,max] | E_cert at eps=2^-13 | E_cert slope vs 1/eps (alpha=2^-10) |
|---|---|---|---|
| star | 0.00883 [0.000549, 0.152] | 2 .. 2 | -0.00 |
| spider | 0.0189 [0.000672, 0.447] | 2 .. 3 | n/a |
| spider2 | 0.11 [0.000336, 14.2] | 2 .. 257 | -0.00 |
| caterpillar | 0.0717 [1e-05, 1.09] | 7 .. 422 | 0.43 |
| btree | 0.00873 [3.18e-05, 0.439] | 6 .. 12 | 0.15 |
| grid | 0.166 [2.86e-05, 1.39] | 7 .. 127 | 0.43 |

## Winner tables (specified coarse grid; P=push, W=WY, t suffix = trivial cell, number = ratio_to_target)

### star

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.62 | P/P 0.62 | P/P 0.62 | P/P 0.62 | P/P 0.62 | P/P 0.62 |
| 2^-4 | P/P 1.4 | P/W 1.4 | W/W 1.4 | W/W 1.4 | W/W 1.4 | W/W 1.4 |
| 2^-6 | W/W 1.4 | W/W 0.95 | W/W 0.85 | W/W 0.82 | W/W 0.81 | W/W 0.81 |
| 2^-8 | W/W 0.84 | W/W 0.56 | W/W 0.49 | W/W 0.47 | W/W 0.47 | W/W 0.47 |
| 2^-10 | W/W 0.5 | W/W 0.32 | W/W 0.28 | W/W 0.27 | W/W 0.27 | W/W 0.27 |
| 2^-12 | W/W 0.29 | W/W 0.18 | W/W 0.16 | W/W 0.15 | W/W 0.15 | W/W 0.15 |
| 2^-14 | W/W 0.16 | W/W 0.1 | W/W 0.087 | W/W 0.083 | W/W 0.082 | W/W 0.082 |

### spider

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.5 | W/P 0.47 | W/P 0.4 | W/P 0.38 | W/P 0.38 | W/P 0.38 |
| 2^-4 | W/P 0.38 | W/P 0.23 | W/P 0.2 | W/P 0.19 | W/P 0.19 | W/P 0.19 |
| 2^-6 | W/Pt 0.19 | W/Pt 0.12 | W/Pt 0.1 | W/Pt 0.095 | W/Pt 0.094 | W/Pt 0.094 |
| 2^-8 | W/Pt 0.094 | W/Pt 0.059 | W/Pt 0.05 | W/Pt 0.048 | W/Pt 0.047 | W/Pt 0.047 |
| 2^-10 | W/Pt 0.047 | W/Pt 0.029 | W/Pt 0.025 | W/Pt 0.024 | W/Pt 0.024 | W/Pt 0.023 |
| 2^-12 | W/Pt 0.023 | W/Pt 0.015 | W/Pt 0.012 | W/Pt 0.012 | W/Pt 0.012 | skip |
| 2^-14 | W/Pt 0.012 | W/Pt 0.0073 | W/Pt 0.0062 | W/Pt 0.006 | W/Pt 0.0059 | skip |

### spider2

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.5 | P/P 0.44 | P/P 0.44 | P/P 0.44 | P/P 0.44 | P/P 0.44 |
| 2^-4 | W/P 0.38 | P/P 0.83 | P/P 0.83 | P/P 0.83 | P/P 0.83 | P/P 0.83 |
| 2^-6 | W/Pt 0.19 | P/P 1.4 | W/P 0.99 | W/P 0.96 | W/P 0.95 | W/P 0.95 |
| 2^-8 | W/Pt 0.094 | W/P 0.023 | W/P 2.1 | W/P 2.1 | W/P 2.1 | W/P 2.1 |
| 2^-10 | W/Pt 0.047 | W/Pt 0.012 | W/P 1.7 | W/P 2 | W/P 2 | W/P 2 |
| 2^-12 | W/Pt 0.023 | W/Pt 0.0059 | W/P 0.0015 | W/W 2 | W/W 1.9 | W/W 1.9 |
| 2^-14 | W/Pt 0.012 | W/Pt 0.0029 | W/Pt 0.00073 | W/W 1.5 | W/W 1.9 | W/W 1.9 |

### caterpillar

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.62 | P/P 0.45 | P/P 0.27 | P/P 0.12 | P/P 0.05 | P/P 0.019 |
| 2^-4 | P/P 1.2 | P/P 1 | P/P 0.75 | P/P 0.39 | P/P 0.17 | P/P 0.066 |
| 2^-6 | P/W 2.5 | W/P 1.2 | W/P 1.6 | W/P 0.9 | W/W 0.38 | W/W 0.14 |
| 2^-8 | W/W 1.4 | W/P 1.5 | W/P 1.5 | W/W 1.2 | W/W 0.76 | W/W 0.29 |
| 2^-10 | W/W 0.8 | W/W 1.9 | W/W 2.6 | W/W 2.2 | W/W 0.84 | W/W 0.47 |
| 2^-12 | W/W 0.44 | W/W 0.95 | W/W 1.1 | W/W 2.6 | W/W 1.6 | W/W 0.75 |
| 2^-14 | W/W 0.24 | W/W 0.48 | W/W 1.8 | W/W 2.4 | W/W 2.1 | W/W 1.1 |

### btree

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.25 | P/P 0.41 | P/P 0.3 | P/P 0.18 | P/P 0.11 | W/P 0.061 |
| 2^-4 | P/Pt 0.12 | P/P 0.42 | W/P 0.45 | W/P 0.22 | W/P 0.32 | W/P 0.13 |
| 2^-6 | P/Pt 0.062 | W/P 0.047 | W/P 0.07 | W/P 0.14 | W/P 0.19 | W/P 0.19 |
| 2^-8 | P/Pt 0.031 | W/Pt 0.023 | W/P 0.0059 | W/P 0.029 | W/P 0.041 | W/P 0.045 |
| 2^-10 | P/Pt 0.016 | W/Pt 0.012 | W/Pt 0.0029 | W/P 0.00073 | W/P 0.0036 | W/P 0.0052 |
| 2^-12 | P/Pt 0.0078 | W/Pt 0.0059 | W/Pt 0.0015 | W/Pt 0.00037 | W/P 9.2e-05 | W/P 0.00045 |
| 2^-14 | P/Pt 0.0039 | W/Pt 0.0029 | W/Pt 0.00073 | W/Pt 0.00018 | W/Pt 4.6e-05 | W/P 1.1e-05 |

### grid

| alpha \ eps | 2^-3 | 2^-5 | 2^-7 | 2^-9 | 2^-11 | 2^-13 |
|---|---|---|---|---|---|---|
| 2^-2 | P/P 0.25 | P/P 0.41 | P/P 0.31 | P/P 0.19 | P/P 0.099 | P/P 0.048 |
| 2^-4 | P/Pt 0.12 | W/P 0.56 | P/P 0.77 | P/P 0.66 | P/P 0.42 | P/P 0.22 |
| 2^-6 | P/Pt 0.062 | W/P 0.047 | W/P 0.4 | P/P 1.5 | P/P 1.3 | P/P 0.84 |
| 2^-8 | P/Pt 0.031 | W/Pt 0.023 | W/P 0.045 | W/P 1 | W/P 2.8 | P/P 2.6 |
| 2^-10 | P/Pt 0.016 | W/Pt 0.012 | W/Pt 0.0029 | W/P 0.059 | P/P 4.5 | W/P 3.8 |
| 2^-12 | P/Pt 0.0078 | W/Pt 0.0059 | W/Pt 0.0015 | W/Pt 0.00037 | W/P 0.1 | W/P 8 |
| 2^-14 | P/Pt 0.0039 | W/Pt 0.0029 | W/Pt 0.00073 | W/Pt 0.00018 | W/P 4.6e-05 | W/P 0.21 |
