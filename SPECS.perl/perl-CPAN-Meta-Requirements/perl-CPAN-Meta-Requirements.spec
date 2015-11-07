Name:           perl-CPAN-Meta-Requirements
Version:	2.133
Release:	2%{?dist}
Summary:        Set of version requirements for a CPAN dist
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CPAN-Meta-Requirements/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-Requirements-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(version) >= 0.77
# Test
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::More)
# Extra Tests (not run when bootstrapping due to circular build dependencies)
%if !%{defined perl_bootstrap} && ! ( 0%{?rhel} )
BuildRequires:  perl(English)
BuildRequires:  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:  perl(Perl::Critic::Policy::Miscellanea::RequireRcsKeywords)
BuildRequires:  perl(Pod::Coverage::TrustPod)
BuildRequires:  perl(Pod::Wordlist::hanekomu)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::MinimumVersion)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl(Test::Pod::Coverage) >= 1.08
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(Test::Spelling) >= 0.12, aspell-en
BuildRequires:  perl(Test::Version) >= 0.04
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

# CPAN-Meta-Requirements was split from CPAN-Meta
Conflicts:      perl-CPAN-Meta < 2.120921
# and used to have six decimal places
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(CPAN::Meta::Requirements\\)
Provides:       perl(CPAN::Meta::Requirements) = %{version}000

%description
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions. It
can be built up by adding more and more constraints, and it will reduce them
to the simplest representation.

Logically impossible constraints will be identified immediately by thrown
exceptions.

%prep
%setup -q -n CPAN-Meta-Requirements-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test AUTHOR_TESTING=1
%if !%{defined perl_bootstrap} && ! ( 0%{?rhel} )
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::Requirements.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.133-2
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 2.133-1
- 更新到 2.133

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 2.125-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.125-9
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.125-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.125-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.125-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.125-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.125-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.125-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Paul Howarth <paul@city-fan.org> - 2.125-1
- Update to 2.125
  - On Perls prior to v5.12, CPAN::Meta::Requirements will force UNINST=1 when
    necessary to remove stale copies from ExtUtils::MakeMaker
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
- README.PATCHING renamed to CONTRIBUTING
- Classify buildreqs by usage
- Add note about logically-impossible constraints to %%description

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 2.122-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 2.122-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 2.122-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.122-6
- Conditionalize Test::*

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.122-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.122-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.122-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com>
- Skip some tests on bootstrap

* Mon May 07 2012 Iain Arnell <iarnell@gmail.com> 2.122-1
- update to latest upstream version

* Tue Apr 03 2012 Iain Arnell <iarnell@gmail.com> 2.121-3
- provide perl(CPAN::Meta::Requirements) with six decimal places

* Mon Apr 02 2012 Iain Arnell <iarnell@gmail.com> 2.121-2
- clean up spec following review
- run release/author tests too

* Sun Apr 01 2012 Iain Arnell <iarnell@gmail.com> 2.121-1
- Specfile autogenerated by cpanspec 1.79.
