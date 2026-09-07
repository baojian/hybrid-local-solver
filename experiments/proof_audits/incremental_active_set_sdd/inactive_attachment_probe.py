"""Full attachment classification can read an arbitrarily large inactive star.

This is a scoped implementation witness. An initial gate check avoids it.
"""

from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess

from bounded_attachment_cycle import LocalOracle, local_bounded_cycle
from local_sun_solver import check_solution
import networkx as nx


def main():
    rows = []
    alpha, lam = F(1, 3), F(1, 10)
    for q in [4, 16, 64, 256]:
        graph = nx.cycle_graph(3)
        graph.add_edge(0, 3)
        graph.add_edges_from((3, i) for i in range(4, q + 3))
        oracle = LocalOracle(graph)
        answer, info = local_bounded_cycle(oracle, 0, alpha, lam)
        assert answer == {0: F(7, 30)}
        check_solution(graph, 0, alpha, lam, answer)
        assert oracle.counts["row_exposures"] >= q
        rows.append(
            {
                "attachment_vertices": q,
                "ambient_vertices": len(graph),
                "support_volume": 3,
                "answer": {str(i): str(x) for i, x in answer.items()},
                "counts": dict(oracle.counts),
                "info": info,
            }
        )
    repo = Path(__file__).resolve().parents[3]
    payload = {
        "audit": "incremental_active_set_sdd.inactive_attachment_probe",
        "claim_status": "Refuted: full classification has uniform support-local work",
        "limitation": "Specific implementation witness; initial gate check avoids this family",
        "arithmetic": "exact fractions; separate full-graph KKT audit",
        "alpha_lazy": str(alpha),
        "gamma": "1/2",
        "lambda": str(lam),
        "seed": 0,
        "random_seed": None,
        "stopping_rule": "exact source-derivative zero and obstacle KKT",
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
        "solver_sha256": hashlib.sha256(
            Path(__file__).with_name("bounded_attachment_cycle.py").read_bytes()
        ).hexdigest(),
    }
    output = repo / "results/raw/op3_inactive_attachment_probe.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
