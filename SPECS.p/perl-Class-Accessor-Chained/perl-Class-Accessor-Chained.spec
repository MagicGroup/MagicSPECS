Name:           perl-Class-Accessor-Chained
Version:        0.01
Release:        24%{?dist}
Summary:        Make chained accessors
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Class-Accessor-Chained/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RC/RCLAMP/Class-Accessor-Chained-%{version}.tar.gz
Patch0:         Class-Accessor-Chained-0.01-pod.patch
BuildArch:      noarch
BuildRequires:  /usr/bin/pod2text
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Class::Accessor)
Requires:       perl(Class::Accessor::Fast)

%description
A chained accessor is one that always returns the object when called with
parameters (to set), and the value of the field when called with no arguments.
This module subclasses Class::Accessor in order to provide the same
mk_accessors interface.

%prep
%setup -q -n Class-Accessor-Chained-%{version}

# Fix broken POD in README (#914250)
%patch0

# Convert POD-formatted README to plain text for %%doc
pod2text README > README.txt

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%files
%doc Changes README.txt
%{perl_vendorlib}/Class/Accessor/
%{_mandir}/man3/Class::Accessor::Chained.3pm*
%{_mandir}/man3/Class::Accessor::Chained::Fast.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.01-24
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.01-21
- Perl 5.18 rebuild

* Tue Feb 26 2013 Paul Howarth <paul@city-fan.org> - 0.01-20
- Add patch to fix broken POD in README, causing FTBFS (#914250)
- BR:/R: perl(Carp)
- BR: /usr/bin/pod2text, perl(base), perl(Class::Accessor::Fast) and
  perl(ExtUtils::MakeMaker)
- Upstream doesn't ship license files so neither should we
- Enhance %%description
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.01-17
- Perl 5.16 rebuild

* Sun Jan 22 2012 Tom Callaway <spot@fedoraproject.org> - 0.01-16
- fix build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.01-14
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-12
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-11
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.01-10
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.01-7
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-6
- rebuild for new perl

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-5
- license fix

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-4
- fc6 bump

* Tue Aug 30 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-3
- more cleanups

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-1
- Initial package for Fedora Extras
