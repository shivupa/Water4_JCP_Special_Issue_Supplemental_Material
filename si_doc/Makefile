LATEX=pdflatex
LATEXOPT=--shell-escape

LATEXMK=latexmk
LATEXMKOPT=-pdf

MAIN=si
BIB=si
HEADER=header
MAINDIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

all:
	mkdir -p compile
	cp *.bst compile
	cp $(MAIN).tex compile
	cp $(BIB).bib compile
	cp $(HEADER).tex compile
	if [ -d "compile/images" ]; then cp images/* compile/images; fi
	if [ ! -d "compile/images" ]; then cp -r images compile; fi
	if [ -d "compile/parts" ]; then cp parts/* compile/parts; fi
	if [ ! -d "compile/parts" ]; then cp -r parts compile; fi
	cd compile && \
	$(LATEXMK) $(LATEXMKOPT) $(MAIN).tex
	cp $(MAINDIR)/compile/$(MAIN).pdf $(MAINDIR)
clean:
	rm -rf compile
veryclean:
	rm -rf compile
	rm $(MAIN).pdf
edit:
	$(VISUAL) -p $(MAIN).tex parts/*

.PHONY: clean veryclean all
