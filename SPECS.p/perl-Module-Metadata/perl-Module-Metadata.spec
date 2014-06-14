Name:		perl-Module-Metadata
Version:	1.000024
Release:	1%{?dist}
Summary:	Gather package and POD information from perl module files
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Module-Metadata/
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Module-Metadata-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(strict)
BuildRequires:	perl(version) >= 0.87
BuildRequires:	perl(warnings)
# Regular test suite
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(lib)
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::More) >= 0.82
BuildRequires:	perl(vars)
# Optional test requirements
BuildRequires:	perl(CPAN::Meta)
BuildRequires:	perl(CPAN::Meta::Requirements)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Fcntl)

%description
This module provides a standard way to gather metadata about a .pm file
without executing unsafe code.

%prep
%setup -q -n Module-Metadata-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%doc Changes CONTRIBUTING LICENSE README README.md
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Metadata.3pm*

%changelog
* Tue Jun 10 2014 Paul Howarth <paul@city-fan.org> - 1.000024-1
- Update to 1.000024
  - Support installations on older perls with an ExtUtils::MakeMaker earlier
    than 6.63_03
- Don't bother trying to run the release tests
- Package new documentation files from upstream: CONTRIBUTING LICENSE README.md

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Paul Howarth <paul@city-fan.org> - 1.000022-1
- Update to 1.000022
  - New is_indexable() object method (CPAN RT#84357)
  - Eliminated dependency on IO::File (and by virtue, XS)
  - Removed cruft in test infrastructure left behind from separation from
    Module::Build
  - Repository moved to https://github.com/Perl-Toolchain-Gang/Module-Metadata
  - .pm file is now wholly ascii, for nicer fatpacking (CPAN RT#95086)
  - Some code micro-optimizations
    (https://github.com/Perl-Toolchain-Gang/Module-Metadata/pull/4)
  - Fixed all out of date prereq declarations
  - Work around change in comparison behaviour in Test::More 0.95_01 by being
    more explicit with our tests - now explicitly checking the string form of
    the extracted version, rather than the entire version object
  - Ensure the extracted version is returned as a version object in all cases
    (CPAN RT#87782)
- Drop redundant Group: tag

* Sun Oct  6 2013 Paul Howarth <paul@city-fan.org> - 1.000019-1
- Update to 1.000019
  - Warnings now disabled inside during the evaluation of generated version sub
    (CPAN RT#89282)
- BR: perl(Config), perl(File::Basename) and perl(IO::File) for the test suite

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000018-1
- Update to 1.000018
  - Re-release of de-tainting fix without unstated non-core test dependencies
- Drop BR: perl(Test::Fatal)

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.000017-1
- Update to 1.000017
  - De-taint version, if needed (CPAN RT#88576)
- BR: perl(Test::Fatal)

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.000016-1
- Update to 1.000016
  - Re-release to fix prereqs and other metadata
- This release by ETHER -> update source URL
- Specify all dependencies

* Wed Aug 21 2013 Paul Howarth <paul@city-fan.org> - 1.000015-1
- Update to 1.000015
  - Change wording about safety/security to satisfy CVE-2013-1437

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.000014-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.000014-2
- Perl 5.18 rebuild

* Thu May  9 2013 Paul Howarth <paul@city-fan.org> - 1.000014-1
- Update to 1.000014
  - Fix reliance on recent Test::Builder
  - Make tests perl 5.6 compatible
- This release by BOBTFISH -> update source URL

* Sun May  5 2013 Paul Howarth <paul@city-fan.org> - 1.000012-1
- Update to 1.000012
  - Improved package detection heuristics
  - Fix ->contains_pod (CPAN RT#84932)
  - Fix detection of pod after __END__ (CPAN RT#79656)
- This release by ETHER -> update source URL
- Package new upstream README file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 1.000011-1
- Update to 1.000011
  - Fix various warning messages
- This release by APEIRON -> update source URL

* Mon Jul 30 2012 Paul Howarth <paul@city-fan.org> - 1.000010-1
- Update to 1.000010
  - Performance improvement: the creation of a Module::Metadata object
    for a typical module file has been sped up by about 40%%
  - Fix t/metadata.t failure under Cygwin
  - Portability fix-ups for new_from_module() and test failures on VMS
- This release by VPIT -> update source URL
- Drop buildreqs for Perl core modules that aren't dual-lived
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000009-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-4
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-3
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.000009-2
- Skip optional POD tests on bootstrap

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 1.000009-1
- Update to 1.000009
  - Adds 'provides' method to generate a CPAN META provides data structure
    correctly; use of package_versions_from_directory is discouraged
  - Fatal errors now use 'croak' instead of 'die'; Carp added as
    prerequisite
- Improve %%description
- Include all buildreqs explicitly required and classify them by Build,
  Module, Regular test suite, and Release tests
- Run main test suite and release tests separately
- Drop explicit versioned runtime dependency on perl(version) as no supported
  release now requires it

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.000007-2
- Fedora 17 mass rebuild

* Wed Sep  7 2011 Paul Howarth <paul@city-fan.org> - 1.000007-1
- Update to 1.000007
  - Apply VMS fixes backported from blead

* Sun Sep  4 2011 Paul Howarth <paul@city-fan.org> - 1.000006-1
- Update to 1.000006
  - Support PACKAGE BLOCK syntax

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.000005-1
- Update to 1.000005
  - Localize $package::VERSION during version discovery
  - Fix references to Module::Build::ModuleInfo (CPAN RT#66133)
  - Added 'new_from_handle()' method (CPAN RT#68875)
  - Improved documentation (SYNOPSIS, broke out class/object method, and
    other minor edits)
- Install to vendor directories rather than perl directories

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 1.000004-5
- Bump and rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.000004-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-2
- Tweaks from package review (#672779)
  - Explicitly duplicate %%summary in %%description as upstream provides
    nothing particularly useful
  - Drop redundant BuildRoot tag
  - Add BuildRequires for possibly dual-lived perl modules:
    Cwd Data::Dumper Exporter File::Path File::Spec File::Temp IO::File
- Explicitly require perl(version) >= 0.87 for builds on OS releases older
  than Fedora 15 where the versioned dependency isn't picked up automatically

* Thu Feb  3 2011 Paul Howarth <paul@city-fan.org> - 1.000004-1
- Update to 1.000004
  - Fix broken metadata.t when @INC has relative paths

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.000003-2
- Sanitize for Fedora submission
- Drop support for releases prior to F-15 due to needing perl(version) >= 0.87

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.000003-1
- Initial RPM version
