# To skip the lengthy test suite, use:
# rpmbuild --without checks

Summary:	Perl module implementing the Diffie-Hellman key exchange system
Name:		perl-Crypt-DH
Version:	0.06
Release:	19%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-DH/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BT/BTROTT/Crypt-DH-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Test::More)
# Pull in Math::BigInt::GMP for GMP support for suitably recent versions of Math::BigInt
# else use Math::GMP
%if %(perl -MMath::BigInt -e 'use Math::BigInt 1.87;' 2>/dev/null && echo 1 || echo 0)
BuildRequires:	perl(Math::BigInt::GMP)
Requires:	perl(Math::BigInt::GMP)
%else
BuildRequires:	perl(Math::GMP)
Requires:	perl(Math::GMP)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Crypt::DH is a Perl implementation of the Diffie-Hellman key exchange system.
Diffie-Hellman is an algorithm by which two parties can agree on a shared
secret key, known only to them. The secret is negotiated over an insecure
network without the two parties ever passing the actual shared secret, or their
private keys, between them.

%prep
%setup -q -n Crypt-DH-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%check
%{!?_without_checks:}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes ToDo
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::DH.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-19
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-18
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 0.06-17
- Nobody else likes macros for commands

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.06-16
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.06-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 0.06-14
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 0.06-13
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 0.06-12
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Paul Howarth <paul@city-fan.org> 0.06-9
- BuildRequire and Require a GMP support module, either Math::GMP or
  Math::BigInt::GMP depending on how recent Math::BigInt is

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.06-8
- Rebuild for new perl

* Sat Aug 11 2007 Paul Howarth <paul@city-fan.org> 0.06-7
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 0.06-6
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.06-5
- FE6 mass rebuild

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 0.06-4
- Simplify conditional build by not using %%bcond_* macros

* Mon Dec 12 2005 Paul Howarth <paul@city-fan.org> 0.06-3
- Add support for FC-3, which doesn't have %%bcond_with{,out} predefined

* Fri Dec  9 2005 Paul Howarth <paul@city-fan.org> 0.06-2
- Add facility to skip test suite at build time if desired

* Tue Nov 29 2005 Paul Howarth <paul@city-fan.org> 0.06-1
- Initial build
