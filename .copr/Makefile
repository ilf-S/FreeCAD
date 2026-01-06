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

# Compute prerelease identifiers WITHOUT calling git:
	# gdate: UTC YYYYMMDD; gshort: first 9 chars of HEAD (ref or detached)
	GDATE="$$(date -u +%Y%m%d)"; \
	if [ -f "$(REPO_ROOT)/.git/HEAD" ]; then \
	  HEAD="$$(cat '$(REPO_ROOT)/.git/HEAD')"; \
	  if printf '%s' "$$HEAD" | grep -q '^ref:'; then \
	    REF="$${HEAD#ref: }"; \
	    GSHORT="$$(cut -c1-9 '$(REPO_ROOT)/.git/'"$$REF" 2>/dev/null || echo unknown)"; \
	  else \
	    GSHORT="$$(printf '%s' "$$HEAD" | cut -c1-9)"; \
	  fi; \
	else \
	  GSHORT="unknown"; \
	fi; \
	echo "gdate=$$GDATE gshort=$$GSHORT"

# Create Source0 with topdir "FreeCAD" (matches: %setup -q -n FreeCAD)
	rm -f "$(OUTDIR)/freecad-sources.tar.gz"
	tar -czf "$(OUTDIR)/freecad-sources.tar.gz" -C "$(REPO_ROOT)" \
		--exclude=.git --exclude=.copr \
		--transform 's|^\./|FreeCAD/|' .
	
# Build SRPM and pass our prerelease macros
	rpmbuild -bs "$(SPEC)" \
		--define "_sourcedir $(OUTDIR)" \
		--define "_srcrpmdir $(OUTDIR)" \
		--define "gdate $$GDATE" \
		--define "gshort $$GSHORT"

	@echo "SRPM written to $(OUTDIR)"

# COPR sometimes calls make_srpm; keep it as an alias.
make_srpm: srpm

clean:
	rm -f "$(OUTDIR)"/freecad-*.src.rpm "$(OUTDIR)/freecad-sources.tar.gz"
