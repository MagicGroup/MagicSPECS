# Define pkgdocdir for releases that don't define it already
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global _perldocdir %{_docdir}/perl-qpid-messaging-%{version}
%global _pythondocdir %{_docdir}/python-qpid-messaging-%{version}

Name:          qpid-cpp
Version:       0.34
Release:       4%{?dist}
Summary:       Libraries for Qpid C++ client applications
License:       ASL 2.0
URL:           http://qpid.apache.org

Source0:       http://www.apache.org/dist/qpid/cpp/%{version}/%{name}-%{version}.tar.gz
Patch0001:     0001-NO-JIRA-qpidd.service-file-for-use-on-Fedora.patch
Patch0002:     0002-NO-JIRA-Allow-overriding-the-Perl-install-location.patch
Patch0003:     0003-NO-JIRA-Allow-overriding-the-Ruby-install-location.patch
Patch4:        qpid-boost-test-message.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: libtool
BuildRequires: doxygen
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: python
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: cyrus-sasl-devel
BuildRequires: cyrus-sasl-lib
BuildRequires: cyrus-sasl
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: libuuid-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: xqilla-devel
BuildRequires: xerces-c-devel
BuildRequires: libaio-devel
BuildRequires: qpid-proton-c-devel%{?_isa} >= 0.10
BuildRequires: libdb-devel
BuildRequires: libdb4-cxx-devel
BuildRequires: swig
BuildRequires: perl(ExtUtils::MakeMaker)

%ifnarch s390 s390x
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
%endif


%description

Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.



%package client
Summary:   Libraries for Qpid C++ client applications

Provides:  qpid(cpp-client)%{?_isa} = %{version}-%{release}

Requires:  boost
Requires:  chkconfig
Requires:  initscripts
Requires:  qpid-proton-c%{?_isa} >= 0.10

%description client
Run-time libraries for AMQP client applications developed using Qpid
C++. Clients exchange messages with an AMQP message broker using
the AMQP protocol.

%files client
%doc DESIGN
%doc LICENSE
%doc NOTICE
%doc README.txt
%doc RELEASE_NOTES
%{_libdir}/libqpidcommon.so*
%{_libdir}/libqpidclient.so*
%{_libdir}/libqpidtypes.so*
%{_libdir}/libqpidmessaging.so*
%dir %{_libdir}/qpid

%ifnarch s390 s390x
%{_libdir}/qpid/client/*
%endif

%ifnarch s390 s390x
%exclude %{_libdir}/qpid/client/rdmaconnector.so*
%endif

%dir %{_sysconfdir}/qpid
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig



%package client-devel
Summary:   Header files, documentation and testing tools for developing Qpid C++ clients

Provides:  qpid(cpp-client-devel)%{?_isa} = %{version}-%{release}
Requires:  qpid(cpp-client)%{?_isa} = %{version}-%{release}
Requires:  boost-devel
Requires:  boost-filesystem
Requires:  boost-program-options
Requires:  libuuid-devel
Requires:  python

%description client-devel
Libraries and header files for developing AMQP clients in C++ using Qpid.
Qpid implements the AMQP messaging specification.

%files client-devel
%dir %{_includedir}/qpid
%{_includedir}/qpid/*.h
%{_includedir}/qpid/qpid.i
%{_includedir}/qpid/swig_perl_typemaps.i
%{_includedir}/qpid/swig_python_typemaps.i
%{_includedir}/qpid/swig_ruby_typemaps.i
%{_includedir}/qpid/client
%{_includedir}/qpid/framing
%{_includedir}/qpid/sys
%{_includedir}/qpid/messaging
%{_includedir}/qpid/types
%{_libdir}/libqpidcommon.so
%{_libdir}/libqpidclient.so
%{_libdir}/libqpidtypes.so
%{_libdir}/libqpidmessaging.so
%{_libdir}/pkgconfig/qpid.pc
%{_datadir}/qpid
%defattr(755,root,root,-)
%{_bindir}/qpid-perftest
%{_bindir}/qpid-topic-listener
%{_bindir}/qpid-topic-publisher
%{_bindir}/qpid-latency-test
%{_bindir}/qpid-client-test
%{_bindir}/qpid-txtest
%{_bindir}/qpid-ping
%{_bindir}/qpid-txtest2
%{_bindir}/qpid-send
%{_bindir}/qpid-receive
%{_libexecdir}/qpid/tests
%{_libdir}/cmake/Qpid

%post client-devel -p /sbin/ldconfig

%postun client-devel -p /sbin/ldconfig



%package client-devel-docs
Summary:   AMQP client development documentation

BuildArch: noarch

%description client-devel-docs
This package includes the AMQP clients development documentation in HTML
format for easy browsing.

%files client-devel-docs
%doc %{_pkgdocdir}



%package server
Summary:   An AMQP message broker daemon

Provides:  qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires:  cyrus-sasl
Requires:  qpid-proton-c%{?_isa} >= 0.10

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description server
A message broker daemon that receives stores and routes messages using
the open AMQP messaging protocol.

%files server
%{_libdir}/libqpidbroker.so.*
%{_sbindir}/qpidd
%{_unitdir}/qpidd.service
%config(noreplace) %{_sysconfdir}/qpid/qpidd.conf
%config(noreplace) %{_sysconfdir}/sasl2/qpidd.conf
%dir %{_libdir}/qpid/daemon
%{_libdir}/qpid/daemon/amqp.so
%attr(755, qpidd, qpidd) %{_localstatedir}/lib/qpidd
%ghost %attr(755, qpidd, qpidd) /var/run/qpidd
%doc %{_mandir}/man1/qpidd*

%pre server
getent group qpidd >/dev/null || groupadd -r qpidd
getent passwd qpidd >/dev/null || \
  useradd -r -M -g qpidd -d %{_localstatedir}/lib/qpidd -s /sbin/nologin \
    -c "Owner of Qpidd Daemons" qpidd
exit 0

%post server
%systemd_post qpidd.service

%preun server
%systemd_preun qpidd.service

%postun server
%systemd_postun_with_restart qpidd.service
/sbin/ldconfig

# === Package: qpid-cpp-server-devel ===

%package server-devel
Summary: Libraries and header files for developing Qpid broker extensions
Group: Development/System
Requires: %{name}-client-devel = %{version}-%{release}
Requires: %{name}-server = %{version}-%{release}
Requires: boost-filesystem
Requires: boost-program-options
Obsoletes: qpidd-devel <= %{version}

%description server-devel
Libraries and header files for developing extensions to the
Qpid broker daemon.

%files server-devel
%defattr(-,root,root,-)
%_libdir/libqpidbroker.so

%post server-devel
/sbin/ldconfig

%postun server-devel
/sbin/ldconfig

%package server-ha
Summary: Provides extensions to the AMQP message broker to provide high availability

Provides: qpid(cpp-server-ha)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires: qpid-qmf%{?_isa}
# for systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description server-ha
%{summary}.

%files server-ha
%{_unitdir}/qpidd-primary.service
%{_libdir}/qpid/daemon/ha.so
%doc README-HA.txt

%post server-ha
/sbin/ldconfig
%systemd_post qpidd-primary.service

%preun server-ha
%systemd_preun qpidd-primary.service

%postun server-ha
%systemd_postun_with_restart qpidd-primary.service
/sbin/ldconfig



%ifnarch s390 s390x
%package client-rdma
Summary:  RDMA Protocol support (including Infiniband) for Qpid clients

Provides: qpid(cpp-client-rdma)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-client)%{?_isa} = %{version}-%{release}

%description client-rdma
A client plugin and support library to support RDMA protocols (including
Infiniband) as the transport for Qpid messaging.

%files client-rdma
%{_libdir}/librdmawrap.so*
%{_libdir}/qpid/client/rdmaconnector.so*
%config(noreplace) %{_sysconfdir}/qpid/qpidc.conf

%post client-rdma -p /sbin/ldconfig

%postun client-rdma -p /sbin/ldconfig



%package server-rdma
Summary:   RDMA Protocol support (including Infiniband) for the Qpid daemon

Provides: qpid(cpp-server-rdma)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-client-rdma)%{?_isa} = %{version}-%{release}

%description server-rdma
A Qpid daemon plugin to support RDMA protocols (including Infiniband) as the
transport for AMQP messaging.

%files server-rdma
%{_libdir}/qpid/daemon/rdma.so

%post server-rdma -p /sbin/ldconfig

%postun server-rdma -p /sbin/ldconfig
%endif



%package server-xml
Summary:  XML extensions for the Qpid daemon

Provides: qpid(cpp-server-xml)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires: xqilla
Requires: xerces-c

%description server-xml
A Qpid daemon plugin to support extended XML-based routing of AMQP
messages.

%files server-xml
%{_libdir}/qpid/daemon/xml.so

%post server-xml -p /sbin/ldconfig

%postun server-xml -p /sbin/ldconfig



%package server-linearstore
Summary: Red Hat persistence extension to the Qpid messaging sytem

Provides: qpid(cpp-server-lineastore)%{?_isa} = %{version}-%{release}
Requires: qpid(cpp-server)%{?_isa} = %{version}-%{release}
Requires: db4
Requires: libaio
Obsoletes: qpid-cpp-server-store <= %{version}
Obsoletes: qpid(cpp-server-store)%{?_isa} <= %{version}

%description server-linearstore
Red Hat persistence extension to the Qpid AMQP broker: persistent message
storage using a libaio-based asynchronous journal.
%files server-linearstore
%{_libdir}/qpid/daemon/linearstore.so
%{_libdir}/liblinearstoreutils.so


%package -n perl-qpid-messaging
Summary:  Perl bindings for the QPid messaging framework

Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: qpid(cpp-client)%{?_isa} = %{version}-%{release}

# remove with qpid-cpp 0.36
Obsoletes: perl-qpid < %{version}
Provides:  perl-qpid = %{version}

%description -n perl-qpid-messaging
%{summary}.

%files -n perl-qpid-messaging
%{perl_vendorarch}/*
%doc LICENSE
%doc %{_perldocdir}



%package -n python-qpid-messaging
Summary: Python bindings for the Qpid messaging framework

Requires: python
Requires: qpid(cpp-client)%{?_isa} = %{version}-%{release}
Requires: python-qpid-common

# remove with qpid-cpp 0.36
Obsoletes: python-qpid_messaging < %{version}
Provides:  python-qpid_messaging = %{version}-%{release}

%{?filter_setup:
  %filter_provides_in %{python_sitearch}/.*\.so$
  %filter_setup}

%description -n python-qpid-messaging
%{summary}.

%files -n python-qpid-messaging
%doc LICENSE
%{python2_sitearch}/qpid_messaging.py*
%{python2_sitearch}/_qpid_messaging.so
%{_pythondocdir}/examples



%prep
%setup -q -n qpid-cpp-%{version}

%patch0001 -p2
%patch0002 -p3
%patch0003 -p3
%patch4 -p1



%global perftests "qpid-perftest qpid-topic-listener qpid-topic-publisher qpid-latency-test qpid-client-test qpid-txtest qpid-ping qpid-txtest2"


%build
%cmake -DDOC_INSTALL_DIR:PATH=%{_pkgdocdir} \
       -DBUILD_LEGACYSTORE=false \
       -DBUILD_LINEARSTORE=true \
       -DPERL_PFX_ARCHLIB=%{perl_vendorarch} \
       -DBUILD_BINDING_RUBY=false \
       .
make %{?_smp_mflags}
make docs-user-api


%install
mkdir -p -m0755 %{buildroot}/%{_bindir}
mkdir -p -m0755 %{buildroot}/%{_unitdir}

# install examples
mkdir -p -m0755 %{buildroot}%{_perldocdir}/examples
mkdir -p -m0755 %{buildroot}%{_pythondocdir}/examples

pushd bindings/qpid/examples/perl
install -pm 644 * %{buildroot}%{_perldocdir}/examples
popd

pushd bindings/qpid/examples/python
install -pm 644 * %{buildroot}%{_pythondocdir}/examples
popd

make install DESTDIR=%{buildroot}/

# clean up items we're not installing
rm -f  %{buildroot}/%{_bindir}/qmf*
rm -f  %{buildroot}/%{_bindir}/qpid-python-test
rm -rf %{buildroot}/%{_includedir}/qmf
rm -f  %{buildroot}/%{_libdir}/libcqpid_perl.so
rm -f  %{buildroot}/%{_libdir}/ruby/cqpid.so
rm -f  %{buildroot}/%{ruby_sitelib}
rm -rf %{buildroot}/%{_libdir}/*qmf*
rm -f  %{buildroot}/%{_libdir}/pkgconfig/qmf2.pc
rm -rf %{buildroot}/%{python2_sitearch}/qpid_python*egg-info
rm -rf %{buildroot}/%{python2_sitearch}/mllib
rm -rf %{buildroot}/%{python2_sitearch}/qpid
rm -rf %{buildroot}/%{python2_sitelib}/qmfgen
rm -rf %{buildroot}/%{python2_sitelib}/qpidtoollibs
rm -rf %{buildroot}/%{python2_sitearch}/*qmf*
rm -rf %{buildroot}/%{_libdir}/qpid/daemon/store.so*
rm -rf %{buildroot}/%{_initrddir}/qpidd-primary

# install systemd files
mkdir -p %{buildroot}/%{_unitdir}
install -pm 644 %{_builddir}/qpid-cpp-%{version}/cpp/etc/qpidd.service \
    %{buildroot}/%{_unitdir}
install -pm 644 %{_builddir}/qpid-cpp-%{version}/cpp/etc/qpidd-primary.service \
    %{buildroot}/%{_unitdir}
rm -f %{buildroot}/%{_initrddir}/qpidd
rm -f %{buildroot}/%{_sysconfdir}/init.d/qpidd.service

# install perftests utilities
mkdir -p %{buildroot}/%{_bindir}
pushd src/tests
for ptest in %{perftests}; do
  libtool --mode=install install -m755 $ptest %{buildroot}/%{_bindir}
done
popd

mkdir -p %{buildroot}/%{_localstatedir}/run
touch %{buildroot}/%{_localstatedir}/run/qpidd
mkdir -p %{buildroot}/%{_localstatedir}/lib/qpidd

# clean up leftover ruby files
rm -rf %{buildroot}/usr/local/%{_lib}/ruby/site_ruby

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%changelog
* Thu Sep 03 2015 Jonathan Wakely <jwakely@redhat.com> - 0.34-4
- Rebuilt for Boost 1.59

* Wed Sep  2 2015 Irina Boverman <iboverma@redhat.com> - 0.34-3
- Rebuilt against qpid-proton-0.10-1

* Sun Aug 30 2015 Jonathan Wakely <jwakely@redhat.com> 0.34-2
- Patched and rebuilt for Boost 1.59
- Rebased to 0.34
- Rebuilt against qpid-proton-0.10-1
- Added qpid-cpp-server-devel
- Added qpid-send and qpid-qpid-receive to qpid-client-devel sub-package
- Removed python-qpid-common, python-qpid, qpid-tools and qpid-server-store sub-packages
  Note: python-qpid-common and python-qpid will be 
        added to python-qpid package
        qpid-tools will be added to qpid-tools package

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.32-7
- rebuild for Boost 1.58

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.32-5
- Perl 5.22 rebuild

* Wed May 27 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-4
- Removed qpid-send and qpid-receive from qpid-cpp-client-devel.
* Fri May 22 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-3
- Include the qpid.tests module in python-qpid
- Resolves: BZ#1224260

* Mon Apr 13 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.32-2
- Re-add patch that fixes builds on aarch64/ppc64le

* Tue Apr  7 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-1.1
- Bumped the release to force a build against Proton 0.9 in F22.

* Mon Apr  6 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.32-1
- Rebased on Qpid 0.32.
- Added build flag to enable building the legacy store.
- Added the perl-qpid-messaging subpackage.
- Added the python-qpid-messaging subpackage.
- Added the python-qpid subpackage.

* Wed Feb 25 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-12
- Added qpidtoollibs to the qpid-tools package.

* Fri Feb 20 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-11
- Fixed path to qpid-ha in the systemd service descriptor.

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 0.30-10
- Bump for rebuild.

* Mon Feb  2 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-9
- Resolves: BZ#1186308

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.30-8
- Rebuild for boost 1.57.0

* Thu Jan 22 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-7
- Apply patch 10.

* Wed Jan 21 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-6
- Resolves: BZ#1184488

* Fri Jan 16 2015 Darryl L. Pierce <dpierce@redhat.com> - 0.30-5
- Resolves: BZ#1181721

* Wed Oct 29 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.30-4
- QPID-6170: Fixes builds on aarch64 and ppc64le architectures.

* Thu Oct  2 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.30-1
- Rebased on Qpid 0.30.
- Upstream tarball filename changed from qpid-##.#.tar.gz to qpid-cpp-##.#.tar.gz.
- qpid-tools moved out to a separate package.
- Moved qpid-send and qpid-receive to the qpid-cpp-client-devel package.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-7
- Removed ssl package references.

* Thu Aug 14 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-6
- Renamed the virtual provides to conform with project needs.

* Thu Jul 10 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-5
- Removed parameterized ldconfig.
- Removed comments between subpackages.
- * This is what appears to have caused the (post)install error messages.

* Thu Jul  3 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-4
- Parameterized ldconfig location based on RHEL/Fedora release.

* Tue Jun 10 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-3
- Fixes alignment issues on ARM platforms.
- Resolves: BZ#1106272

* Sat Jun  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.28-2
- Remove arm conditionals as we now have the dependencies
- Fix aarch64 defines (it's not arm64)

* Wed Jun  4 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.28-1
- Rebased on Qpid 0.28.

* Tue Jun  3 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-9
- Fixed dependency of server-ha on qpid(server).

* Wed May 28 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-8
- Fixed a few typos that slipped into the specfile for virtual packages.

* Tue May 27 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-7
- Added virtual packages for all binary subpackages.
- Updated requires to be for virtual packages.

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.26-6
- Rebuild for boost 1.55.0

* Thu May 22 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-5
- Removed the architecture macro from the virtual provides.

* Wed May 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-4
- Added virtual packages for qpid-cpp-client and -client-devel.y

* Wed May  7 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-3
- Changed qpid-cpp-server-ha to use systemd macros for pre/post/postun
- Resoves: BZ#1094928

* Fri Feb 21 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-2
- QPID-5499: Fix for building with -Werror=format-security enabled.
- * This was previously for files include in qpid-cpp-client-devel.

* Thu Feb 20 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.26-1
- Rebased on Qpid 0.26.
- Updated qpid-cpp-server-ha to be a systemd service.
- Removed qpid-cpp-server dependency on qpid-cpp-server-store.
- * The package was mistakenly including store libraries.
- Added BR for gcc-c++.
- Removed -n option from all subpackages.
- Removed clean and check sections.
- Updated package to use systemd macros correctly.
- Removed unnecessary BRs.
- Cleaned up the deletes after the build finishes.

* Wed Jan 22 2014 Darryl L. Pierce <dpierce@redhat.com> - 0.24-9
- Set qpidd service to start after the network service.
- QPID-5499: Updated the Swig descriptors.
- Resolves: BZ#1055660
- Resolves: BZ#1037295

* Wed Nov 27 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-8
- Removed rdma.so from the -server subpackage.
- Resolves: BZ#1035323

* Wed Nov 27 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-7
- Removed rdmaconnector.so from the -client subpackage.
- Resolves: BZ#1035323

* Fri Nov  1 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-6
- Removed the following subpackages:
- - qpid-qmf
- - qpid-qmf-devel
- - python-qpid-qmf
- - ruby-qpid-qmf
- Updated all QMF dependencies to not require the specific release.
- Removed the QMF header files from qpid-cpp-devel

* Thu Oct 10 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-5
- QPID-4582: Fix the legacy store when building on ARM
- QPID-5215: Legacy store tests
- Resolves: BZ#1010397

* Thu Sep 26 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-4.1
- Provide a symlink from /etc/qpid/qpidd.conf to /etc/qpidd.conf:
-  * this will be removed with the 0.26 release
-  * for upgrades any existing file is preserved for now
- Resolves: BZ#1012001

* Mon Sep 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-4
- Fixed dependencies on python-qmf to be python-qpid-qmf.

* Mon Sep 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-3
- Add arch checks for all requires to block potential multilib errors on upgrade.
- Added virtual provides for both obsoleted -ssl packages.
- Resolves: BZ#1010999

* Fri Sep 20 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-2
- Disabled building on ARM due to failure of the legacy store to build.

* Mon Sep 16 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.24-1
- Rebased on Qpid 0.24.
- Relocated qpidd.conf to /etc/qpid
- Trimmed old changelog entries due to bogus date complaints.
- Added fixes to support ARM as a primary platform.
- Build depends on qpid-proton 0.5.
- QPID-4938: Stop building ssl and acl support as separate plugin modules on Unix
- Cleaner encoding of index for delivery tags - QPID-5122
- QPID-5123: Changes to Fedora 19 packaging of libdb4 prevents legacystore from building
- QPID-5016: Legacy store not correctly initialising rmgr
- QPID-5126: Fix for building legacy store on ARM platforms

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.22-3
- Rebuild for boost 1.54.0

* Tue Jul  2 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-2
- Fixed adding the soversion to shared libraries.
- Resolves: BZ#980364

* Thu Jun 13 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.22-1
- Rebased on Qpid 0.22.
- The package now uses the CMake build system from Qpid.
- No longer use a separate source for the store.
- Resolves: BZ#616080
- Resolves: BZ#966780
- Resolves: BZ#967100

* Mon Mar 25 2013 Vít Ondruch <vondruch@redhat.com> - 0.20-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-5
- Moved the Qpidd swig descriptors to /usr/include/qpid
- Moved the QMF swig descriptors to /usr/include/qmf

* Tue Feb 12 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-4
- Moved Functor and MemFuncRef out of the definition of Handler.
- Resolves: BZ#910201

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.20-3
- Rebuild for Boost-1.53.0

* Mon Jan 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-2
- Fixed memory leak in Perl bindings typemap.
- Resolves: BZ#885149

* Wed Jan 23 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.20-1
- Rebased Qpid on release 0.20.
- Rebased Store on SVN revision 4521.
- Fixed builds on ARM system by disabling RDMA support.
- Added a check in the store for ARM architecture.
- Resolves: BZ#820282

* Mon Nov 12 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-6
- Changed qpidd.service to not start until after networking.

* Tue Oct 16 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-5
- Install CMake file for C++ messaging examples.
- Moved qfm2.pc from qpid-qmf to qpid-qmf-devel
- Resolves: BZ#866892

* Sat Oct 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-4
- Fixed building C++ messaging examples.
- Fixed ownership for /usr/share/qpidc and /usr/shar/qpidc/messaging
- Resolves: BZ#802791
- Resolves: BZ#756927

* Wed Oct 10 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3.2
- Fixed reference to systemctl.
- Resolves: BZ#864987

* Wed Oct 10 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3.1
- Added space to fix conditional.
- Resolves: BZ#864792

* Wed Sep 26 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-3
- Removed the perl-qpid subpackage.

* Fri Sep 21 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-2
- Added systemd support.
- Removed SysVInit support.
- Related: BZ#832724

* Wed Sep  5 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.18-1
- Rebased on Qpid release 0.18.
- Added the new HA subpackage: qpid-cpp-server-ha
- Merged the qpid-cpp-server-daemon package back into qpid-cpp-server
- Resolves: BZ#854263
- qpid-cpp-server now provides qpid-cpp-server-daemon

* Mon Aug 20 2012 Dan Horák <dan[at]danny.cz> - 0.16-9
- allow build without InfiniBand eg. on s390(x)
- fix build on non-x86 64-bit arches

* Fri Aug 17 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-8
- Added the qpid-cpp-server-daemon subpackage.
  * This package delivers the SysVInit scripts needed by qpidd.

* Mon Aug 13 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-7
- QPID4095: Boost 1.50.0 has removed filesystem version 2 from the library

* Wed Aug  1 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-6.1
- Moved the QMF related swig descriptors to the qmf-devel package.

* Mon Jul 30 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-6
- Added patches for qpid-store to work with the new BDB packages.
- Added BR for libdb-devel and libdb4-cxx-devel, replacing db4-devel.

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-4
- Added the swig descriptor files to the client-devel package.

* Fri Jun 29 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-3
- Removed colons from conditions in QMF Ruby.
- Fixed string encoding for Ruby.

* Wed Jun 27 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-2
- Makes qmf/BrokerImportExport.h public.

* Mon Jun 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.16-1.5
- -server: Obsoletes -server-devel (and so it doesn't Obsoletes itself)

* Thu Jun 07 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.4
- Replaced the dependency on chkconfig and service binaries with packages.

* Wed Jun 06 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.3
- Fixed the Ruby directory macros to use the updated macros.

* Wed Jun 06 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.2
- Removed the qpid-cpp-server-devel subpackage.
  * qpid-cpp-server now obsoletes this as well.
- Removed macros that were defined for a shared specfile.
- Cleaned up the use of other macros.
- Cleaned up the package macros to be more consistent
- Fixed many rpmlint warnings and errors.

* Tue May 29 2012 Darryl L. Pierce <dpierce@redhat.com> - 0.16-1.1
- Release 0.16 of Qpid upstream.
- Removed non-Fedora conditional areas of the specfile.
- Changed the location of qmfgen to the python sitelib directory.

* Tue Apr 17 2012 Dan Horák <dan[at]danny.cz> - 0.14-1.3
- fix build when size_t != unsigned int

* Tue Mar 20 2012 Nuno Santos <nsantos@redhat.com> - 0.14-3.1
- BZ692583 - QMF header files are in the wrong RPM

* Tue Mar 20 2012 Nuno Santos <nsantos@redhat.com> - 0.14-2.1
- BZ756927 - Spec file fixes for qpid-cpp

* Thu Feb 16 2012 Nuno Santos <nsantos@redhat.com> - 0.14-1.1
- Rebased to sync with upstream's official 0.14 release

* Wed Jan 18 2012 Nuno Santos <nsantos@redhat.com> - 0.12-7.1
- Added missing subpackage dependency

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
