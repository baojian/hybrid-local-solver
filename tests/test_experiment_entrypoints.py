from experiments import check_appr_lower_bound, generate_figures, run_eps_sweep, run_omega_sweep


def test_experiment_modules_import_without_running():
    assert callable(check_appr_lower_bound.main)
    assert callable(generate_figures.main)
    assert callable(run_eps_sweep.main)
    assert callable(run_omega_sweep.main)
