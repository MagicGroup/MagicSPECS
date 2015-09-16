Name:		perl-Class-Load
Version:	0.23
Release:	1%{?dist}
Summary:	A working (require "Class::Name") and more
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Class-Load/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-%{version}.tar.gz
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Data::OptList)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(Module::Implementation) >= 0.04
BuildRequires:	perl(Module::Runtime) >= 0.012
BuildRequires:	perl(Package::Stash) >= 0.14
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Try::Tiny)
# ===================================================================
# Regular test suite requirements
# ===================================================================
# Class::Load::XS -> Class::Load
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Class::Load::XS)
%endif
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Without::Module)
BuildRequires:	perl(version)
# ===================================================================
# Author/Release test requirements
# ===================================================================
# Can't use aspell-en from EPEL-7 as BR: for RHEL-7 package so skip the spell
# check test there; test would fail rather than skip without Test::Spelling so
# we need to keep that as a buildreq
%if 0%{?rhel} < 7
BuildRequires:	aspell-en
%endif
# Pod::Coverage::Moose -> Moose -> Class::Load
%if 0%{!?perl_bootstrap:1} && 0%{?rhel} < 7
BuildRequires:	perl(Pod::Coverage::Moose)
%endif
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::Spelling)
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Also requires core module perl(Exporter) via a "use base" construct

%description
require EXPR only accepts Class/Name.pm style module names, not Class::Name.
How frustrating! For that, we provide load_class 'Class::Name'.

It's often useful to test whether a module can be loaded, instead of throwing
an error when it's not available. For that, we provide
try_load_class 'Class::Name'.

Finally, sometimes we need to know whether a particular class has been loaded.
Asking %%INC is an option, but that will miss inner packages and any class for
which the filename does not correspond to the package name. For that, we
provide is_class_loaded 'Class::Name'.

%prep
%setup -q -n Class-Load-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
%if 0%{!?perl_bootstrap:1} && 0%{?rhel} < 7
 RELEASE_TESTING=1
%else

%endif

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Class/
%{_mandir}/man3/Class::Load.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.23-1
- 更新到 0.23

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.20-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.20-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.20-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.20-3
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Same as the most recent 0.19, but with a new version (CPAN RT#78389)

* Sun Jul 15 2012 Paul Howarth <paul@city-fan.org> - 0.19-7
- New upstream re-release of 0.19 by DROLSKY
  - The load_class() subroutine now returns the class name on success
    (CPAN RT#76931)
  - Exceptions and errors from Class::Load no longer contain references to line
    numbers in Class::Load or Module::Runtime; this applies to exceptions
    thrown by load_class, load_first_existing_class, and load_optional_class,
    as well as the error returned by try_load_class
  - Exceptions are now croaked properly so they appear to come from the calling
    code, not from an internal subroutine; this makes the exceptions look more
    like the ones thrown by Perl's require (CPAN RT#68663)
- This release by DROLSKY -> update source URL
- BR: perl(Scalar::Util) for the module
- BR: perl(lib) for the test suite
- Drop buildreqs perl(strict) and perl(warnings) - not dual-lived

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.19-6
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 26 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-5
- Conditionalize Pod::Coverage::Moose

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.19-4
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.19-3
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-2
- Conditionalize aspell-en dependency

* Tue Apr  3 2012 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19 (no functional changes)
- This release by DOY -> update source URL
- BR: perl(Exporter)
- Don't need to remove empty directories from buildroot

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18:
  - Require Package::Stash ≥ 0.14 (CPAN RT#75095)

* Sun Feb 12 2012 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17:
  - Require Module::Runtime 0.012, which has a number of useful bug fixes
  - A bug in Class::Load caused test failures when Module::Runtime 0.012 was
    used with Perl 5.8.x (CPAN RT#74897)

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15:
  - Small test changes to accomodate latest version of Module::Implementation
- BR: at least version 0.04 of perl(Module::Implementation)

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14:
  - Use Module::Implementation to handle loading the XS or PP versions of the
    code; using this module fixes a few bugs
  - Under taint mode, setting an implementation in the
    CLASS_LOAD_IMPLEMENTATION env var caused a taint error
  - An invalid value in the CLASS_LOAD_IMPLEMENTATION env var is now detected
    and reported immediately; no attempt is made to load an invalid
    implementation
- BR: perl(Module::Implementation)
- BR: perl(base), perl(Carp), perl(strict) and perl(warnings) for completeness
- Drop version requirement for perl(Package::Stash), no longer present upstream
- Drop explicit runtime dependencies, no longer needed
- Don't BR: perl(Class::Load::XS) or perl(Pod::Coverage::Moose) if we're
  bootstrapping
- Don't run the release tests when bootstrapping as the Pod coverage test will
  fail in the absence of Pod::Coverage::Moose

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 0.13-2
- Fedora 17 mass rebuild

* Thu Dec 22 2011 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13:
  - Fix some bugs with our use of Try::Tiny, which could cause warnings on some
    systems where Class::Load::XS wasn't installed (CPAN RT#72345)
- BR: perl(Test::Without::Module)

* Tue Oct 25 2011 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12:
  - Require Module::Runtime ≥ 0.011, which fixes problems with Catalyst under
    Perl 5.8 and 5.10
- Add versioned runtime dependencies for Module::Runtime and Package::Stash

* Wed Oct  5 2011 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11:
  - Don't accept package names that start with a digit
  - Rewrite some of the guts to use Module::Runtime rather than reimplementing
    its functionality
- BR: perl(Module::Runtime) ≥ 0.009
- Drop all support for older distributions as required module
  Module::Runtime ≥ 0.009 will not be available prior to F-16

* Tue Sep  6 2011 Paul Howarth <paul@city-fan.org> - 0.10-1
- Update to 0.10:
  - Fix is_class_loaded to ignore $ISA (but still look for @ISA) when trying to
    determine whether a class is loaded
  - Lots of internals cleanup
- BR: perl(Package::Stash) ≥ 0.32 and perl(Try::Tiny)
- Update patches to apply cleanly

* Tue Aug 16 2011 Paul Howarth <paul@city-fan.org> - 0.08-1
- Update to 0.08:
  - The previous version was missing a prereq declaration for Data::OptList
    (CPAN RT#70285)
- This release by DROLSKY -> update source URL
- Package new documentation: LICENSE and README
- Add build requirements for new release tests and run them:
  - perl(Pod::Coverage::Moose)
  - perl(Test::CPAN::Changes)
  - perl(Test::EOL)
  - perl(Test::NoTabs)
  - perl(Test::Pod)
  - perl(Test::Pod::Coverage)
  - perl(Test::Requires)
  - perl(Test::Spelling) and aspell-en
- Add patch for building with ExtUtils::MakeMaker < 6.30
- Add patch for building with Test::More < 0.88
- Add patch for building without Test::Requires
- Add patch for fixing spell checker word list
- Don't try to run the POD Coverage test if we don't have Pod::Coverage::Moose

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Paul Howarth <paul@city-fan.org> - 0.06-3
- Drop explicit dependency on core module perl(Exporter) (#656408)

* Tue Nov 23 2010 Paul Howarth <paul@city-fan.org> - 0.06-2
- Sanitize spec for Fedora submission

* Mon Nov 22 2010 Paul Howarth <paul@city-fan.org> - 0.06-1
- Initial RPM version
