# Next target: finish the supplied recursion with explicit failed-run caps

The fifth third-campaign block has implemented and proved resistance
estimation and bounded core sparsification. Its final source-backed
constructor is `cor:op3-weighted-constructor-contract`. This is a
supplied-graph result; it does not find a local support. The next block
must decide whether the existing conditional recurrence now becomes a
complete source-backed supplied theorem.

## Exact input contract to check

Read `sec:op3-supplied-recursion`, `sec:op3-recursive-vwf-ranges`, and
`sec:op3-mixed-additive-oracles`. The constructor has quality
O(m L^2/j), core O(j L), and work O(m[L^6+log(weight_ratio)]),
including the checked arbitrary-weight Abraham--Neiman source tree.
For `j=n`, use the whole-graph constant-factor sparsifier. Every
nonaborted output is connected; its total weight and minimum edge weight
are bounded even when the resistance estimator is wrong. The source
tree is not an implemented audit backend and must remain identified.

In the original recurrence, set K=A L^12, take
j=min(n,ceil(C2 m L^2/K)), and use the spectral floor. On successful
paths the child-size sum is at most half the parent size. Hence depth
O(log M0), total node mass <=2M0, at most 2M0 constructor calls,
and log(weight_ratio)=O(L^2) by the simultaneous range theorem.
The new constructor work is therefore O(m L^6), fitting its former
hypothesis. The dense base has O(m+(S+1)n^4) work with n<=K.
All persistent copies, failed objective guards and compressed residual
exports are already charged by the existing numerical lemmas.

## Failure branches must be bounded before expensive work

A successful spectral event makes all earlier correctness/range/size
proofs applicable. An incorrect preconditioner could invalidate those
proofs without producing an explicit FAIL. Do not assume a spectral
test detects that. Instead give the actual word algorithm a global
resource budget and halt with FAIL before exceeding it:

- constructor-call cap 2M0 with fresh conditional confidence p/(4M0);
- a depth cap ceil(log2 M0)+1;
- a total executed-word-operation and total allocated-word cap at a
  fixed computable upper bound C M0 L^d from the good-run analysis;
- reject invalid denominators/structural inputs before dependent
  operations, in addition to the constructor's explicit guards.

The resource cap must wrap primitive steps and allocations, not merely
check a finished opaque call. A standard step-by-step RAM simulation
has constant overhead and can also cap an imported source algorithm.
On the joint good-constructor event no cap is reached, so the wrapped
algorithm gives the same mixed output. Every other branch respects the
cap. A conditional union bound applies to each adaptively supplied input;
no independence of complete recursive instances is required.

Prove this cap lemma explicitly and audit its charging/early-abort
semantics using adversarial consumers, including attempts to allocate a
large buffer, repeated failed branches and a nested call tree. Do not
present a meta-level audit as a full implementation of the source tree
or the entire asymptotic VWF recursion.

## Completion conditions

Only after the explicit good-run cost, caps and failure accounting have
been reconciled should a new source-backed supplied-recursion corollary
be marked Proved here. Retain the old conditional theorem as a reusable
contract statement and point it to the new corollary. Update the current
status, conclusion and literature continuation pointer consistently.
Then return to potential-driven local discovery or the geometric boundary
event producer, which remains the central general-OP3 gap.
