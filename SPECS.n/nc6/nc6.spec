Summary:        Netcat with IPv6 Support
Name:           nc6
Version:        1.0
Release:        21%{?dist}
Group:          Applications/Internet
URL:            http://www.deepspace6.net/projects/netcat6.html
License:        GPLv2+
Source:         ftp://ftp.deepspace6.net/pub/ds6/sources/nc6/%{name}-%{version}.tar.bz2
# Given that the trailing newlines are now a part of the comments,
# some macros with comments on the same line break.
Patch0:         %{name}-1.0-dnl.patch
# rhbz#1161432
Patch1:         %{name}-1.0-afindep-close-the-accepted-socket-when-done.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel

%description
netcat6 is an IPv6-enabled clone of the original netcat utility.

"Netcat is a simple Unix utility which reads and writes data across
network connections.  It is designed to be a reliable "back-end" tool
that can be used directly or easily driven by other programs and
scripts.  At the same time, it is a feature-rich network debugging and
exploration tool, since it can create almost any kind of connection you
would need and has several interesting built-in capabilities.  Netcat,
or "nc" as the actual program is named, should have been supplied long
ago as another one of those cryptic but standard Unix tools."

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
autoreconf -fiv
%configure --prefix=%{_prefix} --mandir=%{_mandir} CFLAGS="%{optflags} -D_GNU_SOURCE"
make %{?_smp_mflags}

%install
make DESTDIR="%{buildroot}" install

%files
%{_bindir}/%{name}
%doc %{_mandir}/man1/nc6.1*
%doc README AUTHORS COPYING NEWS TODO

%changelog
* Fri Nov 07 2014 Petr Šabata <contyk@redhat.com> - 1.0-21
- Close sockets after the client disconnects (#1161432)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Petr Šabata <contyk@redhat.com> - 1.0-19
- Fix FTBFS with the current autoconf

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Petr Šabata <contyk@redhat.com> - 1.0-16
- Upstream bootstrap isn't enough; call autoreconf -fiv instead

* Mon Mar 25 2013 Petr Šabata <contyk@redhat.com> - 1.0-15
- Run bootstrap to utilize Fedora autoconf (#926203)
- Minor cleanup
- Build in parallel

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 01 2011 Petr Sabata <psabata@redhat.com> - 1.0-11
- Buildroot garbage cleanup

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-7
- fix license tag

* Tue Feb 12 2008 Jan Safranek <jsafrane@redhat.com> 1.0-6
- fix compilation with gcc 4.3

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> 1.0-5
- rebuilt

* Mon Sep 11 2006 Radek Vokal <rvokal@redhat.com> 1.0-4
- rebuilt for FC6

* Mon Mar 13 2006 Radek Vokál <rvokal@redhat.com> 1.0-3
- add ?dist and rebuilt in extras

* Wed Mar 8 2006 Radek Vokál <rvokal@redhat.com> 1.0-2
- clean RPM_BUILD_ROOT before install
- group Application/Internet
- fix BuildRoot

* Tue Mar 7 2006 Radek Vokál <rvokal@redhat.com> 1.0-1
- initial build for Fedora Extras
