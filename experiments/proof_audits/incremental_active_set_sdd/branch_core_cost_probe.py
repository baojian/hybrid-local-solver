"""Charge the dense-core backend on easy balanced trees; not an OP3 lower bound."""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import time

from bounded_attachment_cycle import LocalOracle
from branch_core_flux import check_acl, local_branch_core
import networkx as nx


def main():
    started = time.time()
    rows = []
    for height in [3, 4, 5, 6]:
        graph = nx.balanced_tree(2, height)
        alpha = F(1, 1009)
        epsilon = alpha / (10 * 6**height)
        oracle = LocalOracle(graph)
        answer, info = local_branch_core(oracle, 0, alpha, epsilon)
        check_acl(graph, 0, alpha, epsilon, answer)
        assert set(answer) == set(graph) == set(oracle.rows)
        r = len(info["cores"])
        assert r == 2**height - 1
        mandatory = r * (r - 1) * (2 * r - 1) // 6
        assert info["inverse_entry_updates"] >= mandatory
        rows.append(
            {
                "height": height,
                "ambient_vertices": len(graph),
                "positive_vertices": len(answer),
                "support_volume": 2 * len(graph.edges),
                "alpha_lazy": str(alpha),
                "eps_appr": str(epsilon),
                "lambda": str(epsilon / 2),
                "retained_vertices": r,
                "mandatory_inverse_writes_at_core_births": mandatory,
                "counts": info,
                "oracle_counts": dict(oracle.counts),
            }
        )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.branch_core_cost_probe",
        "claim_status": "Proved here draft and Measured: this dense backend has cubic work on balanced trees",
        "scope": "Representation-specific accounting, not a lower bound for local solvers or OP3",
        "arithmetic": "exact fractions",
        "graph": "unweighted complete binary tree",
        "seed": 0,
        "random_seed": None,
        "stopping_rule": "scalar flux publication and original-degree ACL gate of branch_core_flux",
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
            Path(__file__).with_name("branch_core_flux.py").read_bytes()
        ).hexdigest(),
        "elapsed_seconds_including_audit": round(time.time() - started, 3),
    }
    output = repo / "manuscript/notes/incremental_active_set_sdd/BRANCH_CORE_COST_AUDIT.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
