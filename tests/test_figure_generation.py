import json

import pytest

from experiments import generate_figures
from src.baselines.appr import APPR_ORDERINGS


def _complete_figure_records():
    records = []
    for alpha in generate_figures.ALPHAS:
        for eps_appr in generate_figures.EPS_VALUES:
            for ordering in APPR_ORDERINGS:
                work = 0.3 / (alpha * eps_appr)
                records.append(
                    {
                        "graph_kind": "star",
                        "alpha": alpha,
                        "eps_appr": eps_appr,
                        "ordering": ordering,
                        "work": work,
                        "scaled_work": alpha * eps_appr * work,
                        "lower_bound_applies": True,
                        "code_version": "test-version",
                    }
                )
    return records


def test_figure_grid_survives_json_round_trip_and_small_float_perturbation():
    records = json.loads(json.dumps(_complete_figure_records()))
    records[0]["alpha"] += 1.0e-15

    indexed = generate_figures.index_star_records(records)

    assert len(indexed) == 112


def test_figure_grid_rejects_missing_and_duplicate_records():
    records = _complete_figure_records()
    with pytest.raises(ValueError, match="missing 1 figure records"):
        generate_figures.index_star_records(records[:-1])

    with pytest.raises(ValueError, match="duplicate figure record"):
        generate_figures.index_star_records([*records, records[0].copy()])
