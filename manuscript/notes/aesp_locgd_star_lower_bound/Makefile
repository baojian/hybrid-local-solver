# Build the standalone AESP-LocGD star lower-bound note.
MAIN := main
LATEXMK := latexmk
LATEXMKFLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error

.PHONY: all pdf clean distclean

all: $(MAIN).pdf
pdf: all

$(MAIN).pdf: $(MAIN).tex
	$(LATEXMK) $(LATEXMKFLAGS) $(MAIN).tex

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
