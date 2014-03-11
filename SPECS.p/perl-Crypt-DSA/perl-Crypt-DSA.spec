Summary:	Perl module for DSA signatures and key generation
Name:		perl-Crypt-DSA
Version:	1.17
Release:	6%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-DSA/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Crypt-DSA-%{version}.tar.gz
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Convert::PEM)
BuildRequires:	perl(Crypt::DES_EDE3)
BuildRequires:	perl(Data::Buffer) >= 0.01
BuildRequires:	perl(Digest::SHA1)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Which) >= 0.05
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Math::BigInt) >= 1.78
BuildRequires:	perl(Math::BigInt::GMP)
BuildRequires:	perl(Perl::MinimumVersion) >= 1.20
BuildRequires:	perl(Test::CPAN::Meta) >= 0.12
BuildRequires:	perl(Test::More) >= 0.42
BuildRequires:	perl(Test::MinimumVersion) >= 0.008
BuildRequires:	perl(Test::Pod) >= 1.26
BuildRequires:	openssl
# Crypt::DSA::Keychain calls openssl for DSA parameter generation
Requires:	openssl
# Some operations are really slow without GMP (or Pari, but we test with GMP)
Requires:	perl(Math::BigInt::GMP)

%description
Crypt::DSA is an implementation of the DSA (Digital Signature Algorithm)
signature verification system. This package provides DSA signing, signature
verification, and key generation.

%prep
%setup -q -n Crypt-DSA-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check

 AUTOMATED_TESTING=1 TEST_FILES="xt/*.t"

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::DSA.3pm*
%{_mandir}/man3/Crypt::DSA::Key.3pm*
%{_mandir}/man3/Crypt::DSA::Key::PEM.3pm*
%{_mandir}/man3/Crypt::DSA::Key::SSH2.3pm*
%{_mandir}/man3/Crypt::DSA::KeyChain.3pm*
%{_mandir}/man3/Crypt::DSA::Signature.3pm*
%{_mandir}/man3/Crypt::DSA::Util.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.17-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.17-5
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 1.17-4
- Fedora 17 mass rebuild
- Use %%{_fixperms} macro rather than our own chmod incantation
- BR: perl(Carp)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> 1.17-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> 1.17-2
- Perl mass rebuild

* Fri Jun 17 2011 Paul Howarth <paul@city-fan.org> 1.17-1
- Update to 1.17
  - Upgrade to Module::Install 1.01
  - Added support for OpenSSL 1.0.0 dsaparam format change (CPAN RT#49668)
  - Requires perl 5.6 now (CPAN RT#58094)
  - Fixes for 64-bit support
- Drop upstreamed patches
- Release tests moved to xt/ directory upstream and now tested separately
- Nobody else likes macros for commands
- Drop backwards compatibility with ancient distributions

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 1.16-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Jun  3 2010 Paul Howarth <paul@city-fan.org> 1.16-4
- META.yml should specify perl >= 5.006 due to use of 3-arg open (CPAN RT#58094)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.16-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 1.16-2
- Rebuild against perl 5.10.1

* Fri Sep 11 2009 Paul Howarth <paul@city-fan.org> 1.16-1
- Update to 1.16 (first production release)
- New upstream maintainer -> change source URL
- Change buildreq which to perl(File::Which)
- Add new buildreqs perl(Crypt::DES_EDE3), perl(File::Spec), perl(IPC::Open3)
- Buildreq perl(Math::BigInt) >= 1.78
- Enable AUTOMATED_TESTING
- New test requirements:
  - perl(Perl::MinimumVersion) >= 1.20
  - perl(Test::CPAN::Meta) >= 0.12
  - perl(Test::MinimumVersion) >= 0.008
  - perl(Test::Pod) >= 1.26
- ToDo no longer present upstream, but add LICENSE and README as %%doc
- Add runtime dependency on openssl (used for DSA parameter generation)
- Add patch for openssl dsaparam 1.0 compatibility (CPAN RT#49668)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov  3 2008 Paul Howarth <paul@city-fan.org> 0.14-7
- BuildRequire and Require a GMP support module, either Math::GMP or
  Math::BigInt::GMP depending on how recent Math::BigInt is
- BuildRequire openssl, which significantly speeds up the keygen test

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.14-6
- Rebuild for new perl

* Sat Aug 11 2007 Paul Howarth <paul@city-fan.org> 0.14-5
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 0.14-4
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.14-3
- FE6 mass rebuild

* Mon May 29 2006 Paul Howarth <paul@city-fan.org> 0.14-2
- Add missing buildreq: which

* Tue May  9 2006 Paul Howarth <paul@city-fan.org> 0.14-1
- Update to 0.14

* Mon Nov 28 2005 Paul Howarth <paul@city-fan.org> 0.13-1
- Initial build
