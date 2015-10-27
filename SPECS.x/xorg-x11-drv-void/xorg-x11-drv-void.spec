%global tarball xf86-input-void
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

#global gitdate 20101202
#global gitversion cb8d19b8a

Summary:   Xorg X11 void input driver
Summary(zh_CN.UTF-8): Xorg X11 无输入驱动
Name:      xorg-x11-drv-void
Version:	1.4.1
Release:	3%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0:    http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
%endif


ExcludeArch: s390 s390x

BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: xorg-x11-util-macros >= 1.3.0

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires xinput)

%description 
X.Org X11 void input driver.

%description -l zh_CN.UTF-8
Xorg X11 无输入驱动。

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static
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
%doc COPYING
%{driverdir}/void_drv.so
%{_mandir}/man4/void.4*

%changelog
* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.4.1-3
- 为 Magic 3.0 重建

* Mon Oct 26 2015 Liu Di <liudidi@gmail.com> - 1.4.1-2
- 更新到 1.4.1

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 1.4.0-24
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 1.4.0-23
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 1.4.0-22
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 1.4.0-21
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 1.4.0-20
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-18
- Force autoreconf

* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 1.4.0-17
- Less RHEL customization

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-16
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-15
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-14
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 1.4.0-13
- ABI rebuild

* Fri Nov 09 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-12
- Fix {?dist} tag

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> - 1.4.0-10
- ABI rebuild

* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 1.4.0-9
- RHEL arch exclude updates

* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-8
- ABI rebuild

* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-7
- ABI rebuild

* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-6
- ABI rebuild

* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-5
- Rebuild for server 1.12

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 1.4.0-4
- ABI rebuild

* Wed Nov 09 2011 ajax <ajax@redhat.com> - 1.4.0-3
- ABI rebuild

* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 1.4.0-2
- Rebuild for xserver 1.11 ABI

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.4.0-1
- void 1.4.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4.20101202gitcb8d19b8a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-3.20101202gitcb8d19b8a
- add commitid and snapshot file

* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-2.20101202gitcb8d19b8a
- Add git hooks, update to today's snapshot

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.1-1
- void 1.3.1

* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 1.3.0-7
- Add ABI requires magic (#542742)

* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.0-6
- rebuild for X Server 1.9

* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 1.3.0-5
- Rebuild for server 1.8

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-4
- Use global instead of define as per Packaging Guidelines 

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-3
- Silence rpmlint spaces/tabs warning.
- move COPYING under defattr to get the right attr.

* Fri Sep 11 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-2
- Require xorg-x11-util-macros 1.3.0

* Fri Sep 11 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- void 1.3.0

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.2.0-2.1
- ABI bump

* Mon Jun 22 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-2
- void-1.2.0-Adjust-for-ABI_XINPUT_VERSION-7.patch: cope with new input ABI.

* Wed Feb 25 2009 Peter Hutterer <peter.hutterer@redhat.com> - 1.2.0-1
- void 1.2.0

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.1-9
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.1-8
- Don't own %%{mandir}.

* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 1.1.1-7
- Require xserver 1.4.99.1

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.1.1-6
- xf86-input-void 1.1.1

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 1.1.0-6
- Rebuild for ppc toolchain bug

* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 1.1.0-5
- Update Requires and BuildRequires.  Disown the module directories.

* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 1.1.0-4
- ExclusiveArch -> ExcludeArch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 28 2006 Mike A. Harris <mharris@redhat.com> 1.1.0-3
- Remove system owned directories from file manifest.

* Tue Jun 13 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-2
- Build on ppc64

* Sun Apr 09 2006 Adam Jackson <ajackson@redhat.com> 1.1.0-1
- Update to 1.1.0 from 7.1RC1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.0.5-1
- Updated xorg-x11-drv-void to version 1.0.0.5 from X11R7.0

* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.4-1
- Updated xorg-x11-drv-void to version 1.0.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.

* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.2-1
- Updated xorg-x11-drv-void to version 1.0.0.2 from X11R7 RC2

* Fri Nov 04 2005 Mike A. Harris <mharris@redhat.com> 1.0.0.1-1
- Updated xorg-x11-drv-void to version 1.0.0.1 from X11R7 RC1
- Fix *.la file removal.

* Fri Sep 02 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-0
- Initial spec file for void input driver generated automatically
  by my xorg-driverspecgen script.
