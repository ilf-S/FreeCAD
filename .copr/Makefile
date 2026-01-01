srpm:
	# Create the tarball the spec expects
	# We use 'freecad-sources' as the folder name inside the tar
	tar -czf freecad-sources.tar.gz --exclude=.git --transform 's|^\.|freecad-sources|' -C .. FreeCAD
	
	# Move it to the result directory where rpmbuild will look
	mkdir -p $(outdir)
	cp freecad-sources.tar.gz $(outdir)/
	
	# Build the SRPM
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
