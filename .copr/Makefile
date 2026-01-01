srpm:
	mkdir -p $(outdir)
	# Create a clean snapshot from the git commit (avoids "file changed" errors)
	git archive --format=tar.gz --prefix=FreeCAD-1.0.2/ -o $(outdir)/freecad-sources.tar.gz HEAD
	
	# Build the SRPM
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
