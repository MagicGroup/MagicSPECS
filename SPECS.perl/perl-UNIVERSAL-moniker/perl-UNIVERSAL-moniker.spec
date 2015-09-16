Name:           perl-UNIVERSAL-moniker
Version:        0.08
Release:        26%{?dist}
Summary:        Real world naming for classes
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/UNIVERSAL-moniker/
Source0:        http://search.cpan.org/CPAN/authors/id/K/KA/KASEI/UNIVERSAL-moniker-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More), perl(Lingua::EN::Inflect)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Filter bogus provide for perl(UNIVERSAL) (rpm 4.9 onwards)
%global __provides_exclude ^perl\\(UNIVERSAL\\)

%description
UNIVERSAL::moniker enables classes to make a good 
guess at what they would be called in the real world.

%prep
%setup -q -n UNIVERSAL-moniker-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/UNIVERSAL/
%{_mandir}/man3/UNIVERSAL::moniker.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.08-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.08-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.08-24
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.08-21
- Perl 5.18 rebuild

* Tue Feb 26 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.08-20
- Add BR: perl(ExtUtils::MakeMaker) (Fix FTBFS #914323).
- Modernize spec.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.08-17
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.08-15
- Perl mass rebuild

* Thu Apr 14 2011 Paul Howarth <paul@city-fan.org> - 0.08-14
- Tweak provides filter to work with rpm >= 4.9 too

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-12
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-11
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-10
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-7
- Rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-6
- rebuild for new perl

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-5
- license tag fix

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-4
- filter out false provide

* Fri Aug  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-3
- add BR: perl(Lingua::EN::Inflect) to improve test coverage
- add README to %%doc

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-1
- Initial package for Fedora Extras
