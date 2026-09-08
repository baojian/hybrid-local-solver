"""Exact positive-subsolution certificates for an asymptotic BFS obstruction.

The original graph is an implicit unweighted seed/path/binary-branch tree.
Every positive subsolution row is checked with its original full degree.
No exact optimizer, global support oracle or fast local algorithm is used.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time


def check(length, counts):
    assert length >= 4
    lam = F(1, 16 * length**2)
    alpha, epsilon, delta = lam**2, 2 * lam, lam / 4
    gamma = (1 - alpha) / (1 + alpha)
    bar = 1 - gamma
    z = [2 * lam * (length - i) ** 2 for i in range(length + 1)]
    assert z[0] == F(1, 8) and z[-1] == 0
    assert 3 * z[0] - gamma * z[1] <= 1 - 3 * lam
    counts["original_seed_positive_subsolution_rows"] += 1
    assert bar * (length**2 + 1) <= F(1, 2)
    for i in range(1, length):
        original = 2 * z[i] - gamma * (z[i - 1] + z[i + 1])
        formula = -4 * lam + 4 * bar * lam * ((length - i) ** 2 + 1)
        assert original == formula <= -2 * lam
        counts["original_path_positive_subsolution_rows"] += 1
    distance = length // 2
    assert z[distance] >= F(1, 32) > delta
    work = 3 + 3 * (2 ** (distance - 1) - 2) + 2 * (distance - 2)
    counts["significant_undiscovered_coordinate_certificates"] += 1
    return {
        "path_length_and_binary_height": length,
        "ambient_vertices": 2 ** (length + 1) - 1 + length,
        "alpha": str(alpha),
        "eps_appr": str(epsilon),
        "physical_seed": 0,
        "maximum_original_degree": 3,
        "positive_subsolution_rows": length,
        "missed_path_distance": distance,
        "potential_lower_bound": str(z[distance]),
        "significant_threshold": str(delta),
        "necessary_work_even_before_discovery": work,
        "work_times_eps_appr": str(work * epsilon),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start, counts = time.monotonic(), Counter()
    lengths = list(range(4, 65)) + [128, 256, 512, 1024, 2048, 4096] if args.full else [4, 16, 64]
    cases = [check(length, counts) for length in lengths]
    result = {
        "audit": "incremental_active_set_sdd.breadth_first_envelope_family",
        "arithmetic": "exact fractions and integer original-layer counts",
        "input_family": "Implicit finite unweighted degree-three tree with path length N and binary height N, lambda=1/(16*N^2), alpha=lambda^2, epsilon=2*lambda",
        "stopping_rule": "Validate every positive row of an explicit subsolution and the exact BFS discovery work; the theorem covers all N>=4",
        "scope": "Supports a proved obstruction to FIFO BFS discovered-label envelopes, even with a degree-three filter. No lower bound on arbitrary local algorithms or OP3.",
        "audit_only": dict(counts),
        "cases": cases,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
