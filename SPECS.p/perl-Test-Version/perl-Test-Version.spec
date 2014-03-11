# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Test-Version
Version:	1.002001
Release:	9%{?dist}
Summary:	Check to see that versions in modules are sane
License:	Artistic 2.0
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Version/
Source0:	http://search.cpan.org/CPAN/authors/id/X/XE/XENO/Test-Version-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	perl(ExtUtils::MakeMaker)
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Find::Rule::Perl)
BuildRequires:	perl(Module::Metadata)
BuildRequires:	perl(parent)
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(version) >= 0.86
BuildRequires:	perl(warnings)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Exception)
BuildRequires:	perl(Test::Requires)
BuildRequires:	perl(Test::Tester)
# ===================================================================
# Author/Release test requirements
#
# Don't run these tests or include their requirements if we're
# bootstrapping, as many of these modules require each other for
# their author/release tests.
# ===================================================================
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(English)
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Mojibake)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
BuildRequires:	perl(Test::Vars)
# RHEL-7+ package cannot BR: packages from EPEL
%if ! (0%{?rhel} >= 7)
BuildRequires:	aspell-en
BuildRequires:	perl(Pod::Wordlist::hanekomu)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::Spelling) >= 0.12
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module's goal is to be a one stop shop for checking to see that your
versions across your dist are sane.

%prep
%setup -q -n Test-Version-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
 %{!?perl_bootstrap:AUTHOR_TESTING=1 RELEASE_TESTING=1}

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Version.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.002001-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002001-7
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.002001-6
- Perl 5.16 rebuild

* Thu Jun  7 2012 Paul Howarth <paul@city-fan.org> - 1.002001-5
- If we don't have buildreqs aspell-en and perl(Pod::Wordlist::hanekomu), we
  don't need perl(Test::Spelling) either

* Thu Jun  7 2012 Marcela Mašláňová <mmaslano@redhat.com> - 1.002001-4
- Conditionalize aspell-en dependency

* Tue Apr 24 2012 Paul Howarth <paul@city-fan.org> - 1.002001-3
- Don't BR: perl(Pod::Wordlist::hanekomu) for RHEL-7+ either (#815759)

* Tue Apr 24 2012 Paul Howarth <paul@city-fan.org> - 1.002001-2
- RHEL-7+ package cannot BR: perl(Test::Kwalitee) from EPEL (#815759)

* Wed Mar 14 2012 Paul Howarth <paul@city-fan.org> - 1.002001-1
- Update to 1.002001:
  - Fix metadata caused by a bug in DZP::GitHub after asking repo to be
    unlinked from gitpan
- Don't need to remove empty directories from buildroot
- Use %%{_fixperms} macro rather than our own chmod incantation
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Drop %%defattr, redundant since rpm 4.4
- Don't attempt to run author/release tests when bootstrapping

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 1.002000-1
- Update to 1.002000:
  - Use Module::Metadata - apparently it's closer to how Perl works than
    Module::Extract::VERSION
  - Use perl decimal style semantic versioning because of bugs in EUMM with
    vstring versions
  - Allow disabling of 'has_version'
  - Require at least 1 version
  - Allow for checking that a module is_strict
  - Fix some issues in the pod
- BR: perl(Module::Metadata) rather than perl(Module::Extract::VERSION)
- BR: perl(Test::Exception) and perl(Test::Requires) for test suite
- BR: perl(strict) and perl(warnings) for completeness

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-3
- Don't run the author/release tests when bootstrapping
- BR: perl(Test::DistManifest) unconditionally
- Additional BR's for improved release test coverage:
  - perl(Pod::Wordlist::hanekomu)
  - perl(Test::CPAN::Meta::JSON)
  - perl(Test::Mojibake)
  - perl(Test::Spelling) ≥ 0.12 and aspell-en
  - perl(Test::Vars)

* Thu Aug  4 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-2
- Sanitize for Fedora submission

* Wed Aug  3 2011 Paul Howarth <paul@city-fan.org> - 1.0.0-1
- Initial RPM version
