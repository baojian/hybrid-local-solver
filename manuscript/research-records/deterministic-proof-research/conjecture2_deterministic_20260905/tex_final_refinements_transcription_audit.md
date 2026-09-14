# Audit of the final two TeX subsections

Audited the `app:rounded-deficit` and `app:singleton` subsections of
`practical_schedules_appendix.tex`, and the final forward reference in
`practical_refinements_appendix.tex`. The surrounding definitions and
referenced equations were checked in these two files and the fresh
`deterministic_conjecture2.tex`. No TeX or implementation file was edited.

The transcription is mathematically sound. No correction is required.

For `app:rounded-deficit`, the seed-positivity argument correctly supplies
`eta>=eta_*(r)>=r*d_v>=r`. The auxiliary energy retains source mass, including
the possible negativity of its comparison energy, and yields the stated
response bound with coefficient 18 and additive `4 Gamma`. The unchanged
grid chain has exactly the audited coefficient `29/8192`. Replacing the
core volume and response bounds in the perturbed selected ledger gives
`16*22+4*2=360`. The `363 eta(K+1)/r` exposure estimate includes additive
seed and baseline records because `eta/r>=1`.

The text retains zero-step initialization, repeated fixed-source work,
full scalar rebase/key visits, geometric checkpoint scans, all terminal
operations, and temporary-state reclamation. The actual repair and
concavity argument gives `eta_j/r_j<=4 eta_*(rho)/rho`, including the
initial zero baseline. Summing the already charged stage estimate over
the explicit `O(L)` stages yields the displayed `L^4` word and `L^2`
adjacency bounds. It does not erase that stage logarithm or assert an
unproved weighted geometric sum. The prior unweighted bounds may indeed
be combined by taking their minimum. The existing bounded encoding and
`B^3` bit multiplier are unchanged. The interpretation using total graph
volume is analytical only; no volume query is introduced.

For `app:singleton`, the restricted density, all positive/zero KKT signs,
the integer comparison, equality acceptance, early failed-prefix stopping,
and cutoff are correct. The stated trial costs include the seed degree,
all visited neighbor degrees, and every visited entry. Its use of constant
auxiliary scalar storage and integer products avoids a degree-denominator
sum. Both `d_v<1/rho` and `d_v<=eta_*(rho)/rho` hold in the stipulated
nontrivial regime, so the prefix preserves both local bounds. Repeated
fallback reads are explicitly paid, and a general rational singleton
output is correctly distinguished from an intermediate dyadic baseline.
Zero and alpha-one branches remain qualified by the preceding regime
paragraph and the subsection's opening sentence.

One optional terminology clarification was sent to the root: the quantity
`alpha*rho*d_i-c*f_v` is the gradient with respect to density coordinate
`f_i`, equivalently `w_i` times the normalized-coordinate gradient. Thus
“density-coordinate gradient” is more explicit than “density-form KKT
slack.” The formula and its sign test are correct as written.

The new forward reference accurately says that the same default rounded
precision suffices; it does not broaden the result to unchecked floating
point. A mechanical reference check across the three fresh TeX files found
no unresolved local references or duplicate labels. Compilation and layout
were left to the root, as requested.
