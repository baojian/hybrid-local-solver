DOC := hybrid_local_solver_synthesis

.PHONY: all clean

all: $(DOC).pdf

$(DOC).pdf: $(DOC).tex references.bib $(wildcard sections/*.tex)
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(DOC).tex

clean:
	latexmk -C $(DOC).tex
