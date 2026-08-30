#!/usr/bin/env python3
"""Audit the saved literal two-stage tables and semantic-error columns."""

import csv
from pathlib import Path

from experiments.two_stage_point_source_aesp_cd.strict_two_stage_summary import main


ROOT = Path(__file__).resolve().parents[3]


def audit_randomized_op2_transfer() -> None:
    path = (
        ROOT
        / "experiments/two_stage_point_source_aesp_cd"
        / "randomized_op2_inner_face_results.csv"
    )
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 67
    assert sum(int(row["omitted_support_vertices"]) > 0 for row in rows) == 4
    assert sum(row["stop"] == "cap" for row in rows) == 4
    for row in rows:
        assert float(row["maximum_certified_residual_ratio"]) <= 1.0 + 1.0e-9
        assert float(row["stage2_certified_residual_ratio"]) <= 1.0 + 1.0e-9
        assert float(row["face_gap_ratio"]) <= 1.0 + 1.0e-6
        assert float(row["direct_semantic_ratio"]) <= 1.0 + 1.0e-6
        assert float(row["stage2_semantic_ratio"]) <= 1.0 + 1.0e-6
    print("randomized OP2 transfer rows audited: 67 (4 strict inner faces)")


if __name__ == "__main__":
    main()
    audit_randomized_op2_transfer()
