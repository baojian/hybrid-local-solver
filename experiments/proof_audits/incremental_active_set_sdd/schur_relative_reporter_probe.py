"""Source-valid failure of a constant-relative Schur-key quietness test.

Two path arms have retained seed potential x. One inactive tip is quiet and
is a valid 1.1-approximate normalized extreme point, while the other tip's
original ACL residual exceeds the requested tolerance. All checks are exact.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess


def check(length):
    other = length + (length + 39) // 40
    gamma = 1 - F(1, (length + other + 3) ** 4)
    alpha = (1 - gamma) / (1 + gamma)
    lam = F(length + 1, (length + other + 2) * (length + other + 3))
    core_diagonal, core_load = F(2), 1 - 2 * lam
    records = [(F(2), -2 * lam, gamma), (F(2), -2 * lam, gamma)]
    admitted = [0, 0]
    targets = [length, other]
    eta = F(1, 10)
    while admitted != targets:
        value = core_load / core_diagonal
        keys = [coupling * value / -load for _, load, coupling in records]
        choice = max((i for i in range(2) if admitted[i] < targets[i]), key=lambda i: keys[i])
        assert keys[choice] > 1
        assert keys[choice] >= max(keys) / (1 + eta)
        diagonal, load, coupling = records[choice]
        core_diagonal -= coupling * coupling / diagonal
        core_load += coupling * load / diagonal
        records[choice] = (
            2 - gamma * gamma / diagonal,
            -2 * lam + gamma * load / diagonal,
            gamma * coupling / diagonal,
        )
        admitted[choice] += 1
    value = core_load / core_diagonal
    normalized = [coupling * value / -load for _, load, coupling in records]
    gates = [load + coupling * value for _, load, coupling in records]
    assert normalized[0] > 1 >= normalized[1]
    assert normalized[1] >= normalized[0] / (1 + eta)
    epsilon = 2 * lam
    residual = gates[0] + 2 * lam
    assert residual > epsilon * 2
    # Independent full-face solve in left-to-right path order, with the
    # seed in the interior; this is validation work, not the proposed gate.
    n = length + other + 1
    diagonal = [F(2)] * n
    rhs = [F(int(i == length)) - 2 * lam for i in range(n)]
    for i in range(1, n):
        diagonal[i] -= gamma * gamma / diagonal[i - 1]
        rhs[i] += gamma * rhs[i - 1] / diagonal[i - 1]
    solution = [F(0)] * n
    for i in reversed(range(n)):
        solution[i] = (rhs[i] + (gamma * solution[i + 1] if i + 1 < n else 0)) / diagonal[i]
    assert min(solution) > 0 and solution[length] == value
    assert gamma * solution[0] == residual
    assert gamma * solution[-1] == gates[1] + 2 * lam
    return {
        "admitted_arm_lengths": [length, other],
        "ambient_arm_lengths": [length + 2, other + 2],
        "ambient_vertices": length + other + 5,
        "alpha_lazy": str(alpha),
        "gamma": str(gamma),
        "lambda": str(lam),
        "eps_appr": str(epsilon),
        "relative_factor": "11/10",
        "decimal_diagnostics_only": {
            "true_normalized_extreme": float(normalized[0]),
            "allowed_quiet_return": float(normalized[1]),
            "missed_gate": float(gates[0]),
            "residual_over_requested_degree_tolerance": float(residual / (2 * epsilon)),
            "schur_load_over_native_load": float(-records[0][1] / (2 * lam)),
        },
        "exact_strict_admission_checks": length + other,
        "approximate_extreme_contract_on_every_admission": "passed",
        "exact_failure_and_approximation_checks": "passed",
        "independent_full_face_coordinates": n,
    }


def main():
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.schur_relative_reporter_probe",
        "claim_status": "Refuted: a constant-relative normalized extreme query alone certifies original ACL quietness",
        "scope": "An oracle-contract failure, not a lower bound or a refutation of geometric original-value reporting",
        "arithmetic": "exact fractions; only displayed diagnostics converted to decimals",
        "graph": "degree-two seed with two path arms, actual degree two at both inactive tips",
        "seed": 0,
        "random_seed": None,
        "stopping_rule_tested": "accept quiet when the returned approximate normalized extreme is <= 1",
        "rows": [check(length) for length in [64, 128, 256]],
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = repo / "results/raw/op3_schur_relative_reporter.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
