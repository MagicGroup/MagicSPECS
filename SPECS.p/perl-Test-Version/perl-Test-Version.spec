# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Test-Version
Version:	1.002004
Release:	4%{?dist}
Summary:	Check to see that versions in modules are sane
License:	Artistic 2.0
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Test-Version/
Source0:	http://search.cpan.org/CPAN/authors/id/X/XE/XENO/Test-Version-%{version}.tar.gz
Patch1:		Test-Version-1.002003-pod-spell.patch
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
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
BuildRequires:	perl(Test::More) >= 0.88
BuildRequires:	perl(version) >= 0.86
BuildRequires:	perl(warnings)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Exception)
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
BuildRequires:	perl(Pod::Wordlist)
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::CPAN::Meta::JSON)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::Mojibake)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod) >= 1.41
BuildRequires:	perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	perl(Test::Pod::LinkCheck)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Spelling) >= 0.12, hunspell-en
BuildRequires:	perl(Test::Synopsis)
BuildRequires:	perl(Test::Vars)
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

# Some spell checkers check "doesn" rather than "doesn't"
%patch1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test %{!?perl_bootstrap:AUTHOR_TESTING=1 RELEASE_TESTING=1}

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Version.3pm*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 1.002004-3
- Bootstrap build for epel7 done

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 1.002004-2
- Bootstrap epel7 build

* Thu Nov 21 2013 Paul Howarth <paul@city-fan.org> - 1.002004-1
- Update to 1.002004
  - Fix bugs in argument handling
  - Fix whitespace

* Tue Oct 15 2013 Paul Howarth <paul@city-fan.org> - 1.002003-1
- Update to 1.002003
  - Fix synopsis (https://github.com/xenoterracide/Test-Version/pull/6)
  - Change Dist::Zilla plugins
  - Remove old documentation that no longer applies
  - Fix misgithap
  - More dist.ini updates
- Update patches and buildreqs as needed
- Drop support for old rpm versions as this package's requirements will never
  be satisfied in EPEL-5

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.002001-13
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.002001-11
- Perl 5.18 rebuild

* Fri Jun 14 2013 Paul Howarth <paul@city-fan.org> - 1.002001-10
- Fix FTBFS with current test modules
  - Disable Test::Kwalitee's "use_strict" test
  - Schwern not in dictionary

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002001-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

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
