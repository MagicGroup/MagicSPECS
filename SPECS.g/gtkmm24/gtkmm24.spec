# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')
%global tarname gtkmm
%global api_ver 2.4

Name:           gtkmm24
Version:        2.24.4
Release:        5%{?dist}

Summary:        C++ interface for GTK2 (a GUI library for X)
Summary(zh_CN.UTF-8): GTK2 的 C++ 接口

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gtkmm/%{release_version}/gtkmm-%{version}.tar.xz

BuildRequires:  glibmm24-devel >= 2.24
BuildRequires:  atkmm-devel >= 2.22
BuildRequires:  gtk2-devel >= 2.24
BuildRequires:  cairomm-devel >= 1.2.2
BuildRequires:  pangomm-devel >= 2.26


%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance
and a comprehensive set of widget classes that can be freely combined to
quickly create complex user interfaces.

%description -l zh_CN.UTF-8
GTK 2 的 C++ 接口。

%package        devel
Summary:        Headers for developing programs that will use %{name}.
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       glibmm24-devel
Requires:       atkmm-devel
Requires:       pangomm-devel
Requires:       cairomm-devel


%description devel
This package contains the static libraries and header files needed for
developing gtkmm applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        docs
Summary:        Documentation for %{name}, includes full API docs
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm24-doc

%description    docs
This package contains the full API documentation for %{name}.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q -n gtkmm-%{version}


%build
%configure %{!?_with_static: --disable-static} --enable-shared
# removing rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*


%files devel
%doc PORTING demos/gtk-demo/
%{_includedir}/gtkmm-2.4/
%{_includedir}/gdkmm-2.4/
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_libdir}/gtkmm-2.4/
%{_libdir}/gdkmm-2.4/
%{_libdir}/pkgconfig/*.pc


%files docs
%doc %{_docdir}/%{tarname}-%{api_ver}
%doc %{_datadir}/devhelp/

%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.24.4-5
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.24.4-4
- 为 Magic 3.0 重建

* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 2.24.4-3
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Kalev Lember <kalevlember@gmail.com> - 2.24.4-1
- Update to 2.24.4

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 2.24.3-2
- Don't install ChangeLog

* Fri Apr 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.24.3-1
- Update to 2.24.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.24.2-2
- Rebuild for new libpng

* Sat Jul 09 2011 Kalev Lember <kalevlember@gmail.com> - 2.24.2-1
- Update to 2.24.2
- Removed mm-common buildrequire which is no longer needed for tarball builds
- Cleaned up the spec file for modern rpmbuild

* Thu Jul 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.24.1-1
- Update to 2.24.1
- Dropped the doctooldir patch

* Mon Jul 04 2011 Karsten Hopp <karsten@redhat.com> 2.24.0-4
- buildrequire mm-common
- fix pkg-config call to figure out doctooldir

* Wed Mar 02 2011 Kalev Lember <kalev@smartlink.ee> - 2.24.0-3
- Co-own /usr/share/devhelp/ directory
- Require base package from -doc subpackage
- Dropped unneeded doxygen and graphviz BRs

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.24.0-2
- fix documentation location

* Thu Feb 10 2011 Kalev Lember <kalev@smartlink.ee> - 2.24.0-1
- Update to 2.24.0
- Use macro for automatically figuring out the download URL
- Cleaned up unnecessary BuildRequires / Requires

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Kalev Lember <kalev@smartlink.ee> - 2.22.0-1
- Update to 2.22.0

* Tue Sep 21 2010 Kalev Lember <kalev@smartlink.ee> - 2.21.8.1-1
- Update to 2.21.8.1

* Tue Sep 21 2010 Kalev Lember <kalev@smartlink.ee> - 2.21.8-1
- Update to 2.21.8

* Tue Sep 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.21.7-2
- Dropped gtkmm24-2.21.1-gtkcalendar.patch
- Build docs subpackage as noarch
- Co-own gtk-doc directory (#604169)
- Fixed macro-in-changelog rpmlint warning

* Wed Sep 08 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.21.7-1
- Update to upstream 2.21.7

* Mon Jul 05 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.21.1-1
- Update to upstream 2.21.1
- close RHBZ #610195 (first step for parallel installable Gtkmm stacks)
- build patch from Kalev

* Thu Apr 29 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.20.2-1
- Update to upstream 2.20.2

* Sat Mar 20 2010 Denis Leroy <denis@poolshark.org> - 2.19.7-1
- Update to unstable 2.19.7

* Sat Feb 27 2010 Denis Leroy <denis@poolshark.org> - 2.19.6-1
- Update to unstable 2.19.6, fixes #568905

* Thu Feb 18 2010 Denis Leroy <denis@poolshark.org> - 2.19.4-1
- Update to upstream 2.19.4

* Sun Jan 17 2010 Denis Leroy <denis@poolshark.org> - 2.19.2-1
- Update to upstream 2.19.2, new unstable branch

* Sat Oct 24 2009 Denis Leroy <denis@poolshark.org> - 2.18.2-1
- Update to upstream 2.18.2

* Fri Sep 25 2009 Denis Leroy <denis@poolshark.org> - 2.18.1-1
- Update to upstream 2.18.1

* Mon Sep 14 2009 Denis Leroy <denis@poolshark.org> - 2.17.11-1
- Update to upstream 2.17.11
- Added demo code to devel package doc directory

* Sun Aug 16 2009 Denis Leroy <denis@poolshark.org> - 2.17.2-1
- Update to upstream 2.17.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr  6 2009 Denis Leroy <denis@poolshark.org> - 2.16.0-1
- Update to upstream 2.16.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Denis Leroy <denis@poolshark.org> - 2.15.3-1
- Update to upstream 2.15.3

* Wed Jan 14 2009 Denis Leroy <denis@poolshark.org> - 2.15.0-1
- Update to upstream 2.15.0

* Thu Dec 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.14.3-2
- Rebuild for pkgconfig provides

* Wed Nov 26 2008 Denis Leroy <denis@poolshark.org> - 2.14.3-1
- Update to 2.14.3 version
- Devhelp patch upstreamed

* Sat Oct 11 2008 Denis Leroy <denis@poolshark.org> - 2.14.1-1
- Update to 2.14.1
- Fix documentation links

* Tue Sep 23 2008 Denis Leroy <denis@poolshark.org> - 2.14.0-1
- Update to stable 2.14.0

* Fri Sep  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.13.7-2
- Patch from svn temporarily to make compatible with GTK 2.14
  (bug 461227)

* Sun Aug 24 2008 Denis Leroy <denis@poolshark.org> - 2.13.7-1
- Update to upstream 2.13.7, with pangomm split

* Wed Jul 23 2008 Denis Leroy <denis@poolshark.org> - 2.13.4-1
- Update to upstream 2.13.4

* Fri Jul  4 2008 Denis Leroy <denis@poolshark.org> - 2.13.1-1
- Update to version 2.13.1

* Sat May 31 2008 Denis Leroy <denis@poolshark.org> - 2.13.0-1
- Following gtk2 to 2.13 unstable branch

* Sat Apr 12 2008 Denis Leroy <denis@poolshark.org> - 2.12.7-1
- Update to upstream 2.12.7

* Wed Mar 12 2008 Denis Leroy <denis@poolshark.org> - 2.12.5-1
- Update to upstream 2.12.5

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.12.4-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Denis Leroy <denis@poolshark.org> - 2.12.4-1
- Update to upstream 2.12.4, includes gcc 4.3 build fix

* Sun Nov 11 2007 Denis Leroy <denis@poolshark.org> - 2.12.3-1
- Update to 2.12.3, bug fix

* Mon Sep 17 2007 Denis Leroy <denis@poolshark.org> - 2.12.0-1
- Update to new stable branch 2.12.0

* Tue Aug 28 2007 Denis Leroy <denis@poolshark.org> - 2.11.7-1
- Update to 2.11.7
- License tag update
- ppc32 rebuild

* Wed Aug  1 2007 Denis Leroy <denis@poolshark.org> - 2.11.6-1
- Update to 2.11.6

* Tue Jul  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.11.3-2
- Rebuild against newest GLib (due to #245141, #245634)

* Thu Jun 21 2007 Denis Leroy <denis@poolshark.org> - 2.11.3-1
- Update to unstable 2.11 tree to follow gtk2 version
- Fixed documentation devhelp support

* Mon Apr 30 2007 Denis Leroy <denis@poolshark.org> - 2.10.9-1
- Update to 2.10.9

* Thu Mar 15 2007 Denis Leroy <denis@poolshark.org> - 2.10.8-1
- Update to 2.10.8

* Sun Jan 28 2007 Denis Leroy <denis@poolshark.org> - 2.10.7-1
- Update to 2.10.7, fixed Source url path

* Tue Dec 12 2006 Denis Leroy <denis@poolshark.org> - 2.10.6-1
- Update to 2.10.6

* Mon Dec  4 2006 Denis Leroy <denis@poolshark.org> - 2.10.5-1
- Update to 2.10.5

* Tue Oct  3 2006 Denis Leroy <denis@poolshark.org> - 2.10.2-1
- Update to 2.10.2

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-3
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-2
- Added cairomm Require in devel 

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Update to 2.10.0. Now depends on cairomm

* Sun Jun 25 2006 Denis Leroy <denis@poolshark.org> - 2.8.8-2
- Added dist postfix to release version

* Sun Jun 25 2006 Denis Leroy <denisleroy@yahoo.com> - 2.8.8-1
- Update to 2.8.8

* Sun May  7 2006 Denis Leroy <denis@poolshark.org> - 2.8.5-1
- Update to 2.8.5

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.8.3-1
- Update to version 2.8.3
- Added optional macro to compile static libs

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.8.1-1
- Update to gtkmm 2.8.1
- Disabled static libraries build

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.8.0-1
- Update to gtkmm 2.8.0
- Incorporated dependency updates from Rick Vinyard

* Fri Apr 29 2005 Denis Leroy <denis@poolshark.org> - 2.6.2-2
- Disabled building of demo and examples

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.6.2-1
- Update to gtkmm 2.6.2
- Added demo binary to devel package

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 15 2005 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0:2.4.8-1
- Update for gtkmm 2.4.8

* Wed Nov 17 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.7-1
- Update for gtkmm 2.4.7

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.5-0.fdr.1
- Upgrade to 2.4.5

* Thu Oct 8 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.3
- Incorporated more of Michael Schwendt's Comments in fedora bug 727
- Seperate -docs package with devhelp support disabled.

* Tue Oct 7 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.2
- Split the documentation into a separate -docs package
- Included devhelp

* Sat Oct 4 2003 Michael Koziarski <michael@koziarski.org> - 0:2.2.8-0.fdr.1
- Incorporated Michael Schwendt's Comments in fedora bug 727
- Updated to 2.2.8

* Tue Sep 16 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:2.2.7-0.fdr.1
- Initial Fedora Release.
- Updated to 2.2.7.

* Fri Dec 6 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.2-1
- Removed "--without docs" option and simplified the spec file since the
  documentation is included in the tarball now

* Thu Dec 5 2002 Walter H. van Holst <rpm-maintainer@fossiel.xs4all.nl> - 1.0.2
- Removed reference to patch
- Added the documentation files in %%files

* Thu Oct 31 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.0-gp1
- Update to 2.0.0

* Wed Oct 30 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp3
- Added "--without docs" option to disable DocBook generation

* Sat Oct 26 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp2
- Update to 1.3.26
- Spec file cleanups
- Removed examples from devel package
- Build html documentation (including a Makefile patch)

* Mon Oct 14 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.24-gp1
- Initial release of gtkmm2, using gtkmm spec file as base
