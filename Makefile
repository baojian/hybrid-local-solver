.PHONY: test lint paper experiments eps-sweep omega-sweep figures reproduce clean

paper:
	$(MAKE) -C manuscript

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

experiments:
	uv run python experiments/run_convergence.py
	uv run python experiments/run_runtime.py

eps-sweep:
	uv run python -m experiments.run_eps_sweep

omega-sweep:
	uv run python -m experiments.run_omega_sweep

figures:
	uv run python experiments/generate_figures.py

reproduce: test experiments figures paper

clean:
	$(MAKE) -C manuscript distclean
