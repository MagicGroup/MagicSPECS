Name:		perl-Test-CPAN-Meta-YAML
Version:	0.25
Release:	4%{?dist}
Summary:	Validate a META.yml file within a CPAN distribution
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Test-CPAN-Meta-YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BA/BARBIE/Test-CPAN-Meta-YAML-%{version}.tar.gz
Patch0:		Test-CPAN-Meta-YAML-0.25-utf8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::YAML::Valid) >= 0.03
BuildRequires:	perl(vars)
BuildRequires:	perl(warnings)
BuildRequires:	perl(YAML::Syck)
# Test Suite
BuildRequires:	perl(IO::File)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
# Optional Tests
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Test::Pod::Coverage) >= 0.08
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Explicitly requests the YAML::Syck backend for Test::YAML::Valid
Requires:	perl(YAML::Syck)

%description
This module was written to ensure that a META.yml file, provided with a
standard distribution uploaded to CPAN, meets the specifications that are
slowly being introduced to module uploads, via the use of ExtUtils::MakeMaker,
Module::Build and Module::Install.

See CPAN::Meta for further details of the CPAN Meta Specification.

%prep
%setup -q -n Test-CPAN-Meta-YAML-%{version}

# Recode documentation as UTF-8
%patch0

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test AUTOMATED_TESTING=1

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CPAN::Meta::YAML.3*
%{_mandir}/man3/Test::CPAN::Meta::YAML::Version.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.25-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.25-2
- Perl 5.22 rebuild

* Wed May  6 2015 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - POD fixes
- Update UTF8 patch

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Documentation updates

* Thu Jan 15 2015 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Extended META test suite
  - Added META.json and tests
- Update UTF8 patch
- Use %%license where possible
- Classify buildreqs by usage

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-4
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Changes file dates changed to meet W3CDTF standard

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.21-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Added minimum perl version (5.006)
  - Reworked Makefile.PL for clarity
  - Implemented Perl::Critic suggestions
  - Added meta_yaml_ok test and example
  - Several Version.pm updates, including new() parameter name change:
    'yaml' is now 'data'

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.20-2
- Perl 5.16 rebuild

* Fri Apr 20 2012 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Further spelling fix
  - Removed DSLIP info

* Tue Apr 17 2012 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - CPAN RT#76611: Spelling fix

* Sun Apr 15 2012 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - CPAN RT#74317: Imported url validation from CPAN::Meta
  - CPAN RT#66692: Updated license type
  - Updates to examples
- Update UTF8 patch
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.17-3
- Perl mass rebuild

* Wed Mar 16 2011 Paul Howarth <paul@city-fan.org> - 0.17-2
- Sanitize for Fedora submission

* Wed Mar 16 2011 Paul Howarth <paul@city-fan.org> - 0.17-1
- Initial RPM version
