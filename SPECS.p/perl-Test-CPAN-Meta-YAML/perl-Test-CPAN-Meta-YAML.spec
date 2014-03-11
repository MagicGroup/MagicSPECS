Name:		perl-Test-CPAN-Meta-YAML
Version:	0.21
Release:	2%{?dist}
Summary:	Validate a META.yml file within a CPAN distribution
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Test-CPAN-Meta-YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BA/BARBIE/Test-CPAN-Meta-YAML-%{version}.tar.gz
Patch0:		Test-CPAN-Meta-YAML-0.18-utf8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::YAML::Valid) >= 0.03
BuildRequires:	perl(YAML::Syck)
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

# Recode LICENSE as UTF-8
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
 AUTOMATED_TESTING=1

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CPAN::Meta::YAML.3pm*
%{_mandir}/man3/Test::CPAN::Meta::YAML::Version.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.21-2
- 为 Magic 3.0 重建

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
