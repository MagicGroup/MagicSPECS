%define po_package libgtop-2.0

Name:     libgtop2
Summary:  LibGTop library (version 2)
Summary(zh_CN.UTF-8): LibGTop 库 （版本 2）
Version:	2.32.0
Release:  3%{?dist}
License:  GPLv2+
URL:      http://download.gnome.org/sources/libgtop/2.28
Group:    System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
#VCS: git://git.gnome.org/libgtop
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source:   http://download.gnome.org/sources/libgtop/%{majorver}/libgtop-%{version}.tar.xz
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libtool gettext
BuildRequires:  intltool libtool

%description
LibGTop is a library for portably obtaining information about processes,
such as their PID, memory usage, etc.

%description -l zh_CN.UTF-8
这个库是用来获取进程信息的，比如 PID, 内存使用等。

%package devel
Summary:  Libraries and include files for developing with libgtop
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:    Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with LibGTop.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libgtop-%{version}

%build
%configure --disable-gtk-doc --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

magic_rpm_clean.sh
%find_lang %{po_package}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{po_package}.lang
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GTop-2.0.typelib

%files devel
%{_libdir}/*.so
%{_includedir}/libgtop-2.0
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GTop-2.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libgtop
# not worth fooling with
%exclude %{_datadir}/info

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.32.0-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.32.0-2
- 更新到 2.32.0

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 2.30.0-1
- 更新到 2.30.0

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 2.28.4-2
- 为 Magic 3.0 重建

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-1
- Update to 2.28.4

* Wed Aug 17 2011 Michel Salim <salimma@fedoraproject.org> - 2.28.3-2
- Enable introspection (# 693419, 720109)
- Remove -doc dependency on gtk-doc (# 604389)

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.3-1
- Update to 2.28.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.28.2-2
- Merge-review cleanup (#226026)

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Fri Feb 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Examples don't build with pedantic linkers, so don't build them

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3
- http://download.gnome.org/sources/libgtop/2.27/libgtop-2.27.3.news

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/libgtop/2.26/libgtop-2.26.1.news

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-4
- Rebuild for pkg-config auto-provides

* Sun Nov  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Read /proc/cpuinfo completely (#467455)

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Jul  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.21.5-2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update top 2.21.1

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.19.5-3
- Rebuild for PPC toolchain bug

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-2
- Update the license field

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.8-1
- Update to 2.14.8

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-1
- Update to 2.14.7

* Sun Jan 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.6-1
- Update to 2.14.6

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.5-1
- Update to 2.14.5
- Require pkgconfig in the -devel package

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.14.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Soren Sandmann <sandmann@redhat.com> - 2.14.4-1.fc6
- Update to 2.14.4. The only change from 2.14.3 is the fix for 
  b.r.c 206616 / b.g.o 255290. 

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1.fc6
- Update to 2.14.3

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1.fc6
- Update to 2.14.2

* Wed Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 2.14.1-4
- rebuild
- add missing br libtool gettext

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-3
- Rebuild

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 24 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.3

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.2

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.1

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.2-1
- Update to 2.12.2
- Drop static libraries

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- New upstream version

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.90-1
- New upstream version

* Tue Jul 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to newer upstream version

* Fri Apr 29 2005 David Zeuthen <davidz@redhat.com> - 2.10.1-1
- New upstream version (#155188)

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.10.0-2
- Rebuilt

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.10.0-1
- Even newer upstream version

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.9.92-1
- New upstream version

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-2
- Rebuild

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- Update to 2.9.90

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Thu Aug  5 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 2.5.2-2
- BR libtool texinfo gettext

* Fri Mar 12 2004 Alex Larsson <alexl@redhat.com> 2.5.2-1
- update to 2.5.2

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.1-1
- update to 2.5.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.0-1
- update to 2.5.0

* Wed Jul 23 2003 Havoc Pennington <hp@redhat.com>
- automated rebuild

* Fri Jul 18 2003 Havoc Pennington <hp@redhat.com> 2.0.2-1
- 2.0.2
- forward port prog_as patch
- attempted fix to handle >4mb on IA32, #98676

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 2.0.0-10
- fix URL (#79390)

* Mon Feb  3 2003 Havoc Pennington <hp@redhat.com> 2.0.0-9
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.0-7
- More missing libXau hackery (prog_as.patch so we can run auto* to pull 
in an updated libtool)
- _smp_mflags

* Wed Dec  4 2002 Havoc Pennington <hp@redhat.com>
- rebuild more, woot!

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- rebuild to try and fix weird undefined Xau symbols

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- rebuild
- remove nonexistent doc files
- fix uninstalled but unpackaged files

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Fix missing po files

* Sat Jun 15 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- check file list, lose libgnomesupport

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- .la files evil

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- rebuild for glib 2.0

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.90.2

* Mon Jan 28 2002 Havoc Pennington <hp@redhat.com>
- Initial build

