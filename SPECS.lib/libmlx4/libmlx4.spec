Name: libmlx4
Version: 1.0.2
Release: 4%{?dist}
Summary: Mellanox ConnectX InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openib.org/
Source: http://openib.org/downloads/mlx4/%{name}-%{version}.tar.gz
Source1: libmlx4-modprobe.conf
Source2: libmlx4-mlx4.conf
Source3: libmlx4-setup-mlx4.awk
Patch4:  0004-Add-IBoE-support.patch
Patch5:  0005-Add-IBoE-UD-VLANs-support.patch
Patch6:  0006-Align-the-list-of-supported-ConnectX-devices-with-ke.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: libmlx4-devel = %{version}-%{release}
Obsoletes: %{name}-devel < 1.0.1-2
BuildRequires: libibverbs-devel > 1.1.4
%ifnarch ia64 %{sparc} %{arm} mips64el
BuildRequires: valgrind-devel
%endif
ExcludeArch: s390 s390x

%description
libmlx4 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Provides: %{name}-devel-static = %{version}-%{release}
Obsoletes: %{name}-devel-static < 1.0.1-2
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%ifnarch ia64 %{sparc} %{arm} mips64el
%configure --with-valgrind
%else
%configure
%endif
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d/libmlx4.conf
install -D -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/rdma/mlx4.conf
install -D -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/rdma/setup-mlx4.awk
# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/libmlx4.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx4-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
%{_sysconfdir}/modprobe.d/libmlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%{_sysconfdir}/rdma/setup-mlx4.awk
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx4.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.2-4
- 为 Magic 3.0 重建

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-3
- Actually bump the release number this time

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-2
- Update with changesets in current git head so we can get IBoE
  support

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest version
- Fix modprobe.conf to look in /etc/rdma instead of /etc/ofed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 08 2010 Dennis Gilmore <dennis@ausil.us> - 1.0.1-7
- arm arches dont have valgrind disable its support on them

* Wed Mar 24 2010 Dennis Gilmore <dennis@ausil.us> - 1.0.1-6
- sparc arches dont have valgrind disable its support on them

* Thu Feb 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-5
- Minor cleanups to Obsoletes to resolve some repo issues

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-4
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-3
- Tweak the provides and obsoletes a little bit to make sure we only pull in
  the -static package to replace past -devel-static packages, and not past
  -devel packages.

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-2
- Merge various bits from Red Hat package into Fedora package

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-1
- Update to latest upstream release
- Add pseudo provides of libibverbs-driver
- Update buildrequires for libibverbs API change

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 27 2008 Roland Dreier <rdreier@cisco.com> - 1.0-2
- Spec file cleanups, based on Fedora review: don't mark
  libmlx4.driver as a config file, since it is not user modifiable,
  and change the name of the -devel-static package to plain -devel,
  since it would be empty without the static library.

* Sun Dec  9 2007 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Fri Apr  6 2007 Roland Dreier <rdreier@cisco.com> - 1.0-0.1.rc1
- Initial Fedora spec file
