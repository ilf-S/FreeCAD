srpm:
	mkdir -p $(outdir)
	# Force tar to finish even if it grumbles about file timestamps
	tar -cz --exclude-vcs --transform 's|^\.|FreeCAD-1.0.2|' -f $(outdir)/freecad-sources.tar.gz . || :
	
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
