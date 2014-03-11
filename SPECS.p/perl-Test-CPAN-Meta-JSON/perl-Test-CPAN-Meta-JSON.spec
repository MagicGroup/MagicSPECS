Name:		perl-Test-CPAN-Meta-JSON
Version:	0.14
Release:	2%{?dist}
Summary:	Validate a META.json file within a CPAN distribution
Group:		Development/Libraries
License:	Artistic 2.0
URL:		http://search.cpan.org/dist/Test-CPAN-Meta-YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BA/BARBIE/Test-CPAN-Meta-JSON-%{version}.tar.gz
Patch0:		Test-CPAN-Meta-JSON-0.14-utf8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(JSON) >= 2.15
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module was written to ensure that a META.json file, provided with a
standard distribution uploaded to CPAN, meets the specifications that are
slowly being introduced to module uploads, via the use of ExtUtils::MakeMaker,
Module::Build and Module::Install.

See CPAN::Meta for further details of the CPAN Meta Specification.

%prep
%setup -q -n Test-CPAN-Meta-JSON-%{version}

# Recode LICENSE as UTF-8
%patch0 -p1

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
%doc Changes LICENSE README examples/
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::CPAN::Meta::JSON.3pm*
%{_mandir}/man3/Test::CPAN::Meta::JSON::Version.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-2
- 为 Magic 3.0 重建

* Tue Aug 21 2012 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Added minimum perl version (5.006)
  - Reworked Makefile.PL for clarity
  - Implemented Perl::Critic suggestions
  - Added meta_json_ok test and example
  - Several Version.pm updates
- Update UTF8 patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.13-2
- Perl 5.16 rebuild

* Fri Apr 20 2012 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Further spelling fix
  - Removed DSLIP info

* Tue Apr 17 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - CPAN RT#76609: Spelling fix

* Sun Apr 15 2012 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - CPAN RT#74317: imported url validation from CPAN::Meta
  - CPAN RT#66692: updated license type
  - Updates to examples
- BR: perl(Test::CPAN::Meta) rather than perl(Test::CPAN::Meta::YAML)
- Don't need to remove empty directories from buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Paul Howarth <paul@city-fan.org> - 0.10-2
- Sanitize for Fedora/EPEL submission

* Wed Aug 10 2011 Paul Howarth <paul@city-fan.org> - 0.10-1
- Initial RPM version
