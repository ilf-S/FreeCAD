# .copr/Makefile
SHELL := /bin/bash
SPEC   ?= $(spec)
OUTDIR ?= $(outdir)
REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

GDATE  := $(shell date -u +%Y%m%d)
GSHORT := $(shell sh -c 'set -e; \
  if [ -f "$(REPO_ROOT)/.git/HEAD" ]; then \
    H="$$(cat "$(REPO_ROOT)/.git/HEAD")"; \
    R="$$(printf "%s" "$$H" | sed -n "s/^ref: //p")"; \
    if [ -n "$$R" ]; then \
      if [ -f "$(REPO_ROOT)/.git/$$R" ]; then \
        cut -c1-9 "$(REPO_ROOT)/.git/$$R"; \
      elif [ -f "$(REPO_ROOT)/.git/packed-refs" ]; then \
        awk "\$$2==\"$$R\"{print substr(\$$1,1,9)}" "$(REPO_ROOT)/.git/packed-refs" | head -n1; \
      else echo unknown; fi; \
    else printf "%s" "$$H" | cut -c1-9; fi; \
  else echo unknown; fi')

.PHONY: srpm make_srpm clean
srpm:
	@test -n "$(SPEC)"   || { echo "ERROR: set spec=<path/to/spec>"; exit 2; }
	@test -n "$(OUTDIR)" || { echo "ERROR: set outdir=<output/dir>"; exit 2; }
	mkdir -p "$(OUTDIR)"
	rm -f "$(OUTDIR)/freecad-sources.tar.gz"
	tar -czf "$(OUTDIR)/freecad-sources.tar.gz" -C "$(REPO_ROOT)" \
		--exclude=.git --exclude=.copr \
		--transform 's|^\./|FreeCAD/|' .
	rpmbuild -bs "$(SPEC)" \
		--define "_sourcedir $(OUTDIR)" \
		--define "_srcrpmdir $(OUTDIR)" \
		--define "gdate $(GDATE)" \
		--define "gshort $(GSHORT)"
	@echo "SRPM written to $(OUTDIR)"

make_srpm: srpm

clean:
	rm -f "$(OUTDIR)"/freecad-*.src.rpm "$(OUTDIR)/freecad-sources.tar.gz"
