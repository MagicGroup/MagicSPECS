Summary: X.Org X11 libfontenc runtime library
Summary(zh_CN.UTF-8): X.Org X11 libfontenc 运行库
Name: libfontenc
Version: 1.1.3
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: zlib-devel
BuildRequires: xorg-x11-font-utils

%description
X.Org X11 libfontenc runtime library

%description -l zh_CN.UTF-8
X.Org X11 libfontenc 运行库。

%package devel
Summary: X.Org X11 libfontenc development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libfontenc development package

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
export CFLAGS="$RPM_OPT_FLAGS -Os"
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# Remove all libtool archives (*.la)
find $RPM_BUILD_ROOT -type f -name '*.la' | xargs rm -f -- || :
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog
%{_libdir}/libfontenc.so.1
%{_libdir}/libfontenc.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/fonts/fontenc.h
%{_libdir}/libfontenc.so
%{_libdir}/pkgconfig/fontenc.pc

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 1.1.3-2
- 更新到 1.1.3

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 1.1.2-1
- 更新到 1.1.2

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.1.1-2
- 为 Magic 3.0 重建

* Mon Mar 05 2012 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libfontenc 1.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.1.0-1
- libfontenc 1.1.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Parag Nemade <paragn AT fedoraproject.org> 1.0.5-3
- Merge-review cleanup (#226004)

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.5-2
- libfontenc-1.0.0-get-fontdir-from-pkgconfig.patch: rebase to 1.0.5.

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.5-1
- libfontenc 1.0.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-9
- Un-requires xorg-x11-filesystem

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-8
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.4-6
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-5
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.4-4
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.4-3
- Don't install INSTALL

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 1.0.4-2
- Add BuildRequires on xorg-x11-font-utils to set encodings path correctly.

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.4-1
- Update to 1.0.4

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.3-1.fc7
- Update to 1.0.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-2.1
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-2
- Remove package ownership of mandir/libdir/etc.
- Added "BuildRequires: autoconf" temporarily as long as autoconf is needed

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update to 1.0.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated libfontenc to version 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libfontenc to version 1.0.0 from X11R7 RC4
- Added libfontenc-1.0.0-get-fontdir-from-pkgconfig.patch which now replaces
  libfontenc-0.99.2-use-datadir-for-encodings.patch by using pkgconfig to
  query fontutil.pc for fontdir.
- Added "BuildRequires: font-utils >= 1.0.0" to find fontutil.pc
- Removed libfontenc-0.99.2-use-datadir-for-encodings.patch

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libfontenc to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Bump xorg-x11-filesystem dep to >= 0.99.2-3 as -2 had bugs.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Added libfontenc-0.99.2-use-datadir-for-encodings.patch and invoke aclocal
  and automake to activate the changes.  This fixes a bug reported against
  mkfontscale, in which it looks in _datadir for the font encodings files,
  which was traced back to libfontenc (#173875).
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-2" to ensure that
  /usr/include/X11 is a directory rather than a symlink before this package
  gets installed, to avoid bug (#173384).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libfontenc to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libfontenc to version 0.99.1 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-4
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Added zlib-devel build dependency

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
