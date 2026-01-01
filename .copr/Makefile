srpm:
	mkdir -p $(outdir)
	# Copy to a static temp dir so tar doesn't complain about changing files
	rm -rf /tmp/fc-src
	mkdir -p /tmp/fc-src/FreeCAD-1.0.2
	cp -a . /tmp/fc-src/FreeCAD-1.0.2/
	
	# Create the tarball from the static copy
	tar -czf $(outdir)/freecad-sources.tar.gz -C /tmp/fc-src FreeCAD-1.0.2
	
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
