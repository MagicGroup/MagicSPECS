%define pkgname xsm

Summary: X.Org X11 X Session Manager
Summary(zh_CN.UTF-8): X.Org X11 X 会话管理器
Name: xorg-x11-%{pkgname}
# NOTE: The Version field should be the version of the xsm tarball.
Version: 1.0.2
# Bump the release on rebuilds/bugfixes/etc.
Release: 20%{?dist}
License: MIT
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
URL: http://www.x.org

Source0: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/xsm-1.0.1.tar.bz2
Source1: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/smproxy-1.0.4.tar.bz2
Source2: http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/app/rstart-1.0.2.tar.bz2

# Fedora specific patches

# Patches for xsm (10-19)
Patch10: xsm-1.0.1-xsm-installation-location-fixes.patch
Patch11: xsm-1.0.1-add-needed.patch
Patch12: xsm-1.0.2-ice.patch

# Patches for smproxy (20-29)
Patch20: smproxy-1.0.4-ice.patch

# Patches for rstart (30-39)
Patch30: rstart-1.0.2-rstart-installation-location-fixes.patch

BuildRequires: automake autoconf

BuildRequires: pkgconfig
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libXaw-devel libXext-devel libXt-devel libXpm-devel libICE-devel
BuildRequires: rsh

# rstart script invokes xauth, rsh
Requires: xorg-x11-xauth, rsh

# FIXME:These old provided should be removed
Provides: xsm, smproxy, rstart, rstartd

%description
X.Org X11 X Session Manager

%description -l zh_CN.UTF-8
X.Org X11 X 会话管理器。

%prep
%setup -q -c %{name}-%{version} -a1 -a2
%patch10 -p0 -b .xsm-installation-location-fixes
%patch11 -p0 -b .add-needed
%patch12 -p0 -b .ice
%patch20 -p0 -b .ice
%patch30 -p0 -b .rstart-installation-location-fixes

%build
# Build everything
for pkg in xsm smproxy rstart ; do
    pushd $pkg-*

    sed -i '/XAW_/ s/)/, xaw7)/; /XAW_/ s/XAW_CHECK_XPRINT_SUPPORT/PKG_CHECK_MODULES/' configure.ac
    aclocal ; automake -avf ; autoconf

    %configure
    make  %{?_smp_mflags}
    popd
done

%install
# Install everything
{
   for pkg in xsm smproxy rstart ; do
      pushd $pkg-*
      make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
      popd
   done
}

%files
%defattr(-,root,root,-)
%doc xsm-1.0.1/COPYING xsm-1.0.1/README xsm-1.0.1/ChangeLog

%{_bindir}/rstart
%{_bindir}/rstartd
%{_bindir}/smproxy
%{_bindir}/xsm
%dir %{_datadir}/X11/rstart
%dir %{_datadir}/X11/rstart/commands
%{_datadir}/X11/rstart/commands/@List
%{_datadir}/X11/rstart/commands/ListContexts
%{_datadir}/X11/rstart/commands/ListGenericCommands
%dir %{_datadir}/X11/rstart/commands/x11r6
%{_datadir}/X11/rstart/commands/x11r6/@List
%{_datadir}/X11/rstart/commands/x11r6/LoadMonitor
%{_datadir}/X11/rstart/commands/x11r6/Terminal
%dir %{_datadir}/X11/rstart/contexts
%{_datadir}/X11/rstart/contexts/@List
%{_datadir}/X11/rstart/contexts/default
%{_datadir}/X11/rstart/contexts/x11r6
%{_datadir}/X11/app-defaults/XSm
%{_libexecdir}/rstartd.real
%{_mandir}/man1/rstart.1*
%{_mandir}/man1/rstartd.1*
%{_mandir}/man1/smproxy.1*
%{_mandir}/man1/xsm.1*
%dir %{_sysconfdir}/X11/rstart
%config %{_sysconfdir}/X11/rstart/config
%dir %{_sysconfdir}/X11/xsm
%config %{_sysconfdir}/X11/xsm/system.xsm

%changelog
* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 1.0.2-20
- *-ice.patch: Add missing libICE to link

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 01 2011 Adam Jackson <ajax@redhat.com> 1.0.2-17
- Move rstartd.real to %%_libexecdir

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 1.0.2-16
- smproxy 1.0.4

* Sat Sep 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.2-15
- Merge-review cleanup (#226655)

* Fri Mar 05 2010 Matěj Cepl <mcepl@redhat.com> - 1.0.2-14
- Fixed bad directory ownership of /usr/share/X11

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.0.2-13
- xsm-1.0.1-add-needed.patch, smproxy-1.0.2-add-needed.patch: Fix FTBFS for
  --no-add-needed

* Mon Aug 03 2009 Adam Jackson <ajax@redhat.com> 1.0.2-12
- Un-Requires xorg-x11-filesystem

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Adam Jackson <ajax@redhat.com> 1.0.2-10
- Fix FTBFS due to Xaw xprint macro disappearing. (#511614)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.2-8
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-7
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-6
- Rebuild for build id

* Tue Jan 30 2007 Adam Jackson <ajax@redhat.com> 1.0.2-5
- Fix man page globs and rebuild for FC7.

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-4.fc6
- Remove app-defaults dir from file manifest, as it is owned by libXt (#174021)
- Add 'dist' tag to package release string.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-3.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-3
- Added xsm documentation to doc macro.
- The 1.0.2-1 build had the version accidentally bumped to 1.0.2 before
  an xsm-1.0.2 was available, so I had to hard code the actual 1.0.1 version
  in a few places temporarily until xsm-1.0.2 is available.

* Tue May 30 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-2
- Fix BuildRequires (#191802)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update smproxy and rstart

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated all apps to version 1.0.1 from X11R7.0

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated all apps to version 1.0.0 from X11R7 RC4.
- Changed manpage dir from man1x to man1 to match upstream default.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-4
- Add "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" to avoid bug (#173384).
- Added rstart-0.99.1-rstart-installation-location-fixes.patch and
  xsm-0.99.2-xsm-installation-location-fixes.patch to put config files in
 /etc and data files in /usr/share where they belong.
- Added "Requires: xauth, rsh" as rstart invokes xauth, rsh.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.2-3
- require newer filesystem package (#172610)

* Sun Nov 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Added "Obsoletes: XFree86, xorg-x11", as all of these used to be in there.
- Rebuild against new libXaw 0.99.2-2, which has fixed DT_SONAME. (#173027)

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Initial build of xsm, smproxy, and rstart from X11R7 RC1
