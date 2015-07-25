Summary:	Cryptographically Secure, True Random Number Generator
Name:		perl-Crypt-Random
Version:	1.25
Release:	26%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Crypt-Random/
Source0:	http://search.cpan.org/CPAN/authors/id/V/VI/VIPUL/Crypt-Random-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Class::Loader)	>= 2.00
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Math::Pari)	>= 2.001804
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Crypt::Random is an interface module to the /dev/random device found on most
modern unix systems. It also interfaces with egd, a user space entropy
gathering daemon, available for systems where /dev/random (or similar) devices
are not available. When Math::Pari is installed, Crypt::Random can generate
random integers of arbritary size of a given bitsize or in a specified
interval.

%prep
%setup -q -n Crypt-Random-%{version}

# Remove shellbangs to shut rpmlint up
find ./lib -name '*.pm' -print | xargs sed -i -e '/^#! *\/usr\/bin\/perl /d'

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


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/makerandom
%{perl_vendorlib}/Crypt/
%{_mandir}/man3/Crypt::Random.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.25-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.25-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.25-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.25-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.25-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.25-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.25-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.25-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.25-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.25-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.25-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.25-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.25-14
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 1.25-13
- Nobody else likes macros for commands
- BR: perl(Carp)

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.25-12
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 1.25-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.25-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 1.25-8
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.25-5
- Rebuild for new perl

* Sun Aug 12 2007 Paul Howarth <paul@city-fan.org> 1.25-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 1.25-3
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.25-2
- FE6 mass rebuild

* Mon Dec  5 2005 Paul Howarth <paul@city-fan.org> 1.25-1
- Initial build
