Summary: Cursor management library
Summary(zh_CN.UTF-8): 光标管理库
Name: libXcursor
Version: 1.1.14
Release: 3%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org
#VCS: git:git://anongit.freedesktop.org/xorg/lib/libXcursor
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: index.theme

BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrender-devel >= 0.8.2


%description
This is  a simple library designed to help locate and load cursors.
Cursors can be loaded from files or memory. A library of common cursors
exists which map to the standard X cursor names.Cursors can exist in
several sizes and the library automatically picks the best size.

%description -l zh_CN.UTF-8
光标管理库。

%package devel
Summary: Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
libXcursor development package.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
iconv --from=ISO-8859-2 --to=UTF-8 COPYING > COPYING.new && \
touch -r COPYING COPYING.new && \
mv COPYING.new COPYING

# Disable static library creation by default.
%define with_static 0

%build
#export CFLAGS="$RPM_OPT_FLAGS -DICONDIR=\"%{_datadir}/icons\""
%configure \
%if ! %{with_static}
 --disable-static
%endif
make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/default
install -m 644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/default/index.theme

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/libXcursor.so.1
%{_libdir}/libXcursor.so.1.0.2
%dir %{_datadir}/icons/default
%{_datadir}/icons/default/index.theme

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%if %{with_static}
%{_libdir}/libXcursor.a
%endif
%{_libdir}/libXcursor.so
%{_libdir}/pkgconfig/xcursor.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/Xcursor*.3*

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.1.14-3
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.1.14-2
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1.1.14-1
- 更新到 1.1.14

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.13-2
- 为 Magic 3.0 重建

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.1.13-1
- libXcursor 1.1.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.1.12-1
- libXcursor 1.1.12

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> 1.1.11-2
- Change the default cursor theme
  (also make the dependency a soft one)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.1.11-1
- libXcursor 1.1.11

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.1.10-5
- The theme file should _not_ be a config file

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 1.1.10-4
- Make default cursor theme inherit dmz-aa instead of Bluecurve
- Also require the cursor theme package

* Wed Oct 21 2009 Parag <paragn@fedoraproject.org> - 1.1.10-3
- Merge-Review #226066
- make is not verbose
- preserve timestamp of index.theme

* Thu Oct 08 2009 Parag <paragn@fedoraproject.org> - 1.1.10-2
- Merge-Review #226066
- Removed XFree86-libs, xorg-x11-libs as Obsoletes
- Removed BR:pkgconfig
- Few spec cleanups

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.10-1
- libXcursor 1.1.10

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.1.9-5
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.1.9-3
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.9-2
- Autorebuild for GCC 4.3

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.1.9-1
- libXcursor 1.1.9

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 1.1.8-3
- Rebuild for PPC toolchain bug

* Sat Jul  7 2007 Matthias Clasen <mclasen@redhat.com> 1.1.8-3
- Don't own /usr/share/icons
- Require pkgconfig in -devel

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.1.8-2
- Don't install INSTALL

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.1.8-1
- Update to 1.1.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.7-1.1
- rebuild

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.1.7-1
- Update to 1.1.7 from X11R7.1

* Wed Jun 07 2006 Mike A. Harris <mharris@redhat.com> 1.1.6-2
- Added "BuildRequires: xorg-x11-proto-devel"
- Added "Requires: xorg-x11-proto-devel" to devel package, needed by xcursor.pc
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.1.6-1
- Update to 1.1.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.1.5.2-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.1.5.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.1.5.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.1.5.2-1
- Updated libXcursor to version 1.1.5.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1.1.5.1-1
- Updated libXcursor to version 1.1.5.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Added default index.theme file to set BlueCurve as the default cursor theme
  to fix bug (#175532).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 1.1.5-1
- Updated libXcursor to version 1.1.5 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 1.1.4-1
- Updated libXcursor to version 1.1.4 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 1.1.3-1
- Initial build.
