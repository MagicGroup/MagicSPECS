Summary: Xt / Motif OpenGL widgets
Name: mesa-libGLw
Version: 8.0.0
Release: 3%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: ftp://ftp.freedesktop.org/pub/mesa/glw/glw-%{version}.tar.bz2

BuildRequires: libXt-devel
BuildRequires: libGL-devel
%if 0%{?rhel}
BuildRequires: openmotif-devel
%else
BuildRequires: lesstif-devel
%endif

Provides: libGLw

%description
Mesa libGLw runtime library.

%package devel
Summary: Mesa libGLw development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libGL-devel
%if 0%{?rhel}
Requires: openmotif-devel
%else
Requires: lesstif-devel
%endif
Provides: libGLw-devel

%description devel
Mesa libGLw development package.

%prep
%setup -q -n glw-%{version}

%build
%configure --disable-static --enable-motif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libGLw.so.1
%{_libdir}/libGLw.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libGLw.so
%{_libdir}/pkgconfig/glw.pc
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 8.0.0-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 8.0.0-2
- 为 Magic 3.0 重建

* Mon Sep 10 2012 Adam Jackson <ajax@redhat.com> 8.0.0-1
- Switch to upstream's split-out glw release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Bill Nottingham - 6.5.1-12
- fix prior macros

* Thu Jul 05 2012 Bill Nottingham - 6.5.1-11
- add conditional macros for openmotif/lesstif

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.5.1-6
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.5.1-5
- Autorebuild for GCC 4.3

* Fri Oct 12 2007 Matthias Clasen <mclasen@redhat.com> - 6.5.1-4
- Fix spec file syntax issues  (#330331)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 6.5.1-3
- Rebuild for build id

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 6.5.1-2
- Minor spec fixes (#210798)

* Fri Sep 29 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-1
- lib64 fixes and cleanups from Patrice Dumas (#188974)

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-0.2
- Use 6.5.1 release tarball.  Drop patches and build scripts that are no
  longer necessary.

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-0.1
- Move revision back up to 6.5.1 for upgrade path from FC5.  Misc other
  spec fixes as per bug #188974 comment 30.

* Mon Sep 18 2006 Adam Jackson <ajackson@redhat.com> 1.0-4
- Rename back to mesa-libGLw as per bug #188974.

* Wed Aug 30 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-3
- Fix package for x86_64

* Tue Aug 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-2
- Fix package to depend on lesstif-devel
- -devel now Requires libGL-devel
- use name var in -devel Requires
- actually use RPM_OPT_FLAGS
- symlink devel libs, not copy (except for .*.*.*)

* Fri Aug  7 2006 Adam Jackson <ajackson@redhat.com> 1.0-1
- Split libGLw out from Mesa.
