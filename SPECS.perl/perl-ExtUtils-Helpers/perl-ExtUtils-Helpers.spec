# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION) < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)

Name:		perl-ExtUtils-Helpers
Version:	0.022
Release:	6%{?dist}
Summary:	Various portability utilities for module builders
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		https://metacpan.org/release/ExtUtils-Helpers
Source0:	http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Module::Load)
BuildRequires:	perl(strict)
BuildRequires:	perl(Text::ParseWords) >= 3.24
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::More)
# Release Tests
# perl-Pod-Coverage-TrustPod -> perl-Pod-Eventual -> perl-Mixin-Linewise ->
#   perl-YAML-Tiny -> perl-Module-Build-Tiny -> perl-ExtUtils-Helpers
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides various portable helper functions for module building
modules.

%prep
%setup -q -n ExtUtils-Helpers-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test AUTHOR_TESTING=1 RELEASE_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::Helpers.3pm*
%{_mandir}/man3/ExtUtils::Helpers::Unix.3pm*
%{_mandir}/man3/ExtUtils::Helpers::VMS.3pm*
%{_mandir}/man3/ExtUtils::Helpers::Windows.3pm*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.022-6
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 0.022-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.022-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.022-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar  7 2014 Paul Howarth <paul@city-fan.org> - 0.022-1
- Update to 0.022
  - Cleaned up remains of former functions
  - Skip IO layers on <5.8 for 5.6 compatibility
  - Don't swallow pl2bat exceptions
- Drop patch for using Text::ParseWords < 3.24; even EL-5 has it

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.021-4
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.021-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.021-2
- Perl 5.18 rebuild

* Tue May  7 2013 Paul Howarth <paul@city-fan.org> - 0.021-1
- Update to 0.021
  - Always use the right environmental variable for home directory
  - Use configuration provided manpage extension
- Update patch for building with Test::More < 0.88

* Mon Apr 29 2013 Paul Howarth <paul@city-fan.org> - 0.020-1
- Update to 0.020
  - Fix man3_pagename for top level domains
- Update patch for building with Test::More < 0.88

* Wed Apr 24 2013 Paul Howarth <paul@city-fan.org> - 0.019-1
- Update to 0.019
  - Fix make_executable for '#!/usr/bin/perl'

* Tue Apr 16 2013 Paul Howarth <paul@city-fan.org> - 0.018-1
- Update to 0.018
  - Don't need Pod::Man
- Drop BR: perl(Pod::Man), no longer used

* Mon Apr 15 2013 Paul Howarth <paul@city-fan.org> - 0.017-1
- Update to 0.017
  - Fix man3_pagename to properly split dirs
- Update patch for building with Test::More < 0.88

* Sat Apr 13 2013 Paul Howarth <paul@city-fan.org> - 0.016-1
- Update to 0.016
  - Made man3_pagename more flexible with paths
  - Reverted pl2bat to a more original state
  - Rewrote fixin code
  - Re-added detildefy
  - Add some fixes to batch file generation
- BR: perl(Carp) and perl(Module::Load), now required by the module
- Drop BR: perl(Test::Kwalitee), no longer used
- Update patch for using Test::ParseWords 3.22
- Drop now-redundant POD encoding patch

* Mon Apr  1 2013 Paul Howarth <paul@city-fan.org> - 0.014-2
- Sanitize for Fedora submission

* Sun Mar 31 2013 Paul Howarth <paul@city-fan.org> - 0.014-1
- Initial RPM version
