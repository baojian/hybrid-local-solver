MAIN := main
LATEXMK := latexmk

.PHONY: all clean

all:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

clean:
	$(LATEXMK) -C $(MAIN).tex

