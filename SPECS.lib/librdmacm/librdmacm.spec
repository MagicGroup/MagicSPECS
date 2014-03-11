Name: librdmacm
Version: 1.0.15
Release: 3%{?dist}
Summary: Userspace RDMA Connection Manager
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/rdmacm/%{name}-%{version}.tar.gz
Patch1: 0001-rdma-verbs-Fix-race-polling-for-completions.patch
Patch2: 0002-librdmacm-Fix-duplicate-free-of-connect.patch
Patch3: 0003-librdmacm-Verify-size-of-route_len.patch
Patch4: 0004-librdmacm-udaddy-Fix-resource-leak-in-case-of-error.patch
Patch6: 0006-rdma-cma-minor-code-refactoring-when-saving-a-string.patch
Patch7: 0007-librdmacm-Return-ECONNREFUSED-from-rdma_connect-on-r.patch
Patch8: 0008-udaddy-ucmatose-allow-easy-setting-of-tos-in-hex.patch
Patch9: 0009-librdmacm-Update-web-site-and-email-addresses.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x
BuildRequires: libibverbs-devel > 1.1.4, chrpath

%description
librdmacm provides a userspace RDMA Communication Managment API.

%package devel
Summary: Development files for the librdmacm library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release} libibverbs-devel%{?_isa}

%description devel
Development files for the librdmacm library.

%package static
Summary: Static development files for the librdmacm library
Group: System Environment/Libraries

%description static
Static libraries for the librdmacm library.

%package utils
Summary: Examples for the librdmacm library
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description utils
Example test programs for the librdmacm library.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
%configure LDFLAGS=-lpthread
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la
# kill rpaths
chrpath -d %{buildroot}%{_bindir}/*
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/librdmacm*.so.*
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.15-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.15-1
- Update to latest upstream tarball
- Add in latest git commits as patches

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.14.1-1
- Update to latest upstream release
- Rebuild against latest libibverbs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 19 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-3
- Fix up link problem caused by change to default DSO linking (bz564870)

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.10-2
- ExcludeArch s390(x) as the hardware doesn't exist there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 1.0.10-1
- Update to latest upstream release
- Change Requires on -devel package (bz533937)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Mar 29 2008 Roland Dreier <rolandd@cisco.com> - 1.0.7-1
- New upstream release

* Fri Feb 22 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-2
- Spec file cleanups from Fedora review: add BuildRequires for
  libibverbs, and move the static library to -static.

* Fri Feb 15 2008 Roland Dreier <rdreier@cisco.com> - 1.0.6-1
- Initial Fedora spec file

