"""Exact rational check of the decoy-component obstruction to scalar MSE.

The listed eigenvalues are the Perron eigenvalues of the active two-vertex
blocks described in op2_support_safe_acceleration.md.  All arithmetic is over
fractions; the tiny amplitudes make the decoys negligible in energy but do
not change the componentwise ratios that determine the global momentum.
"""

from fractions import Fraction


alpha = Fraction(1, 100)
c = (1 - alpha) / 2
degrees = [10**6, 9 * 10**5, 8 * 10**5, 7 * 10**5, 6 * 10**5]
lambdas = [c * (1 + Fraction(1, degree)) for degree in degrees]
lambdas.append(1 - alpha)

decoy_amplitude = Fraction(1, 10**12)
amplitudes = [decoy_amplitude] * len(degrees) + [Fraction(1)]


def energy(residual):
    return sum(
        value * value / (1 - eigenvalue)
        for value, eigenvalue in zip(residual, lambdas)
    )


initial_energy = energy(amplitudes)
previous = amplitudes[:]
current = [eigenvalue * value for eigenvalue, value in zip(lambdas, amplitudes)]
thetas = []

for _ in range(1, 10):
    candidates = [
        value / (old_value - value)
        for old_value, value in zip(previous, current)
        if old_value > value
    ]
    theta = min(candidates)
    extrapolated = [
        (1 + theta) * value - theta * old_value
        for old_value, value in zip(previous, current)
    ]
    assert min(extrapolated) >= 0
    following = [
        eigenvalue * value
        for eigenvalue, value in zip(lambdas, extrapolated)
    ]
    thetas.append(theta)
    previous, current = current, following

gap_ratio = energy(current) / initial_energy

assert all(thetas[index] == 0 for index in [1, 3, 5, 7])
assert gap_ratio > Fraction(74, 100)
print("exact MSE decoy counterexample verified")
print("ten-step energy ratio:", float(gap_ratio))
