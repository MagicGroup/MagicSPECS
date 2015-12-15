Name:           isns-utils
Version:        0.94
Release:        1%{?dist}
Summary:        The iSNS daemon and utility programs

Group:          System Environment/Daemons
License:        LGPLv2+
URL:            https://github.com/gonzoleeman/open-isns
Source0:        https://github.com/gonzoleeman/open-isns/archive/%{version}.tar.gz#/open-isns-%{version}.tar.gz
Source1:        isnsd.service

BuildRequires:  openssl-devel automake pkgconfig systemd-devel systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.


%package devel
Group: Development/Libraries
Summary: Development files for iSNS

%description devel
Development files for iSNS


%prep
%setup -q -n open-isns-%{version}


%build
%configure
make %{?_smp_mflags}


%install
sed -i -e 's|-m 555|-m 755|' Makefile
make install DESTDIR=%{buildroot}
make install_hdrs DESTDIR=%{buildroot}
make install_lib DESTDIR=%{buildroot}
rm %{buildroot}%{_unitdir}/isnsd.service
rm %{buildroot}%{_unitdir}/isnsd.socket
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/isnsd.service


%post
%systemd_post isnsd.service


%postun
%systemd_postun isnsd.service


%preun
%systemd_preun isnsd.service


%triggerun -- isns-utils < 0.91-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save isnsd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del isnsd >/dev/null 2>&1 || :
/bin/systemctl try-restart isnsd.service >/dev/null 2>&1 || :


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_mandir}/man8/*
%{_unitdir}/isnsd.service
%dir %{_sysconfdir}/isns
%dir %{_var}/lib/isns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/isns/*


%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/libisns
%{_includedir}/libisns/*.h
%{_libdir}/libisns.a


%changelog
* Mon Oct 05 2015 Chris Leech <cleech@redhat.com> - 0.94-1
- new upstream location, update to 0.94
- new devel package, upstream open-iscsi is dropping it's internal copy

* Wed Jun 17 2015 Chris Leech <cleech@redhat.com> - 0.93-8
- use of systemd rpm macros now require systemd as a BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.93-4
- Fix FTBFS, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 10 2012 Chris Leech <cleech@redhat.com> - 0.93-1
- Rebase to 0.93
- Make use of systemd rpm macros for scriptlets, BZ 850174

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Jon Ciesla <limburgher@gmail.com> - 0.91-7
- Migrate to systemd, BZ 789707.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-1
- rebuild with new openssl

* Wed Jan 16 2008 Mike Christie <mchristie@redhat.com> - 0.91-0.0
- first build
