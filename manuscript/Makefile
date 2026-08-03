# Build the active manuscript (main.pdf).
#
#   make            # build main.pdf
#   make watch      # rebuild continuously on file changes
#   make view       # build and open the PDF
#   make clean      # remove auxiliary files, keep main.pdf
#   make distclean  # remove auxiliary files and main.pdf
#
# Archived papers under archive/ have their own build commands and are not
# built here.

MAIN      := main
LATEXMK   := latexmk
LATEXMKFLAGS := -pdf -interaction=nonstopmode -halt-on-error -file-line-error
SOURCES   := $(MAIN).tex appendix.tex references.bib \
             $(wildcard sections/*.tex) $(wildcard tex/shared/*.tex) \
             $(wildcard figures/*.pdf) $(wildcard *.sty)

ifeq ($(shell uname -s),Darwin)
OPEN := open
else
OPEN := xdg-open
endif

.PHONY: all pdf watch view clean distclean

all: $(MAIN).pdf

pdf: all

$(MAIN).pdf: $(SOURCES)
	$(LATEXMK) $(LATEXMKFLAGS) $(MAIN).tex

watch:
	$(LATEXMK) $(LATEXMKFLAGS) -pvc $(MAIN).tex

view: $(MAIN).pdf
	$(OPEN) $(MAIN).pdf

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
