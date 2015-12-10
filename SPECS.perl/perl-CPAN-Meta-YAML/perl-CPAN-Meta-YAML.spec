Name:		perl-CPAN-Meta-YAML
Version:	0.016
Release:	3%{?dist}
Summary:	Read and write a subset of YAML for CPAN Meta files
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/CPAN-Meta-YAML/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/CPAN-Meta-YAML-%{version}.tar.gz
BuildArch:	noarch
# Build:
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
# Module Runtime:
BuildRequires:	perl(B)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Tests:
# CPAN::Meta requires CPAN::Meta::YAML
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.120900
%endif
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Getopt::Long)
BuildRequires:	perl(IO::Dir)
BuildRequires:	perl(JSON::PP)
BuildRequires:	perl(lib)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More) >= 0.99
BuildRequires:	perl(utf8)
BuildRequires:	perl(vars)
BuildRequires:	perl(version)
BuildRequires:	perl(YAML)
# Extra Tests:
# Don't run extra tests when bootstrapping as many of those
# tests' dependencies build-require this package
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Version)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

%description
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.

%prep
%setup -q -n CPAN-Meta-YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor UNINST=0
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test
%if 0%{!?perl_bootstrap:1}
make test TEST_FILES="xt/*/*.t"
%endif

%files
%doc Changes LICENSE README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::YAML.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.016-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.016-2
- 更新到 0.016

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.012-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.012-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Paul Howarth <paul@city-fan.org> - 0.012-1
- Update to 0.012:
  - Generated from ETHER/YAML-Tiny-1.61.tar.gz

* Fri Feb 14 2014 Paul Howarth <paul@city-fan.org> - 0.011-1
- Update to 0.011:
  - Generated from ETHER/YAML-Tiny-1.60.tar.gz
- Give up trying to support EPEL (test suite now requires Test::More 0.99)

* Mon Sep 23 2013 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010:
  - Generated from ETHER/YAML-Tiny-1.55.tar.gz
  - Makefile.PL will use UNINST=1 on old perls that might have an old version
    incorrectly installed into the core library path
  - Updated Makefile.PL logic to support PERL_NO_HIGHLANDER
- Drop redundant BRs: perl(Pod::Wordlist::hanekomu), perl(Test::Requires),
  perl(Test::Spelling) and aspell-en
- Add new test dependencies perl(IO::Handle) and perl(IPC::Open3)
- Build with UNINST=0 to avoid build failures as we can't remove the system
  version of the package when building an rpm for a new version
- Update patch for building with old Test::More, and add new patch to support
  building with Test::More < 0.94
- Don't run the extra tests in EPEL as we don't have Test::Version there

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.008-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 0.008-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.008-13
- Update dependencies

* Thu Oct 11 2012 Paul Howarth <paul@city-fan.org> - 0.008-12
- Never BR: perl(Test::Version) for EL builds as perl(version) is too old
  prior to EL-7 and this package is included in RHEL ≥ 7 but Test::Version
  is only in EPEL

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 0.008-11
- Restrict Test::Version optional test on RHEL to version 6 only

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.008-9
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.008-8
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.008-7
- Run the extra tests in a separate test run, and only when not bootstrapping
- Don't BR: perl(Test::Spelling) with RHEL ≥ 7 as we don't have the other
  dependencies needed do the spell check test

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-6
- Conditionalize dependency on aspell

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.008-5
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 0.008-4
- Disable author tests on bootstrap

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-3
- Data::Dumper is not really needed, dependencies must be fixed in YAML

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.008-2
- Don't BR: Pod::Wordlist::hanekomu for RHEL-7+ builds; RHEL package cannot
  have buildreq from EPEL
- Add missing Data::Dumper dependency

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008:
  - Generated from ADAMK/YAML-Tiny-1.51.tar.gz
  - Updated from YAML-Tiny to fix compatibility with older Scalar::Util
- Drop upstreamed patch for old Scalar::Util versions
- Don't need to remove empty directories from the buildroot

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007:
  - Documentation fix to replace missing abstract

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006:
  - Set back configure_requires prerequisite for ExtUtils::MakeMaker
    from 6.30 to 6.17
- BR: perl(Test::Requires)
- BR: perl(Test::Spelling), perl(Pod::Wordlist::hanekomu) and aspell-en to
  enable the spell checker test
- Drop patch for building with old ExtUtils::MakeMaker versions, no longer
  needed
- Drop support for soon-to-be-EOL RHEL-4:
  - Drop %%defattr, redundant since rpm 4.4
- Update patch for building with Test::More < 0.88

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.005-2
- Fedora 17 mass rebuild

* Tue Dec 13 2011 Paul Howarth <paul@city-fan.org> - 0.005-1
- Update to 0.005:
  - Fix documentation to clarify that users are responsible for UTF-8
    encoding/decoding

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004:
  - Generated from ADAMK/YAML-Tiny-1.50.tar.gz
- BR: perl(Test::Version) for additional test coverage
- Update patch for building with ExtUtils::MakeMaker < 6.30
- Add patch to support building with Test::More < 0.88
- Add patch to fix operation with Scalar::Util < 1.18

* Tue Aug 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.003-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Paul Howarth <paul@city-fan.org> - 0.003-3
- Trim %%description (#672807)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 0.003-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 0.003-1
- Initial RPM version
