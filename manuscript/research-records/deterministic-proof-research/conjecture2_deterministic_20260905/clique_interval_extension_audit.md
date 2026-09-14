# Exact clique quotient and finite trajectory certificate

The root independently extended the fresh interval verifier to clique
chambers. This is a symmetry-based verification computation, not a local
solver and not an asymptotic work lower bound.

For a clique of size R entered through one port, the port has R neighbors
including its incoming tree edge. Each bulk vertex has one port neighbor
and R-2 bulk neighbors, hence degree R-1. The aggregate transition matrix
must include a bulk self-orbit coefficient (R-2)/(R-1). The Dirichlet energy
of within-orbit edges is zero; omitting those zero differences in the
quotient energy is correct, while omitting the transition coefficient is
incorrect. The new implementation makes this distinction explicitly.

`test_clique_interval_extension.py` independently constructs the full
11-vertex graph for L=2, p=1, R=4. It compares eight ordinary and eight
monotone capped steps with exact Fraction computations, including the
projection, line search, and all orbit state intervals. It passed.
The existing independent interval suite also remains valid; its original
audit predates this clique extension.

`capped_tree_clique_interval_L128.json` uses L=128, p=16, R=L^2,
gamma=1/16, and 1,000-digit directed rounding for 512 monotone steps.
The certified lower and possible upper cumulative kinetic work are equal,
so every support decision needed for that cumulative count is certified.
Every bulk vertex is active on exactly 275 steps. The normalized bulk work
is the exact rational number 73810739475/4294705168, approximately 17.186.
The maximum final aggregate state interval width is below 2.54e-661.

The separate exact volume argument in `mass_cap_adversary.md` excludes all
bulk vertices from the half-rho comparison support. Uniform from-zero
arrival and persistence across arbitrarily large L remain unproved.
This finite certificate does not establish such a uniform theorem and does
not refute Conjecture 2.

Root also reran the five exact cleanup test methods after their independent
implementation audit; all passed in 1.890 seconds. These are deterministic
verification computations, with no randomized test generation.
