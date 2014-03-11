Name:		perl-IO-Socket-SSL
Version:	1.77
Release:	2%{?dist}
Summary:	Perl library for transparent SSL
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/IO-Socket-SSL/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(IO::Socket)
BuildRequires:	perl(Net::LibIDN)
BuildRequires:	perl(Net::SSLeay) >= 1.21
BuildRequires:	procps
# Use IO::Socket::IP for IPv6 support where available, else IO::Socket::INET6
%if 0%{?fedora} > 15 || 0%{?rhel} > 6
BuildRequires:	perl(IO::Socket::IP) >= 0.11, perl(Socket) >= 1.95
Requires:	perl(IO::Socket::IP) >= 0.11, perl(Socket) >= 1.95
%else
BuildRequires:	perl(IO::Socket::INET6), perl(Socket6)
Requires:	perl(IO::Socket::INET6), perl(Socket6)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Net::LibIDN)

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc BUGS Changes README docs/ certs/ example/ util/
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Socket::SSL.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.77-2
- 为 Magic 3.0 重建

* Fri Oct  5 2012 Paul Howarth <paul@city-fan.org> - 1.77-1
- Update to 1.77
  - support _update_peer for IPv6 too (CPAN RT#79916)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.76-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Paul Howarth <paul@city-fan.org> - 1.76-1
- Update to 1.76
  - add support for IO::Socket::IP, which supports inet6 and inet4
    (CPAN RT#75218)
  - fix documentation errors (CPAN RT#77690)
  - made it possible to explicitly disable TLSv11 and TLSv12 in SSL_version
  - use inet_pton from either Socket.pm 1.95 or Socket6.pm
- Use IO::Socket::IP for IPv6 support where available, else IO::Socket::INET6
- Add runtime dependency for appropriate IPv6 support module so that we can
  ensure that we run at runtime what we tested with at build time

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.74-2
- Perl 5.16 rebuild

* Mon May 14 2012 Paul Howarth <paul@city-fan.org> - 1.74-1
- Update to 1.74
  - accept a version of SSLv2/3 as SSLv23, because older documentation could
    be interpreted like this

* Fri May 11 2012 Paul Howarth <paul@city-fan.org> - 1.73-1
- Update to 1.73
  - set DEFAULT_CIPHER_LIST to ALL:!LOW instead of HIGH:!LOW
  -  t/dhe.t hopefully work with more versions of openssl

* Wed May  9 2012 Paul Howarth <paul@city-fan.org> - 1.71-1
- Update to 1.71
  - 1.70 done right: don't disable SSLv2 ciphers; SSLv2 support is better
    disabled by the default SSL_version of 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.70-1
- Update to 1.70
  - make it possible to disable protocols using SSL_version, and make
    SSL_version default to 'SSLv23:!SSLv2'

* Tue May  8 2012 Paul Howarth <paul@city-fan.org> - 1.69-1
- Update to 1.69 (changes for CPAN RT#76929)
  - if no explicit cipher list is given, default to ALL:!LOW instead of the
    openssl default, which usually includes weak ciphers like DES
  - new config key SSL_honor_cipher_order and document how to use it to fight
    BEAST attack
  - fix behavior for empty cipher list (use default)
  - re-added workaround in t/dhe.t

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.66-1
- Update to 1.66
  - make it thread safer (CPAN RT#76538)

* Mon Apr 16 2012 Paul Howarth <paul@city-fan.org> - 1.65-1
- Update to 1.65
  - added NPN (Next Protocol Negotiation) support (CPAN RT#76223)

* Sat Apr  7 2012 Paul Howarth <paul@city-fan.org> - 1.64-1
- Update to 1.64
  - ignore die from within eval to s more stable on Win32
    (CPAN RT#76147)
  - clarify some behavior regarding hostname verification
- Drop patch for t/dhe.t, no longer needed

* Wed Mar 28 2012 Paul Howarth <paul@city-fan.org> - 1.62-1
- Update to 1.62
  - small fix to last version

* Tue Mar 27 2012 Paul Howarth <paul@city-fan.org> - 1.61-1
- Update to 1.61
  - call CTX_set_session_id_context so that server's session caching works with
    client certificates too (CPAN RT#76053)

* Tue Mar 20 2012 Paul Howarth <paul@city-fan.org> - 1.60-1
- Update to 1.60
  - don't make blocking readline if socket was set nonblocking, but return as
    soon no more data are available (CPAN RT#75910)
  - fix BUG section about threading so that it shows package as thread safe
    as long as Net::SSLeay ≥ 1.43 is used (CPAN RT#75749)
- BR: perl(constant), perl(Exporter) and perl(IO::Socket)

* Thu Mar  8 2012 Paul Howarth <paul@city-fan.org> - 1.59-1
- Update to 1.59
  - if SSLv2 is not supported by Net::SSLeay set SSL_ERROR with useful message
    when attempting to use it
  - modify constant declarations so that 5.6.1 should work again
- Drop %%defattr, redundant since rpm 4.4

* Mon Feb 27 2012 Paul Howarth <paul@city-fan.org> - 1.58-1
- Update to 1.58
  - fix t/dhe.t for openssl 1.0.1 beta by forcing TLSv1, so that it does not
    complain about the too small RSA key, which it should not use anyway; this
    workaround is not applied for older openssl versions, where it would cause
    failures (CPAN RT#75165)
- Add patch to fiddle the openssl version number in the t/dhe.t workaround
  because the OPENSSL_VERSION_NUMBER cannot be trusted in Fedora
- One buildreq per line for readability
- Drop redundant buildreq perl(Test::Simple)
- Always run full test suite

* Wed Feb 22 2012 Paul Howarth <paul@city-fan.org> - 1.56-1
- Update to 1.56
  - add automatic or explicit (via SSL_hostname) SNI support, needed for
    multiple SSL hostnames with the same IP (currently only supported for the
    client)
- Use DESTDIR rather than PERL_INSTALL_ROOT
- No need to delete empty directories from buildroot

* Mon Feb 20 2012 Paul Howarth <paul@city-fan.org> - 1.55-1
- Update to 1.55
  - work around IO::Socket's work around for systems returning EISCONN etc. on
    connect retry for non-blocking sockets by clearing $! if SUPER::connect
    returned true (CPAN RT#75101)

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 1.54-1
- Update to 1.54
  - return 0 instead of undef in SSL_verify_callback to fix uninitialized
    warnings (CPAN RT#73629)

* Mon Dec 12 2011 Paul Howarth <paul@city-fan.org> - 1.53-1
- Update to 1.53
  - kill child in t/memleak_bad_handshake.t if test fails (CPAN RT#73146)

* Wed Dec  7 2011 Paul Howarth <paul@city-fan.org> - 1.52-1
- Update to 1.52
  - fix for t/nonblock.t hangs on AIX (CPAN RT#72305)
  - disable t/memleak_bad_handshake.t on AIX, because it might hang
    (CPAN RT#72170)
  - fix syntax error in t/memleak_bad_handshake.t

* Fri Oct 28 2011 Paul Howarth <paul@city-fan.org> - 1.49-1
- Update to 1.49
  - another regression for readline fix: this time it failed to return lines
    at EOF that don't end with newline - extended t/readline.t to catch this
    case and the fix for 1.48

* Wed Oct 26 2011 Paul Howarth <paul@city-fan.org> - 1.48-1
- Update to 1.48
  - further fix for readline fix in 1.45: if the pending data were false (like
    '0'), it failed to read the rest of the line (CPAN RT#71953)

* Fri Oct 21 2011 Paul Howarth <paul@city-fan.org> - 1.47-1
- Update to 1.47
  - fix for 1.46 - check for mswin32 needs to be /i

* Tue Oct 18 2011 Paul Howarth <paul@city-fan.org> - 1.46-1
- Update to 1.46
  - skip signals test on Windows

* Thu Oct 13 2011 Paul Howarth <paul@city-fan.org> - 1.45-1
- Update to 1.45
  - fix readline to continue when getting interrupt waiting for more data
- BR: perl(Carp)

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.44-2
- Perl mass rebuild

* Fri May 27 2011 Paul Howarth <paul@city-fan.org> - 1.44-1
- Update to 1.44
  - fix invalid call to inet_pton in verify_hostname_of_cert when identity
    should be verified as ipv6 address because it contains a colon

* Wed May 11 2011 Paul Howarth <paul@city-fan.org> - 1.43-1
- Update to 1.43
  - add SSL_create_ctx_callback to have a way to adjust context on creation
    (CPAN RT#67799)
  - describe problem of fake memory leak because of big session cache and how
    to fix it (CPAN RT#68073)
  - fix t/nonblock.t
  - stability improvements for t/inet6.t

* Tue May 10 2011 Paul Howarth <paul@city-fan.org> - 1.41-1
- Update to 1.41
  - fix issue in stop_SSL where it did not issue a shutdown of the SSL
    connection if it first received the shutdown from the other side
  - try to make t/nonblock.t more reliable, at least report the real cause of
    SSL connection errors
- No longer need to re-code docs to UTF-8

* Mon May  2 2011 Paul Howarth <paul@city-fan.org> - 1.40-1
- Update to 1.40
  - fix in example/async_https_server
  - get IDN support from URI (CPAN RT#67676)
- Nobody else likes macros for commands

* Thu Mar  3 2011 Paul Howarth <paul@city-fan.org> - 1.39-1
- Update to 1.39
  - fixed documentation of http verification: wildcards in cn is allowed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Paul Howarth <paul@city-fan.org> - 1.38-1
- Update to 1.38
  - fixed wildcards_in_cn setting for http, wrongly set in 1.34 to 1 instead of
    anywhere (CPAN RT#64864)

* Fri Dec 10 2010 Paul Howarth <paul@city-fan.org> - 1.37-1
- Update to 1.37
  - don't complain about invalid certificate locations if user explicitly set
    SSL_ca_path and SSL_ca_file to undef: assume that user knows what they are
    doing and will work around the problems themselves (CPAN RT#63741)

* Thu Dec  9 2010 Paul Howarth <paul@city-fan.org> - 1.36-1
- Update to 1.36
  - update documentation for SSL_verify_callback based on CPAN RT#63743 and
    CPAN RT#63740

* Mon Dec  6 2010 Paul Howarth <paul@city-fan.org> - 1.35-1
- Update to 1.35 (addresses CVE-2010-4334)
  - if verify_mode is not VERIFY_NONE and the ca_file/ca_path cannot be
    verified as valid, it will no longer fall back to VERIFY_NONE but throw an
    error (http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=606058)

* Tue Nov  2 2010 Paul Howarth <paul@city-fan.org> - 1.34-1
- Update to 1.34
  - schema http for certificate verification changed to wildcards_in_cn=1
  - if upgrading socket from inet to ssl fails due to handshake problems, the
    socket gets downgraded back again but is still open (CPAN RT#61466)
  - deprecate kill_socket: just use close()

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.33-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Paul Howarth <paul@city-fan.org> - 1.33-1
- Update to 1.33
  - attempt to make t/memleak_bad_handshake.t more stable
  - fix hostname checking: only check an IP against subjectAltName GEN_IPADD

* Tue Feb 23 2010 Paul Howarth <paul@city-fan.org> - 1.32-1
- Update to 1.32 (die in Makefile.PL if Scalar::Util has no dualvar support)
- Use %%{_fixperms} macro instead of our own %%{__chmod} incantation

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.31-2
- Rebuild against perl 5.10.1

* Sun Sep 27 2009 Paul Howarth <paul@city-fan.org> - 1.31-1
- Update to 1.31 (see Changes for details)

* Thu Aug 20 2009 Paul Howarth <paul@city-fan.org> - 1.30-1
- Update to 1.30 (fix memleak when SSL handshake failed)
- Add buildreq procps needed for memleak test

* Mon Jul 27 2009 Paul Howarth <paul@city-fan.org> - 1.27-1
- Update to 1.27
  - various regex fixes for i18n and service names
  - fix warnings from perl -w (CPAN RT#48131)
  - improve handling of errors from Net::ssl_write_all

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul  4 2009 Paul Howarth <paul@city-fan.org> - 1.26-1
- Update to 1.26 (verify_hostname_of_cert matched only the prefix for the
  hostname when no wildcard was given, e.g. www.example.org matched against a
  certificate with name www.exam in it [#509819])

* Fri Jul  3 2009 Paul Howarth <paul@city-fan.org> - 1.25-1
- Update to 1.25 (fix t/nonblock.t for OS X 10.5 - CPAN RT#47240)

* Thu Apr  2 2009 Paul Howarth <paul@city-fan.org> - 1.24-1
- Update to 1.24 (add verify hostname scheme ftp, same as http)

* Wed Feb 25 2009 Paul Howarth <paul@city-fan.org> - 1.23-1
- Update to 1.23 (complain when no certificates are provided)

* Sat Jan 24 2009 Paul Howarth <paul@city-fan.org> - 1.22-1
- Update to latest upstream version: 1.22

* Thu Jan 22 2009 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to latest upstream version: 1.20

* Tue Nov 18 2008 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to latest upstream version: 1.18
- BR: perl(IO::Socket::INET6) for extra test coverage

* Mon Oct 13 2008 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to latest upstream version: 1.17

* Mon Sep 22 2008 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to latest upstream version: 1.16

* Sat Aug 30 2008 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to latest upstream version: 1.15
- Add buildreq and req for perl(Net::LibIDN) to avoid croaking when trying to
  verify an international name against a certificate

* Wed Jul 16 2008 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to latest upstream version: 1.14
- BuildRequire perl(Net::SSLeay) >= 1.21

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-4
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-3
- Rebuild for new perl

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.12-2
- Cosmetic spec changes suiting new maintainer's preferences

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.12-1
- Update to latest upstream version: 1.12
- Fix license tag
- Add BuildRequires for ExtUtils::MakeMaker and Test::Simple
- Fix package review issues:
- Source URL
- Resolves: bz#226264

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.02-1
- Upgrade to latest CPAN version: 1.02

* Mon Sep 18 2006 Warren Togami <wtogami@redhat.com> - 1.01-1
- 1.01 bug fixes (#206782)

* Sun Aug 13 2006 Warren Togami <wtogami@redhat.com> - 0.998-1
- 0.998 with more important fixes

* Tue Aug 01 2006 Warren Togami <wtogami@redhat.com> - 0.994-1
- 0.994 important bugfixes (#200860)

* Tue Jul 18 2006 Warren Togami <wtogami@redhat.com> - 0.991-1
- 0.991

* Wed Jul 12 2006 Warren Togami <wtogami@redhat.com> - 0.97-3
- Import into FC6

* Tue Feb 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.97-2
- Rebuild for FC5 (perl 5.8.8).
- Rebuild switch: "--with sessiontests".

* Mon Jul 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.97-1
- 0.97.
- Convert docs to UTF-8, drop some unuseful ones.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.96-4
- Rebuilt

* Tue Oct 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-3
- Disable session test suite even if Net::SSLeay >= 1.26 is available.

* Wed Jul  7 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.2
- Bring up to date with current fedora.us Perl spec template.
- Include examples in docs.

* Sat May  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- Update to 0.96.
- Reduce directory ownership bloat.
- Require perl(:MODULE_COMPAT_*).

* Fri Oct 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.95-0.fdr.1
- First build.
