Name: opensm
Version: 3.3.13
Release: 4%{?dist}
Summary: OpenIB InfiniBand Subnet Manager and management utilities
Group: System Environment/Daemons
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source0: http://www.openfabrics.org/downloads/management/%{name}-%{version}.tar.gz
Source1: opensm.conf
Source2: opensm.logrotate
Source3: opensm.initd
Source4: opensm.sysconfig
Patch0: opensm-3.3.13-prefix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibmad-devel = 1.3.8, libtool, bison, flex, byacc
Requires: %{name}-libs = %{version}-%{release}, logrotate, rdma
ExcludeArch: s390 s390x

%description
OpenSM is the OpenIB project's Subnet Manager for Infiniband networks.
The subnet manager is run as a system daemon on one of the machines in
the infiniband fabric to manage the fabric's routing state.  This package
also contains various tools for diagnosing and testing Infiniband networks
that can be used from any machine and do not need to be run on a machine
running the opensm daemon.

%package libs
Summary: Libraries used by opensm and included utilities
Group: System Environment/Libraries

%description libs
Shared libraries for Infiniband user space access

%package devel
Summary: Development files for the opensm-libs libraries
Group: Development/System
Requires: %{name}-libs = %{version}-%{release}

%description devel
Development environment for the opensm libraries

%package static
Summary: Static version of the opensm libraries
Group: Development/System
Requires: %{name}-devel = %{version}-%{release}
%description static
Static version of opensm libraries

%prep
%setup -q
%patch0 -p1 -b .prefix

%build
%configure --with-opensm-conf-sub-dir=rdma
make %{?_smp_mflags}
cd opensm
./opensm -c ../../opensm-%{version}.conf

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la
rm -fr %{buildroot}%{_sysconfdir}/init.d
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rdma/opensm.conf
install -D -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/opensm
install -D -m755 %{SOURCE3} %{buildroot}%{_initddir}/opensm
install -D -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/opensm
mkdir -p ${RPM_BUILD_ROOT}/var/cache/opensm
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	/sbin/chkconfig --add opensm
else
	/sbin/service opensm condrestart
fi

%preun
if [ $1 = 0 ]; then
	/sbin/service opensm stop
	/sbin/chkconfig --del opensm
	rm -f /var/cache/opensm/*
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir /var/cache/opensm
%{_sbindir}/*
%{_initddir}/opensm
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/opensm
%config(noreplace) %{_sysconfdir}/rdma/opensm.conf
%config(noreplace) %{_sysconfdir}/sysconfig/opensm
%doc AUTHORS COPYING ChangeLog INSTALL README NEWS

%files libs
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_includedir}/infiniband

%files static
%defattr(-,root,root,-)
%{_libdir}/lib*.a

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.3.13-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Doug Ledford <dledford@redhat.com> - 3.3.13-2
- Fix the config file comment in the opensm init script
- Resolves: bz802727

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 3.3.13-1
- Update to latest upstream version
- Fix a minor issue in init scripts that would cause systemd to try and
  start/stop things in the wrong order
- Add a patch to allow us to specify the subnet prefix on the command line

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 3.3.12-1
- Update to latest upstream version

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 3.3.9-2
- Rebuilt for rpm bug #728707

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 3.3.9-1
- Update to latest upstream version
- Add /etc/sysconfig/opensm for use by opensm init script
- Enable the ability to start more than one instance of opensm for multiple
  fabric support
- Enable the ability to start opensm with a priority other than default for
  support of backup opensm instances

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 08 2010 Doug Ledford <dledford@redhat.com> - 3.3.5-1
- Update to latest upstream release.  We need various defines in ib_types.h
  for the latest ibutils package to build properly, and the latest ibutils
  package is needed because we found licensing problems in the older
  tarballs during review.

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 3.3.3-2
- ExcludeArch s390(x) as there's no hardware support there

* Thu Dec 03 2009 Doug Ledford <dledford@redhat.com> - 3.3.3-1
- Update to latest upstream release
- Minor tweaks to init script for LSB compliance

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Doug Ledford <dledford@redhat.com> - 3.3.2-1
- Update to latest upstream version

* Wed Apr 22 2009 Doug Ledford <dledford@redhat.com> - 3.3.1-1
- Update to latest upstream version

* Fri Mar 06 2009 Caolán McNamara <caolanm@redhat.com> - 3.2.1-3
- fix bare elifs to rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 3.2.1-1
- Initial package for Fedora review process
