"""Source-valid large live cores despite peeling, on an implicit finite tree.

Only original interior degree-three vertices activate; therefore no first
nonseed degree-two removal exists. This rejects a uniform small-core claim
for the specified representation, not OP3 or other local algorithms.
"""

from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from geometric_value_events import solve
from live_core_peeling import local_peeling


class BinaryOracle:
    def __init__(self, height):
        self._height = height
        self.degrees, self.rows, self.counts = {}, {}, Counter()

    def degree(self, i):
        self.counts["degree_cache_lookups"] += 1
        if i not in self.degrees:
            depth = (i + 1).bit_length() - 1
            assert depth <= self._height
            self.degrees[i] = 2 if i == 0 else 1 if depth == self._height else 3
            self.counts["degree_replies"] += 1
        return self.degrees[i]

    def row(self, i):
        assert i not in self.rows
        depth = (i + 1).bit_length() - 1
        neighbors = [] if i == 0 else [(i - 1) // 2]
        if depth < self._height:
            neighbors += [2 * i + 1, 2 * i + 2]
        self.rows[i] = tuple(neighbors)
        self.counts["row_scans"] += 1
        self.counts["adjacency_entries_read"] += len(neighbors)
        return self.rows[i]


def radial_obstacle(height, gamma, lam):
    """Independent symmetry-reduced full-obstacle reference; audit work only."""
    for last in range(height + 1):
        degree = [2 if i == 0 else 1 if i == height else 3 for i in range(last + 1)]
        matrix = [
            [
                F(degree[i])
                if i == j
                else -gamma
                if j == i - 1
                else -2 * gamma
                if j == i + 1
                else F(0)
                for j in range(last + 1)
            ]
            for i in range(last + 1)
        ]
        load = [F(int(i == 0)) - lam * degree[i] for i in range(last + 1)]
        values = solve(matrix, load)
        assert min(values) > 0
        if last == height or gamma * values[-1] <= lam * (1 if last + 1 == height else 3):
            return values
    raise AssertionError("finite radial reference must terminate")


def main():
    started, rows = time.time(), []
    for h in [1, 2, 3, 4, 5]:
        height, alpha = 3 * h + 5, F(1, 3)
        epsilon, gamma = F(1, 12 * 6**h), F(1, 2)
        reference = radial_obstacle(height, gamma, epsilon / 2)
        assert len(reference) - 1 < height
        for policy in ["fifo", "lifo"]:
            oracle = BinaryOracle(height)
            answer, counts = local_peeling(oracle, 0, alpha, epsilon, policy=policy)
            exposed = set(oracle.degrees)
            for i in exposed:
                depth = (i + 1).bit_length() - 1
                neighbors = [] if i == 0 else [(i - 1) // 2]
                if depth < height:
                    neighbors += [2 * i + 1, 2 * i + 2]
                residual = (
                    F(int(i == 0))
                    - oracle.degrees[i] * answer.get(i, F(0))
                    + gamma * sum(answer.get(j, F(0)) for j in neighbors)
                )
                assert 0 <= residual <= epsilon * oracle.degrees[i]
                if i in answer:
                    assert residual == epsilon * oracle.degrees[i] / 2
                    assert 0 < answer[i] <= reference[depth]
            assert set(oracle.rows) == set(answer)
            assert all(j in exposed for neighbors in oracle.rows.values() for j in neighbors)
            assert set(range(2 ** (h + 1) - 1)) <= set(answer)
            assert counts.get("core_removals", 0) == 0
            assert counts["final_core_size"] == counts["peak_core_size"] == len(answer)
            n = len(answer)
            mandatory = n * (n - 1) * (2 * n - 1) // 6
            assert counts["inverse_entry_updates"] == mandatory
            rows.append(
                {
                    "h": h,
                    "ambient_height": height,
                    "ambient_vertices": 2 ** (height + 1) - 1,
                    "alpha_lazy": str(alpha),
                    "eps_appr": str(epsilon),
                    "lambda": str(epsilon / 2),
                    "policy": policy,
                    "positive_vertices": n,
                    "required_prefix_vertices": 2 ** (h + 1) - 1,
                    "maximum_positive_depth": max((i + 1).bit_length() - 1 for i in answer),
                    "obstacle_last_positive_depth": len(reference) - 1,
                    "support_volume": sum(oracle.degrees[i] for i in answer),
                    "mandatory_inverse_updates": mandatory,
                    "counts": counts,
                    "oracle_counts": dict(oracle.counts),
                }
            )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.live_core_width_probe",
        "claim_status": "Refuted: LIFO plus current-degree-two peeling guarantees a polylogarithmic live core",
        "scope": "Explicit retained inverse on canonical single-seed traces; not an OP3 lower bound",
        "arithmetic": "exact fractions",
        "graph": "finite complete binary tree via degree/row oracle",
        "seed": 0,
        "random_seed": None,
        "stopping_rule": "verified grouped-flux ACL stop, lambda=eps_appr/2",
        "reference": "symmetry-reduced exact obstacle on radial levels; excluded from local counts",
        "rows": rows,
        "git_commit": subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty_worktree": bool(
            subprocess.check_output(
                ["git", "-C", str(repo), "status", "--porcelain"], text=True
            ).strip()
        ),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": hashlib.sha256(
            Path(__file__).with_name("live_core_peeling.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_reference": round(time.time() - started, 3),
    }
    output = repo / "manuscript/notes/incremental_active_set_sdd/LIVE_CORE_WIDTH_AUDIT.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
