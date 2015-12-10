Summary:	RSA public-key cryptosystem
Name:		perl-Crypt-RSA
Version:	1.99
Release:	24%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-RSA/
Source0:	http://search.cpan.org/CPAN/authors/id/V/VI/VIPUL/Crypt-RSA-%{version}.tar.gz
Patch0:		Crypt-RSA-1.99-utf8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Class::Loader)		>= 2.00
BuildRequires:	perl(Convert::ASCII::Armour)
BuildRequires:	perl(Crypt::Random)		>= 0.34
BuildRequires:	perl(Crypt::Primes)		>= 0.38
BuildRequires:	perl(Crypt::CBC)
BuildRequires:	perl(Crypt::Blowfish)
BuildRequires:	perl(Data::Buffer)
BuildRequires:	perl(Digest::MD2)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Digest::SHA1)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Math::Pari)		>= 2.001804
BuildRequires:	perl(Sort::Versions)
BuildRequires:	perl(Tie::EncryptedHash)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Class::Loader)		>= 2.00

%description
Crypt::RSA is a pure-perl, cleanroom implementation of the RSA public-key
cryptosystem. It uses Math::Pari(3), a perl interface to the blazingly fast
PARI library, for big integer arithmetic and number theoretic computations.

Crypt::RSA provides arbitrary size key-pair generation, plaintext-aware
encryption (OAEP) and digital signatures with appendix (PSS). For compatibility
with SSLv3, RSAREF2, PGP and other applications that follow the PKCS #1 v1.5
standard, it also provides PKCS #1 v1.5 encryption and signatures.

%prep
%setup -q -n Crypt-RSA-%{version}

# Convert documentation to UTF-8
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

# Additional manpages
pod2man --section=3 extradocs/crypt-rsa-interoperablity.pod \
	%{buildroot}%{_mandir}/man3/crypt-rsa-interoperablity.3
pod2man --section=3 extradocs/crypt-rsa-interoperablity-template.pod \
	%{buildroot}%{_mandir}/man3/crypt-rsa-interoperablity-template.3

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ARTISTIC Changes COPYING README TODO
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::RSA.3pm*
%{_mandir}/man3/Crypt::RSA::DataFormat.3pm*
%{_mandir}/man3/Crypt::RSA::Debug.3pm*
%{_mandir}/man3/Crypt::RSA::ES::OAEP.3pm*
%{_mandir}/man3/Crypt::RSA::ES::PKCS1v15.3pm*
%{_mandir}/man3/Crypt::RSA::Errorhandler.3pm*
%{_mandir}/man3/Crypt::RSA::Key.3pm*
%{_mandir}/man3/Crypt::RSA::Key::Private.3pm*
%{_mandir}/man3/Crypt::RSA::Key::Private::SSH.3pm*
%{_mandir}/man3/Crypt::RSA::Key::Public.3pm*
%{_mandir}/man3/Crypt::RSA::Key::Public::SSH.3pm*
%{_mandir}/man3/Crypt::RSA::Primitives.3pm*
%{_mandir}/man3/Crypt::RSA::SS::PKCS1v15.3pm*
%{_mandir}/man3/Crypt::RSA::SS::PSS.3pm*
%{_mandir}/man3/crypt-rsa-interoperablity.3*
%{_mandir}/man3/crypt-rsa-interoperablity-template.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.99-24
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.99-23
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.99-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.99-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.99-20
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.99-19
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.99-18
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.99-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.99-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.99-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.99-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.99-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.99-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.99-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.99-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.99-9
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 1.99-8
- Nobody else likes macros for commands
- Use a patch rather than scripted iconv to fix character encodings
- Use %%{_fixperms} macro rather than our own chmod incantation
- BR: perl(Carp)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.99-7
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.99-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 1.99-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.99-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 1.99-3
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  8 2009 Paul Howarth <paul@city-fan.org> 1.99-1
- Update to 1.99
  - Fix CPAN RT#37489 (precedence error in C::R::Key::{Private,Public}::write)
  - Fix CPAN RT#37862 (Crypt::RSA doesn't work under setuid Perl)
  - Fix CPAN RT#46577 (invalid signature calling verify())

* Wed May 13 2009 Paul Howarth <paul@city-fan.org> 1.98-3
- Recode Crypt::RSA manpage as UTF-8

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  8 2008 Paul Howarth <paul@city-fan.org> 1.98-1
- Update to 1.98

* Mon Jul  7 2008 Paul Howarth <paul@city-fan.org> 1.97-1
- Update to 1.97

* Mon Jul  7 2008 Paul Howarth <paul@city-fan.org> 1.96-1
- Update to 1.96
- Convert "Changes" to UTF-8
- Shellbangs no longer need removing
- Module is now UTF-8 and doesn't need converting
- Need manual perl(Class::Loader) dep due to move to use of "use base",
  as rpm auto-dep-finder doesn't spot it

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.58-4
- Rebuild for new perl

* Sun Aug 12 2007 Paul Howarth <paul@city-fan.org> 1.58-3
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Tue Apr 17 2007 Paul Howarth <paul@city-fan.org> 1.58-2
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Fri Dec 22 2006 Paul Howarth <paul@city-fan.org> 1.58-1
- Update to 1.58
- GPL license text now included upstream (CPAN RT#18771)

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.57-3
- FE6 mass rebuild

* Tue Apr 18 2006 Paul Howarth <paul@city-fan.org> 1.57-2
- Fix non-UTF8-encoded manpage (#183888)
- Add manpages for crypt-rsa-interoperablity(3) and
  crypt-rsa-interoperablity-template(3) (#183888)

* Mon Nov 28 2005 Paul Howarth <paul@city-fan.org> 1.57-1
- Initial build
