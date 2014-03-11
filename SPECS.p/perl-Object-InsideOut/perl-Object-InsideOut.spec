Name:           perl-Object-InsideOut
Version:        3.97
Release:        1%{?dist}
Summary:        Comprehensive inside-out object support module
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Object-InsideOut
Source0:        http://search.cpan.org/CPAN/authors/id/J/JD/JDHEDDEN/Object-InsideOut-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(attributes)
BuildRequires:  perl(B)
BuildRequires:  perl(Data::Dumper) >= 2.131
BuildRequires:  perl(Exception::Class) >= 1.32
BuildRequires:  perl(Scalar::Util) >= 1.25
BuildRequires:  perl(warnings)
# Optional run-time
%if %{undefined perl_bootstrap}
BuildRequires:  perl(Math::Random::MT::Auto) >= 6.18
%endif
BuildRequires:  perl(Want) >= 0.21
# Test only
BuildRequires:  perl(Config)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(threads)
BuildRequires:  perl(Thread::Queue)
BuildRequires:  perl(threads::shared)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Data::Dumper) >= 2.131
Requires:       perl(Scalar::Util) >= 1.25

%{?perl_default_filter}
# Remove underspecified dependencies
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Object::InsideOut\\)$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Scalar::Util\\)

%if %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Math::Random::MT::Auto\\)
%endif

%description
This module provides comprehensive support for implementing classes using the
inside-out object model.

This module implements inside-out objects as anonymous scalar references that
are blessed into a class with the scalar containing the ID for the object
(usually a sequence number). For Perl 5.8.3 and later, the scalar reference is
set as read-only to prevent accidental modifications to the ID. Object data
(i.e., fields) are stored within the class's package in either arrays indexed
by the object's ID, or hashes keyed to the object's ID.

%prep
%setup -q -n Object-InsideOut-%{version}
# fix permissions
find lib -type f -print0 | xargs -0 chmod 0644

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Nov 16 2012 Petr Pisar <ppisar@redhat.com> - 3.97-1
- 3.97 bump

* Tue Oct 02 2012 Petr Pisar <ppisar@redhat.com> - 3.96-1
- 3.96 bump

* Wed Jul 25 2012 Jitka Plesnikova <jplesnik@redhat.com> - 3.95-1
- 3.95 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 3.94-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 3.94-2
- Perl 5.16 rebuild

* Fri May 11 2012 Petr Pisar <ppisar@redhat.com> - 3.94-1
- 3.94 bump

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> - 3.93-1
- 3.93 bump

* Wed Mar 14 2012 Petr Pisar <ppisar@redhat.com> - 3.92-1
- 3.92 bump

* Thu Feb 23 2012 Petr Pisar <ppisar@redhat.com> - 3.91-1
- 3.91 bump

* Mon Feb 20 2012 Petr Pisar <ppisar@redhat.com> - 3.89-1
- 3.89 bump

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 3.88-2
- Finish bootstrapping Math::Random::MT::Auto

* Fri Jan 27 2012 Petr Pisar <ppisar@redhat.com> - 3.88-1
- 3.88 bump
- Do not package tests
- Bootstrap new Math::Random::MT::Auto version

* Thu Jan 19 2012 Petr Pisar <ppisar@redhat.com> - 3.87-1
- 3.87 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 20 2011 Iain Arnell <iarnell@gmail.com> 3.84-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.81-3
- Perl mass rebuild

* Tue Jul 19 2011 Iain Arnell <iarnell@gmail.com> 3.81-2
- fix provides filter
- on filter requires when bootstrapping
- remove unnecessary explicit requires

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 3.81-1
- minimize the impact of perl_bootstrap on testing; it's only
  perl-Math-Random-MT-Auto which causes circular deps and is
  automatically skipped in tests if not available

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 3.81-1
- update to latest upstream version

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.79-2
- use perl_bootstrap macro

* Fri Feb 25 2011 Iain Arnell <iarnell@gmail.com> 3.79-1
- update to latest upstream version

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 3.56-8
- only filter unversioned perl(Object::InsideOut) from provides

* Thu Feb 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.56-7
- add into filter requires on Object::InsideOut

* Tue Feb 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.56-6
- clean spec, add correct filters

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.56-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.56-4
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.56-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.56-2
- rebuild against perl 5.10.1

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 3.56-1
- auto-update to 3.56 (by cpan-spec-update 0.01)
- altered br on perl(Scalar::Util) (1.19 => 1.21)
- added a new req on perl(B) (version 0)
- added a new req on perl(Config) (version 0)
- added a new req on perl(Data::Dumper) (version 0)
- added a new req on perl(Exception::Class) (version 1.29)
- added a new req on perl(Scalar::Util) (version 1.21)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 3.55-1
- auto-update to 3.55 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- added a new br on perl(Scalar::Util) (version 1.19)
- added a new br on perl(Config) (version 0)
- added a new br on perl(Test::More) (version 0.5)
- altered br on perl(Exception::Class) (1.22 => 1.29)
- added a new br on perl(B) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 3.51-1
- update to 3.51
- replace filter-provides.sh style filtering with inline

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.38-1
- 3.38

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.06-2
- rebuild for new perl

* Tue Oct 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 2.06-1
- update to 2.06
- add additional BRs: perl(Test::Pod[::Coverage])

* Mon Sep 25 2006 Chris Weyl <cweyl@alumni.drew.edu> 2.02-1
- update to 2.02

* Tue Sep 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.52-1
- update to 1.52

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.51-1
- update to 1.51, which now has a BR of perl(Want)
- rebuild per mass rebuild

* Fri Aug 11 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.49-1
- update to 1.49

* Sat Aug 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.48-1
- update to 1.48
- drop some unneeded bits from the spec

* Wed Jul  5 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.45-1
- bump release for build

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.45-0.1
- corrected url's.

* Sat Jul 01 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.45-0
- Initial spec file for F-E
