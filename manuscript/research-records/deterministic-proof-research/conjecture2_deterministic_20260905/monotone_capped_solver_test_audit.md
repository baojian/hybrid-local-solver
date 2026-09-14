# Exact audit of the monotone capped prototype

The unguarded `MonotoneCappedSolver` agrees with an independent dense rational
recurrence in every checked case. No numerical or recurrence defect was found.
The only production edit was correcting the docstring's proof reference to
`monotone_capped_acceleration_audit.md`; the original lazy solver was not edited.
This verifies a prototype and the stated locality mechanism, not the unresolved
initial-phase support-work bound or general Conjecture 2.

## Reference and coverage

`test_monotone_capped_solver.py` independently constructs the full rational
matrix H=((1+alpha)/2)D-((1-alpha)/2)A, computes the gradient by dense matrix
multiplication, projects by a separately coded sorted weighted water fill, and
minimizes the quadratic along the segment by a direct gradient/direction inner
product. It does not use the production AVL reporter or cached line coefficients.
Small optimal points come from the independent exhaustive dense KKT oracle;
the 101-vertex star uses a closed-form optimum checked against every KKT row.
All inputs, parameters, calculations, and comparisons are deterministic and
exact `Fraction` arithmetic.

The saved run passes all eight test methods: 56 zero-initialized trajectories
on every connected labeled graph with two or three vertices (all seeds, two
values of theta, two values of rho), 292 exact step comparisons, five injected
feasible states, and two explicit stopping tests. Among the compared steps,
42 have segment fraction zero, 32 are strictly interior, 218 have fraction one,
and one has a binding mass cap. The explicit interior example has fraction 4/5.
Injected states test the general feasible-state recurrence; their reachability
from zero is not asserted.

Each compared step checks primal and auxiliary vectors, cap status, exact line
fraction, both masses, the cached quadratic and objective, every exposed
Laplacian response coordinate, monotonicity, the accelerated energy inequality
including its dissipation term, and the reported energy bound. Adjacency scans
per step equal the selected auxiliary-support volume exactly. Cached adjacency
lists are read from the input oracle at most once. The source input wrapper
rejects global iteration and global size requests.

## Energy and lazy scale are separate

The numerical representation uses sigma_next=(1-s*theta)*sigma. The proved
energy multiplier is instead (1-theta) each iteration. Tests inject a nonunit
sigma and cover all three line-search branches. At an optimal primal point
with a different feasible auxiliary point, s=0 and sigma remains one while the
energy multiplier becomes 1-theta. `run` correctly stops by this energy bound.
A separate zero-initialized path run stops after five steps with exact objective
gap 6781/11005853696 and bound epsilon=1/128. Warm initialization recomputes
the quadratic correctly and uses the supplied objective-gap certificate as
documented; the test supplies an independently computed exact certificate.

## What locality does and does not guarantee

On a 32-vertex path, an injected position supported on all 32 vertices and an
empty next auxiliary support require zero additional adjacency scans. During
that measured iteration, guarded dictionaries reject any full iteration over
old X, R, or degree records; no guard fires. This checks the sparse line-search
implementation even when old primal support persists.

For a leaf-seeded star with hub degree 1000, theta=1/4 and rho=1/100, five steps
read only the seed adjacency list (one entry), query two degrees, and perform
five repeated adjacency-entry scans. The hub remains exposed but unscanned.

The corresponding degree-100 star demonstrates a real limitation of the
unguarded method: its exact optimum is only the seed, with density 99/850,
but the auxiliary support volumes are [1,1,101,1,1]. The hub enters the auxiliary
vector at step three, enters the primal vector, and retains positive primal
value afterward. The dense reference agrees. This is neither a code defect
nor a general asymptotic counterexample; it prevents conflating actual
auxiliary support with optimal support. A future fixed-face degree guard is
a different algorithm and is intentionally absent from these tests.

## Scope of measured costs

`monotone_capped_verification.json` retains degree replies, first adjacency
entries, repeated adjacency scans, AVL visits and rotations, key updates,
projection emissions, output words, and iterations. These are structural event
counts, not a complete instrumentation of every Python or rational arithmetic
operation, memory word, comparison, or bit cost. The line-search calculation
adds a constant number of scans over the newly selected auxiliary vector and
scalar operations, already covered by the separate word-model proof. This
suite does not establish a bound on cumulative support work.

The largest numerator or denominator among the measured exact state values
has 581 bits after just five steps of the transient-hub case. Rational exactness
certifies these small experiments; it does not make this implementation
practical for long large-graph runs. No floating-point accuracy is claimed.
