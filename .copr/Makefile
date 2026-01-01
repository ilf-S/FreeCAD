srpm:
	# 1. Create a neutral temp directory to avoid the "file changed" race condition
	mkdir -p /tmp/fc_build/FreeCAD-1.0.2
	
	# 2. Copy the files to the temp location
	cp -rp . /tmp/fc_build/FreeCAD-1.0.2/
	
	# 3. Clean up the copy (remove .git)
	rm -rf /tmp/fc_build/FreeCAD-1.0.2/.git
	
	# 4. Create the tarball from the static copy
	mkdir -p $(outdir)
	tar -czf $(outdir)/freecad-sources.tar.gz -C /tmp/fc_build FreeCAD-1.0.2
	
	# 5. Clean up
	rm -rf /tmp/fc_build
	
	# 6. Build the SRPM using the newly created tarball
	rpmbuild -bs \
		--define "_sourcedir $(outdir)" \
		--define "_srcrpmdir $(outdir)" \
		$(spec)
