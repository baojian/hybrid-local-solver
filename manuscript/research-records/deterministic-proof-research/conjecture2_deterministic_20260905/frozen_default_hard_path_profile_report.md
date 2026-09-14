# Frozen default: one hard-alpha path profile

One guarded `cProfile` run of the delivered default completed successfully on the endpoint-seeded path with one billion vertices, alpha = 1/1000, rho = 1/64, and epsilon = 1e-8. No algorithm or package file changed, and no second solver call was made. The 120-second guard was not reached.

The full exact `SolverResult`—including every repaired stage and all internal ledgers—matches both completed default runs in `research_mass_scaled_grid_abba_benchmark.json`. All numerical package hashes match that reference and are unchanged after profiling. The complete-answer canonical SHA-256 is `320085fd6bdf36f862aa13629a4a6d082050aafa6dc72f63330e74f46cff7829`; the sparse-output canonical SHA-256 is `d1d343c286019132f97ecbe52074f2b78f5528d8a9ceddac6cb65dbd7280baee`. Canonical hashes use `sha256(json.dumps(value, sort_keys=True).encode())`.

## Exact work and output checks

- 6 stages, 2,560 iterations, and 54,656 cumulative kinetic volume.
- 24 vertices received degree queries; 23 vertices had adjacency rows scanned. External calls total 62 degree replies, 55 row requests, and 104 returned adjacency entries.
- Repeated adjacency work totals 55,312 entries: 54,709 in correction, 499 in internal checkpoints, and 104 in terminal repair. These repeated scans are separately charged from external cache-filling calls.
- The returned support has 23 vertices and degree-volume 45. All exact output and count comparisons pass.
- After profiling was disabled, an independent sparse subgradient certificate passed. It used 24 degree replies and one scan of the 23 output rows, totaling 45 entries. Its exact certificate and counts match the saved independent check. The certified additive objective gap is approximately 3.8389e-09 < 1e-8.

## Interpreter cost attribution

CPython 3.14.5 on macOS arm64 recorded 22,357,980 calls (21,017,747 primitive calls). The instrumented total is 13.5734 seconds. This is profiler time, not an estimate of ordinary solve time or evidence of relative speed. The profile encloses exactly the solver call, including its counting oracle, internal checkpoints, and terminal repair; graph setup, the independent final certificate, verification, and serialization are outside it.

Exclusive time can be added across the following rows; cumulative times must not be added because call trees overlap.

| Component | Exclusive profile time | Share | Concrete recorded calls |
|---|---:|---:|---|
| Integer-key AVL map (`_avl.py`) | 7.9664 s | 58.69% | 396,307 map writes; 631,910 map reads; 1,188,716 node refreshes |
| Integer two-tree reporter (`_integer_reporter.py`) | 3.1769 s | 23.40% | 266,604 reporter node refreshes; 2,560 projection calls |
| Direct-exception iteration (`_direct.py`) | 0.8716 s | 6.42% | 2,560 steps |
| Python `fractions.py` | 0.2774 s | 2.04% | 33,094 direct Fraction constructor calls |

The 114 scalar rebase calls account for 0.2417 cumulative profile seconds, and all 2,560 projection calls account for 0.7552 cumulative seconds; these overlap the components above. The 55,311 `math.gcd` calls have 0.0176 exclusive profile seconds. These function-call counts are interpreter observations, not arithmetic-operation or bit-complexity counts.

This run exposes a concrete practical limitation: a small locally discovered graph still causes substantial Python tree maintenance over the long accelerated iteration sequence. The exclusive-time breakdown places most recorded interpreter work in map and reporter operations. It does not establish an asymptotic bottleneck, quantify uninstrumented component costs, compare solvers, or justify changing the algorithm.

## Artifacts

| Artifact | SHA-256 |
|---|---|
| `profile_frozen_default_hard_path.py` | `7231b51cac0ed485b5766e935c016bfeb27be905fc51e132750b6b798aa53971` |
| `frozen_default_hard_path.prof` | `bfee92dfbe129c52f80ab097d5ff733d2ed28a6fa7dd9348f57b6c2851e40e5e` |
| `frozen_default_hard_path_profile.json` | `07a53a89d47e1be6b874622faad957a9b8175f39e0c29f9d1e31612f8d689480` |
| `frozen_default_hard_path_profile.log` | `0327452346770199c10e02512188c908df27fdc62fbbad73f68682a91d0c30e1` |

The JSON contains the complete exact answer, both solver and verifier ledgers, the independent certificate, before/after source hashes, and every function record. The binary `.prof` is readable with Python's standard `pstats` module. No comparative timing or new solver direction is claimed.
