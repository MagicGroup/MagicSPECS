# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-Perl-OSType
Version:	1.008
Release:	1%{?dist}
Summary:	Map Perl operating system names to generic types
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Perl-OSType/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Perl-OSType-%{version}.tar.gz
Patch1:		Perl-OSType-1.005-old-Test::More.patch
Patch2:		Perl-OSType-1.007-stopwords.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(constant)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More)
# Optional tests, not run for this dual-lived module when bootstrapping
# Also not run for EPEL-5/6 builds due to package unavailability
%if !%{defined perl_bootstrap} && 0%{?fedora}
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Pod::Wordlist::hanekomu)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling), aspell-en
BuildRequires:	perl(Test::Version)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.

This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').

%prep
%setup -q -n Perl-OSType-%{version}

# Fix test suite for Test::More < 0.88
%if %{old_test_more}
%patch1
%endif

# More stopwords for the spell checker
%patch2

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test
%if !%{defined perl_bootstrap} && 0%{?fedora}
LANG=en_US make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::OSType.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.008-1
- 更新到 1.008

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.007-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.007-5
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.007-4
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.007-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Paul Howarth <paul@city-fan.org> - 1.007-1
- Update to 1.007
  - Added 'android' as a Unix-type OS
- Update stopwords patch

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 1.006-1
- Update to 1.006
  - Compile test could hang on Windows
  - Dropped configure_requires for ExtUtils::MakeMaker to 6.17

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.005-1
- Update to 1.005
  - Ensured no non-core test dependencies
  - Various non-functional changes to files and metadata included with
    the distribution
- Add patch with additional stopwords for the spell checker
- Reinstate EPEL support as we no longer require Capture::Tiny

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.004-1
- Update to 1.004
  - 'bitrig' is a Unix
- Specify all dependencies
- Drop EPEL-5/EPEL-6 support as they don't have Capture::Tiny
- Always use aspell for the spell check as Pod::Wordlist::hanekomu explicitly
  sets the speller to aspell

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.003-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.003-3
- Perl 5.18 rebuild

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 1.003-2
- Disable optional tests on RHEL 7 too

* Thu Mar 21 2013 Paul Howarth <paul@city-fan.org> - 1.003-1
- Update to 1.003
  - Fixed detection of VOS; $^O reports 'vos', not 'VOS'
  - Additional release tests
- BR: perl(File::Spec::Functions), perl(List::Util),
  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire),
  perl(Pod::Wordlist::hanekomu), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic), perl(Test::Spelling) and perl(Test::Version)
- Identify purpose of each build requirement
- Update patches for building on old distributions
- Don't run extra tests for EPEL-5/6 builds

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-242
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 1.002-241
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't delete the extra tests when bootstrapping, but don't run them either

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.002-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.002-11
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.002-10
- Skip author tests on bootstrap

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.002-9
- Fedora 17 mass rebuild

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 1.002-8
- BR: perl(Pod::Coverage::TrustPod) unconditionally now that it's available in
  EPEL-4

* Tue Aug 16 2011 Marcela Maslanova <mmaslano@redhat.com> - 1.002-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.002-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-3
- BR: perl(constant), perl(Exporter), perl(File::Temp) in case they are
  dual-lived at some point (#672801)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.002-1
- Initial RPM version
