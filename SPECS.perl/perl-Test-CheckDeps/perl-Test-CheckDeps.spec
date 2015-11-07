Name:		perl-Test-CheckDeps
Summary:	Check for presence of dependencies
Version:	0.010
Release:	4%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		https://metacpan.org/release/Test-CheckDeps
Source0:	http://cpan.metacpan.org/authors/id/L/LE/LEONT/Test-CheckDeps-%{version}.tar.gz 
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(CPAN::Meta) >= 2.120920
BuildRequires:	perl(CPAN::Meta::Check) >= 0.007
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(List::Util)
BuildRequires:	perl(Test::Builder) >= 0.82
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::More) >= 0.88
# Release tests
# perl-Pod-Coverage-TrustPod -> perl-Pod-Eventual -> perl-Mixin-Linewise -> perl-YAML-Tiny -> perl-Test-CheckDeps
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module adds a test that assures all dependencies have been installed
properly. If requested, it can bail out all testing on error.

%prep
%setup -q -n Test-CheckDeps-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test RELEASE_TESTING=1

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CheckDeps.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.010-4
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.010-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct  9 2013 Paul Howarth <paul@city-fan.org> - 0.010-1
- Update to 0.010
  - Added Synopsis
  - $Test::Builder::Level increased, so failing tests appear to come from the
    .t file rather than Test/CheckDeps.pm
  - Also test 'develop' prereqs when AUTHOR_TESTING

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Switch to MakeMaker to fix bootstrapping issues

* Thu Sep 19 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Require CPAN::Meta::Check ≥ 0.007, for conflicts fixes
- Bump Module::Build::Tiny version requirement to 0.027
- BR: perl(IO::Handle) and perl(IPC::Open3) rather than
  perl(File::Temp) for the test suite

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.006-4
- Skip the release tests when bootstrapping

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.006-2
- Perl 5.18 rebuild

* Fri Jun 21 2013 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Require CPAN::Meta::Check ≥ 0.004
  - Explicitly require CPAN::Meta ≥ 2.120920
  - Switch to Module::Build::Tiny

* Wed May 15 2013 Paul Howarth <paul@city-fan.org> - 0.004-1
- Update to 0.004
  - Sort dependencies before displaying them
  - check_dependencies() can now optionally also test recommended and suggested
    prerequisites
  - Reinstate loading of CPAN::Meta
- Kwalitee test dropped upstream to avoid circular deps, so longer need to
  BR: perl(Test::Kwalitee)
- No longer need perl(Module::Metadata)
- Bump perl(Test::Builder) version requirement to 0.82 for todo_start/todo_end

* Wed May  1 2013 Paul Howarth <paul@city-fan.org> - 0.002-2
- Sanitize for Fedora submission

* Sat Apr 27 2013 Paul Howarth <paul@city-fan.org> - 0.002-1
- Initial RPM version
