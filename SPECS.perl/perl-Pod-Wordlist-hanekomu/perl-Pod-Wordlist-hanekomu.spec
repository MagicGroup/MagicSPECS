# We need to patch the test suite if we have an old version of Test::More or Test::Spelling
%global old_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.94) ? 1 : 0);' 2>/dev/null || echo 0)
%global older_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.88) ? 1 : 0);' 2>/dev/null || echo 0)
%global even_older_test_more %(perl -MTest::More -e 'print (($Test::More::VERSION < 0.82) ? 1 : 0);' 2>/dev/null || echo 0)
%global old_test_spelling %(perl -MTest::Spelling -e 'print (($Test::Spelling::VERSION < 0.12) ? 1 : 0);' 2>/dev/null || echo 0)
%global old_pod_wordlist %(perl -MPod::Wordlist -e 'print (($Pod::Wordlist::VERSION < 1.06) ? 1 : 0);' 2>/dev/null || echo 0)

# noarch, but to avoid debug* files interfering with manifest test:
%global debug_package %{nil}

Name:		perl-Pod-Wordlist-hanekomu
Version:	1.132680
Release:	9%{?dist}
Summary:	Add words for spell checking POD
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		https://metacpan.org/module/Pod::Wordlist::hanekomu/
Source0:	http://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Pod-Wordlist-hanekomu-%{version}.tar.gz
Patch0:		Pod-Wordlist-hanekomu-1.132680-stopwords.patch
Patch1:		Pod-Wordlist-hanekomu-1.110090-Test::More-version.patch
Patch2:		Pod-Wordlist-hanekomu-1.132680-Test::More-done_testing.patch
Patch3:		Pod-Wordlist-hanekomu-1.113620-Test::More-note.patch
Patch4:		Pod-Wordlist-hanekomu-1.132680-old-Test::Spelling.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# ===================================================================
# Module Build requirements
# ===================================================================
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.30
# ===================================================================
# Module requirements
# ===================================================================
BuildRequires:	perl(strict)
BuildRequires:	perl(Test::Spelling), aspell-en
BuildRequires:	perl(utf8)
BuildRequires:	perl(warnings)
# ===================================================================
# Test Suite requirements
# ===================================================================
BuildRequires:	perl(Carp)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IPC::Open3)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::More)
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
BuildRequires:	perl(Test::HasVersion)
BuildRequires:	perl(Test::CheckChanges)
BuildRequires:	perl(Test::CPAN::Meta)
BuildRequires:	perl(Test::DistManifest)
BuildRequires:	perl(Test::EOL)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::MinimumVersion)
BuildRequires:	perl(Test::NoTabs)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Portability::Files)
BuildRequires:	perl(Test::Synopsis)
# Test::Vars requires Perl 5.10 and so is not available in EPEL-5
%if "%{?rhel}" != "5"
# Disable using of Test::Vars, because it failed with Perl 5.22.0
# There is not a properly fix for it yet
%if ! 0%(perl -e 'print $] >= 5.022')
BuildRequires:	perl(Test::Vars)
%endif
%endif
%endif
# ===================================================================
# Runtime requirements
# ===================================================================
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
When loaded, this module automatically adds Test::Spelling stopwords for
POD spell checking, that is, words that should be ignored by the spell
check.

The stopword list includes some CPAN author names, technical terms (e.g.
JSON, URI) and other commonly-used words not included in the default
word list (e.g. mixin, munging).

%prep
%setup -q -n Pod-Wordlist-hanekomu-%{version}

# We have to patch the test suite if we have an old Test::More
#
# Don't really need Test::More ≥ 0.94
%if %{old_test_more}
%patch1 -p1
%endif
# done_testing requires Test::More ≥ 0.88
%if %{older_test_more}
%patch2
%endif
# note() requires Test::More ≥ 0.82
%if %{even_older_test_more}
%patch3 -p1
%endif

# Need to use our own stopwords unless we have Pod::Wordlist ≥ 1.06
%if %{old_pod_wordlist}
%patch0
%endif

# Don't really need Test::Spelling ≥ 0.12
%if %{old_test_spelling}
%patch4
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
%{perl_vendorlib}/Pod/
%{_mandir}/man3/Pod::Wordlist::hanekomu.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.132680-9
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 1.132680-8
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.132680-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.132680-6
- Perl 5.22 re-rebuild of bootstrapped packages
- Disable using of Test::Vars with Perl 5.22

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.132680-5
- Perl 5.22 rebuild

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.132680-4
- Perl 5.20 re-rebuild of bootstrapped packages

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.132680-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.132680-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 1.132680-1
- Update to 1.132680
  - Marked as deprecated now that words are merged into Pod::Wordlist
- Classify buildreqs by usage
- Update patches as needed
- Add further patch to support building with Pod::Wordlist < 1.06

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.130240-4
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.130240-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 1.130240-2
- Perl 5.18 rebuild

* Thu Jan 24 2013 Paul Howarth <paul@city-fan.org> - 1.130240-1
- Update 1.130240
  - Added "rjbs", "mst", "subclass", "subclasses" and "tuple"

* Wed Oct 10 2012 Paul Howarth <paul@city-fan.org> - 1.122840-1
- Update to 1.122840
  - Added "MongoDB", "RDBMS", "SQLite" and "iteratively"
- Update patch for building with Test::Spelling < 0.12

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.121370-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.121370-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.121370-2
- Perl 5.16 rebuild

* Thu May 17 2012 Paul Howarth <paul@city-fan.org> - 1.121370-1
- Update to 1.121370
  - Added: "GUIDs", "UUID", "UUIDs", "searchable"
- Update patch for building with Test::More < 0.88

* Thu May  3 2012 Paul Howarth <paul@city-fan.org> - 1.121231-1
- Update to 1.121231
  - Added "deserialized" and "parameterizable"
- Drop now-redundant BR: perl(Test::Requires)
- Update patch for building with Test::More < 0.88
- Add new patch for building with Test::Spelling < 0.12 if necessary

* Sun Apr  1 2012 Paul Howarth <paul@city-fan.org> - 1.120920-1
- Update to 1.120920
  - Added "pre", "precompute", "prereq", "prereqs", "symlinked"
- Drop %%defattr, redundant since rpm 4.4
- perl(Test::Kwalitee) and perl(Test::MinimumVersion) now available in EPEL-5

* Thu Mar 15 2012 Paul Howarth <paul@city-fan.org> - 1.120740-1
- Update to 1.120740
  - Documentation and metadata update
  - Added "CamelCase", "CPANPLUS", "EINTR", "GUID", "HTTPS", "IETF", "IRC",
    "ISP", "ISP's", "JSON", "modulino", "SMTP", "SSL", "URI's", "UTC", "wiki"
    "analyses", "chunked", "locator", "redirections", "reusability", and
    "timestamp"
- BR: perl(Test::Requires)
- Update %%description
- Use metacpan.org URLs
- Don't need to remove empty directories from buildroot
- Drop support for EOL EL-4:
  - No longer need to support building with ExtUtils::MakeMaker < 6.30
  - Unconditionally BR: perl(Test::Perl::Critic) and perl(Test::Synopsis)
- Update patch for building with Test::More < 0.88

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.113620-2
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Wed Dec 28 2011 Paul Howarth <paul@city-fan.org> - 1.113620-1
- Update to 1.113620
  - Added "Lapworth", "UTF", "aggregator", "aggregators", "probe's",
    "runtime", "seekable" and "sigils"
- Re-diff patches where necessary to avoid .orig file pollution

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 1.110090-3
- Sanitize for Fedora/EPEL submission

* Tue Aug  9 2011 Paul Howarth <paul@city-fan.org> - 1.110090-2
- BR: perl(Test::HasVersion) and perl(Test::Vars) for full release test
  coverage

* Sun Aug  7 2011 Paul Howarth <paul@city-fan.org> - 1.110090-1
- Initial RPM version
