from experiments.providers.codex import (
    explore_evolving_cg,
    explore_geometric_envelope_obstruction,
    explore_response_hybrid,
)


def test_codex_experiment_modules_import_without_running():
    assert callable(explore_evolving_cg.main)
    assert callable(explore_geometric_envelope_obstruction.main)
    assert callable(explore_response_hybrid.main)
