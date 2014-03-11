Name:           nbd
Version:        2.9.20
Release:        4%{dist}
Summary:        Network Block Device user-space tools (TCP version)

Group:          Applications/System
License:        GPL+
URL:            http://nbd.sourceforge.net/
Source0:        http://downloads.sourceforge.net/nbd/nbd-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  glib2-devel

%description 
Tools for the Linux Kernel's network block device, allowing you to use
remote block devices over a TCP/IP network.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README simple_test nbd-tester-client.c cliserv.h
%{_mandir}/man*/nbd*
%{_bindir}/nbd-server
%{_sbindir}/nbd-client

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 2.9.20-4
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 2.9.20-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 2.9.20-1
- Update to 2.9.20: fix CVE-2005-3534, BZ#673562

* Fri Mar 26 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 2.9.15-1
- Update to 2.9.15
- Remove file dep on stubs-32.h, doesn't seem to be necessary anymore

* Thu Aug  6 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 2.9.13-1
- Update to 2.9.13
- Dropped nbd-module.patch (merged upstream)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 2.9.12-1
- Update to 2.9.12 (resolves BZ#454099).
- Added nbd-module.patch (resolves BZ#496751).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 09 2008 Warren Togami <wtogami@redhat.com> - 2.9.10-1
- match nbd in kernel-2.6.24+
- remove 32bit crack from x86_64 that made no sense

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.9.7-5
- Autorebuild for GCC 4.3

* Wed Nov 07 2007 Warren Togami <wtogami@redhat.com> 2.9.7-4
- include nbd-client i386 in x86-64 RPM because initrd images need it

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-3
- add buildrequires

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-2
- package cleanups

* Sat Oct 13 2007 Eric Harrison <eharrison@mesd.k12.or.us> 2.9.7-1
- update to 2.9.7

