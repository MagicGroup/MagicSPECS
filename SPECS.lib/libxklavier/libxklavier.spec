Summary:	High-level API for X Keyboard Extension
Summary(zh_CN.UTF-8): X 键盘扩展的高级 API
Name:		libxklavier
Version:	5.3
Release: 1%{?dist}
License:	LGPLv2+
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL: http://www.freedesktop.org/wiki/Software/LibXklavier
BuildRequires: libxml2-devel
BuildRequires: libxkbfile-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libxml2-devel
BuildRequires: glib2-devel >= 2.6.0
BuildRequires: iso-codes-devel
BuildRequires: gobject-introspection-devel
# temporary workaround for a typical introspection issue
BuildRequires: libxklavier-devel
%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source: http://download.gnome.org/sources/libxklavier/%{majorver}/%{name}-%{version}.tar.xz

%description
libxklavier is a library providing a high-level API for the X Keyboard
Extension (XKB). This library is intended to support XFree86 and other
commercial X servers. It is useful for creating XKB-related software
(layout indicators etc).

%description -l zh_CN.UTF-8
X 键盘扩展的高级 API。

%package devel
Summary: Development files for libxklavier
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: libxml2-devel

%description devel
This package contains libraries, header files and developer documentation
needed to develop libxklavier applications.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build

%configure \
  --disable-static \
  --with-xkb-base='%{_datadir}/X11/xkb' \
  --with-xkb-bin-base='%{_bindir}'

make V=1 %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)

%doc AUTHORS NEWS README COPYING.LIB
%{_libdir}/libxklavier.so.16*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Xkl-1.0.typelib

%files devel
%defattr(-, root, root)

%{_libdir}/pkgconfig/libxklavier.pc
%{_libdir}/libxklavier.so
%{_includedir}/libxklavier/
%{_datadir}/gtk-doc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Xkl-1.0.gir

%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 5.3-1
- 更新到 5.3

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 5.2.1-2
- 为 Magic 3.0 重建

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 5.2.1-1
- Update to 5.2.1
- Build with introspection

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 5.2-1
- Update to 5.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 5.1-1
- Update to 5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 5.0-2
- Co-own /usr/share/gtk-doc (#604402)

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 5.0-1
- Update to 5.0

* Thu Dec 10 2009 Matthias Clasen <mclasen@redhat.com> - 4.0-7
- Catch more X errors

* Thu Oct 15 2009 Matthias Clasen <mclasen@redhat.com> - 4.0-6
- Incorporate upstream fixes for XInput error handling

* Fri Oct  2 2009 Matthias Clasen <mclasen@redhat.com> - 4.0-5
- Handle BadDrawable errors gracefully

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Matthias Clasen <mclasen@redhat.com> - 4.0-3
- Avoid a critical warning at runtime

* Wed Jul 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.0-2
- %%files: track files closer, esp lib sonames
- %%build: drop --disable-doxygen, add --disable-static, add %%{?_smp_mflags}

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> - 4.0-1
- Update to 4.0

* Thu Mar 19 2009 Matthias Clasen <mclasen@redhat.com> - 3.9-1
- Update to 3.9

* Sat Mar  7 2009 Matthias Clasen <mclasen@redhat.com> - 3.8-4
- Suppress xkbcomp spew in .xsession-errors

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Matthias Clasen <mclasen@redhat.com> - 3.8-2
- Update to 3.8

* Fri Sep 19 2008 Matthias Clasen <mclasen@redhat.com> - 3.7-3
- Plug a memory leak

* Fri Sep  5 2008 Matthias Clasen <mclasen@redhat.com> - 3.7-1
- Update to 3.7

* Fri Jun 27 2008 Ray Strode <rstrode@redhat.com> - 3.6-2
- Apply upstream patch to fix libxklavier crash (bug 452966)

* Wed Apr 30 2008 Matthias Clasen <mclasen@redhat.com> - 3.6-1
- Update to 3.6

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 3.5-1
- Update to 3.5

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 3.4-1
- Update to 3.4

* Wed Sep  5 2007 Matthias Clasen <mclasen@redhat.com> - 3.3-1
- Update to 3.3

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 3.2-3
- Rebuild for build ID

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 3.2-2
- Update the license field

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 3.2-1
- Update to 3.2

* Sat Nov  4 2006 Matthias Clasen <mclasen@redhat.com> - 3.1-2
- Fix a possible crash (#213419)

* Sat Nov  4 2006 Matthias Clasen <mclasen@redhat.com> - 3.1-1
- Update to 3.1

* Wed Aug 30 2006 Matthias Clasen <mclasen@redhat.com> - 3.0-1.fc6
- Update to 3.0
- Require pkgconfig in the -devel package
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.91-1.1
- rebuild

* Wed Jun 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.91-1
- Update to 2.91

* Thu Jun  8 2006 Jesse Keating <jkeating@redhat.com> - 2.2-3
- Add missing BR libxml2-devel

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.2-2
- rebuild for -devel deps

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.com> - 2.2-1
- Update to 2.2

* Thu Mar  9 2006 Ray Strode <rstrode@redhat.com> - 2.1.0.2006.02.23-2
- trap X error reply to limit the damage of bug 183569.

* Thu Feb 23 2006 Ray Strode <rstrode@redhat.com> - 2.1.0.2006.02.23-1
- upgrade to latest cvs to handle xml comments (bug 178163)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Christopher Aillon <caillon@redhat.com> 2.1-3
- Add missing BR: libX11-devel libxml2-devel libxkbfile-devel

* Tue Dec 27 2005 Christopher Aillon <caillon@redhat.com> 2.1-2
- Pull in latest version and get rid of the annoying XKB error dialog

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Ray Strode <rstrode@redhat.com> 2.0-3
- Don't hard code the xkb data prefix.

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 2.0-2
- Fix references to obsolete X11R6 paths

* Mon Mar 21 2005 David Zeuthen <davidz@redhat.com> 2.0-1
- Update to latest upstream version

* Wed Mar 16 2005 David Zeuthen <davidz@redhat.com> 1.14-2
- Rebuild

* Mon Jan 31 2005 Matthias Clasen <mclasen@redhat.com> 1.14-1
- Update to 1.14

* Wed Sep 29 2004 Jonathan Blandford <jrb@redhat.com> 1.02-3
- bump version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 20 2004 Jeremy Katz <katzj@redhat.com> - 1.02-1
- update to 1.02 with real fixes for xorg

* Thu Apr 15 2004 Jeremy Katz <katzj@redhat.com> - 1.00-2
- patch for xorg.xml instead of xfree86.xml

* Fri Apr  2 2004 Alex Larsson <alexl@redhat.com> 1.00-1
- update to 1.00

* Mon Mar 15 2004 Bill Nottingham <notting@redhat.com>
- fix typo (#118237)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt


* Tue Jan 27 2004 Alexander Larsson <alexl@redhat.com> 0.97-1
- First version
