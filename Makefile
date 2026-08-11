.PHONY: test lint paper experiments full-experiments eps-sweep omega-sweep figures reproduce clean

paper:
	$(MAKE) -C manuscript

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

experiments:
	uv run python -m experiments.smoke_reproduce

full-experiments: eps-sweep omega-sweep

eps-sweep:
	uv run python -m experiments.run_eps_sweep

omega-sweep:
	uv run python -m experiments.run_omega_sweep

figures:
	MPLBACKEND=Agg uv run python -m experiments.generate_figures

reproduce: test lint experiments figures paper

clean:
	$(MAKE) -C manuscript distclean
