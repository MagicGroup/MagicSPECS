Summary: X.Org X11 libXv runtime library
Summary(zh_CN.UTF-8): X.Org X11 libXv 运行库
Name:    libXv
Version: 1.0.10
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkgconfig(videoproto) pkgconfig(xext)

%description
X.Org X11 libXv runtime library

%description -l zh_CN.UTF-8
X.Org X11 libXv 运行库。

%package devel
Summary: X.Org X11 libXv development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXv development package

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install

rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog
%{_libdir}/libXv.so.1
%{_libdir}/libXv.so.1.0.0

%files devel
%defattr(-,root,root,-)
%doc man/xv-library-v2.2.txt
%{_includedir}/X11/extensions/Xvlib.h
%{_libdir}/libXv.so
%{_libdir}/pkgconfig/xv.pc
#%dir %{_mandir}/man3x
%{_mandir}/man3/*.3*

%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.0.10-2
- 为 Magic 3.0 重建

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1.0.10-1
- 更新到 1.0.10

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.7-2
- 为 Magic 3.0 重建

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.0.7-1
- libXv 1.0.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.0.6-1
- libXv 1.0.6

* Wed Oct 07 2009 Adam Jackson <ajax@redhat.com> 1.0.5-1
- libXv 1.0.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.4-3
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 1.0.4-1
- libXv 1.0.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-5
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 1.0.3-4
- Merge-Review #226093
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length README file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.3-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.0.3-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.0.3-1
- Update to 1.0.3

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.0.2-1.fc7
- Update to 1.0.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-4.1
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4
- Added "Requires: xorg-x11-proto-devel" to devel package for xv.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added "BuildRequires: pkgconfig" for (#193505)
- Replace "makeinstall" with "make install DESTDIR=..."
- Remove package ownership of mandir/libdir/etc.

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "Requires: libXext-devel" to libXv-devel subpackage, to avoid all
  packages that depend on libXv-devel from having to manually specify that
  dependency themselves, as it is required by Xv.  (#192167)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated libXv to version 1.0.1 from X11R7.0

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXv to version 0.99.2 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXv to version 0.99.1 from X11R7 RC1
- Updated file manifest to find manpages in "man3x"

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
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
