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

# Flattened single-file source for sharing, arXiv upload, or pasting into a
# model. latexpand inlines every \input (the shared preamble, macro files, and
# the source-aligned problem model) and --expand-bbl embeds the resolved
# bibliography, so the result compiles with no access to manuscript/tex/shared.
#
# The output must not live under manuscript/notes/: the notation tests glob
# notes/**/*.tex and would reject a second \documentclass file and the inlined
# \newcommand declarations. It is written to manuscript/dist/ instead.
NOTE_ID := $(notdir $(CURDIR))
DIST := ../../dist
STANDALONE := $(DIST)/$(NOTE_ID)-standalone.tex

.PHONY: standalone

standalone: $(STANDALONE)

$(STANDALONE): $(MAIN).pdf
	@mkdir -p $(DIST)
	latexpand --expand-bbl $(MAIN).bbl $(MAIN).tex > $@
	@echo "wrote $@"
