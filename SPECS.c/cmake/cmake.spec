# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_with bootstrap
# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui
# Set to RC version if building RC, else %{nil}
%define rcver %{nil}

Name:           cmake
Version:        2.8.9
Release:        2%{?dist}
Summary:        Cross-platform make system

Group:          Development/Tools
# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT 
# Source/kwsys/MD5.c is zlib 
# some GPL-licensed bison-generated files, these all include an exception granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            http://www.cmake.org
Source0:        http://www.cmake.org/files/v2.8/cmake-%{version}%{?rcver}.tar.gz
Source2:        macros.cmake
# Patch to find DCMTK in Fedora (bug #720140)
Patch0:         cmake-dcmtk.patch
# (modified) Upstream patch to fix setting PKG_CONFIG_FOUND (bug #812188)
Patch1:         cmake-pkgconfig.patch
# Patch to fix RindRuby vendor settings
# http://public.kitware.com/Bug/view.php?id=12965
# https://bugzilla.redhat.com/show_bug.cgi?id=822796
Patch2:         cmake-findruby.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran
BuildRequires:  ncurses-devel, libX11-devel
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  libarchive-devel
BuildRequires:  zlib-devel
BuildRequires:  emacs
%if %{without bootstrap}
#BuildRequires: xmlrpc-c-devel
%endif
%if %{with gui}
BuildRequires: qt4-devel, desktop-file-utils
%define qt_gui --qt-gui
%endif

Requires:       rpm

Requires: emacs-filesystem >= %{_emacs_version}

# Source/kwsys/MD5.c
# see https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(md5-deutsch)

%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.


%package        gui
Summary:        Qt GUI for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    gui
The %{name}-gui package contains the Qt based GUI for CMake.


%prep
%setup -q -n %{name}-%{version}%{?rcver}
%patch0 -p1 -b .dcmtk
#%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .findruby


%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
mkdir build
pushd build
../bootstrap --prefix=%{_prefix} --datadir=/share/%{name} \
             --docdir=/share/doc/%{name}-%{version} --mandir=/share/man \
             --%{?with_bootstrap:no-}system-libs \
             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
             %{?qt_gui}
make VERBOSE=1 %{?_smp_mflags}


%install
pushd build
make install DESTDIR=%{buildroot}
find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x
popd
cp -a Example %{buildroot}%{_docdir}/%{name}-%{version}/
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{name}
install -m 0644 Docs/cmake-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/%{name}/cmake-mode.el
# RPM macros
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" %{buildroot}%{_sysconfdir}/rpm/macros.cmake
touch -r %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.cmake
mkdir -p %{buildroot}%{_libdir}/%{name}

%if %{with gui}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}/%{_datadir}/applications/CMake.desktop
%endif
magic_rpm_clean.sh

%if 0%{?with_test}
%check
unset DISPLAY
pushd build
#ModuleNotices fails for some unknown reason, and we don't care
#CMake.HTML currently requires internet access
#CTestTestUpload requires internet access
bin/ctest -V -E ModuleNotices -E CMake.HTML -E CTestTestUpload %{?_smp_mflags}
popd
%endif

%if %{with gui}
%post gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
%endif


%files
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake
%{_docdir}/%{name}-%{version}/
%if %{with gui}
%exclude %{_docdir}/%{name}-%{version}/cmake-gui.*
%endif
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/aclocal/cmake.m4
%{_datadir}/%{name}/
%{_mandir}/man1/ccmake.1.gz
%{_mandir}/man1/cmake.1.gz
%{_mandir}/man1/cmakecommands.1.gz
%{_mandir}/man1/cmakecompat.1.gz
%{_mandir}/man1/cmakemodules.1.gz
%{_mandir}/man1/cmakepolicies.1.gz
%{_mandir}/man1/cmakeprops.1.gz
%{_mandir}/man1/cmakevars.1.gz
%{_mandir}/man1/cpack.1.gz
%{_mandir}/man1/ctest.1.gz
%{_emacs_sitelispdir}/%{name}
%{_libdir}/%{name}/

%if %{with gui}
%files gui
%{_docdir}/%{name}-%{version}/cmake-gui.*
%{_bindir}/cmake-gui
%{_datadir}/applications/CMake.desktop
%{_datadir}/mime/packages/cmakecache.xml
%{_datadir}/pixmaps/CMakeSetup32.png
%{_mandir}/man1/cmake-gui.1.gz
%endif


%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.8.9-2
- 为 Magic 3.0 重建


