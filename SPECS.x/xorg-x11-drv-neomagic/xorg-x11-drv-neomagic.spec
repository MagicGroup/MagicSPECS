%define tarball xf86-video-neomagic
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 neomagic video driver
Summary(zh_CN.UTF-8): Xorg X11 neomagic 显卡驱动
Name:      xorg-x11-drv-neomagic
Version:	1.2.9
Release:	3%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:   ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2

ExclusiveArch: %{ix86}

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk >= 1.4.99.1

Requires:  xorg-x11-server-Xorg >= 1.4.99.1

%description 
X.Org X11 neomagic video driver.

%description -l zh_CN.UTF-8
Xorg X11 neomagic 显卡驱动。

%prep
%setup -q -n %{tarball}-%{version}

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/neomagic_drv.so
%{_mandir}/man4/neomagic.4*

%changelog
* Sun Nov 15 2015 Liu Di <liudidi@gmail.com> - 1.2.9-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.2.9-2
- 更新到 1.2.9

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.6-2
- 为 Magic 3.0 重建

* Fri Apr 27 2012 Adam Jackson <ajax@redhat.com> 1.2.6-1
- neomagic 1.2.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 1.2.5-1
- update to latest release for server 1.9

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-4
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.4-3
- Rebuild for server 1.8

* Mon Oct 26 2009 Adam Jackson <ajax@redhat.com> 1.2.4-2
- neomagic-usleep.patch: Fix for new server ABI. (#523800)

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.2.4-1
- neomagic 1.2.4

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.2.3-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.2.3-1
- neomagic 1.2.3

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.2.2-1
- Latest upstream release

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.2.0-1
- Latest upstream release

* Mon Mar 10 2008 Dave Airlie <airlied@redhat.com> 1.1.1-7
- fixup neomagic pciaccess support

* Wed Feb 27 2008 Dave Airlie <airlied@redhat.com> - 1.1.1-6
- add pciaccess support

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-5
- Autorebuild for GCC 4.3

* Thu Sep 06 2007 Adam Jackson <ajax@redhat.com> 1.1.1-4
- Fix license.  Disown the module and driver dirs. (#226610)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.1.1-3
- Rebuild for build id

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.1-2.1
- rebuild

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1
- Update to 1.1.1 from 7.1RC1.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-neomagic to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-neomagic to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-neomagic to version 1.0.0.2 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-neomagic to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for neomagic video driver generated automatically
  by my xorg-driverspecgen script.
