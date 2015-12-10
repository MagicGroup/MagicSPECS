Name:		perl-CPAN-Meta-Check
Summary:	Verify requirements in a CPAN::Meta object
Version:	0.008
Release:	6%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		https://metacpan.org/release/CPAN-Meta-Check
Source0:	http://cpan.metacpan.org/authors/id/L/LE/LEONT/CPAN-Meta-Check-%{version}.tar.gz 
BuildArch:	noarch
# Build
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# Module
BuildRequires:	perl(CPAN::Meta::Prereqs) >= 2.132830
BuildRequires:	perl(CPAN::Meta::Requirements) >= 2.121
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(Module::Metadata)
# Test
BuildRequires:	perl(Env)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More) >= 0.88
# Release tests
# perl-Pod-Coverage-TrustPod -> perl-Pod-Eventual -> perl-Mixin-Linewise -> perl-YAML-Tiny -> perl-CPAN-Meta-Check
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module verifies if requirements described in a CPAN::Meta object are
present.

%prep
%setup -q -n CPAN-Meta-Check-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test RELEASE_TESTING=1

%files
%doc Changes LICENSE README
%{perl_vendorlib}/CPAN/
%{_mandir}/man3/CPAN::Meta::Check.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.008-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.008-5
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.008-4
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.008-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 17 2013 Paul Howarth <paul@city-fan.org> - 0.008-1
- Update to 0.008
  - Switch to using merged_requirements
  - Test Env instead of Carp for version overshoot (CPAN RT#89591)
  - Document $incdirs in the right function

* Wed Sep  4 2013 Paul Howarth <paul@city-fan.org> - 0.007-3
- Skip the release tests when bootstrapping

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Paul Howarth <paul@city-fan.org> - 0.007-1
- Update to 0.007
  - Swap conflicts test, as underscore versions broke it (CPAN RT#87438)

* Sat Jul 27 2013 Paul Howarth <paul@city-fan.org> - 0.006-1
- Update to 0.006
  - Fixed bad dereference during conflicts checking

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.005-3
- Perl 5.18 rebuild

* Wed May  1 2013 Paul Howarth <paul@city-fan.org> - 0.005-2
- Sanitize for Fedora submission

* Sat Apr 27 2013 Paul Howarth <paul@city-fan.org> - 0.005-1
- Initial RPM version
