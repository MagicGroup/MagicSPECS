%global gitdate 20151203
%global gitcommit f941f6b60dea9bb446b97985a9afb6b1b839e81f
%global shortcommit %(c=%{gitcommit}; echo ${c:0:7})
%global xdriinfo xdriinfo-1.0.4
%global demodir %{_libdir}/mesa

Summary: Mesa demos
Name: mesa-demos
Version: 8.3.0
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: ftp://ftp.freedesktop.org/pub/mesa/demos/%{version}/%{name}-%{version}.tar.bz2
#Source0: mesa-demos-%{gitdate}.tar.bz2
Source1: http://www.x.org/pub/individual/app/%{xdriinfo}.tar.bz2
Source2: mesad-git-snapshot.sh
# Patch pointblast/spriteblast out of the Makefile for legal reasons
Patch0: mesa-demos-8.0.1-legal.patch
Patch1: mesa-demos-as-needed.patch
BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: freeglut-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: libGLU-devel
BuildRequires: glew-devel

%description
This package provides some demo applications for testing Mesa.

%package -n glx-utils
Summary: GLX utilities
Group: Development/Libraries
Provides: glxinfo glxinfo%{?__isa_bits}

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.

%package -n egl-utils
Summary: EGL utilities
Group: Development/Libraries
Provides: eglinfo es2_info

%description -n egl-utils
The egl-utils package provides the eglinfo and es2_info utilities.

%prep
%setup -q -n %{name}-%{version} -b1
%patch0 -p1 -b .legal
%patch1 -p1 -b .asneeded

# These two files are distributable, but non-free (lack of permission to modify).
rm -rf src/demos/pointblast.c
rm -rf src/demos/spriteblast.c

%build
autoreconf -vfi
%configure --bindir=%{demodir} --with-system-data-files
make %{?_smp_mflags}

pushd ../%{xdriinfo}
%configure
make %{?_smp_mflags}
popd

%install
make install DESTDIR=%{buildroot}

pushd ../%{xdriinfo}
make %{?_smp_mflags} install DESTDIR=%{buildroot}
popd

install -m 0755 src/xdemos/glxgears %{buildroot}%{_bindir}
install -m 0755 src/xdemos/glxinfo %{buildroot}%{_bindir}
%if 0%{?__isa_bits} != 0
install -m 0755 src/xdemos/glxinfo %{buildroot}%{_bindir}/glxinfo%{?__isa_bits}
%endif

install -m 0755 src/egl/opengl/eglinfo %{buildroot}%{_bindir}
install -m 0755 src/egl/opengles2/es2_info %{buildroot}%{_bindir}

%check

%files
%{demodir}
%{_datadir}/%{name}/

%files -n glx-utils
%{_bindir}/glxinfo*
%{_bindir}/glxgears
%{_bindir}/xdriinfo
%{_datadir}/man/man1/xdriinfo.1*

%files -n egl-utils
%{_bindir}/eglinfo
%{_bindir}/es2_info

%changelog
* Thu Jan 14 2016 Adam Jackson <ajax@redhat.com> - 8.3.0-2
- Rebuild for glew 1.13

* Fri Dec 18 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.3.0-1
- 8.3.0

* Thu Dec 03 2015 Adam Jackson <ajax@redhat.com> 8.2.0-5
- New git snap
- Add EGL/GLES buildreqs and egl-utils subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 8.2.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 05 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 8.2.0-1
- 8.2.0 upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Nov 17 2013 Dave Airlie <airlied@redhat.com> - 8.1.0-5
- rebuilt for glew 1.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com> 8.1.0-3
- Build with --as-needed so glxinfo doesn't needlessly drag in GLEW

* Wed Feb 27 2013 Adam Jackson <ajax@redhat.com> 8.1.0-2
- Copy glxinfo to glxinfo%%{__isa_bits}, to allow people to check that their
  compatibility drivers are working.

* Sun Feb 24 2013 Dave Airlie <airlied@redhat.com> 8.1.0-1
- package upstream demos release 8.1.0 (mainly for new glxinfo)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.1-2.20121218git6eef979
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Tom Callaway <spot@fedoraproject.org> - 8.0.1-1.20121218git6eef979
- update to 8.0.1 (git checkout from 20121218)
- update xdriinfo to 1.0.4
- remove non-free files (bz892925)

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 7.10-9.20101028
- Rebuild for glew 1.9.0

* Fri Jul 27 2012 Kalev Lember <kalevlember@gmail.com> - 7.10-8.20101028
- Rebuilt for GLEW soname bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-7.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-6.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 ajax@redhat.com - 7.10-5.20101028
- Rebuild for new glew soname

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-4.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Adam Jackson <ajax@redhat.com> 7.10-3.20101028
- Install rgba images too (#640688)

* Sat Oct 30 2010 Dave Airlie <airlied@redhat.com> 7.10-2.20101028
- fix install of gears/info (#647947)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 7.10-1.20101028
- Today's git snapshot
- Arbitrary EVR bump to be newer than when the mesa source package dropped
  the demos subpackage.

* Tue Jun 15 2010 Jerome Glisse <jglisse@redhat.com> 7.7
- Initial build.
