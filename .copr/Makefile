srpm:
	mkdir -p $(outdir)
	# Find the root directory relative to this Makefile's location
	$(eval REPO_ROOT := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))/..)
	
	# Archive from the root and wrap in the folder name your %setup expects
	tar -czf $(outdir)/freecad-sources.tar.gz -C $(REPO_ROOT) \
		--exclude=.git \
		--transform 's|^\.|FreeCAD-1.0.2|' .
	
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
