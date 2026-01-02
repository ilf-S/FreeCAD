# .copr/Makefile
# Expects COPR to pass: spec=<path/to/.spec> and outdir=<output/dir>
# Creates Source0 (freecad-sources.tar.gz) with top dir "FreeCAD" and builds SRPM.

SHELL := /bin/bash
SPEC   ?= $(spec)
OUTDIR ?= $(outdir)
REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

.PHONY: srpm make_srpm clean

srpm:
	@test -n "$(SPEC)"   || { echo "ERROR: set spec=<path/to/spec>"; exit 2; }
	@test -n "$(OUTDIR)" || { echo "ERROR: set outdir=<output/dir>"; exit 2; }
	mkdir -p "$(OUTDIR)"
	git -C "$(REPO_ROOT)" submodule update --init --recursive
	rm -f "$(OUTDIR)/freecad-sources.tar.gz"
	tar -czf "$(OUTDIR)/freecad-sources.tar.gz" -C "$(REPO_ROOT)" \
		--exclude=.git --exclude=.copr \
		--transform 's|^\./|FreeCAD/|' .
	rpmbuild -bs "$(SPEC)" \
		--define "_sourcedir $(OUTDIR)" \
		--define "_srcrpmdir $(OUTDIR)"
	@echo "SRPM written to $(OUTDIR)"

# COPR sometimes calls make_srpm; keep it as an alias.
make_srpm: srpm

clean:
	rm -f "$(OUTDIR)"/freecad-*.src.rpm "$(OUTDIR)/freecad-sources.tar.gz"
