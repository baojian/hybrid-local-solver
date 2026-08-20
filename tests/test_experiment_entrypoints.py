from experiments import (
    check_appr_lower_bound,
    explore_geometric_envelope_obstruction,
    explore_evolving_cg,
    explore_response_hybrid,
    generate_figures,
    run_eps_sweep,
    run_omega_sweep,
    smoke_reproduce,
)


def test_experiment_modules_import_without_running():
    assert callable(check_appr_lower_bound.main)
    assert callable(explore_geometric_envelope_obstruction.main)
    assert callable(explore_evolving_cg.main)
    assert callable(explore_response_hybrid.main)
    assert callable(generate_figures.main)
    assert callable(run_eps_sweep.main)
    assert callable(run_omega_sweep.main)
    assert callable(smoke_reproduce.main)
