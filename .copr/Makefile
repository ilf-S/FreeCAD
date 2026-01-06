# .copr/Makefile
SHELL := /bin/bash
SPEC   ?= $(spec)
OUTDIR ?= $(outdir)
REPO_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

# prerelease bits without calling git binary during SRPM step
GDATE  := $(shell date -u +%Y%m%d)
GSHORT := $(shell sh -c 'set -e; \
  if [ -f "$(REPO_ROOT)/.git/HEAD" ]; then \
    H="$$(cat "$(REPO_ROOT)/.git/HEAD")"; \
    if printf "%s" "$$H" | grep -q "^ref:"; then \
      R="$${H#ref: }"; \
      cut -c1-9 "$(REPO_ROOT)/.git/$$R" 2>/dev/null || echo unknown; \
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
