"""Exact finite checks of the new moving-regularizer orthant recurrence.

This is a dense rational proof audit, not a local solver implementation.
All vectors use degree densities: x_i = sqrt(d_i) * density_i.
The D inner product therefore equals the symmetric-coordinate inner product.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

import networkx as nx


def mv(a, x):
    return [sum((v * w for v, w in zip(row, x)), F(0)) for row in a]


def sub(x, y):
    return [a - b for a, b in zip(x, y)]


def dot(d, x, y):
    return sum((di * a * b for di, a, b in zip(d, x, y)), F(0))


def solve(a, b):
    """Exact elimination; every principal matrix here is nonsingular."""
    n = len(b)
    aug = [list(row) + [value] for row, value in zip(a, b)]
    for j in range(n):
        assert aug[j][j]
        scale = aug[j][j]
        aug[j] = [v / scale for v in aug[j]]
        for i in range(j + 1, n):
            scale = aug[i][j]
            if scale:
                aug[i] = [v - scale * w for v, w in zip(aug[i], aug[j])]
    answer = [F(0)] * n
    for i in reversed(range(n)):
        answer[i] = aug[i][-1] - sum(aug[i][j] * answer[j] for j in range(i + 1, n))
    return answer


class ExactObstacle:
    """Reference-only exact principal systems with cached affine solutions."""

    def __init__(self, matrix, source):
        self.matrix = matrix
        self.source = source
        self.affine = {}

    def at(self, lam, initial=()):
        n = len(self.source)
        face = set(initial)
        for _ in range(n + 1):
            labels = tuple(sorted(face))
            x = [F(0)] * n
            if labels:
                if labels not in self.affine:
                    a = [[self.matrix[i][j] for j in labels] for i in labels]
                    self.affine[labels] = (
                        solve(a, [self.source[i] for i in labels]),
                        solve(a, [F(1)] * len(labels)),
                    )
                load, response = self.affine[labels]
                for i, l_i, t_i in zip(labels, load, response):
                    x[i] = l_i - lam * t_i
                    assert x[i] > 0
            residual = [h - lam - q for h, q in zip(self.source, mv(self.matrix, x))]
            new = {i for i in range(n) if i not in face and residual[i] > 0}
            if not new:
                assert all(residual[i] == 0 for i in face)
                assert all(residual[i] <= 0 for i in range(n) if i not in face)
                return x, labels
            face.update(new)
        raise AssertionError("Exact active-set reference did not finish")


def check_case(graph, seed, alpha, rho_factor=16, tail=12):
    n = len(graph)
    degrees = [graph.degree(i) for i in range(n)]
    matrix = [
        [
            (1 + alpha) / 2
            if i == j
            else -(1 - alpha) / (2 * degrees[i])
            if graph.has_edge(i, j)
            else F(0)
            for j in range(n)
        ]
        for i in range(n)
    ]
    source = [alpha / degrees[i] if i == seed else F(0) for i in range(n)]
    theta = F(1, 2)
    while theta**2 > alpha:
        theta /= 2
    mu = theta**2
    chi = 1 - theta
    eta = 1 - theta / 2
    beta = (1 - alpha) / (1 + theta)
    assert beta <= chi < eta
    r = F(1, degrees[seed])
    rho = r / rho_factor
    x = [F(0)] * n
    z = x.copy()
    t = solve(matrix, source)
    assert dot(degrees, t, [F(1)] * n) == 1
    reference = ExactObstacle(matrix, source)
    opt, face = reference.at(alpha * r)
    assert not face
    total_work = 0
    inverse_r_sum = F(0)
    outside_work = 0
    force_square_sum = F(0)
    signed_sum = F(0)
    slack_sum = F(0)
    steps = 0
    frozen = 0
    max_work_ratio = F(0)
    max_response_ratio = F(0)
    max_primal_mass = F(0)

    def objective(u, lam):
        return dot(degrees, u, mv(matrix, u)) / 2 - dot(degrees, sub(source, [lam] * n), u)

    def bank(u, kinetic, lam):
        residual = sub(mv(matrix, u), source)
        dz = sub(kinetic, t)
        return (
            dot(degrees, residual, residual) / 2
            + alpha * lam * (dot(degrees, u, [F(1)] * n) - 1)
            + mu * dot(degrees, dz, mv(matrix, dz)) / 2
        )

    while frozen < tail:
        lam = alpha * r
        r_next = max(rho, eta * r)
        lam_next = alpha * r_next
        if r == rho:
            frozen += 1
        opt_next, next_face = reference.at(lam_next, face)
        core, _ = reference.at(lam / 2, face)
        y = [(a + theta * b) / (1 + theta) for a, b in zip(x, z)]
        grad = [a - b + lam for a, b in zip(mv(matrix, y), source)]
        raw = [chi * b + theta * c - g / theta for b, c, g in zip(z, y, grad)]
        p = [max(F(0), v) for v in raw]
        normal = sub(raw, p)
        x_next = [chi * a + theta * b for a, b in zip(x, p)]

        # This is the new simple projection fact; no box or mass constraint.
        second_sector = dot(degrees, sub(mv(matrix, p), source), normal)
        assert second_sector >= 0
        assert dot(degrees, sub(p, opt), normal) >= 0

        old_first = objective(x, lam) - objective(opt, lam)
        old_first += mu * dot(degrees, sub(z, opt), sub(z, opt)) / 2
        new_first = objective(x_next, lam) - objective(opt, lam)
        new_first += mu * dot(degrees, sub(p, opt), sub(p, opt)) / 2
        assert 0 <= new_first <= chi * old_first

        old_bank = bank(x, z, lam)
        frozen_bank = bank(x_next, p, lam)
        new_bank = bank(x_next, p, lam_next)
        assert frozen_bank <= chi * old_bank
        assert new_bank <= chi * old_bank + alpha * (lam - lam_next)
        assert old_bank <= alpha * lam
        assert new_bank <= alpha * lam_next
        response = sub(mv(matrix, x), source)
        assert dot(degrees, response, response) <= 4 * alpha * lam
        diff = sub(x, opt)
        response_diff = mv(matrix, diff)
        response_sq = dot(degrees, response_diff, response_diff)
        assert response_sq <= 10 * alpha * lam
        max_response_ratio = max(max_response_ratio, response_sq / (alpha * lam))

        force = [-(a - mu * b) / (1 + theta) for a, b in zip(response_diff, diff)]
        slack = [a - b + lam for a, b in zip(mv(matrix, opt), source)]
        selected = [i for i in range(n) if p[i] > opt_next[i]]
        excess = sum(degrees[i] * theta * max(F(0), z[i] - opt[i]) for i in range(n))
        new_excess = sum(degrees[i] * theta * max(F(0), p[i] - opt_next[i]) for i in range(n))
        selected_slack = sum(degrees[i] * slack[i] for i in selected)
        selected_force = sum(degrees[i] * force[i] for i in selected)
        assert new_excess + selected_slack <= beta * excess + selected_force
        assert all(opt_next[i] >= opt[i] for i in range(n))
        assert all(core[i] >= opt_next[i] for i in range(n))

        current_outside = sum(degrees[i] for i in range(n) if p[i] > 0 and core[i] == 0)
        assert selected_slack >= lam * current_outside / 2
        inverse_r_sum += 1 / r
        total_work += sum(degrees[i] for i in range(n) if p[i] > 0)
        outside_work += current_outside
        force_square_sum += dot(degrees, force, force) / lam**2
        signed_sum += selected_force / lam
        slack_sum += selected_slack / lam
        assert outside_work / F(2) <= slack_sum <= signed_sum
        assert force_square_sum <= 10 * inverse_r_sum
        selected_volume_bound = outside_work + 2 * inverse_r_sum
        assert signed_sum**2 <= selected_volume_bound * force_square_sum
        assert total_work <= 44 * inverse_r_sum
        max_work_ratio = max(max_work_ratio, total_work / inverse_r_sum)
        max_primal_mass = max(max_primal_mass, dot(degrees, x_next, [F(1)] * n))
        x, z, r, opt, face = x_next, p, r_next, opt_next, next_face
        steps += 1
    return {
        "n": n,
        "seed": seed,
        "alpha": str(alpha),
        "rho": str(rho),
        "tail_steps": tail,
        "steps": steps,
        "kinetic_degree_work": total_work,
        "max_work_over_inverse_regularizers": float(max_work_ratio),
        "max_response_over_alpha_lambda": float(max_response_ratio),
        "max_primal_mass": float(max_primal_mass),
        "final_objective_gap": float(objective(x, alpha * rho) - objective(opt, alpha * rho)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--alphas", default="1/4,1/16")
    parser.add_argument("--rho-factor", type=int, default=8)
    parser.add_argument("--tail", type=int, default=12)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--skip", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    alphas = [F(v) for v in args.alphas.split(",")]
    root = Path(__file__).resolve().parents[3]
    provenance = {
        "start_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True)
        ),
        "audit_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "exact rational density coordinates",
        "graph_family": "all connected NetworkX graph-atlas representatives through max_n; every seed",
        "random_seed": None,
        "stopping_rule": "specified geometric regularization ramp, followed by fixed tail horizon",
        "parameters": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
    }
    results = []
    counter = 0
    next_report = 15.0
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps({"provenance": provenance, "status": "running"}) + "\n")
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        if not 2 <= len(graph) <= args.max_n or not nx.is_connected(graph):
            continue
        for seed in graph:
            for alpha in alphas:
                counter += 1
                if counter <= args.skip:
                    continue
                if args.limit and len(results) >= args.limit:
                    break
                result = check_case(graph, seed, alpha, args.rho_factor, args.tail)
                result["atlas_id"] = atlas_id
                results.append(result)
                elapsed = time.monotonic() - start
                if elapsed >= next_report:
                    print(
                        json.dumps(
                            {"passed": len(results), "seconds": round(elapsed, 2), "last": result}
                        ),
                        flush=True,
                    )
                    next_report = elapsed + 30
                if args.output and len(results) % 50 == 0:
                    args.output.write_text(
                        json.dumps(
                            {"provenance": provenance, "status": "running", "cases": results},
                            indent=2,
                        )
                        + "\n"
                    )
            if args.limit and len(results) >= args.limit:
                break
        if args.limit and len(results) >= args.limit:
            break
    output = {
        "provenance": provenance,
        "status": "passed",
        "elapsed_seconds": time.monotonic() - start,
        "case_count": len(results),
        "total_exact_steps": sum(row["steps"] for row in results),
        "cases": results,
    }
    if args.output:
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "cases"}), flush=True)


if __name__ == "__main__":
    main()
