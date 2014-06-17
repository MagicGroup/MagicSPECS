# We need to patch the test suite if we have an old version of Test::More and/or Test::Pod
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.96) ? 1 : 0);' 2>/dev/null || echo 0)
%global old_test_pod %(perl -MTest::Pod -e 'print (($Test::Pod::VERSION < 1.41) ? 1 : 0);' 2>/dev/null || echo 0)

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Test-Mojibake
Version:	1.0
Release:	7%{?dist}
Summary:	Check your source for encoding misbehavior
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Test-Mojibake/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SY/SYP/Test-Mojibake-%{version}.tar.gz
Patch0:		Test-Mojibake-1.0-no-Test::Version.patch
Patch1:		Test-Mojibake-1.0-old-Test::More.patch
Patch2:		Test-Mojibake-1.0-old-Test::Pod.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Module build requirements
# ===================================================================
BuildRequires:	perl
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(Pod::Usage)
BuildRequires:	perl(Test::Builder)
# ===================================================================
# Optional module requirements
# ===================================================================
BuildRequires:	perl(Unicode::CheckUTF8)
# ===================================================================
# Regular test suite requirements
# ===================================================================
BuildRequires:	perl(Test::Builder::Tester)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Script)
# ===================================================================
# Author/Release test requirements
#
# Don't run these tests or include their requirements if we're
# bootstrapping, as many of these modules require each other for
# their author/release tests.
# ===================================================================
%if 0%{!?perl_bootstrap:1}
BuildRequires:	perl(Pod::Coverage::TrustPod)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::HasVersion)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
# Modules only available from EL-6
%if 0%{?fedora} || 0%{?rhel} > 5
BuildRequires:	perl(Test::Perl::Critic), perl(Perl::Critic) >= 1.094
BuildRequires:	perl(Test::Vars)
%endif
# Modules only available from EL-7
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires:	perl(Test::CPAN::Changes)
BuildRequires:	perl(Test::Version)
%endif
# Modules only available from EL-8
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:	perl(Perl::Critic::Policy::Modules::ProhibitModuleShebang)
BuildRequires:	perl(Test::Pod::LinkCheck)
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# Unicode::CheckUTF8 is an optional requirement that significantly speeds up
# this module
Requires:	perl(Unicode::CheckUTF8)

%description
Many modern text editors automatically save files using UTF-8 codification.
However, the perl interpreter does not expect it by default. Whilst this does
not represent a big deal on (most) backend-oriented programs, Web framework
(Catalyst, Mojolicious) based applications will suffer so-called Mojibake
(literally: "unintelligible sequence of characters"). Even worse: if an editor
saves BOM (Byte Order Mark, U+FEFF character in Unicode) at the start of a
script with the executable bit set (on Unix systems), it won't execute at all,
due to shebang corruption.

Avoiding codification problems is quite simple:

 * Always use utf8/use common::sense when saving source as UTF-8
 * Always specify =encoding utf8 when saving POD as UTF-8
 * Do neither of above when saving as ISO-8859-1
 * Never save BOM (not that it's wrong; just avoid it as you'll barely
   notice its presence when in trouble)

However, if you find yourself upgrading old code to use UTF-8 or trying to
standardize a big project with many developers, each one using a different
platform/editor, reviewing all files manually can be quite painful, especially
in cases where some files have multiple encodings (note: it all started when I
realized that gedit and derivatives are unable to open files with character
conversion tables).

Enter the Test::Mojibake ;)

%prep
%setup -q -n Test-Mojibake-%{version}

# We need to patch the test suite if we have an old version of Test::More
%if %{old_test_more}
%patch1
%endif

# We need to patch the test suite if we have an old version of Test::Pod
%if %{old_test_pod}
%patch2
%endif

# Test::Version not always available
%if !0%{?fedora} && 0%{?rhel} < 7
%patch0
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test %{!?perl_bootstrap:AUTHOR_TESTING=1 RELEASE_TESTING=1}

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README
%{_bindir}/scan_mojibake
%{perl_vendorlib}/Test/
%{_mandir}/man1/scan_mojibake.1*
%{_mandir}/man3/Test::Mojibake.3pm*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-7
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-6
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Paul Howarth <paul@city-fan.org> - 1.0-1
- Update to 1.0
  - Use proper source for ASCII-only characters
  - Dist::Zilla-related updates
  - Fixing the "comment in regexp" other way around
  - Fix regex to properly ignore comments
- Update EPEL support patches

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 0.9-3
- Bootstrap build for epel7 done

* Mon Jan 27 2014 Paul Howarth <paul@city-fan.org> - 0.9-2
- Bootstrap epel7 build

* Mon Jan 20 2014 Paul Howarth <paul@city-fan.org> - 0.9-1
- Update to 0.9
  - More consistent UTF-8 naming in docs
  - Dist::Zilla maintenance
  - Fixed shebang in scan_mojibake
    (https://github.com/creaktive/Test-Mojibake/issues/7)
- Update patch for building with old Test::More versions

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.8-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.8-2
- Perl 5.18 rebuild

* Sat Jan 26 2013 Paul Howarth <paul@city-fan.org> - 0.8-1
- Update to 0.8
  - Fixed cyclic t/ deps
  - Added the standalone scan_mojibake utility
  - Listed Unicode::CheckUTF8 as a recommended prerequisite
  - Recognize utf8::all
  - Passes perlcritic harsh
- Drop BR: perl(File::Spec)
- BR: perl(File::Spec::Functions), perl(Pod::Usage) and perl(Test::Script)
- BR: perl(Test::Pod::LinkCheck) where available
- Perl::Critic ≥ 1.094 now needed for the 'equivalent_modules' parameter in
  TestingAndDebugging::RequireUseStrict, unavailable in EPEL-5
- Update patch for building with old Test::More versions
- Drop %%defattr, redundant since rpm 4.4

* Mon Oct  1 2012 Paul Howarth <paul@city-fan.org> - 0.7-1
- Update to 0.7
  - Fixed multiple =encoding behavior
  - More deterministic t/01-bad-check.t

* Sat Sep 29 2012 Paul Howarth <paul@city-fan.org> - 0.6-1
- Update to 0.6
  - Fixed incorrect test examples
- Reinstate BR: perl(Test::Kwalitee) now that kwalitee test is back

* Thu Sep 27 2012 Paul Howarth <paul@city-fan.org> - 0.5-1
- Update to 0.5
  - Attempt to fix https://github.com/creaktive/Test-Mojibake/issues/2
    (don't fail when no lib directory exists)
  - Kwalitee won't complain any more
- Kwalitee test dropped upstream, so no longer need BR: perl(Test::Kwalitee)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.4-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 0.4-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Paul Howarth <paul@city-fan.org> - 0.4-1
- Update to 0.4
  - _detect_utf8: PP version now handles overlong UTF-8 sequences
  - Tests update (96% coverage)
  - Dist::Zilla update
- BR: perl(Perl::Critic::Policy::Modules::ProhibitModuleShebang),
  perl(Test::EOL) and perl(Test::Version)
- BR: perl(Test::Kwalitee), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic) and perl(Test::Synopsis) unconditionally
- Drop support for building for EPEL-4
- Drop patch for building with ExtUtils::MakeMaker < 6.30
- Update patch for building with Test::More < 0.88
- Add patch to support building without Test::Version
- Add workaround for the old version of PPI in EPEL-5 not being able to
  handle the unicode byte order mark in t/bom.pl, which breaks
  t/release-minimum-version.t
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.3-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct  4 2011 Paul Howarth <paul@city-fan.org> - 0.3-3
- BR/R: perl(Unicode::CheckUTF8) for improved performance

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 0.3-2
- Sanitize for Fedora/EPEL submission

* Thu Aug 11 2011 Paul Howarth <paul@city-fan.org> - 0.3-1
- Initial RPM version
