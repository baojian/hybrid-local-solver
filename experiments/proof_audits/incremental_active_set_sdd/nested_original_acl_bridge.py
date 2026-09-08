"""Check saved nested solver outputs against original physical ACL rows."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from local_gap_certificate import RestrictedRows, certificate
import networkx as nx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    note = root / "manuscript/notes/incremental_active_set_sdd"
    graph = nx.Graph([(0, 1), (0, 2), (1, 2), (0, 3)])
    cases, inputs = [], {}
    for name in [
        "NESTED_MIXED_FOREST_SOLVER_AUDIT.json",
        "CERTIFIED_NESTED_FOREST_SOLVER_AUDIT.json",
    ]:
        path = note / name
        inputs[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        data = json.loads(path.read_text())
        script = data["audit"].split(".")[-1] + ".py"
        assert (
            data["source_sha256"]
            == hashlib.sha256(Path(__file__).with_name(script).read_bytes()).hexdigest()
        )
        for case in data["cases"]:
            if case.get("physical_result") is None:
                continue
            seed, alpha, eps = case["physical_seed"], F(case["alpha"]), F(case["eps_appr"])
            bar = 2 * alpha / (1 + alpha)
            candidate = [min(1 / bar, max(F(0), F(x))) for x in case["physical_result"]]
            sparse = [(i, x) for i, x in enumerate(candidate) if x > 0]
            oracle = RestrictedRows(graph, [i for i, _ in sparse])
            cert = certificate(oracle, sparse, seed, alpha, eps)
            # Report a failed certificate honestly; it is not an assertion
            # that the saved output meets an unrequested smaller gap target.
            residuals = None
            if cert["accepted"]:
                repaired = dict(cert["repaired"])
                residuals = [
                    F(i == seed)
                    - graph.degree(i) * repaired.get(i, 0)
                    + (1 - bar) * sum(repaired.get(j, 0) for j in graph[i])
                    for i in graph
                ]
                assert all(0 <= r <= eps * graph.degree(i) for i, r in enumerate(residuals))
            cases.append(
                {
                    "input": name,
                    "profile": case["profile"],
                    "physical_seed": seed,
                    "alpha": str(alpha),
                    "eps_appr": str(eps),
                    "gap_certificate": str(cert["value"]),
                    "accepted": cert["accepted"],
                    "original_residuals": None
                    if residuals is None
                    else [str(r) for r in residuals],
                    "certificate_counts": cert["counts"],
                    "original_access_counts": dict(oracle.counts),
                }
            )
    result = {
        "audit": "incremental_active_set_sdd.nested_original_acl_bridge",
        "arithmetic": "exact fractions",
        "scope": "Post-validation of saved supplied numerical outputs, including original graph access and clipping; no new solver invocation or local discovery",
        "cases": cases,
        "input_sha256": inputs,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "backend_sha256": {
            "local_gap_certificate.py": hashlib.sha256(
                Path(__file__).with_name("local_gap_certificate.py").read_bytes()
            ).hexdigest()
        },
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
