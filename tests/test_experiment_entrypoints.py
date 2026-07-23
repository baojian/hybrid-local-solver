from experiments import run_eps_sweep, run_omega_sweep


def test_experiment_modules_import_without_running():
    assert callable(run_eps_sweep.main)
    assert callable(run_omega_sweep.main)
