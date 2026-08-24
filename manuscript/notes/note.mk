# Common build rules for every standalone research note.

MAIN ?= main
LATEXMK ?= latexmk
LATEXMKFLAGS ?= -pdf -interaction=nonstopmode -halt-on-error -file-line-error
SOURCES := $(MAIN).tex \
           $(wildcard sections/*.tex sections/*/*.tex) \
           $(wildcard *.bib) \
           $(wildcard ../../tex/shared/*.tex)

.PHONY: all pdf clean distclean

all: $(MAIN).pdf

pdf: all

$(MAIN).pdf: $(SOURCES)
	$(LATEXMK) $(LATEXMKFLAGS) $(MAIN).tex

clean:
	$(LATEXMK) -c $(MAIN).tex

distclean:
	$(LATEXMK) -C $(MAIN).tex
