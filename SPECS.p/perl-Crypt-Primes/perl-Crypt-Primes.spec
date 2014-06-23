Summary:	Provable prime number generator for cryptographic applications
Name:		perl-Crypt-Primes
Version:	0.50
Release:	26%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-Primes/
Source0:	http://search.cpan.org/CPAN/authors/id/V/VI/VIPUL/Crypt-Primes-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Crypt::Random)	>= 0.33
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Math::Pari)	>= 2.001804
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module implements Ueli Maurer's algorithm for generating large provable
primes and secure parameters for public-key cryptosystems. The generated primes
are almost uniformly distributed over the set of primes of the specified
bitsize and expected time for generation is less than the time required for
generating a pseudo-prime of the same size with Miller-Rabin tests. Detailed
description and running time analysis of the algorithm can be found in Maurer's
paper, "Fast Generation of Prime Numbers and Secure Public-Key Cryptographic
Parameters" (1994).

%prep
%setup -q -n Crypt-Primes-%{version}
sed -i -e '/^#! *\/usr\/bin\/perl /d' lib/Crypt/Primes.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check


%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README docs/*
%{_bindir}/largeprimes
%{perl_vendorlib}/Crypt/Primes.pm
%{_mandir}/man1/largeprimes.1*
%{_mandir}/man3/Crypt::Primes.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.50-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.50-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.50-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.50-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.50-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.50-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.50-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.50-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.50-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.50-14
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 0.50-13
- Nobody else likes macros for commands

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.50-12
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.50-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.50-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.50-8
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.50-5
- Rebuild for new perl

* Sun Aug 12 2007 Paul Howarth <paul@city-fan.org> 0.50-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 0.50-3
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.50-2
- FE6 mass rebuild

* Tue Dec  6 2005 Paul Howarth <paul@city-fan.org> 0.50-1
- Initial build
