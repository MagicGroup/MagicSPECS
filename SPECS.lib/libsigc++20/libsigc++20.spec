# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsigc++20
Version:	2.3.1
Release: 1%{?dist}
Summary:        Typesafe signal framework for C++
Summary(zh_CN.UTF-8): C++ 的类型安全信号框架

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://libsigc.sourceforge.net/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{release_version}/libsigc++-%{version}.tar.xz

BuildRequires:  m4

%description
This library implements a full callback system for use in widget libraries,
abstract interfaces, and general programming. Originally part of the Gtk--
widget set, libsigc++20 is now a separate library to provide for more general
use. It is the most complete library of its kind with the ability to connect
an abstract callback to a class method, function, or function object. It
contains adaptor classes for connection of dissimilar callbacks and has an
ease of use unmatched by other C++ callback libraries.

Package GTK-- (gtkmm), which is a C++ binding to the GTK+ library,
starting with version 1.1.2, uses libsigc++20.

%description -l zh_CN.UTF-8
C++ 的类型安全信号框架。

%package devel
Summary:        Development tools for the typesafe signal framework for C++
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the static libraries and header files
needed for development with %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Documentation for %{name}, includes full API docs
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n libsigc++-%{version}


%build
%configure %{!?_with_static: --disable-static}
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README NEWS ChangeLog TODO
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/sigc++-2.0/
%{_libdir}/pkgconfig/*.pc
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so

%files doc
%doc %{_datadir}/doc/libsigc++-2.0/
# according guidelines, we can co-own this, since devhelp is not required
# for accessing documentation
%doc %{_datadir}/devhelp/


%changelog
* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 2.3.1-1
- 更新到 2.3.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.2.11-2
- 为 Magic 3.0 重建

* Sun Sep 23 2012 Kalev Lember <kalevlember@gmail.com> - 2.2.11-1
- Update to 2.2.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Kalev Lember <kalevlember@gmail.com> - 2.2.10-1
- Update to 2.2.10
- Cleaned up the spec file for modern rpmbuild

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.9-1
- Update to 2.2.9
- Dropped upstreamed libsigc++20-gcc46.patch

* Tue Mar 01 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.8-4
- Spec cleanup
- Use macro for automatically calculating ftp directory name with
  first two digits of tarball version.
- Dropped R: pkgconfig from -devel as it's now automatically added by rpm
- Own /usr/share/doc/libsigc++-2.0/ dir and mark /usr/share/devhelp/ as %%doc
- Require base package from -doc subpackage
- Drop unneeded doxygen and graphviz BRs

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.8-3
- fix documentation location (RHBZ #678981)
- co-own /usr/share/devhelp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.8-1
- upstream 2.2.8
- fix compilation against GCC 4.6 (GNOME BZ #641471)

* Tue Sep  8 2009 Denis Leroy <denis@poolshark.org> - 2.2.4.2-1
- Update to upstream version 2.2.4.2

* Sat Aug 29 2009 Denis Leroy <denis@poolshark.org> - 2.2.4.1-1
- Update to upstream 2.2.4.1
- Added devhelp book and necessary BRs
- Split documentation into new subpackage
- Moved documentation to gtk-doc dir

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.2.2-2
- Rebuild for pkgconfig provides

* Tue Mar 11 2008 Denis Leroy <denis@poolshark.org> - 2.2.2-1
- Update to upstream 2.2.2 version

* Sun Feb 24 2008 Denis Leroy <denis@poolshark.org> - 2.2.0-1
- Update to 2.2.0
- gcc 4.3 patch upstreamed

* Thu Feb  7 2008 Lubomir Kundrak <lkundrak@redhat.com> 2.0.18-3
- Rebuild with gcc4.3

* Thu Jan  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.18-2
- add test case for gcc4.3 failure conditional

* Fri Sep 14 2007 Denis Leroy <denis@poolshark.org> - 2.0.18-1
- Update to 2.0.18

* Fri Aug 10 2007 Denis Leroy <denis@poolshark.org> - 2.0.17-3
- Updated License tag as per new guidelines

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-2
- FE6 Rebuild

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-1
- Upgrade to version 2.0.17
- Added optional macro to compile static libs (use '--with static')

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-2
- Disabled static libraries
- Was missing copy of GPL licence

* Sun Sep 18 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-1
- Upgrade to version 2.0.16

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.0.11-1
- Upgrade to version 2.0.11

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 15 2005 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0:2.0.6-1
- Update to 2.0.6

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.0.3-0.fdr.1
- Update to 2.0.3
- Merged deps from FC2 sigc++ 1.2.5 spec
- Moved docs to regular directory

* Sat Apr 15 2000 Dmitry V. Levin <ldv@fandra.org>
- updated Url and Source fileds
- 1.0.0 stable release

* Sat Jan 22 2000 Dmitry V. Levin <ldv@fandra.org>
- filtering out -fno-rtti and -fno-exceptions options from $RPM_OPT_FLAGS
- minor install section cleanup

* Wed Jan 19 2000 Allan Rae <rae@lyx.org>
- autogen just creates configure, not runs it, so cleaned that up too.

* Wed Jan 19 2000 Dmitry V. Levin <ldv@fandra.org>
- minor attr fix
- removed unnecessary curly braces
- fixed Herbert's adjustement

* Sat Jan 15 2000 Dmitry V. Levin <ldv@fandra.org>
- minor package dependence fix

* Sat Dec 25 1999 Herbert Valerio Riedel <hvr@gnu.org>
- fixed typo of mine
- added traditional CUSTOM_RELEASE stuff
- added SMP support

* Thu Dec 23 1999 Herbert Valerio Riedel <hvr@gnu.org>
- adjusted spec file to get tests.Makefile and examples.Makefile from scripts/

* Fri Oct 22 1999 Dmitry V. Levin <ldv@fandra.org>
- split into three packages: libsigc++, libsigc++-devel and libsigc++-examples

* Thu Aug 12 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- updated source field and merged conflicts between revisions.

* Tue Aug 10 1999 Dmitry V. Levin <ldv@fandra.org>
- updated Prefix and BuildRoot fields

* Thu Aug  5 1999 Herbert Valerio Riedel <hvr@hvrlab.dhs.org>
- made sure configure works on all alphas

* Wed Jul  7 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Added autoconf macro for sigc.

* Fri Jun 11 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Made into a .in to keep version field up to date
- Still need to do release by hand

* Mon Jun  7 1999 Dmitry V. Levin <ldv@fandra.org>
- added Vendor and Packager fields

* Sat Jun  5 1999 Dmitry V. Levin <ldv@fandra.org>
- updated to 0.8.0

* Tue Jun  1 1999 Dmitry V. Levin <ldv@fandra.org>
- initial revision
