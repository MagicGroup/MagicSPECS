%define pkgname xbitmaps

%define debug_package %{nil}

Summary: X.Org X11 application bitmaps
Summary(zh_CN.UTF-8): X.Org X11 应用程序位图
Name: xorg-x11-%{pkgname}
Version: 1.1.1
Release: 6%{?dist}
License: MIT
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://www.x.org
BuildArch: noarch

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/data/xbitmaps-%{version}.tar.bz2

Requires: pkgconfig

%description
X.Org X11 application bitmaps

%description -l zh_CN.UTF-8
X.Org X11 应用程序位图。

%prep
%setup -q -n xbitmaps-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%defattr(-,root,root,-)
%doc COPYING
%{_includedir}/X11
%{_datadir}/pkgconfig/xbitmaps.pc

%changelog
* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 1.1.1-6
- 为 Magic 3.0 重建

* Tue Oct 27 2015 Liu Di <liudidi@gmail.com> - 1.1.1-5
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.1.1-4
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-2
- Requires pkgconfig

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.1.1-1
- xbitmaps 1.1.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.1.0-3
- Own the /usr/include/X11 as discussed on packaging list.

* Mon Aug 30 2010 Adam Jackson <ajax@redhat.com> 1.1.0-2
- Merge review cleanups (#226649)

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 1.1.0-1
- xbitmaps 1.1.0
- BuildArch: noarch

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.1-8
- Un-require xorg-x11-filesystem

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.1-6
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-5.1
- Autorebuild for GCC 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4
- Bump release and rebuild for FC6.

* Thu Mar 02 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Made package arch specific due to pkgconfig files being placed in lib64
  if the noarch packages manage to get built on x86_64/ppc64/s390x.

* Wed Mar 01 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Cleaned up file manifest.
- Made package noarch, as it is just header files.
- Disable debuginfo processing, as there are no ELF objects in package.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xbitmaps 1.0.1 from X11R7.0

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xbitmaps 1.0.0 from X11R7 RC4.

* Wed Nov 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-4
- Updated dep to "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" for new fix.
- Moved bitmap files back into the upstream default of _includedir (#173665).

* Mon Nov 21 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-1" to attempt to
  workaround bug( #173384).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Clean up specfile.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated to xbitmaps 0.99.1 from X11R7 RC2

* Fri Aug 26 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
