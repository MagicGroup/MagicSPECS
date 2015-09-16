# We need to patch the test suite if we have an old version of Test::More
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)

# Test::CPAN::Changes isn't available in EPEL < 7, due to requirement of perl(version) ≥ 0.79
%global cpan_changes_available %(expr 0%{?fedora} + 0%{?rhel} '>' 6)

#TODO: BR: Test::Pod::No404s when available
#TODO: BR: Test::Pod::LinkCheck when available

Name:		perl-Module-Implementation
Version:	0.09
Release:	2%{?dist}
Summary:	Loads one of several alternate underlying implementations for a module
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/perl-Module-Implementation/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Module-Implementation-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Build requirements
# ===================================================================
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Carp)
BuildRequires:	perl(Module::Runtime) >= 0.012
BuildRequires:	perl(Try::Tiny)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# ===================================================================
# Test suite requirements
# ===================================================================
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::Taint)
# ===================================================================
# Author/Release test requirements
# ===================================================================
%if %{cpan_changes_available}
BuildRequires:	perl(Test::CPAN::Changes)
%endif
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Spelling)
# Can't use aspell-en from EPEL-7 as BR: for RHEL-7 package so skip the spell
# check test there; test would fail rather than skip without Test::Spelling so
# we need to keep that as a buildreq
%if 0%{?rhel} < 7
BuildRequires:	aspell-en
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Carp)

%description
This module abstracts out the process of choosing one of several underlying
implementations for a module. This can be used to provide XS and pure Perl
implementations of a module, or it could be used to load an implementation
for a given OS or any other case of needing to provide multiple
implementations.

This module is only useful when you know all the implementations ahead of
time. If you want to load arbitrary implementations then you probably want
something like a plugin system, not this module.

%prep
%setup -q -n Module-Implementation-%{version}

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
%{perl_vendorlib}/Module/
%{_mandir}/man3/Module::Implementation.3pm*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.09-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.09-1
- 更新到 0.09

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.06-4
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 0.06-3
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from buildroot
- Add commentary regarding conditionalized buildreqs

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-2
- Conditionalize aspell-en dependency

* Sun Feb 12 2012 Paul Howarth <paul@city-fan.org> - 0.06-1
- Update to 0.06
  - Require Module::Runtime 0.012, which has a number of useful bug fixes

* Fri Feb 10 2012 Paul Howarth <paul@city-fan.org> - 0.05-1
- Update to 0.05
  - Make Test::Taint an optional dependency; it requires XS, and requiring a
    compiler for Module::Implementation defeats its purpose (CPAN RT#74817)
- BR: perl(Test::Requires)
- Update patch for building with old Test::More versions

* Thu Feb  9 2012 Paul Howarth <paul@city-fan.org> - 0.04-1
- Update to 0.04
  - This module no longer installs an _implementation() subroutine in callers;
    instead, you can call Module::Implementation::implementation_for($package)
    to get the implementation used for a given package
- Update patch for building with old Test::More versions

* Wed Feb  8 2012 Paul Howarth <paul@city-fan.org> - 0.03-3
- Incorporate feedback from package review (#788258)
  - Correct License tag, which should be Artistic 2.0
  - BR: perl(lib) for test suite
  - Explicitly require perl(Carp), not automatically detected

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-2
- Sanitize for Fedora submission

* Tue Feb  7 2012 Paul Howarth <paul@city-fan.org> - 0.03-1
- Initial RPM version
