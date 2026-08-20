.PHONY: test lint paper notes note-audit note-report note-targets note-graph experiments full-experiments eps-sweep omega-sweep figures reproduce clean

paper:
	$(MAKE) -C manuscript

notes: note-audit
	$(MAKE) -C manuscript notes

note-audit:
	uv run python manuscript/notes/tools/note_inventory.py check

note-report:
	uv run python manuscript/notes/tools/note_inventory.py report --format markdown

note-targets:
	uv run python manuscript/notes/tools/note_inventory.py targets --format markdown

note-graph:
	uv run python manuscript/notes/tools/note_inventory.py graph --format mermaid

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
	$(MAKE) -C manuscript notes-clean
