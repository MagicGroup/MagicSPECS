# RHEL6 still has ancient GnuTLS
%define use_gnutls 0%{?fedora} || 0%{?rhel} >= 7

# RHEL5 has no libproxy, and no %make_install macro
%if 0%{?rhel} && 0%{?rhel} <= 5
%define use_libproxy 0
%define make_install %{__make} install DESTDIR=%{?buildroot}
%define use_tokens 0
%else
%define use_libproxy 1
%define use_tokens 1
%endif

Name:		openconnect
Version:	7.02
Release:	2%{?dist}
Summary:	Open client for Cisco AnyConnect VPN

Group:		Applications/Internet
License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source0:	ftp://ftp.infradead.org/pub/openconnect/openconnect-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	pkgconfig(openssl) pkgconfig(libxml-2.0)
BuildRequires:	autoconf automake libtool python gettext
%if 0%{?fedora} || 0%{?rhel} >= 7
Obsoletes:	openconnect-lib-compat%{?_isa} < %{version}-%{release}
Requires:	vpnc-script
%else
Requires:	vpnc
%endif

%if %{use_gnutls}
BuildRequires:	pkgconfig(gnutls) trousers-devel pkgconfig(libpcsclite)
%endif
%if %{use_libproxy}
BuildRequires:	pkgconfig(libproxy-1.0)
%endif
%if %{use_tokens}
BuildRequires:  pkgconfig(liboath) pkgconfig(stoken)
%endif

%description
This package provides a client for the Cisco AnyConnect VPN protocol, which
is based on HTTPS and DTLS.

%package devel
Summary: Development package for OpenConnect VPN authentication tools
Group: Applications/Internet
Requires: %{name}%{?_isa} = %{version}-%{release}
# RHEL5 needs these spelled out because it doesn't automatically infer from pkgconfig
%if 0%{?rhel} && 0%{?rhel} <= 5
Requires: openssl-devel zlib-devel
%endif

%description devel
This package provides the core HTTP and authentication support from
the OpenConnect VPN client, to be used by GUI authentication dialogs
for NetworkManager etc.

%prep
%setup -q

%build
%configure	--with-vpnc-script=/etc/vpnc/vpnc-script \
%if !%{use_gnutls}
		--with-openssl --without-openssl-version-check \
%endif
		--htmldir=%{_docdir}/%{name}
make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libopenconnect.la
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/libopenconnect.so.5*
%{_sbindir}/openconnect
%{_mandir}/man8/*
%doc TODO COPYING.LGPL

%files devel
%defattr(-,root,root,-)
%{_libdir}/libopenconnect.so
/usr/include/openconnect.h
%{_libdir}/pkgconfig/openconnect.pc

%changelog
* Sun Jan 04 2015 Liu Di <liudidi@gmail.com> - 7.02-2
- 为 Magic 3.0 重建

* Fri Dec 19 2014 David Woodhouse <David.Woodhouse@intel.com> - 7.02-1
- Update to 7.02 release (#1175951)

* Sun Dec 07 2014 David Woodhouse <David.Woodhouse@intel.com> - 7.01-1
- Update to 7.01 release

* Thu Nov 27 2014 David Woodhouse <David.Woodhouse@intel.com> - 7.00-2
- Add upstreamed version of Nikos' curve patch with version.c fixed

* Thu Nov 27 2014 David Woodhouse <David.Woodhouse@intel.com> - 7.00-1
- Update to 7.00 release

* Tue Sep 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 6.00-2
- When compiling with old gnutls version completely disable ECDHE instead
  of disabling the curves.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 David Woodhouse <David.Woodhouse@intel.com> - 6.00-1
- Update to 6.00 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 David Woodhouse <David.Woodhouse@intel.com> - 5.99-1
- Update to 5.99 release

* Wed Jan 01 2014 David Woodhouse <David.Woodhouse@intel.com> - 5.02-1
- Update to 5.02 release (#981911, #991653, #1031886)

* Sat Aug 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 5.01-4
- Fix install of docs

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 David Woodhouse <David.Woodhouse@intel.com> - 5.01-2
- Build with stoken and OATH support.

* Sat Jun 01 2013 David Woodhouse <David.Woodhouse@intel.com> - 5.01-1
- Update to 5.01 release (#955710, #964329, #964650)

* Wed May 15 2013 David Woodhouse <David.Woodhouse@intel.com> - 5.00-1
- Update to 5.00 release

* Thu Feb 07 2013 David Woodhouse <David.Woodhouse@intel.com> - 4.99-1
- Update to 4.99 release

* Fri Aug 31 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.07-2
- Obsolete openconnect-lib-compat (#842840)

* Fri Aug 31 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.07-1
- Update to 4.07 release (Fix #845636 CSTP write stall handling)

* Mon Jul 23 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.06-1
- Update to 4.06 release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.05-1
- Update to 4.05 release (PKCS#11 fixes)

* Thu Jul 05 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.04-1
- Update to 4.04 release (Fix PKCS#8 password handling)

* Mon Jul 02 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.03-1
- Update to 4.03 release (#836558)

* Thu Jun 28 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.02-1
- Update to 4.02 release

* Thu Jun 28 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.01-1
- Update to 4.01 release

* Thu Jun 21 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.00-3
- Remove zlib from openconnect.pc dependencies

* Thu Jun 21 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.00-2
- Fix dependencies for RHEL[56]

* Wed Jun 20 2012 David Woodhouse <David.Woodhouse@intel.com> - 4.00-1
- Update to 4.00 release

* Wed Jun 20 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-8
- Add support for building on RHEL[56]

* Wed Jun 20 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-7
- Add OpenSSL encrypted PEM file support for GnuTLS

* Mon Jun 18 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-6
- Fix crash on cleanup when no client certificate is set (#833141)

* Sat Jun 16 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-5
- Enable building compatibility libopenconnect.so.1

* Thu Jun 14 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-4
- Last patch needs autoreconf

* Thu Jun 14 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-3
- Fix library not to reference OpenSSL symbols when linked against GnuTLS 2

* Thu Jun 14 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-2
- Fix GnuTLS BuildRequires

* Thu Jun 14 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.99-1
- Update to OpenConnect v3.99, use GnuTLS (enables PKCS#11 support)

* Sat May 19 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.20-2
- openconnect-devel package should require precisely matching openconnect

* Fri May 18 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.20-1
- Update to 3.20.

* Thu May 17 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.19-1
- Update to 3.19.

* Thu Apr 26 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.18-1
- Update to 3.18.

* Fri Apr 20 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.17-1
- Update to 3.17.

* Sun Apr 08 2012 David Woodhouse <David.Woodhouse@intel.com> - 3.16-1
- Update to 3.16.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.15-1
- Update to 3.15.

* Fri Sep 30 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.14-1
- Update to 3.14.

* Fri Sep 30 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.13-1
- Update to 3.13. (Add localisation support, --cert-expire-warning)

* Mon Sep 12 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.12-1
* Update to 3.12. (Fix DTLS compatibility issue with new ASA firmware)

* Wed Jul 20 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.11-1
- Update to 3.11. (Fix compatibility issue with servers requiring TLS)

* Thu Jun 30 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.10-1
- Update to 3.10. (Drop static library, ship libopenconnect.so.1)

* Tue Apr 19 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.02-2
- Fix manpage (new tarball)

* Tue Apr 19 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.02-1
- Update to 3.02.

* Thu Mar 17 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.01-2
- Provide openconnect-devel-static (#688349)

* Wed Mar  9 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.01-1
- Update to 3.01.

* Wed Mar  9 2011 David Woodhouse <David.Woodhouse@intel.com> - 3.00-1
- Update to 3.00.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 21 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.26-4
- Fix bug numbers in changelog

* Wed Sep 29 2010 jkeating - 2.26-3
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.26-1
- Update to 2.26. (#629979: SIGSEGV in nm-openconnect-auth-dialog)

* Thu Aug 12 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.25-2
- Rebuild for new libproxy

* Sat May 15 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.25-1
- Update to 2.25.

* Fri May  7 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.24-1
- Update to 2.24.

* Fri Apr  9 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.23-1
- Update to 2.23.

* Sun Mar  7 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.22-1
- Update to 2.22. (Works around server bug in ASA version 8.2.2.5)

* Sun Jan 10 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.21-1
- Update to 2.21.

* Mon Jan  4 2010 David Woodhouse <David.Woodhouse@intel.com> - 2.20-1
- Update to 2.20.

* Mon Dec  7 2009 David Woodhouse <David.Woodhouse@intel.com> - 2.12-1
- Update to 2.12.

* Tue Nov 17 2009 David Woodhouse <David.Woodhouse@intel.com> - 2.11-1
- Update to 2.11.

* Wed Nov  4 2009 David Woodhouse <David.Woodhouse@intel.com> - 2.10-1
- Update to 2.10.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.01-3
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 David Woodhouse <David.Woodhouse@intel.com> - 2.01-1
- Update to 2.01.

* Wed Jun  3 2009 David Woodhouse <David.Woodhouse@intel.com> - 2.00-1
- Update to 2.00.

* Wed May 27 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.40-1
- Update to 1.40.

* Wed May 13 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.30-1
- Update to 1.30.

* Fri May  8 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.20-1
- Update to 1.20.

* Tue Apr 21 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.10-2
- Require openssl0.9.8k-4, which has all required DTLS patches.

* Wed Apr  1 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.10-1
- Update to 1.10.

* Wed Mar 18 2009 David Woodhouse <David.Woodhouse@intel.com> - 1.00-1
- Update to 1.00.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.99-2
- rebuild with new openssl

* Tue Dec 16 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.99-1
- Update to 0.99.
- Fix BuildRequires

* Mon Nov 24 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.98-1
- Update to 0.98.

* Thu Nov 13 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.97-1
- Update to 0.97. Add man page, validate server certs.

* Tue Oct 28 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.96-1
- Update to 0.96. Handle split-includes, MacOS port, more capable SecurID.

* Thu Oct 09 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.95-1
- Update to 0.95. A few bug fixes.

* Thu Oct 09 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.94-3
- Include COPYING.LGPL file

* Tue Oct 07 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.94-2
- Fix auth-dialog crash

* Mon Oct 06 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.94-1
- Take cookie on stdin so it's not visible in ps.
- Support running 'script' and passing traffic to it via a socket
- Fix abort when fetching XML config fails

* Sun Oct 05 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.93-1
- Work around unexpected disconnection (probably OpenSSL bug)
- Handle host list and report errors in NM auth dialog

* Sun Oct 05 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.92-1
- Rename to 'openconnect'
- Include NetworkManager auth helper

* Thu Oct 02 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.91-1
- Update to 0.91

* Thu Oct 02 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.90-1
- First package
