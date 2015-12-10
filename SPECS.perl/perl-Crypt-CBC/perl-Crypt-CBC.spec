Summary: Encrypt Data with Cipher Block Chaining Mode
Name: perl-Crypt-CBC
Version:	2.33
Release:	3%{?dist}
# Upstream confirms that they're under the same license as perl.
# Wording in CBC.pm is less than clear, but still.
License: GPL+ or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/Crypt-CBC/
Source0: http://search.cpan.org/CPAN/authors/id/L/LD/LDS/Crypt-CBC-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl(bytes)
BuildRequires: perl(constant)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(ExtUtils::MakeMaker)
# Modules used for test suite, skipped when bootstrapping as
# some of these modules use Crypt::CBC themselves
# Crypt::CAST5 not yet packaged in Fedora
# Crypt::IDEA is unavailable due to patents
%if 0%{!?perl_bootstrap:1}
BuildRequires: perl(Crypt::DES)
%if ! (0%{?rhel} >= 7)
BuildRequires: perl(Crypt::Blowfish)
BuildRequires: perl(Crypt::Blowfish_PP)
BuildRequires: perl(Crypt::Rijndael)
%endif
%endif

%description
This is Crypt::CBC, a Perl-only implementation of the cryptographic
cipher block chaining mode (CBC).  In combination with a block cipher
such as Crypt::DES or Crypt::IDEA, you can encrypt and decrypt
messages of arbitrarily long length.  The encrypted messages are
compatible with the encryption format used by SSLeay.

%prep
%setup -q -n Crypt-CBC-%{version}
chmod 644 eg/*.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README eg/
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 2.33-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.33-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.33-1
- 更新到 2.33

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.29-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.29-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.29-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.29-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.29-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.29-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.29-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.29-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.29-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.29-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.29-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.29-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.29-13
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.29-12
- Perl 5.16 rebuild

* Mon Jun 11 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.29-11
- Do not build-require Crypt::Blowfish, Crypt::Blowfish_PP, and Crypt::Rijndael
  on RHEL >= 7
- Resolves: rhbz#822812

* Sat Apr 21 2012 Paul Howarth <paul@city-fan.org> - 2.29-10
- BR: perl(bytes), perl(constant), perl(Digest::MD5) - required by module
- BR: perl(Crypt::Blowfish), perl(Crypt::Blowfish_PP), perl(Crypt::DES),
  perl(Crypt::Rijndael) for improved test coverage, except when bootstrapping

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.29-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.29-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.29-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.29-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 11 2008 Tom "spot" Callawau <tcallawa@redhat.com> - 2.29-1
- update to 2.29

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-3
- work around buildsystem burp

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-2
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22-1.1
- add BR: perl(ExtUtils::MakeMaker)

* Wed Feb 07 2007 Andreas Thienemann <andreas@bawue.net> - 2.22-1
- Upgrade to 2.22

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.19-1
- Upgrade to 2.19

* Fri Feb 24 2006 Andreas Thienemann <andreas@bawue.net> - 2.17-1
- Upgrade to 2.17

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-2
- Remove execute permissions from example files

* Thu Jul 14 2005 Andreas Thienemann <andreas@bawue.net> - 2.14-1
- Initial package

