.PHONY: test lint paper experiments figures reproduce clean

paper:
	cd manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

experiments:
	uv run python experiments/run_convergence.py
	uv run python experiments/run_runtime.py

figures:
	uv run python experiments/generate_figures.py

reproduce: test experiments figures paper

clean:
	cd manuscript && latexmk -C
