Name: libmthca
Version: 1.0.6
Release: 6%{?dist}
Summary: Mellanox InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openfabrics.org/
Source: http://openfabrics.org/downloads/mthca/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: %{name}-devel = %{version}-%{release}
ExcludeArch: s390 s390x
BuildRequires: libibverbs-devel >= 1.1.5
%ifnarch ia64 %{sparc} %{arm} mips64el
BuildRequires: valgrind-devel
%endif

%description
libmthca provides a device-specific userspace driver for Mellanox HCAs
(MT23108 InfiniHost and MT25208 InfiniHost III Ex) for use with the
libibverbs library.

%package static
Summary: Development files for the libmthca driver
Group: System Environment/Libraries
Provides: %{name}-devel-static = %{version}-%{release}
Obsoletes: %{name}-devel-static < 1.0.5-4
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmthca that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q

%build
%ifnarch ia64 %{sparc} %{arm} mips64el
%configure --with-valgrind
%else
%configure
%endif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/libmthca.so

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libmthca-rdmav2.so
%{_sysconfdir}/libibverbs.d/mthca.driver
%doc AUTHORS COPYING ChangeLog README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmthca.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.6-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.6-4
- Improve the valgrind usage based upon where it's available

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.6-3
- Undo pseudoprovide workaround as it's no longer needed due to
  a change in the libibverbs requirements

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.6-2
- Helps if you put the % in front of a macro :-/

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.6-1
- Update to latest upstream version
- Add pseudoprovide for libibverbs-driver.{_arch} while keeping old
  pseudoprovide until libibverbs can be rebuilt without needing the
  old provide

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.5-8
- Update Obsoletes to resolve problem in update repo

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.5-7
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.0.5-6
- Tweak the provides and obsoletes a little bit to make sure we only pull in
  the -static package to replace past -devel-static packages, and not past
  -devel packages.

* Wed Dec 02 2009 Doug Ledford <dledford@redhat.com> - 1.0.5-5
- Rename devel-static package to just -static, it only has a single static
  lib in it and no actual devel files (like headers, those are part of
  libibverbs-devel instead).  Obsolete the various other named packages we
  want this to supercede
- Enable valgrind annotations on all arches except ia64
- Update to latest code, including update for libibverbs API change
- Bump release to 5 so it is higher than the current rhel5 libmthca release
- Add various patches from the upstream git repo that haven't been rolled into
  a new release tarball yet

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue May 27 2008 Roland Dreier <rolandd@cisco.com> - 1.0.5-1
- New upstream release
- Change openib.org URLs to openfabrics.org URLs

* Thu May 22 2008 Todd Zullinger <tmz@pobox.com> - 1.0.4-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-2
- Autorebuild for GCC 4.3

* Thu Nov  9 2006 Roland Dreier <rdreier@cisco.com> - 1.0.4-1
- New upstream release
- Depend on libibverbs 1.1, and package new library file names.
- Spec file cleanups: remove unused ver macro, improve BuildRoot, move
  static libraries into devel-static package, and don't use makeinstall
  any more (all suggested by Doug Ledford <dledford@redhat.com>).

* Wed Jul 26 2006 Roland Dreier <rdreier@cisco.com> - 1.0.3-1
- New upstream release

* Mon Mar 14 2006 Roland Dreier <rdreier@cisco.com> - 1.0.2-1
- New upstream release

* Thu Feb 16 2006 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Sun Feb 15 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.5.rc7
- New upstream release

* Sun Jan 22 2006 Roland Dreier <rolandd@cisco.com> - 1.0-0.4.rc6
- New upstream release

* Tue Oct 25 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.3.rc5
- New upstream release

* Wed Oct  5 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.2.rc4
- Update to upstream 1.0-rc4 release

* Mon Sep 26 2005 Roland Dreier <rolandd@cisco.com> - 1.0-0.1.rc3
- Initial attempt at Fedora Extras-compliant spec file
