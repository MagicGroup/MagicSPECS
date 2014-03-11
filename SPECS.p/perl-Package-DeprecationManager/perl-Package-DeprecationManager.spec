# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

# Test::CPAN::Changes isn't available in EPEL-6 either, due to requirement of perl(version) ≥ 0.79
%global cpan_changes_available %(expr 0%{?fedora} + 0%{?rhel} '>' 6)

Name:		perl-Package-DeprecationManager
Version:	0.13
Release:	7%{?dist}
Summary:	Manage deprecation warnings for your distribution
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Package-DeprecationManager/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Package-DeprecationManager-%{version}.tar.gz
Patch1:		Package-DeprecationManager-0.12-old-Test::More.patch
Patch3:		Package-DeprecationManager-0.12-stopwords.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(List::MoreUtils)
BuildRequires:	perl(Params::Util)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Sub::Install)
%if %{cpan_changes_available}
BuildRequires:	perl(Test::CPAN::Changes)
%endif
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Output)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::Spelling)
# Can't use aspell-en from EPEL-7 as BR: for RHEL-7 package so skip the spell
# check test there; test would fail rather than skip without Test::Spelling so
# we need to keep that as a buildreq
%if 0%{?rhel} < 7
BuildRequires:	aspell-en
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module allows you to manage a set of deprecations for one or more modules.

When you import Package::DeprecationManager, you must provide a set of
-deprecations as a hash ref. The keys are "feature" names, and the values are
the version when that feature was deprecated.

%prep
%setup -q -n Package-DeprecationManager-%{version}

# Fix tests for Test::More prior to 0.88
%if %{old_test_more}
%patch1
%endif

# "deprecations" not a common dictionary word
%patch3

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
 RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Package/
%{_mandir}/man3/Package::DeprecationManager.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-7
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.13-5
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.13-4
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-3
- Conditionalize aspell-en

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 0.13-2
- Upstream has dropped Kwalitee test, so drop BR: perl(Test::Kwalitee)

* Fri Mar  9 2012 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13:
  - Fix dist.ini to not add Test::Spelling as a requirement
- Drop %%defattr, redundant since rpm 4.4
- Test::Requires available on all supported distributions

* Mon Mar  5 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Fix tests to pass with Carp 1.25 (CPAN RT#75520)
- BR: perl(Test::Spelling), aspell-en
- Add patch to accept "deprecations" as a valid dictionary word
- Update patches to apply cleanly
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop EPEL-4 support:
  - Drop patch supporting build with ExtUtils::MakeMaker < 6.30

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 0.11-3
- Fedora 17 mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.11-2
- Perl mass rebuild

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11:
  - Allow an empty hash for the -deprecations parameter
- BR: perl(ExtUtils::MakeMaker)
- BR: perl(Test::CPAN::Changes)
- BR: perl(Pod::Coverage::TrustPod) unconditionally
- Update patches for old ExtUtils::MakeMaker and Test::More compatibility

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Paul Howarth <paul@city-fan.org> - 0.10-2
- Update patches for old Test::More and no Test::Requires
- perl(Pod::Coverage::TrustPod) now available everywhere except EPEL-4

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> - 0.10-1
- Update to 0.10:
  - Test suite uses Test::Fatal instead of Test::Exception

* Mon Oct 18 2010 Paul Howarth <paul@city-fan.org> - 0.09-1
- Update to 0.09:
  - Added a compilation test

* Fri Oct 15 2010 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08:
  - The use of regular expressions in ignores didn't really work in 0.06
  - Added missing deps on List::MoreUtils and Test::Requires
  - Replaced Test::Warn with Test::Output in the tests
  - Made the tests actually test what they should be testing
- BR: Test::Output rather than Test::Warn
- Update patches

* Fri Oct 15 2010 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06:
  - Removed hard dep on Test::Warn for the benefit of Moose
  - Fixed what looked like a bug in -ignore handling
  - The -ignore parameter now accepts regexes as well as package names
- Update compatibility patches
- BR: List::MoreUtils
- BR: Test::Requires where possible, patch it out elsewhere

* Tue Jul 27 2010 Paul Howarth <paul@city-fan.org> - 0.04-2
- Clean up for Fedora submission

* Mon Jul 26 2010 Paul Howarth <paul@city-fan.org> - 0.04-1
- Initial RPM version
