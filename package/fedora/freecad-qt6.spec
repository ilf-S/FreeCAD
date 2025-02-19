# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_3
%global py_bytecompile 1

# Setup python target for shiboken so the right cmake file is imported.
%global py_suffix %(%{__python3} -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")

# Maintainers:  keep this list of plugins up to date
# List plugins in %%{_libdir}/%{name}/lib, less '.so' and 'Gui.so', here
%global plugins Fem FreeCAD PathApp Import Inspection Mesh MeshPart Part Points ReverseEngineering Robot Sketcher Start Web PartDesignGui _PartDesign Path PathGui Spreadsheet SpreadsheetGui area DraftUtils DraftUtils libDriver libDriverDAT libDriverSTL libDriverUNV libE57Format libOndselSolver libMEFISTO2 libSMDS libSMESH libSMESHDS libStdMeshers libNETGENPlugin Measure TechDraw TechDrawGui libarea-native Surface SurfaceGui AssemblyGui flatmesh QtUnitGui PathSimulator MatGui Material Materials AssemblyApp CAMSimulator


# Some configuration options for other environments
# rpmbuild --with=bundled_zipios:  use bundled version of zipios++
%global bundled_zipios %{?_with_bundled_zipios: 1} %{?!_with_bundled_zipios: 1}
# rpmbuild --without=bundled_pycxx:  don't use bundled version of pycxx
%global bundled_pycxx %{?_without_bundled_pycxx: 0} %{?!_without_bundled_pycxx: 1}
# rpmbuild --without=bundled_smesh:  don't use bundled version of Salome's Mesh
%global bundled_smesh %{?_without_bundled_smesh: 0} %{?!_without_bundled_smesh: 1}


# Prevent RPM from doing its magical 'build' directory for now
%global __cmake_in_source_build 1

# See FreeCAD-main/src/3rdParty/salomesmesh/CMakeLists.txt to find this out.
%global bundled_smesh_version 7.7.1.0

# Some plugins go in the Mod folder instead of lib. Deal with those here:
%global mod_plugins Mod/PartDesign
%define name freecad
%define github_name FreeCAD
%define branch main

Name:           %{name}
Epoch:          1
Version:        1.1
Release:        pre_{{{git_commit_no}}}%{?dist}
Summary:        A general purpose 3D CAD modeler
Group:          Applications/Engineering

License:        LGPLv2+
URL:            http://www.freecadweb.org/
Source0:        https://github.com/%{github_name}/FreeCAD/archive/%{branch}.tar.gz
Source1:        https://github.com/Ondsel-Development/OndselSolver/archive/09d6175a2ba69e7016fcecc4f384946a2f84f92d.tar.gz
Source2:	https://github.com/microsoft/GSL/archive/b39e7e4b0987859f5b19ff7686b149c916588658.tar.gz


# Utilities
BuildRequires:  cmake gcc-c++ gettext dos2unix
BuildRequires:  doxygen swig graphviz
BuildRequires:  gcc-gfortran
BuildRequires:  desktop-file-utils
BuildRequires:  git

BuildRequires:  tbb-devel

# Development Libraries
BuildRequires:  freeimage-devel
BuildRequires:  libXmu-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  opencascade-devel
BuildRequires:  Coin4-devel

BuildRequires:  python3-devel
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pivy
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  eigen3-devel

# Qt6 dependencies
%if 0%{?fedora} > 38

BuildRequires: qt6-qtwebengine-devel
BuildRequires: qt6-qtsvg-devel
BuildRequires: qt6-qttools-devel
BuildRequires: qt6-qttools-static
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-linguist

%else
# Qt5 deps
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtxmlpatterns-devel
%endif

BuildRequires:  fmt-devel

BuildRequires:	yaml-cpp-devel

BuildRequires:  xerces-c
BuildRequires:  xerces-c-devel
BuildRequires:  libspnav-devel

%if 0%{?fedora} > 38
BuildRequires:  python3-shiboken6-devel
BuildRequires:  python3-pyside6-devel
BuildRequires:  pyside6-tools
%else
BuildRequires:  python3-shiboken2-devel
BuildRequires:  python3-pyside2-devel
BuildRequires:  pyside2-tools
%endif

BuildRequires:  netgen-mesher-devel
BuildRequires:  netgen-mesher-devel-private
BuildRequires:	python3-netgen-mesher

%if ! %{bundled_smesh}
BuildRequires:  smesh-devel
%endif

BuildRequires:	netgen-mesher-devel

%if ! %{bundled_zipios}
BuildRequires:  zipios++-devel
%endif

%if ! %{bundled_pycxx}
BuildRequires:  python3-pycxx-devel
%endif

BuildRequires:  libicu-devel
BuildRequires:  vtk-devel
BuildRequires:  openmpi-devel
BuildRequires:  med-devel
BuildRequires:  libkdtree++-devel

BuildRequires:  pcl-devel
BuildRequires:  python3
BuildRequires:  libglvnd-devel
#BuildRequires:  zlib-devel

# For appdata
%if 0%{?fedora}
BuildRequires:  libappstream-glib
%endif

# Packages separated because they are noarch, but not optional so require them
# here.
Requires:       %{name}-data = %{epoch}:%{version}-%{release}
# Obsolete old doc package since it's required for functionality.
Obsoletes:      %{name}-doc < 0.13-5
Requires:       hicolor-icon-theme

Requires:       fmt

Requires:	yaml-cpp

%if 0%{?fedora} > 38
Requires:       python3-pyside6
%else
Requires:       python3-pyside2
%endif

Requires:       python3-pivy
Requires:       python3-matplotlib
Requires:       python3-collada

%if 0%{?fedora} > 38
Requires:       qt6-assistant
%else
Requires:	qt5-assistant
%endif

%if %{bundled_smesh}
Provides:       bundled(smesh) = %{bundled_smesh_version}
%endif
%if %{bundled_pycxx}
Provides:       bundled(python-pycxx)
%endif
Recommends:     python3-pysolar



# plugins and private shared libs in %%{_libdir}/freecad/lib are private;
# prevent private capabilities being advertised in Provides/Requires
%define plugin_regexp /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d
%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}/lib
%filter_from_requires %{plugin_regexp}
%filter_from_provides %{plugin_regexp}
%filter_provides_in %{_libdir}/%{name}/Mod
%filter_requires_in %{_libdir}/%{name}/Mod
%filter_setup
}

%description
FreeCAD is a general purpose Open Source 3D CAD/MCAD/CAx/CAE/PLM modeler, aimed
directly at mechanical engineering and product design but also fits a wider
range of uses in engineering, such as architecture or other engineering
specialities. It is a feature-based parametric modeler with a modular software
architecture which makes it easy to provide additional functionality without
modifying the core system.


%package data
Summary:        Data files for FreeCAD
BuildArch:      noarch
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description data
Data files for FreeCAD


%prep
%autosetup -p1 -n FreeCAD-%{branch}
gzip -dc /builddir/build/SOURCES/09d6175a2ba69e7016fcecc4f384946a2f84f92d.tar.gz | tar -xvvf - --strip 1  -C src/3rdParty/OndselSolver/
gzip -dc /builddir/build/SOURCES/b39e7e4b0987859f5b19ff7686b149c916588658.tar.gz | tar -xvvf - --strip 1  -C src/3rdParty/GSL/
# Remove bundled pycxx if we're not using it
%if ! %{bundled_pycxx}
rm -rf src/CXX
%endif

%if ! %{bundled_zipios}
rm -rf src/zipios++
#sed -i "s/zipios-config.h/zipios-config.hpp/g" \
#    src/Base/Reader.cpp src/Base/Writer.h
%endif

# Fix encodings
dos2unix -k src/Mod/Test/unittestgui.py

#            data/License.txt \
#            ChangeLog.txt \

# Removed bundled libraries


%build
rm -rf build && mkdir build && cd build

# Deal with cmake projects that tend to link excessively.
CXXFLAGS='-Wno-error=cast-function-type -Wdeprecated-declarations'; export CXXFLAGS
LDFLAGS='-Wl,--as-needed -Wl,--no-undefined'; export LDFLAGS

%define MEDFILE_INCLUDE_DIRS %{_includedir}/med/

#  -DFREECAD_USE_PCL=TRUE \

%cmake \
       -DCMAKE_INSTALL_PREFIX=%{_libdir}/%{name} \
       -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
       -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
       -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
       -DRESOURCEDIR=%{_datadir}/%{name} \
       -DFREECAD_USE_EXTERNAL_PIVY=TRUE \
       -DPYTHON_SUFFIX=.%{py_suffix} \
       -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 \
       -DMEDFILE_INCLUDE_DIRS=%{MEDFILE_INCLUDE_DIRS} \
       -DOpenGL_GL_PREFERENCE=GLVND \
       -DCOIN3D_INCLUDE_DIR=%{_includedir}/Coin4 \
       -DCOIN3D_DOC_PATH=%{_docdir}/Coin4 \
       -DUSE_OCC=TRUE \
%if 0%{?fedora} > 38
	-DFREECAD_QT_VERSION:STRING=6 \
	-DPYSIDE_INCLUDE_DIR=/usr/include/PySide6 \
	-DPYSIDE_LIBRARY=-lpyside6.%{py_suffix} \
	-DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken6 \
	-DSHIBOKEN_LIBRARY=-lshiboken6.%{py_suffix} \
	-DGCC_COLORS= \
%else
       -DBUILD_QT5=ON \
	   -DFREECAD_QT_VERSION=5 \
       -DSHIBOKEN_INCLUDE_DIR=%{_includedir}/shiboken2 \
       -DSHIBOKEN_LIBRARY=-lshiboken2.%{py_suffix} \
       -DPYSIDE_INCLUDE_DIR=/usr/include/PySide2 \
       -DPYSIDE_LIBRARY=-lpyside2.%{py_suffix} \
%endif
%if ! %{bundled_smesh}
       -DFREECAD_USE_EXTERNAL_SMESH=TRUE \
       -DSMESH_FOUND=TRUE \
       -DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
       -DSMESH_DIR=`pwd`/../cMake \
%endif
	-DBUILD_FEM_NETGEN=TRUE \
%if ! %{bundled_zipios}
       -DFREECAD_USE_EXTERNAL_ZIPIOS=TRUE \
%endif
%if ! %{bundled_pycxx}
       -DPYCXX_INCLUDE_DIR=$(pkg-config --variable=includedir PyCXX) \
       -DPYCXX_SOURCE_DIR=$(pkg-config --variable=srcdir PyCXX) \
%endif
       -DPACKAGE_WCREF="%{release} (Git)" \
       -DPACKAGE_WCURL="git://github.com/%{github_name}/FreeCAD.git main" \
       -DENABLE_DEVELOPER_TESTS=FALSE \
	   -DBUILD_GUI=TRUE \
       ../

make fc_version
for I in src/Build/Version.h src/Build/Version.h.out; do
	sed -i 's,FCRevision      \"Unknown\",FCRevision      \"%{release} (Git)\",' $I
	sed -i 's,FCRepositoryURL \"Unknown\",FCRepositoryURL \"git://github.com/FreeCAD/FreeCAD.git main\",' $I
done

%{make_build}

%install
cd build
%make_install

# Symlink binaries to /usr/bin
mkdir -p %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{name}/bin/FreeCAD %{buildroot}%{_bindir}/FreeCAD
ln -s ../%{_lib}/%{name}/bin/FreeCADCmd %{buildroot}%{_bindir}/FreeCADCmd

mkdir %{buildroot}%{_metainfodir}/
mv %{buildroot}%{_libdir}/%{name}/share/metainfo/* %{buildroot}%{_metainfodir}/

mkdir %{buildroot}%{_datadir}/applications/
mv %{buildroot}%{_libdir}/%{name}/share/applications/* %{buildroot}%{_datadir}/applications/


mkdir -p %{buildroot}%{_datadir}/thumbnailers/
mv %{buildroot}%{_libdir}/%{name}/share/thumbnailers/* %{buildroot}%{_datadir}/thumbnailers/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/
mv %{buildroot}%{_libdir}/%{name}/share/icons/hicolor/scalable/* %{buildroot}%{_datadir}/icons/hicolor/scalable/

mkdir -p %{buildroot}%{_datadir}/pixmaps/
mv %{buildroot}%{_libdir}/%{name}/share/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

mkdir -p %{buildroot}%{_datadir}/mime/packages/
mv %{buildroot}%{_libdir}/%{name}/share/mime/packages/* %{buildroot}%{_datadir}/mime/packages/

pushd %{buildroot}%{_libdir}/%{name}/share/
rmdir metainfo/
rmdir applications/
rm -rf mime
rm -rf icons
popd

# Remove obsolete Start_Page.html
rm -f %{buildroot}%{_docdir}/%{name}/Start_Page.html
# Belongs in %%license not %%doc
rm -f %{buildroot}%{_docdir}/freecad/ThirdPartyLibraries.html

# Remove header from external library that's erroneously installed
rm -f %{buildroot}%{_libdir}/%{name}/include/E57Format/E57Export.h
#rm -dfr %{buildroot}%{_includedir}/OndselSolver
#rm -f %{buildroot}%{_libdir}/%{name}/share/pkgconfig/OndselSolver.pc

# Bug maintainers to keep %%{plugins} macro up to date.
#
# Make sure there are no plugins that need to be added to plugins macro
new_plugins=`ls %{buildroot}%{_libdir}/%{name}/%{_lib} | sed -e  '%{plugin_regexp}'`
if [ -n "$new_plugins" ]; then
    echo -e "\n\n\n**** ERROR:\n" \
        "\nPlugins not caught by regexp:  " $new_plugins \
        "\n\nPlugins in %{_libdir}/%{name}/lib do not exist in" \
         "\nspecfile %%{plugins} macro.  Please add these to" \
         "\n%%{plugins} macro at top of specfile and rebuild.\n****\n" 1>&2
    exit 1
fi
# Make sure there are no entries in the plugins macro that don't match plugins
for p in %{plugins}; do
    if [ -z "`ls %{buildroot}%{_libdir}/%{name}/%{_lib}/$p*.so`" ]; then
        set +x
        echo -e "\n\n\n**** ERROR:\n" \
             "\nExtra entry in %%{plugins} macro with no matching plugin:" \
             "'$p'.\n\nPlease remove from %%{plugins} macro at top of" \
             "\nspecfile and rebuild.\n****\n" 1>&2
        exit 1
    fi
done

# Bytecompile Python modules
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/%{name}


%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/org.freecad.FreeCAD.desktop
%{?fedora:appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/*.FreeCAD.metainfo.xml}


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/scalable/apps &>/dev/null || :


%files
##%license data/License.txt
##%doc ChangeLog.txt

%{_bindir}/*
%{_metainfodir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/%{_lib}/
%{_libdir}/%{name}/Ext/
%{_libdir}/%{name}/Mod/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/scalable/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{_datadir}/thumbnailers/*

%{_includedir}/OndselSolver/
%{_libdir}/%{name}/share/pkgconfig/OndselSolver.pc

%{python3_sitelib}/%{name}/*

%files data
%{_datadir}/%{name}/
%{_docdir}/%{name}/LICENSE.html


%changelog
* Sun Sep 29 2024 Iliyan ilf Stoyano <ilf.stoyanov@redacted>
- A bit of clean up

* Sat Mar 9 2024 Iliyan ilf Stoyanov <ilf.stoyanov@redacted>
- Plagarized Michele spec file to attemp a qt6 build on f39
- Modified some paths and sources with edits from my f38 spec file

* Fri Sep 29 2023 Michele Giorato <fedora@mr-miky.com>
- Added missing MatGui.so Material.so to regex

* Thu Sep 28 2023 Michele Giorato <fedora@mr-miky.com>
- Fixed spec file. FreeCAD now require yaml-cpp and yaml-cpp-devel to build it

* Fri Sep 22 2023 Michele Giorato <fedora@mr-miky.com>
-
