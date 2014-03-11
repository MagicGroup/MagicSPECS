%define tarball xf86-video-tdfx
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

#global gitdate 20120104
%global gitversion fe60f0ed2

Summary:   Xorg X11 tdfx video driver
Name:      xorg-x11-drv-tdfx
Version:   1.4.5
Release:   13%{?gitdate:.%{gitdate}git%{gitversion}}%{dist}
URL:       http://www.x.org
License: MIT
Group:     User Interface/X Hardware Support

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
%endif

Patch0: 0001-Remove-mibstore.h.patch

ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel 
#>= 1.4.99.1
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: xorg-x11-util-macros >= 1.1.5
BuildRequires: mesa-libGL-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 tdfx video driver.

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}
%patch0 -p1

%build
autoreconf -v --install || exit 1
%configure --disable-static --disable-dri
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/tdfx_drv.so
%{_mandir}/man4/tdfx.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.4.5-13
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.4.5-12
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.4.5-11
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.4.5-10
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.4.5-9
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.5-7
- require xorg-x11-server-devel, not -sdk

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.5-6
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.5-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.5-4
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.4.5-3
- ABI rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 1.4.5-1
- tdfx 1.4.5

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.4.3-19.20120104gitfe60f0ed2
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-18.20120104gitfe60f0ed2
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-17.20120104gitfe60f0ed2
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-16.20120104gitfe60f0ed2
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.4.3-15.20120104gitfe60f0ed2
- Update to git
- Add hack to allow building with --disable-dri

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-14
- Rebuild for server 1.12

* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 1.4.3-13
- Drop xinf file

* Thu Nov 17 2011 Adam Jackson <ajax@redhat.com> 1.4.3-12
- Disable DRI1

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 1.4.3-11
- ABI rebuild
- tdfx-1.4.3-git.patch: Sync with git for new ABI
- tdfx-1.4.3-vga.patch: Fix VGA port access

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.4.3-9
- Rebuild for xserver 1.11 ABI

* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-8
- Rebuild for server 1.11

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-7
- Rebuild for server 1.10

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-5
- Rebuild for server 1.10

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.4.3-4
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-3
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.3-2
- Rebuild for server 1.8

* Tue Aug 04 2009 Dave Airlie <airlied@redhat.com> 1.4.3-1
- tdfx 1.4.3

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.4.2-1.1
- ABI bump

* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 1.4.2-1
- tdfx 1.4.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Dave Airlie <airlied@redhat.com> 1.4.1-1
- Latest upstream release

* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 1.4.0-1
- Latest upstream release

* Wed Feb 27 2008 Dave Airlie <airlied@fedoraproject.org> - 1.3.0-8
- make tdfx build again by rebasing to upstream - may not work

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-7
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1.3.0-6
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.3.0-5
- Update Requires and BuildRequires.  Add Requires: hwdata.

* Mon Mar 19 2007 Adam Jackson <ajax@redhat.com> 1.3.0-4
- tdfx-1.3.0-fix-ddc-order.patch: Move DDC probe before mode validation.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.3.0-3
- ExclusiveArch -> ExcludeArch

* Thu Nov 30 2006 Adam Jackson <ajax@redhat.com> 1.3.0-2.fc7
- Update to 1.3.0.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri May 26 2006 Mike A. Harris <mharris@redhat.com> 1.2,1-3
- Added "BuildRequires: libdrm-devel >= 2.0-1" for (#192358)

* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-2
- Rebuild for 7.1 ABI fix.

* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 1.2.1-1
- Update to 1.2.1 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.1.3-1.3
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.1.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.1.1.3-1
- Updated xorg-x11-drv-tdfx to version 1.1.1.3 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.1.1.2-1
- Updated xorg-x11-drv-tdfx to version 1.1.1.2 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.1.1-1
- Updated xorg-x11-drv-tdfx to version 1.1.1 from X11R7 RC2

* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 1.1.0.1-1
- Updated xorg-x11-drv-tdfx to version 1.1.0.1 from X11R7 RC1
- Fix *.la file removal.

* Tue Oct 4 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Limit "ExclusiveArch" to x86, x86_64

* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for tdfx video driver generated automatically
  by my xorg-driverspecgen script.
