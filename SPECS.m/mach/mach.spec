Name:           mach
Version:        1.0.0
Release:        3%{?dist}
Summary:        Make a chroot

Group:          Applications/System
License:        GPLv2+
URL:            http://thomas.apestaart.org/projects/mach/
Source:         http://thomas.apestaart.org/download/mach/%{name}-%{version}.tar.bz2
Patch1:		mach-1.0.0-gcc4.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       python
Requires:       rpm
Requires:       rpm-build
Requires:       rpm-python
Requires:       yum
Requires:       createrepo
Requires:       sed
Requires:       cpio

BuildRequires:  python
BuildRequires:  gcc-c++

%if 0%{!?flavor:1}
%if 0%{?rhel}
%define flavor epel
%else
%define flavor updates
%endif
%endif
%{!?builduser:  %define builduser  machbuild}
%{!?buildgroup: %define buildgroup machbuild}

%description
mach makes a chroot.
Using yum or apt-get and a suid binary, it manages to install clean chroot
environments based on the original packages for that distribution.

The clean root can be used to run jail roots, to create image files, or
to build clean packages.

Authors:
--------
Thomas Vander Stichele (thomas (at) apestaart (dot) org)

%prep
%setup -q
%patch1 -p1

%build
%configure \
        --enable-builduser=%{builduser} \
        --enable-buildgroup=%{buildgroup} \
        --disable-selinux \
        --with-flavor=%{flavor}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# no dev package
rm -f $RPM_BUILD_ROOT%{_libdir}/*.so

install -d -m 2775 $RPM_BUILD_ROOT%{_localstatedir}/lib/mach
install -d -m 2775 $RPM_BUILD_ROOT%{_localstatedir}/lib/mach/states
install -d -m 2775 $RPM_BUILD_ROOT%{_localstatedir}/lib/mach/roots
install -d -m 2775 $RPM_BUILD_ROOT%{_localstatedir}/tmp/mach
install -d -m 775 $RPM_BUILD_ROOT%{_localstatedir}/cache/mach

find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group mach >/dev/null || groupadd -r mach || :
/sbin/ldconfig

%preun
if [ "$1" == 0 ];
then
  # last removal
  # be a good boy and clean out the dirs we filled with junk
  rm -rf %{_localstatedir}/lib/mach/states/*
  umount %{_localstatedir}/lib/mach/roots/*/proc > /dev/null 2>&1 || :
  rm -rf %{_localstatedir}/lib/mach/roots/*
  rm -rf %{_localstatedir}/cache/mach/* > /dev/null 2>&1 || :
  rmdir %{_localstatedir}/lib/mach/states > /dev/null 2>&1 || :
  rmdir %{_localstatedir}/lib/mach/roots > /dev/null 2>&1 || :
  rmdir %{_localstatedir}/cache/mach > /dev/null 2>&1 || :
  rm -rf %{_localstatedir}/tmp/mach > /dev/null 2>&1 || :
fi
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README AUTHORS TODO FORGETMENOT RELEASE mach.doap
%dir %{_sysconfdir}/mach
%config(noreplace) %{_sysconfdir}/mach/conf
%config(noreplace) %{_sysconfdir}/mach/location
%config(noreplace) %{_sysconfdir}/mach/dist.d
%attr(2775,root,mach) %dir %{_localstatedir}/lib/mach
%attr(2775,root,mach) %dir %{_localstatedir}/lib/mach/states
%attr(2775,root,mach) %dir %{_localstatedir}/lib/mach/roots
%ghost %attr(2775,root,mach) %dir %{_localstatedir}/tmp/mach
%attr(2775,root,mach) %{_localstatedir}/cache/mach
%{_bindir}/mach
#%{_libdir}/libselinux-mach.*
%attr(04750,root,mach) %{_sbindir}/mach-helper

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.0
- new upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.6-1
- Updated to new upstream release.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-1
- new release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-1
- new release

* Thu May 22 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-1
- new release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.2-4
- Autorebuild for GCC 4.3

* Wed Sep 12 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.9.2-3
- Set default flavour to "epel" for EPEL builds.

* Sun Sep  9 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.9.2-2
- Drop no longer needed (and failing) old ppc config bug workarounds.
- Sync group creation scriptlet with current Fedora packaging guidelines.
- Set default config to the "updates" flavour.

* Sat Sep 08 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.2-1
- new release

* Thu Aug 16 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.9.1-3
- License: GPLv2+

* Wed Jan 24 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-2
- add ppc files

* Sun Jan 07 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.1-1
- new release

* Mon Oct  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.0-3
- Rebuild.

* Tue Sep 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9.0-2
- Rebuild.

* Fri Jun 09 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.0-1
- new release

* Sun Apr 09 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.9-1
- new release

* Fri Nov 25 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.8-1
- new release

* Mon Aug  9 2004 Ville Skyttä <ville.skytta at iki.fi>
- Create only the "mach" group, and do not remove it on erase.  The
  "mach" user is not really needed for anything.

* Sun Jun  6 2004 Ville Skyttä <ville.skytta at iki.fi>
- Properly redirect STDERR from umount to /dev/null at erase time.

* Wed Apr 14 2004 Ville Skyttä <ville.skytta at iki.fi>
- Own %%{_localstatedir}/mach, thanks to John Dalbec for the catch.

* Thu Apr  8 2004 Ville Skyttä <ville.skytta at iki.fi>
- Require apt >= 0.5.5cnc2 due to internal use of the "rpm-dir" index type.

* Tue Mar 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- package dist.d and location

* Thu Mar 11 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- use --with-flavor

* Fri Jan  9 2004 Ville Skyttä <ville.skytta at iki.fi>
- Use the bzip2'd tarball.

* Thu Jan  8 2004 Ville Skyttä <ville.skytta at iki.fi>
- Make mach chroot build user/group configurable using
  "rpmbuild --define 'build(user|group) foo'"
- Build in the %%build section.

* Wed Sep 17 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- add Requires: cpio
- change home dir to %%{_localstatedir}/lib/mach

* Mon Sep 08 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4.0-0.fdr.1: first public release.

* Sat Aug 16 2003 Ville Skyttä <ville.skytta at iki.fi>
- Add COPYING to docs.

* Wed May 21 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- added mach-helper

* Wed Apr 30 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- initial creation
