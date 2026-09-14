# Audit of possible uniform arrival arguments

Status: exact finite recurrences and limitations of proposed comparison
arguments. These statements do not establish zero-start arrival for the
tree–clique family.

## 1. A small exact virgin-front calculation

In the limiting ordinary recurrence `a=1`, with no cap, source, or
regularization, freeze one binary-tree level's aggregate position at C
and its auxiliary velocity at zero. Start the next two levels at zero,
and freeze the farther boundary at zero. If their aggregate positions
are u1,u2 and velocities v1,v2, the exact update is

    v1new=[(v1-u1)/2+(2*C+u2+v2)/6]_+,
    v2new=[(v2-u2)/2+(u1+v1)/3]_+,
    unew=u+vnew.

The first-level positions, divided by C, at steps 1 through 5 are

    1/3, 2/3, 49/54, 19/18, 1087/972.

The second-level positions are

    0, 2/9, 5/9, 67/81, 77/81.

Both velocities are zero at step 6. Thus a virgin local front can
amplify the stored boundary position by a fixed factor in five steps.
For C<=1 the sum of these two velocities never exceeds 31C/54<1,
so this particular isolated calculation does not need a cap.

The calculation suggests that a finite-window profile invariant could
explain the observed arrival and the constant-height capped pulse. It
cannot be iterated without controlling the actual preloaded profiles,
the neighboring levels, and the global cap multiplier.

## 2. More past forcing does not order later positions

There is a simple exact obstruction to a tempting monotone-comparison
proof. Consider the one-dimensional positive-velocity recurrence

    vnew=[(v-u)/2+b]_+,
    unew=u+vnew.

Starting at zero with b=1 gives positions 1,2,5/2, then zero velocity.
Change b to 2 after this stopping point. The next positions are

    13/4, 4, 35/8,

then the velocity vanishes. In contrast, a trajectory kept at zero
until b changes to 2 has subsequent positions 2,4,5 and then stops.
The trajectory with the larger earlier forcing ends at 35/8<5.

Thus the negative own-position term prevents a general ordering by
past nonnegative forcing, despite nonnegative velocities and monotone
positions. A claimed lower comparison against a restarted virgin-front
trajectory needs an additional state invariant.

Likewise, a two-level state u1=99C/100,u2=33C/40 with both velocities
zero is stationary under the frozen C/zero boundaries from section 1:
both raw velocities are strictly negative. Its first coordinate is
below C. This is an arbitrary-state check, not a claimed initialized
RPPR trajectory or a counterexample on an infinite unfrozen tail.

## 3. What is still needed

The remaining task for the tree–clique work obstruction is to prove
that a port reservoir of order theta, together with a sufficiently
small outside positive raw auxiliary mass, occurs from the actual zero
initialization within a polylogarithmic number of steps. The exact
post-arrival conditional theorem is in `mass_cap_adversary.md`.

One possible route is a finite-window invariant for the cap-normalized
binary-tree pulse. In aggregate mass coordinates its zero-source,
`a=1` limit is translation-compatible: shifting one level multiplies
the degree weights by two and halves the simplex density multiplier,
while preserving the total auxiliary mass cap. The observed pulse
deposits a position wake of constant aggregate height. No invariant
region or attraction proof for this limiting system has been certified.

The ordinary primal update is simpler for this purpose. The monotone
segment variant additionally needs either a lower bound on its segment
fractions during arrival or a proof that the full candidate is selected
through the required interval. The post-arrival persistence theorem
itself does not require such a bound.
