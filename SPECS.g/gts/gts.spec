%global snapshot 111025

Name:           gts
Version:        0.7.6
Release:        24.20%{snapshot}%{?dist}
Summary:        GNU Triangulated Surface Library
Summary(zh_CN.UTF-8): GNU 三角曲面库
Group:          Applications/Engineering
Group(zh_CN.UTF-8): 应用程序/工程
License:        LGPLv2+
URL:            http://gts.sourceforge.net/index.html
Source0:        http://gts.sourceforge.net/tarballs/gts-snapshot-%{snapshot}.tar.gz
# Misc accumulated patches
Patch0:         gts-snapshot-111025.patch

BuildRequires:  glib2-devel
BuildRequires:  netpbm-devel

%package devel
Summary:        Development files for gts
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Applications/Engineering
Group(zh_CN.UTF-8): 开发/库
Requires:       pkgconfig
Requires:       glib2-devel
Requires:       %{name} = %{version}-%{release}

%description
GTS provides a set of useful functions to deal with 3D surfaces meshed
with interconnected triangles including collision detection,
multiresolution models, constrained Delaunay triangulations and robust
set operations (union, intersection, differences).

%description -l zh_CN.UTF-8
GNU 三角曲面库。

%description devel
This package contains the gts header files and libs.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n %{name}-snapshot-%{snapshot}
%patch0 -p1

# Fix broken permissions
chmod +x test/*/*.sh

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# File names are too general, rename ...
mv -f $RPM_BUILD_ROOT%{_bindir}/delaunay $RPM_BUILD_ROOT%{_bindir}/gtsdelaunay 
mv -f $RPM_BUILD_ROOT%{_bindir}/happrox $RPM_BUILD_ROOT%{_bindir}/gtshapprox
mv -f $RPM_BUILD_ROOT%{_bindir}/transform $RPM_BUILD_ROOT%{_bindir}/gtstransform
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/delaunay.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtsdelaunay.1 
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/happrox.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtshapprox.1
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/transform.1 $RPM_BUILD_ROOT%{_mandir}/man1/gtstransform.1
magic_rpm_clean.sh

%check
# Urgh, something is very broken with gts rsp. its testsuite
make check ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/gtsdelaunay
%{_bindir}/gts2dxf
%{_bindir}/gts2oogl
%{_bindir}/gts2stl
%{_bindir}/gtscheck
%{_bindir}/gtscompare
%{_bindir}/gtstemplate
%{_bindir}/gtshapprox
%{_bindir}/stl2gts
%{_bindir}/gtstransform
%{_libdir}/*.so.*
%{_mandir}/man1/gtsdelaunay.1*
%{_mandir}/man1/gts2dxf.1*
%{_mandir}/man1/gts2oogl.1*
%{_mandir}/man1/gts2stl.1*
%{_mandir}/man1/gtscheck.1*
%{_mandir}/man1/gtscompare.1*
%{_mandir}/man1/gtstemplate.1*
%{_mandir}/man1/gtshapprox.1*
%{_mandir}/man1/stl2gts.1*
%{_mandir}/man1/gtstransform.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/gts-config
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_mandir}/man1/gts-config.1*

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 0.7.6-24.20111025
- 为 Magic 3.0 重建

* Mon Apr 14 2014 Liu Di <liudidi@gmail.com> - 0.7.6-23.20111025
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.7.6-22.20111025
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-21.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-20.20111025
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.7.6-19.20111025
- Update to new upstream snapshot
- Rebase patches.
- Spec file cleanup.

* Wed Nov 16 2011 Jindrich Novy <jnovy@redhat.com> - 0.7.6-16
- rebuild against new netpbm

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun  1 2010 Dan Horák <dan[at]danny.cz> - 0.7.6-14
- fix include path for pgm.h (#538971)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-11
- Let *-devel Require: glib2-devel (BZ: 457099).
- Pass LIBS=-lm to %%configure (avoid non-weak refs to libm).
- Add gts-0.7.6-hacks.diff (Various configuration fixes).
- Add gts-0.7.6-autotools.diff (regenerate autotool-generated files).
- Add %%check.

* Fri May 23 2008 Jon Stanley <jonstanley@gmail.com> - 0.7.6-10
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.6-9
- Autorebuild for GCC 4.3

* Sun Oct 21 2007 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-8
- Address BZ 341431:
  - Rework gts-config.
  - Rework gts.pc.
  - Regenerate gts-0.7.6-pkg_config.diff.

* Tue Aug 28 2007 Ed Hill <ed@eh3.com> - 0.7.6-7
- rebuild for BuildID

* Fri Sep  1 2006 Ed Hill <ed@eh3.com> - 0.7.6-6
- rebuild for imminent FC-6 release

* Mon May 22 2006 Ralf Corsépius <rc040203@freenet.de> - 0.7.6-5
- BR: netpbm-devel (Required to build happrox).
- Add --disable-dependency-tracking.

* Sun May 21 2006 Ed Hill <ed@eh3.com> - 0.7.6-4
- add gts-config patch

* Sun May 21 2006 Ed Hill <ed@eh3.com> - 0.7.6-3
- add Ralf's includedir patch

* Fri May 19 2006 Ed Hill <ed@eh3.com> - 0.7.6-2
- fix FE review items provided by Ralf Corsepius

* Thu May 18 2006 Ed Hill <ed@eh3.com> - 0.7.6-1
- initial package creation

