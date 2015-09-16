Name:       perl-Test-Aggregate
Version:    0.372
Release:    4%{?dist}
# lib/Test/Aggregate.pm -> GPL+ or Artistic
# lib/Test/Aggregate/Builder.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Aggregate *.t tests to make them run faster
Source:     http://search.cpan.org/CPAN/authors/id/R/RW/RWSTAUNER/Test-Aggregate-%{version}.tar.gz
# Do not touch Test::Builder internals that will change in 2.0, CPAN RT#64604
Patch0:     Test-Aggregate-0.371-Don-t-grab-at-Test-Builder-hash-keys.patch
Url:        http://search.cpan.org/dist/Test-Aggregate
BuildArch:  noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(Module::Build) >= 0.40
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(FindBin) >= 1.47
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::More)
# Unused BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(vars)
# Unused BuildRequires:  perl(Data::Dump::Streamer)
# Tests only
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Trap)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))
Requires:       perl(FindBin) >= 1.47
Requires:       perl(Test::NoWarnings)

%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(FindBin\\)$

%description
A common problem with many test suites is that they can take a
long time to run. The longer they run, the less likely you are to run
the tests. This module borrows a trick from 'Apache::Registry' to load
up your tests at once, create a separate package for each test and wraps
each package in a method named 'run_the_tests'. This allows us to load
perl only once and related modules only once. If you have modules which
are expensive to load, this can dramatically speed up a test suite.

%prep
%setup -q -n Test-Aggregate-%{version}
%patch0 -p1

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install 'destdir=%{buildroot}' create_packlist=0
%{_fixperms} %{buildroot}/*

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.372-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.372-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.372-2
- Perl 5.22 rebuild

* Fri Jan 09 2015 Petr Šabata <contyk@redhat.com> - 0.372-1
- 0.372 bump
- Update outdated description

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.371-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.371-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 0.371-2
- Do not touch Test::Builder internals (CPAN RT#64604)

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 0.371-1
- 0.371 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.364-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.364-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.364-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.364-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.364-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.364-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.364-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.364-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.363-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.363-3
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.363-2
- Mass rebuild with perl-5.12.0

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.363-1
- auto-update to 0.363 (by cpan-spec-update 0.01)
- altered br on perl(FindBin) (0 => 1.47)
- added a new br on perl(Module::Build) (version 0.35)
- added a new br on perl(Test::Most) (version 0.21)
- altered br on perl(Test::Simple) (0.74 => 0.94)
- added a new req on perl(FindBin) (version 1.47)
- added a new req on perl(Test::Harness) (version 3.09)
- added a new req on perl(Test::NoWarnings) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.35-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-1
- submission

* Sat Apr 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
