Summary: X.Org X11 libFS runtime library
Summary(zh_CN.UTF-8): X.Org X11 libFS 运行库
Name: libFS
Version: 1.0.6
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-4

%description
X.Org X11 libFS runtime library

%description -l zh_CN.UTF-8
X.Org X11 libFS 运行库。

%package devel
Summary: X.Org X11 libFS development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libFS development package

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# hack, we'll %%doc this on our own
rm -rf $RPM_BUILD_ROOT%{_docdir}

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/libFS.so.6
%{_libdir}/libFS.so.6.0.0

%files devel
%defattr(-,root,root,-)
%doc doc/FSlib.txt
%{_includedir}/X11/fonts/FSlib.h
%{_libdir}/libFS.so
%{_libdir}/pkgconfig/libfs.pc

%changelog
* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.0.6-1
- 更新到 1.0.6

* Thu Jul 31 2014 Liu Di <liudidi@gmail.com> - 1.0.4-2
- 更新到 1.0.6

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.4-2
- 为 Magic 3.0 重建

* Mon Mar 05 2012 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libFS 1.0.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.0.3-1
- libFS 1.0.3

* Mon Aug 30 2010 Adam Jackson <ajax@redhat.com> 1.0.2-1
- libFS 1.0.2
- merge review cleanups (#226005)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.1-4
- Un-require xorg-x11-filesystem

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.1-2
- Fix license tag.

* Tue Jun 10 2008 Adam Jackson <ajax@redhat.com> 1.0.1-1
- libFS 1.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Thu Sep 20 2007 Adam Jackson <ajax@redhat.com> 1.0.0-6
- Update xtrans dep and rebuild.

* Mon Sep 17 2007 Adam Jackson <ajax@redhat.com> 1.0.0-5
- Rebuild for abstract socket support.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.0-4
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1.0.0-4
- Don't install INSTALL

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-3.1
- rebuild

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-3
- Added "Requires: xorg-x11-proto-devel" to devel package.
- Remove package ownership of mandir/libdir/etc.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libFS to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libFS to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Removed "Provides: {name}" that got left from old package naming.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libFS to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-4
- Remove CFLAGS -D_XOPEN_SOURCE hack to test if upstream now builds ok.

* Thu Oct 27 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Add RPM_OPT_FLAGS to CFLAGS, as redefining CFLAGS lost the defaults

* Thu Oct 27 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Invoke 'make' in build stage
- Add -D_XOPEN_SOURCE to CFLAGS to work around build failure

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libFS to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Added BuildRequires: pkgconfig

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove "xorg-x11" from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
